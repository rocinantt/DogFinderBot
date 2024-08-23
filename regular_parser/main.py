#main.py
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep
from config import logger
from vk_parser import get_group_info, parse_new_posts
from database import (save_posts_to_db,
                      update_last_post_date,
                      delete_old_posts,
                      check_group_exists,
                      conn_pool)


def check_new_posts_for_group(group):
    """
    Проверяет наличие новых постов в одной группе и обновляет базу данных.

    :param group: информация о группе
    """
    group_id, last_post_date, region, area, district, include_reposts = group
    group_name, group_link = get_group_info(group_id)

    if group_name and group_link:
        logger.info(f"Проверка новых постов для группы {group_id} ({group_name}) с момента {last_post_date}")

        new_posts = parse_new_posts(group_id, last_post_date, include_reposts)
        if new_posts:
            save_posts_to_db(new_posts, region, area, district)
            update_last_post_date(group_id)
            delete_old_posts(group_id, len(new_posts))
    else:
        logger.error(f"Не удалось получить информацию для группы {group_id}")

def check_new_posts_for_all_groups():
    """
    Проверяет наличие новых постов для всех групп в базе данных.
    """
    conn = conn_pool.getconn()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT group_id, last_post_date, region, area, district, include_reposts FROM vk_groups")
            groups = cursor.fetchall()

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(check_new_posts_for_group, group) for group in groups]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"Ошибка при обработке группы: {e}")
    finally:
        conn_pool.putconn(conn)

if __name__ == "__main__":
    while True:
        try:
            check_new_posts_for_all_groups()
            logger.info("Ожидание 20 минут перед следующей проверкой...")
            sleep(20 * 60)
        except Exception as e:
            logger.error(f"Ошибка в основном цикле: {e}")