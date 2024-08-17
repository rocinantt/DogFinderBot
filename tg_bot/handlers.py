#handlers.py
import logging
import asyncio
from aiogram import types, F, Dispatcher, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from keyboards import get_regions_markup, get_days_markup, get_areas_markup, get_districts_markup
from utils import load_faq, search_similar_posts, send_results
from database import get_user_region, save_user_region, get_groups, get_districts
from config import logger

router = Router()


class Form(StatesGroup):
    photo = State()
    region = State()
    area = State()
    district = State()
    days = State()


def register_handlers(dp: Dispatcher):
    dp.message.register(send_welcome, Command(commands=['start']))
    dp.message.register(handle_faq, Command(commands=['faq']))
    dp.message.register(handle_change_region, Command(commands=['change_region']))
    dp.message.register(handle_get_groups, Command(commands=['get_groups']))
    dp.message.register(handle_end, Command(commands=['end']))
    dp.message.register(handle_photo, Form.photo, F.content_type == types.ContentType.PHOTO)

    dp.callback_query.register(handle_region, F.data.startswith("region_"))
    dp.callback_query.register(handle_area, F.data.startswith("area_"))
    dp.callback_query.register(handle_district, F.data.startswith("district_"))
    dp.callback_query.register(handle_days, F.data.startswith("days_"))
    dp.callback_query.register(handle_unassigned, F.data == "unassigned")
    dp.callback_query.register(skip_area, F.data == "skip_area")
    dp.callback_query.register(skip_district, F.data == "skip_district")
    dp.callback_query.register(custom_days, F.data == "custom_days")
    dp.callback_query.register(handle_more_results, F.data == "more_results")
    dp.callback_query.register(handle_start, F.data == "start")

