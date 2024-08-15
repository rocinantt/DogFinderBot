#config.py
import os
from dotenv import load_dotenv
import vk_api
import logging

load_dotenv()

TOKEN = os.getenv('TOKEN')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DATABASE_URL = os.getenv('DATABASE_URL')

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)