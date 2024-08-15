#config.py
import os
from dotenv import load_dotenv
import vk_api
import logging

# Load environment variables from .env file
load_dotenv()

# Get environment variables
TOKEN = os.getenv('TOKEN')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DATABASE_URL = os.getenv('DATABASE_URL')

# Initialize VK API session
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

