#database.py
import psycopg2
from psycopg2.extras import DictCursor
from config import DATABASE_URL, logger


# ----------------------- Обработка региона пользователя --------------------------------------

def get_user_region(user_id):
    """Fetches the region of a user by user ID."""
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
        with conn.cursor() as cursor:
            cursor.execute("SELECT region FROM user_regions WHERE user_id = %s", (user_id,))
            result = cursor.fetchone()
            return result[0] if result else None
    except psycopg2.Error as e:
        logger.error(f"Error fetching user region: {e}")
        return None
    finally:
        if conn:
            conn.close()


def save_user_region(user_id, region):
    """Saves or updates the region of a user."""
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
        logger.error(f"Error saving user region: {e}")
    finally:
        if conn:
            conn.close()


# ----------------------- Получение данных из бд --------------------------------------
def get_regions():
    """Fetches all unique regions from the vk_groups table."""
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
        with conn.cursor() as cursor:
            cursor.execute("SELECT DISTINCT region FROM vk_groups")
            regions = cursor.fetchall()
            return [region[0] for region in regions]
    except psycopg2.Error as e:
        logger.error(f"Error fetching regions: {e}")
        return []
    finally:
        if conn:
            conn.close()


def get_areas(region, animal_type):
    """Fetches all unique areas and count of posts for a specific region and animal type."""
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
        logger.error(f"Error fetching areas: {e}")
        return []
    finally:
        if conn:
            conn.close()


def get_districts(area, animal_type):
    """Fetches all unique districts and count of posts for a specific area and animal type."""
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
        logger.error(f"Error fetching districts: {e}")
        return []
    finally:
        if conn:
            conn.close()


# ----------------------- Получение списка групп --------------------------------------
def get_groups(region):
    """Fetches group names and links for a given region."""
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
        with conn.cursor() as cursor:
            cursor.execute("SELECT group_name, group_link FROM vk_groups WHERE region = %s", (region,))
            groups = cursor.fetchall()
            return [{"group_name": group[0], "group_link": group[1]} for group in groups]
    except psycopg2.Error as e:
        logger.error(f"Error fetching groups: {e}")
        return []
    finally:
        if conn:
            conn.close()
