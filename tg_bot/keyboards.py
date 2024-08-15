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
    for area in get_areas(region):
        builder.button(text=area, callback_data=f"area_{area}")
        builder.adjust(3)
    builder.button(text="Пропустить", callback_data="skip_area")
    builder.button(text="Нераспределенные", callback_data="unassigned")
    builder.adjust(3)

    return builder.as_markup()

def get_districts_markup(districts):
    """Генерирует клавиатуру с выбором районов."""
    builder = InlineKeyboardBuilder()
    for district in districts:
        builder.button(text=district, callback_data=f"district_{district}")
        builder.adjust(3)
    builder.button(text="Пропустить", callback_data="skip_district")

    return builder.as_markup()

def get_days_markup():
    days_options = [1, 3, 7, 15]
    builder = InlineKeyboardBuilder()
    for days in days_options:
        builder.button(text=str(days), callback_data=f"days_{days}")
    builder.button(text="Ввести свое количество дней", callback_data="custom_days")
    builder.adjust(2)
    return builder.as_markup()
