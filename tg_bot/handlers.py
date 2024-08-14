#handlers.py
import logging
from aiogram import types, F, Dispatcher, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.enums import ParseMode
from keyboards import get_regions_markup,  get_days_markup, get_areas_markup, get_districts_markup
from utils import load_faq, search_similar_posts
from database import get_user_region, save_user_region, get_groups, get_areas, get_regions, get_districts
from config import logger
from locations import regions_data, get_districts_by_area, get_areas_by_region

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
    dp.message.register(handle_region, Form.region)
    dp.message.register(handle_area, Form.area)
    dp.message.register(handle_district, Form.district)
    dp.message.register(handle_days, Form.days)

@router.message(Command(commands=['start']))
async def send_welcome(message: types.Message, state: FSMContext):
    await state.clear()
    user_region = get_user_region(message.from_user.id)
    if user_region:
        await message.answer(f"Привет! Ваш текущий регион: {user_region}. Отправьте мне фото найденной Вами собаки, и я помогу найти похожие объявления о пропавших.", reply_markup=types.ReplyKeyboardRemove())
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

@router.message(Form.region)
async def handle_region(message: types.Message, state: FSMContext):
    logger.info(f"Region selected by {message.from_user.id}: {message.text}")
    save_user_region(message.from_user.id, message.text)
    await message.answer(f"Вы выбрали регион {message.text}. Теперь отправьте фото найденной собаки.", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Form.photo)

@router.message(Form.photo, F.content_type == types.ContentType.PHOTO)
async def handle_photo(message: types.Message, state: FSMContext):
    logger.info(f"Received photo from {message.from_user.id}")
    await state.update_data(photo=message.photo[-1].file_id)
    user_region = get_user_region(message.from_user.id)
    if user_region:
        await state.update_data(region=user_region)
        await message.answer("Фото получено, выберите район поиска или нажмите 'Нераспределенные' или 'Пропустить'.", reply_markup=get_areas_markup(user_region))
        await state.set_state(Form.area)
    else:
        await message.answer("Произошла ошибка. Пожалуйста, сначала выберите регион.", reply_markup=get_regions_markup())
        await state.set_state(Form.region)

@router.message(Form.area)
async def handle_area(message: types.Message, state: FSMContext):
    logger.info(f"Area selected by {message.from_user.id}: {message.text}")
    data = await state.get_data()

    if message.text == "Пропустить":
        await state.update_data(area=None)
        await message.answer("Выбран поиск по всему региону. За какой период искать объявления? Выберите из предложенных вариантов или введите свое количество дней.", reply_markup=get_days_markup())
        await state.set_state(Form.days)
    elif message.text == "Нераспределенные":
        await state.update_data(area=None, district=None, unassigned=True)
        await message.answer("Выбран поиск по нераспределенным постам. За какой период искать объявления? Выберите из предложенных вариантов или введите свое количество дней.", reply_markup=get_days_markup())
        await state.set_state(Form.days)
    else:
        await state.update_data(area=message.text, unassigned=False)
        # Проверка, если для выбранной области есть районы (districts)
        region = data['region']
        districts = get_districts_by_area(region, message.text)
        if districts:
            await message.answer("Вы можете сузить область поиска или нажать 'Пропустить'.",
                                 reply_markup=get_districts_markup(districts))
            await state.set_state(Form.district)
        else:
            await message.answer(
                f"Вы выбрали {message.text}. За какой период искать объявления? Выберите из предложенных вариантов или введите свое количество дней.",
                reply_markup=get_days_markup())
            await state.set_state(Form.days)

@router.message(Form.district)
async def handle_district(message: types.Message, state: FSMContext):
    logger.info(f"District selected by {message.from_user.id}: {message.text}")
    if message.text == "Пропустить":
        await state.update_data(district=None)
    else:
        await state.update_data(district=message.text)
    await message.answer(f"Вы выбрали {message.text} За какой период искать объявления? Выберите из предложенных вариантов или введите свое количество дней.", reply_markup=get_days_markup())
    await state.set_state(Form.days)

@router.message(Form.days)
async def handle_days(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        logger.info(f"Days input by {message.from_user.id}: {message.text}")
        await state.update_data(days=int(message.text))
        await message.answer("Начинаю поиск объявлений о пропавших собаках за выбранный период. Пожалуйста, подождите.", reply_markup=types.ReplyKeyboardRemove())
        await search_similar_posts(message, state)
    elif message.text == "Ввести свое количество дней":
        await message.answer("Введите количество дней.", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("Пожалуйста, выберите один из предложенных вариантов или введите свое количество дней.")

@router.message(Command(commands=['get_groups']))
async def handle_get_groups(message: types.Message, state: FSMContext):
    user_region = get_user_region(message.from_user.id)
    if user_region:
        groups = get_groups(user_region)
        if groups:
            response = "\n".join([f"{i+1}. {group['group_name']}\n{group['group_link']}" for i, group in enumerate(groups)])
        else:
            response = "Группы не найдены."
        await message.answer(response, reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("Сначала выберите регион с помощью команды /change_region.")

@router.message(Command(commands=['end']))
async def handle_end(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Сессия завершена. Для начала новой сессии используйте команду /start.")
