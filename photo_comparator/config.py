import os
import logging
from dotenv import load_dotenv

# Настройка логирования
logger = logging.getLogger(__name__)

# Загрузка переменных окружения из файла .env
load_dotenv()

# Параметры подключения к базе данных
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    logger.error("DATABASE_URL не определен в переменных окружения")
    raise ValueError("DATABASE_URL не может быть пустым")