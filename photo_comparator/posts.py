from datetime import datetime, timedelta
from database import get_db_connection
from typing import Optional

async def get_posts(region: str, days: int, city: Optional[str] = None):
    """Retrieve posts from the database."""
    conn = await get_db_connection()

    date_threshold = datetime.now() - timedelta(days=days)

    query = """
    SELECT vk_posts.post_link, vk_posts.features, vk_posts.date
    FROM vk_posts
    JOIN vk_groups ON vk_posts.group_id = vk_groups.group_id
    WHERE vk_groups.region = $1 AND ($2::text IS NULL OR vk_groups.city = $2) AND vk_posts.date >= $3
    """
    posts = await conn.fetch(query, region, city, date_threshold)
    await conn.close()
    return posts
