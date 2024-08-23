import asyncpg
from config import DATABASE_URL, logger

async def get_db_connection():
    """Создает и возвращает соединение с базой данных."""
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        return conn
    except asyncpg.PostgresError as e:
        logger.error(f"Ошибка при подключении к базе данных: {e}")
        raise

