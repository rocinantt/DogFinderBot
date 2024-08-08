# keyboards.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from database import get_regions, get_cities

def get_regions_markup():
    builder = ReplyKeyboardBuilder()
    for region in get_regions():
        builder.add(KeyboardButton(text=region))
    return builder.as_markup(resize_keyboard=True)

def get_cities_markup(region):
    builder = ReplyKeyboardBuilder()
    cities = get_cities(region)
    if cities:
        for city in cities:
            builder.add(KeyboardButton(text=city))
        builder.add(KeyboardButton(text="Пропустить"))
    return builder.as_markup(resize_keyboard=True)

def get_days_markup():
    builder = ReplyKeyboardBuilder()
    days_options = [1, 3, 7]
    for days in days_options:
        builder.add(KeyboardButton(text=str(days)))
    builder.add(KeyboardButton(text="Ввести свое количество дней"))
    return builder.as_markup(resize_keyboard=True)


