import os
import redis
import logging
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения из файла .env
load_dotenv()

# Параметры API и базы данных
API_TOKEN = os.getenv("TELEGRAM_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

# Проверка загрузки переменных окружения
if not API_TOKEN:
    logger.error("Переменная окружения TELEGRAM_TOKEN не найдена.")
else:
    logger.info("TELEGRAM_TOKEN успешно загружен.")

if not DATABASE_URL:
    logger.error("Переменная окружения DATABASE_URL не найдена.")
else:
    logger.info("DATABASE_URL успешно загружен.")

# Подключение к Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)