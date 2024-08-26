import asyncpg
from datetime import datetime, timedelta
from typing import Optional
from time import time

from database import get_db_connection
from config import logger


async def get_posts(region: str, days: int, animal_type: str, area: Optional[str] = None,
                    district: Optional[str] = None, unassigned: bool = False):
    """
    Получает посты из базы данных по заданным критериям.

    :param region: регион поиска
    :param days: количество дней для фильтрации
    :param animal_type: тип животного (собака или кошка)
    :param area: область поиска (опционально)
    :param district: район поиска (опционально)
    :param unassigned: флаг, указывающий на нераспределенные области (по умолчанию False)
    :return: список постов, соответствующих критериям
    :rtype: List[dict]
    """
    start_time = time()
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
        posts = await conn.fetch(query, *params)
        logger.info(f"Время выполнения get_posts: {time() - start_time:.2f} секунд")
        return posts
    except asyncpg.PostgresError as e:
        logger.error(f"Ошибка выполнения запроса к базе данных: {e}")
        raise
    finally:
        await conn.close()