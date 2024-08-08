# main.py
import sys
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep
from datetime import datetime
from vk_parser import get_group_info, parse_new_posts
from database import save_posts_to_db, update_last_post_date, delete_old_posts, check_group_exists, add_group_to_db, conn_pool
from config import logger

def check_new_posts_for_group(group):
    """Check for new posts in a single group and update the database."""
    group_id, last_post_date, region, city = group
    group_name, group_link = get_group_info(group_id)
    
    if group_name and group_link:
        logger.info(f"Checking new posts for group {group_id} ({group_name}) since {last_post_date}")
        
        new_posts = parse_new_posts(group_id, last_post_date)
        if new_posts:
            save_posts_to_db(new_posts)
            update_last_post_date(group_id)
            delete_old_posts(group_id, len(new_posts))
    else:
        logger.error(f"Unable to retrieve info for group {group_id}")

def check_new_posts_for_all_groups():
    """Check new posts for all groups in the database."""
    conn = conn_pool.getconn()
    cursor = conn.cursor()

    cursor.execute("SELECT group_id, last_post_date, region, city FROM vk_groups")
    groups = cursor.fetchall()

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(check_new_posts_for_group, group) for group in groups]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logger.error(f"Error while processing group: {e}")

    cursor.close()
    conn_pool.putconn(conn)

if __name__ == "__main__":
    while True:
        check_new_posts_for_all_groups()
        logger.info("Sleeping for 120 minutes...")
        sleep(120 * 60)

