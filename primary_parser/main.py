import sys
from config import logger, vk
from vk_parser import parse_all_posts, get_group_info
from database import save_posts_to_db, check_group_exists, add_group_to_db

def main(group_url, n_days, region, area, district, include_reposts=False):
    """
    Основная функция для парсинга постов из группы VK и сохранения их в базу данных.

    :param group_url: URL группы VK
    :param n_days: количество дней для парсинга постов
    :param region: регион по умолчанию
    :param area: область по умолчанию
    :param district: район по умолчанию
    :param include_reposts: включать ли репосты
    """
    try:
        vk_group_id = vk.utils.resolveScreenName(screen_name=group_url.split('/')[-1])
        group_id = -vk_group_id['object_id']
        group_name, group_link = get_group_info(group_id)

        if check_group_exists(group_id):
            logger.info(f"Группа {group_name} уже существует в базе данных.")
        else:
            logger.info(f"Начинаю парсинг постов для группы {group_url} за последние {n_days} дней")
            posts = parse_all_posts(group_id, n_days, include_reposts)
            save_posts_to_db(posts, region, area, district)
            add_group_to_db(group_id, region, area, district, group_name, group_link, include_reposts)
            last_post_date = posts[-1]['date'] if posts else "N/A"
            logger.info(f"Парсинг постов для группы {group_url} завершен. Собрано {len(posts)} постов. Дата последнего поста: {last_post_date}")
    except Exception as e:
        logger.error(f"Ошибка в процессе парсинга группы {group_url}: {e}")
        raise

if __name__ == "__main__":
    try:
        group_url = sys.argv[1]
        n_days = int(sys.argv[2])
        region = sys.argv[3]
        area = sys.argv[4]
        district = sys.argv[5]
        include_reposts = sys.argv[6].lower() == 'true'

        main(group_url, n_days, region, area, district, include_reposts)
    except IndexError as e:
        logger.error(f"Недостаточно аргументов командной строки: {e}")
        print(f"Использование: docker-compose run primary_parser python main.py <group_url> <n_days> <region> <area> <district> <include_reposts>")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Неверный формат аргументов: {e}")
        print(f"Использование: docker-compose run primary_parser python main.py <group_url> <n_days> <region> <area> <district> <include_reposts>")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        sys.exit(1)
