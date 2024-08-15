# vk_parser.py
from datetime import datetime, timedelta
from tqdm import tqdm
import vk_api
from config import vk, logger

def get_posts(group_id, count=100, offset=0):
    """Get posts from a VK group."""
    try:
        response = vk.wall.get(owner_id=group_id, count=count, offset=offset)
        logger.info(f"Received {len(response['items'])} posts from group {group_id}")
        return response['items']
    except vk_api.exceptions.ApiError as e:
        logger.error(f"Error while retrieving posts for group {group_id}: {e}")
        return []

def get_group_info(group_id):
    """Retrieve group information."""
    try:
        response = vk.groups.getById(group_id=abs(group_id))
        group_info = response[0]
        return group_info['name'], f"https://vk.com/{group_info['screen_name']}"
    except vk_api.exceptions.ApiError as e:
        logger.error(f"Error while retrieving group information: {e}")
        return None, None

def extract_photos_from_post(post):
    """Extract photo URLs from a post."""
    photos = []
    if 'attachments' in post:
        for attachment in post['attachments']:
            if attachment['type'] == 'photo':
                photo_sizes = attachment['photo']['sizes']
                max_size_photo = max(photo_sizes, key=lambda size: size['width'])
                if max_size_photo['url'] not in photos:
                    photos.append(max_size_photo['url'])
    return photos if photos else None

def format_post_data(post, group_id):
    """Format post data for database insertion."""
    photos = extract_photos_from_post(post)
    if photos is None or len(photos) > 4:
        return None

    post_data = {
        "post_id": post['id'],
        "date": datetime.utcfromtimestamp(post['date']).strftime('%Y-%m-%d %H:%M:%S'),
        "photos": photos,
        "post_link": f"https://vk.com/wall{post['owner_id']}_{post['id']}",
        "group_id": group_id,
        "text": post['text']
    }
    return post_data

def parse_new_posts(group_id, last_post_date, include_reposts=False):
    """Parse new posts for a group since the last post date."""
    new_posts = []
    offset = 0

    with tqdm(desc=f"Parsing new posts for group {group_id}", unit="posts") as pbar:
        while True:
            posts = get_posts(group_id, count=100, offset=offset)
            if not posts:
                break

            for post in posts:
                post_date = datetime.utcfromtimestamp(post['date'])

                if 'is_pinned' in post and post['is_pinned']:
                    logger.info(f"Skipping pinned post with id {post['id']}")
                    continue

                if post_date <= last_post_date:
                    logger.info(f"Stopping post collection for group {group_id} as post date is before or equal to last post date")
                    logger.info(f"Post date: {post_date}, Last post date: {last_post_date}")
                    return new_posts

                if 'copy_history' in post:
                    if include_reposts:
                        original_post = post['copy_history'][0]
                        original_post['date'] = post_date.timestamp()
                        post = original_post
                    else:
                        continue



                post_data = format_post_data(post, group_id)
                if post_data:
                    new_posts.append(post_data)

            #offset += 100
            pbar.update(100)

    post_cache = {}

    for post in all_posts:
        photo_links = tuple(post['photos'])
        if photo_links not in post_cache or post_cache[photo_links]['date'] < post['date']:
            post_cache[photo_links] = post 

    return list(post_cache.values())
