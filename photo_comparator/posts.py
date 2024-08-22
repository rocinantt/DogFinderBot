from datetime import datetime, timedelta
from database import get_db_connection
from typing import Optional


async def get_posts(region: str, days: int, animal_type: str, area: Optional[str] = None,
                    district: Optional[str] = None, unassigned: bool = False):
    conn = await get_db_connection()
    try:
        date_threshold = datetime.now() - timedelta(days=days)

        query = """
        SELECT post_link, features, date
        FROM vk_posts
        WHERE region = $1 AND date >= $2 AND animal_type = $3
        """

        params = [region, date_threshold, animal_type]

        if unassigned:
            query += " AND area = ''"
        else:
            if area:
                query += " AND area = $4"
                params.append(area)
            if district:
                query += " AND district = $5"
                params.append(district)

        return await conn.fetch(query, *params)
    finally:
        await conn.close()