@router.message(Command(commands=['start']))
async def send_welcome(message: types.Message, state: FSMContext):
    await state.clear()
    user_region = get_user_region(message.from_user.id)
    if user_region:
        await message.answer(
            f"Привет! Ваш текущий регион: {user_region}. Отправьте мне фото найденной Вами собаки, и я помогу найти похожие объявления о пропавших.",
            reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(Form.photo)
    else:
        logging.info(f"Пользователь {message.from_user.id} начал пользоваться ботом")
        await message.answer("Привет! Я DogFinderBot. Для начала выберите регион.", reply_markup=get_regions_markup())
        await state.set_state(Form.region)


@router.message(Command(commands=['faq']))
async def handle_faq(message: types.Message):
    faq_content = load_faq()
    await message.answer(faq_content, parse_mode='Markdown', reply_markup=types.ReplyKeyboardRemove())


@router.message(Command(commands=['change_region']))
async def handle_change_region(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, выберите новый регион.", reply_markup=get_regions_markup())
    await state.set_state(Form.region)


@router.callback_query(F.data.startswith("region_"))
async def handle_region(callback_query: CallbackQuery, state: FSMContext):
    region = callback_query.data.split("_")[1]
    logger.info(f"Region selected by {callback_query.from_user.id}: {region}")
    save_user_region(callback_query.from_user.id, region)
    await callback_query.message.edit_text(f"Вы выбрали регион {region}. Теперь отправьте фото найденной собаки.")
    await state.set_state(Form.photo)


@router.message(Form.photo, F.content_type == types.ContentType.PHOTO)
async def handle_photo(message: types.Message, state: FSMContext):
    logger.info(f"Received photo from {message.from_user.id}")
    await state.update_data(photo=message.photo[-1].file_id)
    user_region = get_user_region(message.from_user.id)
    if user_region:
        await state.update_data(region=user_region)
        await message.answer("Фото получено, выберите район поиска. \nПропустить - поиск по всему региону.\nНерасgределенные - среди постов без указания адреса.",
                             reply_markup=get_areas_markup(user_region))
        await state.set_state(Form.area)
    else:
        await message.answer("Произошла ошибка. Пожалуйста, сначала выберите регион.",
                             reply_markup=get_regions_markup())
        await state.set_state(Form.region)


@router.callback_query(F.data.startswith("area_"))
async def handle_area(callback_query: CallbackQuery, state: FSMContext):
    area = callback_query.data.split("_")[1]
    logger.info(f"Area selected by {callback_query.from_user.id}: {area}")
    data = await state.get_data()

    await state.update_data(area=area, unassigned=False)
    districts = get_districts(area)
    if districts:
        await callback_query.message.edit_text("Вы можете сузить область поиска или нажать 'Пропустить'.",
                                               reply_markup=get_districts_markup(districts))
        await state.set_state(Form.district)
    else:
        await callback_query.message.edit_text(
            f"Вы выбрали {area}. За какой период искать объявления? Выберите из предложенных вариантов или введите свое количество дней.",
            reply_markup=get_days_markup())
        await state.set_state(Form.days)


@router.callback_query(F.data == "skip_area")
async def skip_area(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(area=None)
    await callback_query.message.edit_text(
        "Выбран поиск по всему региону. За какой период искать объявления? Выберите из предложенных вариантов или введите свое количество дней.",
        reply_markup=get_days_markup())
    await state.set_state(Form.days)


@router.callback_query(F.data.startswith("district_"))
async def handle_district(callback_query: CallbackQuery, state: FSMContext):
    district = callback_query.data.split("_")[1]
    logger.info(f"District selected by {callback_query.from_user.id}: {district}")
    await state.update_data(district=district)
    await callback_query.message.edit_text(
        f"Вы выбрали {district}. За какой период искать объявления? Выберите из предложенных вариантов или введите свое количество дней.",
        reply_markup=get_days_markup())
    await state.set_state(Form.days)


@router.callback_query(F.data.startswith("days_"))
async def handle_days(callback_query: CallbackQuery, state: FSMContext):
    days = int(callback_query.data.split("_")[1])
    logger.info(f"Days input by {callback_query.from_user.id}: {days}")
    await state.update_data(days=days)
    await callback_query.message.edit_text(
        "Начинаю поиск объявлений о пропавших собаках за выбранный период. Пожалуйста, подождите.")
    await search_similar_posts(callback_query.message, state)


@router.callback_query(F.data == "custom_days")
async def custom_days(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("Введите количество дней.", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Form.days)


@router.message(Command(commands=['get_groups']))
async def handle_get_groups(message: types.Message, state: FSMContext):
    user_region = get_user_region(message.from_user.id)
    if user_region:
        groups = get_groups(user_region)
        if groups:
            response = "\n".join(
                [f"{i + 1}. {group['group_name']}\n{group['group_link']}" for i, group in enumerate(groups)])
        else:
            response = "Группы не найдены."
        await message.answer(response, reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("Сначала выберите регион с помощью команды /change_region.")

@router.callback_query(F.data == "unassigned")
async def handle_unassigned(callback_query: CallbackQuery, state: FSMContext):
    logger.info(f"Unassigned selected by {callback_query.from_user.id}")
    await state.update_data(area=None, district=None, unassigned=True)
    await callback_query.message.edit_text("Выбраны нераспределенные посты. За какой период искать объявления? Выберите из предложенных вариантов или введите свое количество дней.", reply_markup=get_days_markup())
    await state.set_state(Form.days)

@router.callback_query(F.data == "skip_district")
async def skip_district(callback_query: CallbackQuery, state: FSMContext):
    logger.info(f"District skipped by {callback_query.from_user.id}")
    await state.update_data(district=None)
    await callback_query.message.edit_text("Вы пропустили выбор района. За какой период искать объявления? Выберите из предложенных вариантов или введите свое количество дней.", reply_markup=get_days_markup())
    await state.set_state(Form.days)


@router.callback_query(F.data == "more_results")
async def handle_more_results(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    results = data.get('results', [])
    offset = data.get('offset', 5)
    await callback_query.message.edit_reply_markup(reply_markup=None)
    if offset < len(results):
        await send_results(callback_query.message, results[offset:offset+5], offset)
        await state.update_data(offset=offset+5)  # Обновляем смещение
    else:
        await callback_query.message.answer("Больше постов нет. Перейдите в меню чтобы начать сначала")

@router.callback_query(F.data == 'start')
async def handle_start(callback_query: types.CallbackQuery, state: FSMContext):
    """Handles the start command initiated by inline keyboard."""
    await state.clear()
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await send_welcome(callback_query.message, state)


@router.message(Command(commands=['end']))
async def handle_end(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Сессия завершена. Для начала новой сессии перейдите в меню.")