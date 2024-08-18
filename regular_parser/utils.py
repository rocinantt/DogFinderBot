#utils.py
import re


#Отдельный словарь для районов Санкт-Петербурга
spb_district_dict = {
    "выборгский":  ("Ленинградская область", "Санкт-Петербург", "Выборгский"),
    "адмиралтейский": ("Ленинградская область", "Санкт-Петербург", "Адмиралтейский"),
    "василеостровский": ("Ленинградская область", "Санкт-Петербург", "Василеостровский"),
    "калининский": ("Ленинградская область", "Санкт-Петербург", "Калининский"),
    "кировский": ("Ленинградская область", "Санкт-Петербург", "Кировский"),
    "колпинский": ("Ленинградская область", "Санкт-Петербург", "Колпинский"),
    "красногвардейский": ("Ленинградская область", "Санкт-Петербург", "Красногвардейский"),
    "красносельский": ("Ленинградская область", "Санкт-Петербург", "Красносельский"),
    "кронштадтский": ("Ленинградская область", "Санкт-Петербург", "Кронштадтский"),
    "курортный": ("Ленинградская область", "Санкт-Петербург", "Курортный"),
    "московский": ("Ленинградская область", "Санкт-Петербург", "Московский"),
    "невский": ("Ленинградская область", "Санкт-Петербург", "Невский"),
    "петроградский": ("Ленинградская область", "Санкт-Петербург", "Петроградский"),
    "приморский": ("Ленинградская область", "Санкт-Петербург", "Приморский"),
    "пушкинский": ("Ленинградская область", "Санкт-Петербург", "Пушкинский"),
    "фрунзенский": ("Ленинградская область", "Санкт-Петербург", "Фрунзенский"),
    "центральный": ("Ленинградская область", "Санкт-Петербург", "Центральный"),
    "петродворцовый": ("Ленинградская область", "Санкт-Петербург", "Петродворцовый")
}

#Отдельный словарь для крупных объектов
lo_dict = {
    "всеволожский": ("Ленинградская область", "Всеволожский", None),
    "гатчинский": ("Ленинградская область", "Гатчинский", None),
    'выборгский': ("Ленинградская область", "Выборгский", None),
    "бокситогорский": ("Ленинградская область", "Бокситогорский", None),
    "волосовский": ("Ленинградская область", "Волосовский", None),
    "волховский": ("Ленинградская область", "Волховский", None),
    "кингисеппский": ("Ленинградская область", "Кингисеппский", None),
    "киришский": ("Ленинградская область", "Киришский", None),
    "кировский": ("Ленинградская область", "Кировский", None),
    "лодейнопольский": ("Ленинградская область", "Лодейнопольский", None),
    "ломоносовский": ("Ленинградская область", "Ломоносовский", None),
    "лужский": ("Ленинградская область", "Лужский", None),
    "подпорожский": ("Ленинградская область", "Подпорожский", None),
    "приозерский": ("Ленинградская область", "Приозерский", None),
    "сланцевский": ("Ленинградская область", "Сланцевский", None),
    "тихвинский": ("Ленинградская область", "Тихвинский", None),
    "тосненский": ("Ленинградская область", "Тосненский", None),
    "мурино": ("Ленинградская область", "Всеволожский", None),
    "кудрово": ("Ленинградская область", "Всеволожский", None),
    "спб": ("Ленинградская область", "Санкт-Петербург", None),
    "питер": ("Ленинградская область", "Санкт-Петербург", None),
    "санкт-петербург": ("Ленинградская область", "Санкт-Петербург", None),
}


def find_all_locations(text):
    # Формирование регулярных выражений
    pattern_spb = re.compile(r'\b(' + '|'.join(re.escape(key) for key in spb_district_dict.keys()) + r')\b',
                             re.IGNORECASE)
    pattern_lo = re.compile(r'\b(' + '|'.join(re.escape(key) for key in lo_dict.keys()) + r')\b', re.IGNORECASE)

    # Проверка типа данных и извлечение текста из списка, если нужно
    if isinstance(text, list):
        text = ' '.join(text)  # Соединяем элементы списка в одну строку

    text_lower = text.lower()

    # Ищем по районам Санкт-Петербурга
    keys_spb = pattern_spb.findall(text_lower)
    locations = []

    # Флаг для учета только одного упоминания СПБ
    spb_found = False

    if keys_spb:
        for key in keys_spb:
            locations.append(spb_district_dict[key])

    else:
        # Ищем по районам Ленинградской области (включая СПБ и Питер)
        keys_lo = pattern_lo.findall(text_lower)
        for key in keys_lo:
            if key in ['спб', 'питер', 'санкт-петербург']:
                if not spb_found:
                    locations.append(lo_dict[key])
                    spb_found = True
            else:
                locations.append(lo_dict[key])


    return locations


def filter_other_animal(text):
    excluded_words = r"(?:\b|\s|#)(кот|кота|кошка|кошку|котенок|котик|попугай|котёнок)\b|#\S*(кот|кота|кошка|кошку|котенок|котик|попугай|котёнок)\S*"
    pattern = re.compile(excluded_words, re.IGNORECASE)
    return bool(pattern.search(text))
