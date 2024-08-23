from datetime import datetime, timedelta
from tqdm import tqdm
import vk_api
from config import vk, logger

def get_posts(group_id, count=100, offset=0):
    """
    Извлекает посты из группы VK.

    :param group_id: ID группы
    :param count: количество постов для извлечения за один запрос
    :param offset: смещение для извлечения постов
    :return: список постов
    """
    try:
        response = vk.wall.get(owner_id=group_id, count=count, offset=offset)
        logger.info(f"Получено {len(response['items'])} постов из группы {group_id}")
        return response['items']
    except vk_api.exceptions.ApiError as e:
        logger.error(f"Ошибка при получении постов для группы {group_id}: {e}")
        return []

def get_group_info(group_id):
    """
    Извлекает информацию о группе VK.

    :param group_id: ID группы
    :return: название группы и ссылка на группу
    """
    try:
        response = vk.groups.getById(group_id=abs(group_id))
        group_info = response[0]
        return group_info['name'], f"https://vk.com/{group_info['screen_name']}"
    except vk_api.exceptions.ApiError as e:
        logger.error(f"Ошибка при получении информации о группе {group_id}: {e}")
        return None, None

def extract_photos_from_post(post):
    """
    Извлекает URL-адреса фотографий из поста.

    :param post: пост VK
    :return: список URL фотографий или None
    """
    photos = []
    try:
        if 'attachments' in post:
            for attachment in post['attachments']:
                if attachment['type'] == 'photo':
                    photo_sizes = attachment['photo']['sizes']
                    preferred_types = {'r': None, 'x': None, 'y': None}
                    for size in photo_sizes:
                        if size['type'] in preferred_types:
                            preferred_types[size['type']] = size['url']
                    selected_photo = next((preferred_types[ptype] for ptype in ['r', 'x', 'y'] if preferred_types[ptype]),
                                          None)
                    if selected_photo and selected_photo not in photos:
                        photos.append(selected_photo)
                    else:
                        max_size_photo = max(photo_sizes, key=lambda size: size['width'])
                        if max_size_photo['url'] not in photos:
                            photos.append(max_size_photo['url'])

        return photos if photos else None
    except Exception as e:
        logger.error(f"Ошибка при извлечении фотографий из поста {post['id']}: {e}")
        return None

def format_post_data(post, group_id):
    """
    Форматирует данные поста для вставки в базу данных.

    :param post: пост VK
    :param group_id: ID группы
    :return: отформатированные данные поста или None
    """
    photos = extract_photos_from_post(post)
    if photos is None or len(photos) > 4:
        return None

    post_data = {
        "post_id": post['id'],
        "date": datetime.utcfromtimestamp(post['date']).strftime('%Y-%m-%d %H:%M:%S'),
        "photos": photos,
        "post_link": f"https://vk.com/wall{post['owner_id']}_{post['id']}",
        "group_id": group_id,
        'text': post.get('text', '')
    }
    return post_data

def parse_all_posts(group_id, n_days=100, include_reposts=False):
    """
    Парсит все посты из группы VK за заданное количество дней.

    :param group_id: ID группы VK
    :param n_days: количество дней для парсинга постов
    :param include_reposts: включать ли репосты
    :return: список отформатированных данных постов
    """
    all_posts = []
    offset = 0
    n_days_ago = datetime.now() - timedelta(days=n_days)

    with tqdm(desc="Парсинг постов", unit="постов", leave=False) as pbar:
        while True:
            posts = get_posts(group_id, count=100, offset=offset)
            if not posts:
                break

            for post in posts:
                post_date = datetime.utcfromtimestamp(post['date'])

                if 'is_pinned' in post and post['is_pinned']:
                    logger.info(f"Пропуск закрепленного поста с id {post['id']}")
                    continue

                if post_date < n_days_ago:
                    logger.info("Завершение сбора: Дата поста старше указанного предела.")
                    return all_posts

                if 'copy_history' in post:
                    if include_reposts:
                        original_post = post['copy_history'][0]
                        original_post['date'] = post_date.timestamp()
                        post = original_post
                    else:
                        continue

                post_data = format_post_data(post, group_id)
                if post_data:
                    all_posts.append(post_data)

            offset += 100
            pbar.update(100)

    post_cache = {}
    for post in all_posts:
        photo_links = tuple(post['photos'])
        if photo_links not in post_cache or post_cache[photo_links]['date'] < post['date']:
            post_cache[photo_links] = post 

    return list(post_cache.values())
