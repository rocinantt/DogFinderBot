import sys
from config import logger
from vk_parser import parse_all_posts, get_group_info
from database import save_posts_to_db, check_group_exists, add_group_to_db

def main(group_url, n_days, region, city):
    from config import vk

    vk_group_id = vk.utils.resolveScreenName(screen_name=group_url.split('/')[-1])
    group_id = -vk_group_id['object_id']
    group_name, group_link = get_group_info(group_id)

    if check_group_exists(group_id):
        logger.info(f"Group {group_name} already exists in the database.")
    else:
        logger.info(f"Starting to parse posts for group {group_url} for the past {n_days} days")
        posts = parse_all_posts(group_id, n_days)
        save_posts_to_db(posts)
        add_group_to_db(group_id, region, city, group_name, group_link)
        last_post_date = posts[-1]['date'] if posts else "N/A"
        logger.info(f"Parsing posts for group {group_url} completed. Collected {len(posts)} posts. Last post date: {last_post_date}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: docker-compose run primary_parser python main.py <group_url> <n_days> <region> <city>")
        sys.exit(1)

    group_url = sys.argv[1]
    n_days = int(sys.argv[2])
    region = sys.argv[3]
    city = sys.argv[4]

    main(group_url, n_days, region, city)

