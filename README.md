# api_yamdb
# API YaMDb
![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/-Django-092E20?style=flat&logo=django&logoColor=white)
![Django REST framework](https://img.shields.io/badge/-Django%20REST%20framework-ff9900?style=flat&logo=django&logoColor=white)
![Postman](https://img.shields.io/badge/-Postman-FF6C37?style=flat&logo=postman&logoColor=white)
## Описание проекта
YaMDb - это проект, на котором люди могут оставлять отзывы о книгах, фильмах, музыке и других произведениях.  Произведения разделены на категории и им можно присвоить жанр. Администраторы могут добавлять новые произведения, категории и жанры. Пользователи могут оставлять свои отзывы и ставить оценки произведениям и комментировать отзывы других пользователей.
## Запуск проекта
- Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/Milkyaway13/api_yamdb
```
```
cd api_yamdb
```
- Cоздать и активировать виртуальное окружение
```
python -m venv venv # Для Windows
python3 -m venv venv # Для Linux и macOS
```
```
source venv/Scripts/activate # Для Windows
source venv/bin/activate # Для Linux и macOS
```
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
- Перейти в папку со скриптом управления и выполнить миграции
```
cd yatube_api
```
```
python manage.py migrate
```

- Запустить проект
```
python manage.py runserver
```
## Регистрация нового пользователя
- Передать на эндпоинт 127.0.0.1:8000/api/v1/auth/signup/ **username** и **email**
- Получить код подтверждения на переданный **email**. Использовать имя 'me' в качестве **username** запрещено. Поля **email** и **username** должны быть уникальными. 

## Получение JWT-токена
- Передать на эндпоинт 127.0.0.1:8000/api/v1/auth/token/ **username** и **confirmation** code из письма.

## Примеры запросов
- Отправить POST-запрос на адрес http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/ и передать поле text и поле score <br>
Пример запроса на создание отзыва: 
```
{
"text": "Отзыв на произведение",
"score": 5
}
```
Пример ответа: 
```
{
"id": 0,
"text": "Отзыв на произведение",
"author": "voronovsv",
"score": 5,
"pub_date": "2019-08-24T14:15:22Z"
}
```
- Отправить POST-запрос на адрес http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/ и передать поле text <br>
Пример запроса на создание комментария к отзыву:
```
{
"text": "Классный отзыв!"
}
```
Пример ответа:
```
{
"id": 0,
"text": "Классный отзыв!",
"author": "string",
"pub_date": "2019-08-24T14:15:22Z"
}
```
## Полная документация к API проекта:

Перечень запросов к ресурсу можно посмотреть в описании API

```
http://127.0.0.1:8000/redoc/
```
## Над проектом работали
<br>[Боярчук Василий](https://github.com/Milkyaway13)</br>
<br>[Бурсянина София](https://github.com/sofiya05)</br>
<br>[Павлов Никита](https://github.com/jojo3228)</br>