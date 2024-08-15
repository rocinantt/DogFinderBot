#database.py
import psycopg2
from psycopg2.extras import Json
from psycopg2 import pool
from config import DATABASE_URL, logger
from image_processing import process_post
from tqdm import tqdm
from utils import find_all_locations


conn_pool = pool.SimpleConnectionPool(1, 10, dsn=DATABASE_URL)


def save_posts_to_db(posts, default_region, default_area):
    """Save posts to the database."""
    conn = conn_pool.getconn()
    cursor = conn.cursor()

    try:
        for post in tqdm(posts, desc='Processing posts', total=len(posts)):
            features = process_post(post)

            # Extract locations from post text
            text = post.get('text', '')
            locations = find_all_locations(text)

            if not locations:
                locations = [(default_region, default_area, '')]

            for region, area, district in locations:
                cursor.execute("""
                    INSERT INTO vk_posts (post_id, group_id, date, post_link, features, region, area, district)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (post['post_id'], post['group_id'], post['date'], post['post_link'],
                          Json(features), region, area, district))
        conn.commit()
        logger.info(f"Added {len(posts)} posts to the database for group {posts[0]['group_id']}")
    except Exception as e:
        logger.error(f"Error while saving posts: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn_pool.putconn(conn)

def update_last_post_date(group_id):
    """Update the last post date for the group."""
    conn = conn_pool.getconn()
    cursor = conn.cursor()

    try:
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
        logger.info(f"Updated last post date for group {group_id} to {last_post_date}")
    except Exception as e:
        logger.error(f"Error while updating last post date: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn_pool.putconn(conn)

def delete_old_posts(group_id, num_posts_to_delete):
    """Delete old posts from the database."""
    conn = conn_pool.getconn()
    cursor = conn.cursor()

    try:
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
        logger.info(f"Deleted {num_posts_to_delete} old posts for group {group_id}")
    except Exception as e:
        logger.error(f"Error while deleting old posts: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn_pool.putconn(conn)

def check_group_exists(group_id):
    """Check if a group exists in the database."""
    conn = conn_pool.getconn()
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM vk_groups WHERE abs(group_id::bigint) = abs(%s::bigint)", (group_id,))
    exists = cursor.fetchone()

    cursor.close()
    conn_pool.putconn(conn)

    return exists

def add_group_to_db(group_id, region, city, group_name, group_link):
    """Add a new group to the database."""
    conn = conn_pool.getconn()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO vk_groups (group_id, region, city, group_name, group_link, last_post_date)
        VALUES (%s, %s, %s, %s, %s, (SELECT MAX(date) FROM vk_posts WHERE group_id = %s))
    """, (group_id, region, city, group_name, group_link, group_id))
    conn.commit()

    cursor.close()
    conn_pool.putconn(conn)
    logger.info(f"Group {group_name} added to the database")

