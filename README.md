<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/rocinantt/DogFinderBot">
    <img src="https://github.com/rocinantt/DogFinderBot/blob/main/photo/dog2.jpg" alt="Logo" width="770" height="435">
  </a>

  <h3 align="center">Dog Finder Bot</h3>

  <p align="center">
    Бот, который помогает потерявшимся собакам вернуться домой.
    <br />
    <br />
    <a href="https://web.telegram.org/a/#7411138567">Использовать бота</a>
    ·
    <a href="https://github.com/rocinantt/DogFinderBot/issues/new?labels=bug&template=bug-report---.md">Сообщить о багах</a>
    ·
    <a href="https://github.com/rocinantt/DogFinderBot/issues/new?labels=enhancement&template=feature-request---.md">Предложить улучшение</a>
  </p>
</div>



<!-- ABOUT THE PROJECT -->
## About The Project



<img align="right" width="385" height="605" src="https://github.com/rocinantt/DogFinderBot/blob/main/photo/5.jpg">
Dog Finder Bot — это Telegram-бот, разработанный для оперативного соединения владельцев потерявшихся собак и тех, кто их нашел. Бот автоматически сопоставляет фотографии найденных животных с объявлениями о пропаже, увеличивая шансы на успешное возвращение питомцев домой.

### Как помогает бот:

  Когда собака теряется, её хозяевам приходится сталкиваться с множеством сложностей. Они вынуждены искать пропавшего питомца, распространять объявления о пропаже, постоянно проверять информацию в группах и чатах, посвящённых потерянным животным. Однако даже активные поиски не всегда гарантируют успех. Люди, которые встречают бездомную собаку, могут не быть участниками таких сообществ, бояться задерживать животное или просто не иметь времени на просмотр множества постов, не будучи уверенными, что кто-то действительно разыскивает эту собаку. В это время каждая минута имеет значение, так как увлеченная, или, наоборот, испуганная и дезориентированная собака рискует попасть под машину, столкнуться с агрессией других животных или удалиться слишком далеко от зоны поиска.

  Dog Finder Bot не является универсальным решением всех этих проблем, но он может стать важным дополнительным инструментом. Хозяева могут использовать его для мониторинга социальных сетей, а прохожие, заметившие бездомную собаку, потратив всего несколько минут, могут легко проверить, не ищут ли её, получить актуальный список групп и сообщить о находке. В подобных ситуациях бот может внести существенный вклад в воссоединение потерявшихся собак с их владельцами.

### Технический обзор

Проект состоит из нескольких основных модулей:

- **Модули [первичного](https://github.com/rocinantt/DogFinderBot/tree/main/primary_parser) и [регулярного](https://github.com/rocinantt/DogFinderBot/tree/main/regular_parser) парсинга:**<br/>
  🕵️‍♂️🔍 Эти модули парсят посты из тематических групп VK. Они фильтруют посты, собирают информацию и с помощью модели обученной на классификации пород собак извлекают эмбеддинги из фотографий. Затем вся информация сохраняется в базу данных.

- **Модуль [Telegram-бота](https://github.com/rocinantt/DogFinderBot/tree/main/tg_bot):**<br/>
  🤖💬 Этот модуль отвечает за взаимодействие с пользователем, принимая фотографию и данные для фильтрации постов. Он отправляет все это в модуль сравнения фотографий и возвращает пользователю полученные посты. Также предоставляет доступ к актуальному списку региональных групп "потеряшек".
 
- **Модуль [сравнения фотографий](https://github.com/rocinantt/DogFinderBot/tree/main/photo_comparator):**<br/>
   🐩🐕 Этот модуль принимает запрос от бота, извлекает срез данных по региону, населённому пункту и временному периоду. Используя косинусное сходство эмбеддингов, он отбирает 5 наиболее похожих постов и отправляет их боту.

- **Модули [логирования](https://github.com/rocinantt/DogFinderBot/tree/main/loki), [сбора](https://github.com/rocinantt/DogFinderBot/tree/main/promtail) и [мониторинга](https://github.com/rocinantt/DogFinderBot/tree/main/grafana):**<br/>
  📊📋  Для обеспечения централизованного сбора логов и их визуализации используется связка Promtail, Loki и Grafana, предоставляющая удобные средства для мониторинга и анализа работы всех модулей проекта.

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


<!-- Further plans  -->
## Further plans 

- [ ] Расширение списка групп региона
- [ ] Переезд на более мощный сервер
- [ ] Расширение списка регионов
- [ ] Усовершенствование системы фильтрации постов
- [ ] Добавление возможности отправки информации о найденном животном в группы через бота



!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact


<br/>

<div align="left">
  <a href="https://t.me/rocinantt">
    <img src="https://github.com/rocinantt/DogFinderBot/blob/main/photo/8726389_telegram_alt_icon.png" alt="Telegram" width="100" height="100">
    
  </a>
<br/>
<br/>

<div align="left">
  <a href="https://github.com/rocinantt">
    <img src="https://github.com/rocinantt/DogFinderBot/blob/main/photo/8725822_github_icon.png" alt="Telegram" width="100" height="100">
  </a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>
