from datetime import datetime, timedelta
from database import get_db_connection
from typing import Optional

async def get_posts(region: str, days: int, area: Optional[str] = None, district: Optional[str] = None, unassigned: bool = False):
    """Retrieve posts from the database."""
    conn = await get_db_connection()

    date_threshold = datetime.now() - timedelta(days=days)

    query = """
    SELECT vk_posts.post_link, vk_posts.features, vk_posts.date
    FROM vk_posts
    JOIN vk_groups ON vk_posts.group_id = vk_groups.group_id
    WHERE vk_groups.region = $1 AND vk_posts.date >= $2
    """

    params = [region, date_threshold]

    if unassigned:
        query += " AND vk_posts.area IS NULL AND vk_posts.district IS NULL"
    else:
        if area:
            query += " AND vk_groups.area = $3"
            params.append(area)
        if district:
            query += " AND vk_groups.district = $4"
            params.append(district)

    posts = await conn.fetch(query, *params)
    await conn.close()
    return posts
