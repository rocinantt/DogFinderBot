import os
import vk_api
import logging
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение переменных окружения
TOKEN = os.getenv('TOKEN')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DATABASE_URL = os.getenv('DATABASE_URL')

# Инициализация сессии VK API
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Проверка на наличие обязательных переменных окружения
if not TOKEN:
    logger.error("Переменная окружения 'TOKEN' не найдена!")
    raise ValueError("Переменная окружения 'TOKEN' не может быть пустой")
if not DATABASE_URL:
    logger.error("Переменная окружения 'DATABASE_URL' не найдена!")
    raise ValueError("Переменная окружения 'DATABASE_URL' не может быть пустой")