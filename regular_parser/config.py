import os
import vk_api
import logging
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение переменных окружения
TOKEN = os.getenv('TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')

# Инициализация сессии VK API
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Проверка наличия обязательных переменных окружения
if not TOKEN:
    logger.error("Переменная окружения 'TOKEN' не найдена!")
    raise ValueError("Переменная окружения 'TOKEN' не может быть пустой")
if not DATABASE_URL:
    logger.error("Переменная окружения 'DATABASE_URL' не найдена!")
    raise ValueError("Переменная окружения 'DATABASE_URL' не может быть пустой")
