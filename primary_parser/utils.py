#utils.py
import re
from regions_dict import regions_dict


def normalize_text(text):
    """Приводит текст к нижнему регистру и заменяет небуквенные символы на пробелы."""
    text = text.lower()
    text = re.sub(r'[^a-zA-Zа-яА-Я0-9\s]', ' ', text)
    return text

def find_all_locations(normalized_text, default_region, default_area, default_district):
    """
    Извлекает локации из нормализованного текста на основании текущей области.

    :param normalized_text: нормализованный текст
    :param default_region: регион по умолчанию
    :param default_area: область по умолчанию
    :param default_district: район по умолчанию
    :return: список найденных локаций или дефолтные значения
    """
    locations = []

    # Проверка на районы главного города
    for district, location in regions_dict.get(default_region, {}).get('districts', {}).items():
        if district in normalized_text:
            locations.append(location)

    # Проверка на районы области
    if not locations:
        for area, location in regions_dict.get(default_region, {}).get('areas', {}).items():
            if area in normalized_text:
                locations.append(location)

    # Если локации не найдены, возвращаем дефолтные
    if not locations:
        locations.append((default_region, default_area, default_district))

    return locations

def determine_animal_type(normalized_text):
    """
    Определяет тип животного на основе нормализованного текста поста.

    :param normalized_text: нормализованный текст поста
    :return: 'cat' или 'dog' в зависимости от найденных ключевых слов
    """
    cat_keywords = r"\b(кот|кота|кошка|кошку|котенок|котик|киса|киска|коты|киску|котом|кошке|котятам|котёнок|котятки|кошки|котенка|кошечка|кошечку|кошечки|котята)\b"
    if re.search(cat_keywords, normalized_text):
        return 'cat'
    return 'dog'


