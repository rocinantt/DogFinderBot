from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import get_regions, get_areas, get_districts


def get_regions_markup():
    """
    Генерирует клавиатуру с выбором региона.
    """
    builder = InlineKeyboardBuilder()
    for region in get_regions():
        builder.button(text=region, callback_data=f"region_{region}")
    builder.adjust(2)
    return builder.as_markup()


def get_areas_markup(region, animal_type):
    """
    Генерирует клавиатуру с выбором области.

    :param region: регион
    :param animal_type: тип животного (собака или кошка)
    :return: инлайн-клавиатура
    """
    builder = InlineKeyboardBuilder()
    areas = get_areas(region, animal_type)

    for area, count in areas:
        button_text = f"{area} ({count})"
        builder.button(text=button_text, callback_data=f"area_{area}")
    builder.adjust(2)
    builder.button(text="Пропустить", callback_data="skip_area")
    builder.button(text="Нераспределенные", callback_data="unassigned")
    builder.adjust(2)

    return builder.as_markup()


def get_districts_markup(area, animal_type):
    """
    Генерирует клавиатуру с выбором района.

    :param area: область
    :param animal_type: тип животного (собака или кошка)
    :return: инлайн-клавиатура
    """
    builder = InlineKeyboardBuilder()
    districts = get_districts(area, animal_type)

    for district, count in districts:
        button_text = f"{district} ({count})"
        builder.button(text=button_text, callback_data=f"district_{district}")
    builder.adjust(2)
    builder.button(text="Пропустить", callback_data="skip_district")
    builder.adjust(2)

    return builder.as_markup()


def get_days_markup():
    """
    Генерирует клавиатуру с выбором периода в днях.

    :return: инлайн-клавиатура
    """
    days_options = [1, 3, 7, 15, 20, 30]
    builder = InlineKeyboardBuilder()
    for days in days_options:
        builder.button(text=str(days), callback_data=f"days_{days}")
        builder.adjust(2)
    return builder.as_markup()


def get_more_results_markup():
    """
    Генерирует клавиатуру с кнопками для показа дополнительных результатов или начала заново.

    :return: инлайн-клавиатура
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="Показать еще", callback_data="more_results")
    builder.button(text="Начать заново", callback_data="start")
    builder.adjust(2)
    return builder.as_markup()


def get_animal_type_markup():
    """
    Генерирует клавиатуру с выбором типа животного (собака или кошка).

    :return: инлайн-клавиатура
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="🐶", callback_data="dog")
    builder.button(text="🐱", callback_data="cat")
    builder.adjust(2)
    return builder.as_markup()


def start_again_markup():
    """
    Генерирует клавиатуру для начала поиска заново.

    :return: инлайн-клавиатура
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="Начать заново", callback_data="start")
    return builder.as_markup()