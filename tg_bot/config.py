#config.py
import os
import logging
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

# Проверка загрузки переменных окружения
if not API_TOKEN:
    logging.error("TELEGRAM_TOKEN not found in environment variables")
else:
    logging.info(f"TELEGRAM_TOKEN loaded successfully.")

if not DATABASE_URL:
    logging.error("DATABASE_URL not found in environment variables")
else:
    logging.info(f"DATABASE_URL loaded successfully: {DATABASE_URL}")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)
