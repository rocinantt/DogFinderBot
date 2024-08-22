#keyboards.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import get_regions, get_areas, get_districts

def get_regions_markup():
    builder = InlineKeyboardBuilder()
    for region in get_regions():
        builder.button(text=region, callback_data=f"region_{region}")
    builder.adjust(2)
    return builder.as_markup()

def get_areas_markup(region):
    """Генерирует клавиатуру с выбором area."""
    builder = InlineKeyboardBuilder()
    areas = get_areas(region)

    for area, count in areas:
        button_text = f"{area} ({count})"
        builder.button(text=button_text, callback_data=f"area_{area}")
    builder.adjust(2)
    builder.button(text="Пропустить", callback_data="skip_area")
    builder.button(text="Нераспределенные", callback_data="unassigned")
    builder.adjust(2)

    return builder.as_markup()

def get_districts_markup(districts):
    """Генерирует клавиатуру с выбором районов."""
    builder = InlineKeyboardBuilder()

    for district, count in districts:
        button_text = f"{district} ({count})"
        builder.button(text=button_text, callback_data=f"district_{district}")
    builder.adjust(2)
    builder.button(text="Пропустить", callback_data="skip_district")
    builder.adjust(2)

    return builder.as_markup()

def get_days_markup():
    days_options = [1, 3, 7, 10, 20, 30]
    builder = InlineKeyboardBuilder()
    for days in days_options:
        builder.button(text=str(days), callback_data=f"days_{days}")
        builder.adjust(2)
    return builder.as_markup()

def get_more_results_markup():
    builder = InlineKeyboardBuilder()
    builder.button(text="Показать еще", callback_data="more_results")
    builder.button(text="Начать заново", callback_data="start")
    builder.adjust(2)
    return builder.as_markup()

def get_animal_type_markup():
    builder = InlineKeyboardBuilder()
    builder.button(text="🐶", callback_data="animal_dog")
    builder.button(text="🐱", callback_data="animal_cat")
    builder.adjust(2)
    return builder.as_markup()

def start_again_markup():
    builder = InlineKeyboardBuilder()
    builder.button(text="Начать заново", callback_data="start")
    return builder.as_markup()