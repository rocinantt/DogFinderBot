#utils.py
import re
from regions_dict import regions_dict


def normalize_text(text):
    """Приводит текст к нижнему регистру и заменяет небуквенные символы на пробелы."""
    text = text.lower()  # Приводим к нижнему регистру
    text = re.sub(r'[^a-zA-Zа-яА-Я0-9\s]', ' ', text)  # Заменяем все небуквенные символы на пробелы
    return text

def find_all_locations(normalized_text, default_region, default_area, default_district):
    """Извлекает локации из нормализованного текста на основании текущей области. Если локация не найдена, возвращает дефолтные значения."""
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
    """Определяет тип животного на основе нормализованного текста поста с помощью регулярного выражения."""
    cat_keywords = r"\b(кот|кота|кошка|кошку|котенок|котик|киса|киска|коты|киску|котом|кошке|котятам|котёнок|котятки|кошки|котенка|кошечка|кошечку|кошечки|котята)\b"
    if re.search(cat_keywords, normalized_text):
        return 'cat'
    return 'dog'


