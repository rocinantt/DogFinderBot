import asyncpg
from config import DATABASE_URL

async def get_db_connection():
    """Create a connection to the database."""
    conn = await asyncpg.connect(DATABASE_URL)
    return conn
