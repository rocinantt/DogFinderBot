#config.py
import os
import logging
from dotenv import load_dotenv
from arq.connections import RedisSettings

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

