#main.py
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import API_TOKEN, logger
from handlers import register_handlers

# Инициализация бота и диспетчера
try:
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    logging.info("Бот и диспетчер успешно инициализированы.")
except Exception as e:
    logging.error(f"Ошибка инициализации бота или диспетчера: {e}")
    exit(1)

# Регистрация обработчиков
register_handlers(dp)

if __name__ == '__main__':
    logging.info("Запуск бота")
    dp.run_polling(bot, polling_timeout=3)
