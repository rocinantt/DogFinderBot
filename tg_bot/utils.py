import os
import aiohttp
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from config import API_TOKEN
from aiogram import Bot
from config import logger

# Load FAQ file
def load_faq():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'faq.md'), 'r', encoding='utf-8') as file:
            faq_content = file.read()
        return faq_content
    except FileNotFoundError:
        logger.error("FAQ file not found")
        return "FAQ файл не найден. Пожалуйста, попробуйте позже."

# Search for similar posts
async def search_similar_posts(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    photo_file_id = data['photo']
    region = data.get('region')
    days = data['days']
    city = data.get('city')

    bot = Bot(token=API_TOKEN)
    async with bot:
        photo_file = await bot.get_file(photo_file_id)
        photo_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{photo_file.file_path}"
        logger.info(f"Пользователь {user_id} загрузил фото {photo_url}")
        session = aiohttp.ClientSession()
        try:
            async with session.post('http://photo_comparator:5000/compare', json={
                'image_url': photo_url,
                'region': region,
                'days': days,
                'city': city
            }, timeout=aiohttp.ClientTimeout(total=60)) as response:
                if response.status == 200:
                    results = await response.json()
                    await send_results(message, results)
                else:
                    logger.error(f"Error response from photo_comparator: {response.status}")
                    await message.answer("Произошла ошибка при поиске. Пожалуйста, попробуйте снова позже.")
        except Exception as e:
            logger.exception(f"Exception during search_similar_posts: {e}")
            await message.answer("Произошла ошибка при поиске. Пожалуйста, попробуйте снова позже.")
        finally:
            await session.close()

# Send results to the user
async def send_results(message: types.Message, results):
    if not results:
        await message.answer("Не найдено объявлений по заданным критериям.")
        return

    for index, result in enumerate(results, 1):
        text = f"""
        <b>#{index}  {result['date']}</b>
{result['post_link']}
        """
        await message.answer(text, parse_mode=ParseMode.HTML)
