#config.py
import os
import logging
from dotenv import load_dotenv
logger = logging.getLogger(__name__)

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

# Проверка загрузки переменных окружения
if not API_TOKEN:
    logger.error("TELEGRAM_TOKEN not found in environment variables")
else:
    logger.info("TELEGRAM_TOKEN loaded successfully.")

if not DATABASE_URL:
    logger.error("DATABASE_URL not found in environment variables")
else:
    logger.info("DATABASE_URL loaded successfully")


