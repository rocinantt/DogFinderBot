# keyboards.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from database import get_regions, get_areas, get_districts
#from locations import  get_areas_by_region, get_districts_by_area

def get_regions_markup():
    builder = ReplyKeyboardBuilder()
    for region in get_regions():
        builder.add(KeyboardButton(text=region))
    return builder.as_markup(resize_keyboard=True)

def get_areas_markup(region):
    """Генерирует клавиатуру с выбором area."""
    builder = ReplyKeyboardBuilder()
    for area in get_areas(region):
        builder.add(KeyboardButton(text=area))
    builder.add(KeyboardButton(text="Пропустить"))
    builder.add(KeyboardButton(text="Нераспределенные"))
    return builder.as_markup(resize_keyboard=True)

def get_districts_markup(districts):
    """Генерирует клавиатуру с выбором районов СПБ."""
    builder = ReplyKeyboardBuilder()
    for district in districts:
        builder.add(KeyboardButton(text=district))
    builder.add(KeyboardButton(text="Пропустить"))
    return builder.as_markup(resize_keyboard=True)

def get_days_markup():
    builder = ReplyKeyboardBuilder()
    days_options = [1, 3, 7, 15]
    for days in days_options:
        builder.add(KeyboardButton(text=str(days)))
    builder.add(KeyboardButton(text="Ввести свое количество дней"))
    return builder.as_markup(resize_keyboard=True)


