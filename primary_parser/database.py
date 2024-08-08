import psycopg2
from psycopg2.extras import Json
from config import DATABASE_URL, logger
from image_processing import process_post
from tqdm import tqdm


def save_posts_to_db(posts):
    """Save posts to the database."""
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    for post in tqdm(posts, desc='Extracting features and saving posts to the database', total=len(posts)):
        try:
            features = process_post(post)
            cursor.execute("""
                INSERT INTO vk_posts (post_id, group_id, date, post_link, features)
                VALUES (%s, %s, %s, %s, %s)
                """, (post['post_id'], post['group_id'], post['date'], post['post_link'], Json(features)))
        except Exception as e:
            logger.error(f"Error processing post {post['post_id']}: {e}")
            continue

    conn.commit()
    logger.info(f"Added {len(posts)} posts to the database for group {posts[0]['group_id']}")
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

def add_group_to_db(group_id, region, city, group_name, group_link):
    """Add a new group to the database."""
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO vk_groups (group_id, region, city, group_name, group_link, last_post_date)
        VALUES (%s, %s, %s, %s, %s, (SELECT MAX(date) FROM vk_posts WHERE group_id = %s))
    """, (group_id, region, city, group_name, group_link, group_id))
    conn.commit()

    cursor.close()
    conn.close()
    logger.info(f"Group {group_name} added to the database")

