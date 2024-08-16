#utils.py
import os
import aiohttp
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from config import API_TOKEN
from aiogram import Bot
from config import logger
from keyboards import get_more_results_markup

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
# Search for similar posts
# Search for similar posts
async def search_similar_posts(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    photo_file_id = data['photo']
    region = data.get('region')
    days = data['days']
    area = data.get('area')
    district = data.get('district')
    unassigned = data.get('unassigned', False)
    file_info = await Bot(token=API_TOKEN).get_file(photo_file_id)
    image_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}"

    query_params = {
        'image_url': image_url,
        'region': region,
        'days': days,
    }

    if unassigned:
        query_params['unassigned'] = True
    else:
        query_params['area'] = area
        if district:
            query_params['district'] = district

    logger.info(f"Пользователь {user_id} запрашивает поиск с параметрами: {query_params}")

    try:
        async with aiohttp.ClientSession() as session:
            logger.info("Sending request to photo comparator service...")
            async with session.post('http://photo_comparator:5000/compare', json=query_params, timeout=aiohttp.ClientTimeout(total=60)) as response:
                logger.info(f"Received response with status: {response.status}")
                if response.status == 200:
                    results = await response.json()
                    await state.update_data(results=results)
                    logger.info(f"len results {len(results)}")
                    await send_results(message, results[:5])

                else:
                    logger.error(f"Error response from photo_comparator: {response.status}")
                    await message.answer("Произошла ошибка при поиске. Пожалуйста, попробуйте снова позже.")
    except Exception as e:
        logger.exception(f"Exception during search_similar_posts: {e}")
        await message.answer("Произошла ошибка при поиске. Пожалуйста, попробуйте снова позже.")
    finally:
        await session.close()  # Явное закрытие сессии




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

    if len(results) == 5:
        await message.answer("Нажмите кнопку ниже для получения следующих результатов.",
                             reply_markup=get_more_results_markup())


