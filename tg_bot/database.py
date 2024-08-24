import json
import psycopg2
from psycopg2.extras import DictCursor
from config import DATABASE_URL, logger, redis_client


def get_user_region(user_id):
    """
    Получает регион пользователя по его ID.

    :param user_id: ID пользователя
    :return: регион пользователя или None, если не найдено
    """
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
        with conn.cursor() as cursor:
            cursor.execute("SELECT region FROM user_regions WHERE user_id = %s", (user_id,))
            result = cursor.fetchone()
            return result[0] if result else None
    except psycopg2.Error as e:
        logger.error(f"Ошибка при получении региона пользователя: {e}")
        return None
    finally:
        if conn:
            conn.close()


def save_user_region(user_id, region):
    """
    Сохраняет или обновляет регион пользователя.

    :param user_id: ID пользователя
    :param region: регион, который нужно сохранить
    """
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO user_regions (user_id, region) VALUES (%s, %s)
                ON CONFLICT (user_id) DO UPDATE SET region = EXCLUDED.region
            """, (user_id, region))
            conn.commit()
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        logger.error(f"Ошибка при сохранении региона пользователя: {e}")
    finally:
        if conn:
            conn.close()


def get_regions():
    """
    Получает все уникальные регионы из таблицы vk_groups.

    :return: список регионов
    """
    cache_key = "regions"
    cached_regions = None

    if redis_client:
        cached_regions = redis_client.get(cache_key)

    if cached_regions:
        logger.info('Загружено из кэша Redis')
        return json.loads(cached_regions)

    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
        with conn.cursor() as cursor:
            cursor.execute("SELECT DISTINCT region FROM vk_groups")
            regions = cursor.fetchall()
            logger.info('Загружено из DB')
            regions_list = [region[0] for region in regions]

            # Сохранение в Redis
            if redis_client:
                redis_client.setex(cache_key, 3600, json.dumps(regions_list))
                logger.info('Сохранено в кэш Redis')

            return regions_list
    except psycopg2.Error as e:
        logger.error(f"Ошибка при получении списка регионов: {e}")
        return []
    finally:
        if conn:
            conn.close()


def get_areas(region, animal_type):
    """
    Получает все уникальные области и количество постов для конкретного региона и типа животного.

    :param region: регион
    :param animal_type: тип животного (собака или кошка)
    :return: список областей и количество постов
    """
    cache_key = f"areas:{region}:{animal_type}"
    cached_areas = None

    if redis_client:
        cached_areas = redis_client.get(cache_key)

    if cached_areas:
        logger.info('Загружено из кэша Redis')
        return json.loads(cached_areas)

    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT area, COUNT(*)
                FROM vk_posts
                WHERE region = %s AND animal_type = %s AND area != ''
                GROUP BY area
                ORDER BY COUNT(*) DESC
            """, (region, animal_type))
            areas = cursor.fetchall()
            logger.info('Загружено из DB')
            return areas
    except psycopg2.Error as e:
        logger.error(f"Ошибка при получении областей: {e}")
        return []
    finally:
        if conn:
            conn.close()


def get_districts(area, animal_type):
    """
    Получает все уникальные районы и количество постов для конкретной области и типа животного.

    :param area: область
    :param animal_type: тип животного (собака или кошка)
    :return: список районов и количество постов
    """

    cache_key = f"districts:{area}:{animal_type}"
    cached_districts = None

    if redis_client:
        cached_districts = redis_client.get(cache_key)

    if cached_districts:
        logger.info("Загружено из кэша Redis")
        return json.loads(cached_districts)

    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT district, COUNT(*)
                FROM vk_posts
                WHERE area = %s AND animal_type = %s AND district != ''
                GROUP BY district
                ORDER BY COUNT(*) DESC
            """, (area, animal_type))
            districts = cursor.fetchall()
            logger.info('Загружено из DB')
            return districts
    except psycopg2.Error as e:
        logger.error(f"Ошибка при получении районов: {e}")
        return []
    finally:
        if conn:
            conn.close()


def get_groups(region):
    """
    Получает названия и ссылки групп для конкретного региона.

    :param region: регион
    :return: список групп с названиями и ссылками
    """
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
        with conn.cursor() as cursor:
            cursor.execute("SELECT group_name, group_link FROM vk_groups WHERE region = %s", (region,))
            groups = cursor.fetchall()
            return [{"group_name": group[0], "group_link": group[1]} for group in groups]
    except psycopg2.Error as e:
        logger.error(f"Ошибка при получении групп: {e}")
        return []
    finally:
        if conn:
            conn.close()
