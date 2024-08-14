#database.py
import psycopg2
from psycopg2.extras import DictCursor
from config import DATABASE_URL, logger
from locations import regions_data

# Establish a database connection
try:
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
except psycopg2.Error as e:
    logger.error(f"Error connecting to the database: {e}")
    raise

def get_user_region(user_id):
    """Fetches the region of a user by user ID."""
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT region FROM user_regions WHERE user_id = %s", (user_id,))
            result = cursor.fetchone()
            return result[0] if result else None
    except psycopg2.Error as e:
        logger.error(f"Error fetching user region: {e}")
        return None

def save_user_region(user_id, region):
    """Saves or updates the region of a user."""
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO user_regions (user_id, region) VALUES (%s, %s)
                ON CONFLICT (user_id) DO UPDATE SET region = EXCLUDED.region
            """, (user_id, region))
            conn.commit()
    except psycopg2.Error as e:
        logger.error(f"Error saving user region: {e}")

def get_regions(regions_data):
    """Fetches all unique regions from regions_data."""
    try:
        return list(regions_data.keys())
    except Exception as e:
        logger.error(f"Error fetching regions: {e}")
        return []



def get_groups(region):
    """Fetches group names and links for a given region."""
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT group_name, group_link FROM vk_groups WHERE region = %s", (region,))
            groups = cursor.fetchall()
            return [{"group_name": group[0], "group_link": group[1]} for group in groups]
    except psycopg2.Error as e:
        logger.error(f"Error fetching groups: {e}")
        return []
