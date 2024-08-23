import psycopg2
from psycopg2.extras import Json
from psycopg2 import pool
from tqdm import tqdm
from config import DATABASE_URL, logger
from image_processing import process_post
from utils import find_all_locations, determine_animal_type, normalize_text

# Инициализация пула соединений с базой данных
conn_pool = pool.SimpleConnectionPool(1, 10, dsn=DATABASE_URL)

def save_posts_to_db(posts, default_region, default_area, default_district):
    """
    Сохраняет посты в базу данных.

    :param posts: список постов
    :param default_region: регион по умолчанию
    :param default_area: область по умолчанию
    :param default_district: район по умолчанию
    """
    conn = conn_pool.getconn()
    try:
        with conn.cursor() as cursor:
            for post in tqdm(posts, desc='Processing posts', total=len(posts)):
                try:
                    # Извлечение признаков изображения
                    features = process_post(post)
                    # Нормализация текста поста
                    text = post.get('text', '')
                    normalized_text = normalize_text(text)
                    # Извлечение локаций и типа животного из нормализованного текста
                    locations = find_all_locations(normalized_text, default_region, default_area, default_district)
                    animal_type = determine_animal_type(normalized_text)

                    # Сохранение поста для каждой найденной локации
                    for region, area, district in locations:
                        cursor.execute("""
                            INSERT INTO vk_posts (post_id, group_id, date, post_link, features, region, area, district, animal_type)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (post['post_id'], post['group_id'], post['date'], post['post_link'],
                              Json(features), region, area, district, animal_type))
                except Exception as e:
                    logger.error(f"Ошибка при обработке поста {post['post_id']}: {e}")
                    continue

        conn.commit()
        logger.info(f"Добавлено {len(posts)} постов в базу данных для группы {posts[0]['group_id']}")
    except Exception as e:
        logger.error(f"Ошибка при сохранении постов в базу данных: {e}")
        conn.rollback()
        raise
    finally:
        conn_pool.putconn(conn)

def update_last_post_date(group_id):
    """
    Обновляет дату последнего поста для группы.

    :param group_id: ID группы
    """
    conn = conn_pool.getconn()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE vk_groups
                SET last_post_date = (
                    SELECT MAX(date)
                    FROM vk_posts
                    WHERE vk_posts.group_id = vk_groups.group_id
                )
                WHERE group_id = %s
            """, (group_id,))
            conn.commit()

            cursor.execute("SELECT last_post_date FROM vk_groups WHERE group_id = %s", (group_id,))
            last_post_date = cursor.fetchone()[0]
            logger.info(f"Дата последнего поста для группы {group_id} обновлена на {last_post_date}")
    except Exception as e:
        logger.error(f"Ошибка при обновлении даты последнего поста для группы {group_id}: {e}")
        conn.rollback()
        raise
    finally:
        conn_pool.putconn(conn)

def delete_old_posts(group_id, num_posts_to_delete):
    """
    Удаляет старые посты из базы данных.

    :param group_id: ID группы
    :param num_posts_to_delete: количество постов для удаления
    """
    conn = conn_pool.getconn()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM vk_posts
                WHERE id IN (
                    SELECT id FROM vk_posts
                    WHERE group_id = %s
                    ORDER BY date ASC
                    LIMIT %s
                )
            """, (group_id, num_posts_to_delete))
            conn.commit()
            logger.info(f"Удалено {num_posts_to_delete} старых постов для группы {group_id}")
    except Exception as e:
        logger.error(f"Ошибка при удалении старых постов для группы {group_id}: {e}")
        conn.rollback()
        raise
    finally:
        conn_pool.putconn(conn)

def check_group_exists(group_id):
    """
    Проверяет, существует ли группа в базе данных.

    :param group_id: ID группы
    :return: True, если группа существует, иначе False
    """
    conn = conn_pool.getconn()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM vk_groups WHERE abs(group_id::bigint) = abs(%s::bigint)", (group_id,))
            return bool(cursor.fetchone())
    except psycopg2.Error as e:
        logger.error(f"Ошибка при проверке существования группы {group_id}: {e}")
        raise
    finally:
        conn_pool.putconn(conn)
