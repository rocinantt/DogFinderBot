# keyboards.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from database import get_regions, get_areas, get_districts
#from locations import  get_areas_by_region, get_districts_by_area

def get_regions_markup():
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=region, callback_data=f"region_{region}")]
        for region in get_regions()
    ])
    return markup

def get_areas_markup(region):
    """Генерирует клавиатуру с выбором area."""
    markup = InlineKeyboardMarkup()
    for area in get_areas(region):
        markup.add(InlineKeyboardButton(text=area, callback_data=f"area_{area}"))
    markup.add(InlineKeyboardButton(text="Пропустить", callback_data="skip_area"))
    markup.add(InlineKeyboardButton(text="Нераспределенные", callback_data="unassigned"))
    return markup

def get_districts_markup(districts):
    """Генерирует клавиатуру с выбором районов."""
    markup = InlineKeyboardMarkup()
    for district in districts:
        markup.add(InlineKeyboardButton(text=district, callback_data=f"district_{district}"))
    markup.add(InlineKeyboardButton(text="Пропустить", callback_data="skip_district"))
    return markup

def get_days_markup():
    markup = InlineKeyboardMarkup()
    days_options = [1, 3, 7, 15]
    for days in days_options:
        markup.add(InlineKeyboardButton(text=str(days), callback_data=f"days_{days}"))
    markup.add(InlineKeyboardButton(text="Ввести свое количество дней", callback_data="custom_days"))
    return markup


