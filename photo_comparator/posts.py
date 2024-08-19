#posts.py
from datetime import datetime, timedelta
from database import get_db_connection
from typing import Optional

async def get_posts(region: str, days: int, area: Optional[str] = None, district: Optional[str] = None, unassigned: bool = False):
    conn = await get_db_connection()
    try:
        date_threshold = datetime.now() - timedelta(days=days)

        query = """
        SELECT post_link, features, date
        FROM vk_posts
        WHERE region = $1 AND date >= $2
        """

        params = [region, date_threshold]

        if unassigned:
            query += " AND area = ''"
        else:
            if area:
                query += " AND area = $3"
                params.append(area)
            if district:
                query += " AND district = $4"
                params.append(district)

        return await conn.fetch(query, *params)
    finally:
        await conn.close()
