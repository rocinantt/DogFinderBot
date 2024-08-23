#database.py
import psycopg2
from psycopg2.extras import Json
from config import DATABASE_URL, logger
from image_processing import process_post
from tqdm import tqdm
from utils import find_all_locations, determine_animal_type, normalize_text


def save_posts_to_db(posts, default_region, default_area, default_district):
    """Сохраняет посты в базу данных."""
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    for post in tqdm(posts, desc='Извлечение признаков и сохранение постов в базу данных', total=len(posts)):
        try:
            # Извлечение признаков изображения
            features = process_post(post)
            logger.info(f'признаки извлечены, {len(features)}')
            # Нормализация текста поста
            text = post.get('text', '')
            normalized_text = normalize_text(text)
            logger.info(f'текст обработан, {normalized_text}')

            # Извлечение локаций и типа животного из нормализованного текста
            locations = find_all_locations(normalized_text, default_region, default_area, default_district)
            logger.info(f'локации извлечены, {locations}')
            animal_type = determine_animal_type(normalized_text)
            logger.info(f'тип животногоопределен, {animal_type}')

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
    cursor.close()
    conn.close()

def check_group_exists(group_id):
    """Check if a group exists in the database."""
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM vk_groups WHERE abs(group_id::bigint) = abs(%s::bigint)", (group_id,))
    exists = cursor.fetchone()

    cursor.close()
    conn.close()

    return exists

def add_group_to_db(group_id, region, area, group_name, group_link, include_reposts):
    """Add a new group to the database."""
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO vk_groups (group_id, region, area, group_name, group_link, last_post_date, include_reposts)
        VALUES (%s, %s, %s, %s, %s, (SELECT MAX(date) FROM vk_posts WHERE group_id = %s), %s)
    """, (group_id, region, area, group_name, group_link, group_id, include_reposts))
    conn.commit()

    cursor.close()
    conn.close()
    logger.info(f"Group {group_name} added to the database")
