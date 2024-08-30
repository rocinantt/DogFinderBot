#utils.py
import os
import aiohttp
import asyncio
from aiogram import types, Dispatcher, Bot
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_TOKEN, logger
from keyboards import get_more_results_markup, start_again_markup


def load_faq():
    """
    Загружает FAQ из файла.

    :return: содержимое файла FAQ
    """
    try:
        with open(os.path.join(os.path.dirname(__file__), 'faq.md'), 'r', encoding='utf-8') as file:
            faq_content = file.read()
        return faq_content
    except FileNotFoundError:
        logger.error("FAQ файл не найден")
        return "FAQ файл не найден. Пожалуйста, попробуйте позже."


async def search_similar_posts(message: types.Message, state: FSMContext):
    """
    Выполняет поиск похожих постов с помощью сервиса photo_comparator.

    :param message: сообщение пользователя
    :param state: состояние FSM
    """

    data = await state.get_data()
    user_id = data['user_id']
    photo_file_id = data['photo']
    region = data.get('region')
    days = data['days']
    animal_type = data['animal_type']
    area = data.get('area')
    district = data.get('district')
    unassigned = data.get('unassigned', False)
    file_info = await message.bot.get_file(photo_file_id)
    image_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}"

    query_params = {
        'image_url': image_url,
        'region': region,
        'days': days,
        'animal_type': animal_type,
    }

    if unassigned:
        query_params['unassigned'] = True
    else:
        query_params['area'] = area
        if district:
            query_params['district'] = district

    name, last_name = user_id.first_name, user_id.last_name
    logger.info(f"Пользователь {user_id}, {name, last_name} запрашивает поиск с параметрами: {query_params}")

    try:
        async with aiohttp.ClientSession() as session:
            logger.info("Отправка запроса в сервис photo_comparator...")
            async with session.post('http://photo_comparator:5000/compare', json=query_params,
                                    timeout=aiohttp.ClientTimeout(total=60)) as response:
                logger.info(f"Ответ от photo_comparator: статус {response.status}")
                if response.status == 200:
                    results = await response.json()
                    await state.update_data(results=results)
                    await send_results(message, results[:5], 0)
                else:
                    logger.error(f"Ошибка ответа от photo_comparator: {response.status}")
                    await message.answer("Произошла ошибка при поиске. Пожалуйста, попробуйте снова позже.")
    except Exception as e:
        logger.exception(f"Исключение при поиске похожих постов: {e}")
        await message.answer("Произошла ошибка при поиске. Пожалуйста, попробуйте снова позже.")
    finally:
        await session.close()


async def send_results(message: types.Message, results, offset):
    """
    Отправляет результаты поиска пользователю.

    :param message: сообщение пользователя
    :param results: результаты поиска
    :param offset: смещение для отображения постов
    """
    if not results:
        await message.answer("Не найдено объявлений по заданным критериям.", reply_markup=start_again_markup())
        return

    for index, result in enumerate(results, offset + 1):
        text = f"""
        <b>#{index}  {result['date']}</b>
{result['post_link']}
        """
        await message.answer(text, parse_mode=ParseMode.HTML)

    if len(results) > 0:
        await message.answer('Не нашли нужный пост?', reply_markup=get_more_results_markup())
    else:
        await message.answer('Все загруженные посты показаны.', reply_markup=start_again_markup())





