import psycopg2
from psycopg2.extras import DictCursor
from config import DATABASE_URL, logger


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
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
        with conn.cursor() as cursor:
            cursor.execute("SELECT DISTINCT region FROM vk_groups")
            regions = cursor.fetchall()
            return [region[0] for region in regions]
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
