#main.py
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from handlers import register_handlers
from config import API_TOKEN

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Check if API_TOKEN is available
if not API_TOKEN:
    logging.error("TELEGRAM_TOKEN not found in environment variables")
    exit(1)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Register handlers
register_handlers(dp)

if __name__ == '__main__':
    logging.info("Starting bot")
    dp.run_polling(bot, polling_timeout=3)
