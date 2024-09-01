<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/rocinantt/sledoPET">
    <img src="https://github.com/rocinantt/DogFinderBot/blob/main/photo/logo.png" alt="Logo" width="768" height="768">
  </a>

  <h3 align="center"></h3>

  <h3 align="center">
    Бот, который помогает потерявшимся питомцам вернуться домой.
</h3>
<p>
    <br />
    <br />
    <a href="https://web.telegram.org/a/#7411138567">Использовать бота</a>
    ·
    <a href="https://github.com/rocinantt/sledoPET/issues/new?labels=bug&template=bug-report---.md">Сообщить о багах</a>
    ·
    <a href="https://github.com/rocinantt/sledoPET/issues/new?labels=enhancement&template=feature-request---.md">Предложить улучшение</a>
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

<img align="right" width="385" height="605" src="https://github.com/rocinantt/DogFinderBot/blob/main/photo/qr_new.png">
sledoPET — это Telegram-бот, созданный для быстрой помощи владельцам потерявшихся питомцев. Бот автоматически сопоставляет фотографии найденных животных с объявлениями о пропаже, повышая шансы на успешное возвращение питомцев домой.

### Как помогает бот:

Когда питомец теряется, его хозяевам приходится сталкиваться с множеством сложностей. Они вынуждены искать пропавшего друга, распространять объявления о пропаже, постоянно проверять информацию в группах и чатах, посвящённых потерянным животным. Однако даже активные поиски не всегда приносят результат. Люди, встретившие животное на улице, могут не состоять в тематических сообществах, бояться задерживать его или просто не иметь времени на просмотр множества объявлений, не зная точно, разыскивают ли питомца хозяева. В это время каждая минута имеет значение, так как увлеченное или, наоборот, испуганное и дезориентированное животное рискует попасть под машину, столкнуться с агрессией других животных или удалиться слишком далеко от зоны поиска.

sledoPET не является универсальным решением всех этих проблем, но он может стать важным дополнительным инструментом. Хозяева могут использовать его для мониторинга социальных сетей, а прохожие, заметившие бездомное животное, потратив всего несколько минут, могут легко проверить, не ищут ли его, получить актуальный список групп и сообщить о находке. В подобных ситуациях бот может внести существенный вклад в воссоединение потерявшихся питомцев с их владельцами.

### Технический обзор

Проект состоит из нескольких основных модулей:

- **Модули [первичного](https://github.com/rocinantt/sledoPET/tree/main/primary_parser) и [регулярного](https://github.com/rocinantt/sledoPET/tree/main/regular_parser) парсинга:**<br/>
  🕵️‍♂️🔍 Эти модули парсят посты из тематических групп VK. Они фильтруют посты, собирают информацию и с помощью модели, обученной на классификации пород собак, извлекают эмбеддинги из фотографий. Затем вся информация сохраняется в базу данных.

- **Модуль [Telegram-бота](https://github.com/rocinantt/sledoPET/tree/main/tg_bot):**<br/>
  🤖💬 Этот модуль взаимодействует с пользователем, принимая фотографию и параметры для фильтрации постов. Затем он отправляет данные в систему сравнения изображений и возвращает пользователю результаты. Также предоставляет доступ к актуальному списку региональных групп "потеряшек".
 
- **Модуль [сравнения фотографий](https://github.com/rocinantt/sledoPET/tree/main/photo_comparator):**<br/>
   🐾🐈🐕 Бот взаимодействует с пользователем, принимая фотографию и данные для поиска. Полученные данные отправляются в систему сравнения изображений, которая возвращает подходящие результаты.

- **Модули [логирования](https://github.com/rocinantt/sledoPET/tree/main/loki), [сбора](https://github.com/rocinantt/sledoPET/tree/main/promtail) и [мониторинга](https://github.com/rocinantt/sledoPET/tree/main/grafana):**<br/>
  📊📋 Для централизованного сбора и визуализации данных используется связка Promtail, Loki и Grafana. Эти инструменты обеспечивают удобный мониторинг и анализ работы всех компонентов проекта.

- **CV модель, [обученная](https://github.com/rocinantt/sledoPET/blob/main/vit-dog-breed.ipynb) и используемая в проекте для извлечения эмбеддингов из фотографий.**<br/>
  💻📈 Для этой цели была выбрана модель vit-large-patch32-384 от Google и дообучена на [Stanford Dogs Dataset](http://vision.stanford.edu/aditya86/ImageNetDogs/) с accuracy на валидации - 0.914.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Built With

* ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
* ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
* ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
* ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
* ![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)
* ![AIOHTTP](https://img.shields.io/badge/iohttp-%232C5bb4.svg?style=for-the-badge&logo=aiohttp&logoColor=white)
* ![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
* ![Grafana](https://img.shields.io/badge/grafana-%23F46800.svg?style=for-the-badge&logo=grafana&logoColor=white)
* ![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
* ![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage
<br />

<p align="center">
  <img src="https://github.com/rocinantt/DogFinderBot/blob/main/photo/tg1.jpg" alt="Screenshot 1" width="30%" style="margin-right: 20px;">
  <img src="https://github.com/rocinantt/DogFinderBot/blob/main/photo/tg2.jpg" alt="Screenshot 2" width="30%" style="margin-right: 20px;">
  <img src="https://github.com/rocinantt/DogFinderBot/blob/main/photo/tg3.jpg" alt="Screenshot 3" width="30%" style="margin-right: 20px;">
</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Further plans -->
## Further plans 

- [x] Определение локации по тексту
- [x] Расширенный выбор локаций для поиска
- [x] Добавление поиска котов
  - [x] Усовершенствование системы фильтрации для раздельного сохранения постов с собаками и с кошками.
  - [x] Добавить в бота возможность выбирать вид искомого животного.
- [ ] Заменить модель ансамблем
- [ ] Добавление Московской области
- [ ] Добавить парсинг из tg.

<!-- CONTACT -->
## Contact

<br/>

<div align="left">
  <a href="https://t.me/rocinantt">
    <img src="https://github.com/rocinantt/DogFinderBot/blob/main/photo/8726389_telegram_alt_icon.png" alt="Telegram" width="100" height="100">
  </a>
<br/>
<br/>
  <a href="https://github.com/rocinantt">
    <img src="https://github.com/rocinantt/DogFinderBot/blob/main/photo/8725822_github_icon.png" alt="GitHub" width="100" height="100">
  </a>
</div>

<p align="right">(<a href="#readme-top">back to top</a>)</p>
