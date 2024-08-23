import psycopg2
from psycopg2.extras import Json
from tqdm import tqdm

from config import DATABASE_URL, logger
from image_processing import process_post
from utils import find_all_locations, determine_animal_type, normalize_text

def get_db_connection():
    """Создает и возвращает соединение с базой данных."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except psycopg2.Error as e:
        logger.error(f"Ошибка подключения к базе данных: {e}")
        raise

def save_posts_to_db(posts, default_region, default_area, default_district):
    """
    Сохраняет посты в базу данных.

    :param posts: список постов
    :param default_region: регион по умолчанию
    :param default_area: область по умолчанию
    :param default_district: район по умолчанию
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            for post in tqdm(posts, desc='Извлечение признаков и сохранение постов в базу данных', total=len(posts)):
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
        conn.close()

def check_group_exists(group_id):
    """
    Проверяет, существует ли группа в базе данных.

    :param group_id: ID группы
    :return: True, если группа существует, иначе False
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM vk_groups WHERE abs(group_id::bigint) = abs(%s::bigint)", (group_id,))
            exists = cursor.fetchone()
            return bool(exists)
    except psycopg2.Error as e:
        logger.error(f"Ошибка при проверке существования группы {group_id}: {e}")
        raise
    finally:
        conn.close()

def add_group_to_db(group_id, region, area, district, group_name, group_link, include_reposts):
    """
    Добавляет новую группу в базу данных.

    :param group_id: ID группы
    :param region: регион группы
    :param area: область группы
    :param district: район группы
    :param group_name: название группы
    :param group_link: ссылка на группу
    :param include_reposts: включать ли репосты
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO vk_groups (group_id, region, area, district, group_name, group_link, last_post_date, include_reposts)
                VALUES (%s, %s, %s, %s, %s, %s, (SELECT MAX(date) FROM vk_posts WHERE group_id = %s), %s)
            """, (group_id, region, area, district, group_name, group_link, group_id, include_reposts))
        conn.commit()
        logger.info(f"Группа {group_name} добавлена в базу данных")
    except psycopg2.Error as e:
        logger.error(f"Ошибка при добавлении группы {group_name} в базу данных: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()