# Тестовое задание

## UPD 14.12.22
Добавлена документация swagger с помощью drf_yasg

## Запуск проекта:
1. pip install -r requirements.txt
2. sudo docker run -d -p 6379:6379 redis
3. celery -A django_test_task worker -l info
4. python manage.py makemigrations
5. python manage.py migrate
6. python manage.py runserver 0.0.0.0:8000

# Примеры API:
## Title
Получить список всех Title: <br> **GET http://0.0.0.0:8000/api/v1/titles/?per_page=3** <br>
Ответ API:
```json
{
    "count": 53,
    "next": "http://0.0.0.0:8000/api/v1/titles/?page=2&per_page=3",
    "previous": null,
    "results": [
        {
            "id": 248,
            "ru_name": "Тайтл 1",
            "en_name": "Title 1",
            "alt_name": "title_1",
            "description": "Это 1ый тайтл",
            "tags": [
                {
                    "id": 87,
                    "tag_name": "Тег 1"
                },
                {
                    "id": 89,
                    "tag_name": "Тег 3"
                }
            ]
        },
        {
            "id": 249,
            "ru_name": "Тайтл 2",
            "en_name": "Title 2",
            "alt_name": "title_2",
            "description": "Это 2ый тайтл",
            "tags": [
                {
                    "id": 88,
                    "tag_name": "Тег 2"
                },
                {
                    "id": 89,
                    "tag_name": "Тег 3"
                }
            ]
        },
        {
            "id": 250,
            "ru_name": "Тайтл 3",
            "en_name": "Title 3",
            "alt_name": null,
            "description": "",
            "tags": []
        }
    ]
}
```

Получить список одного Title: <br> **GET http://0.0.0.0:8000/api/v1/titles/1/** <br>
Ответ API:
```json
{
    "id": 1,
    "ru_name": "Тайтл 1",
    "en_name": "Title 1",
    "alt_name": "title_1",
    "description": "Это 1ый тайтл",
    "tags": [
        {
            "id": 87,
            "tag_name": "Тег 1"
        },
        {
            "id": 89,
            "tag_name": "Тег 3"
        }
    ],
    "volume_titles": [
        {
            "id": 15,
            "volume_name": "4ий Вол тайтла 3",
            "volume_price": 10,
            "volume_number": 4,
            "volume_chapters": []
        },
        {
            "id": 14,
            "volume_name": "3ий Вол тайтла 3",
            "volume_price": 500,
            "volume_number": 3,
            "volume_chapters": [
                {
                    "id": 14,
                    "chapter_number": 3,
                    "chapter_content": "Чаптер 3",
                    "chapter_views_count": 0,
                    "chapter_likes_count": 0
                },
                {
                    "id": 13,
                    "chapter_number": 2,
                    "chapter_content": "Чаптер 2",
                    "chapter_views_count": 0,
                    "chapter_likes_count": 0
                },
                {
                    "id": 12,
                    "chapter_number": 1,
                    "chapter_content": "чаптер 1",
                    "chapter_views_count": 0,
                    "chapter_likes_count": 0
                }
            ]
        },
        {
            "id": 12,
            "volume_name": "2ой Вол тайтла 1",
            "volume_price": 20,
            "volume_number": 2,
            "volume_chapters": []
        },
        {
            "id": 11,
            "volume_name": "1ый Вол тайтла 1",
            "volume_price": 10,
            "volume_number": 1,
            "volume_chapters": [
                {
                    "id": 10,
                    "chapter_number": 2,
                    "chapter_content": "cont 2",
                    "chapter_views_count": 0,
                    "chapter_likes_count": 0
                },
                {
                    "id": 9,
                    "chapter_number": 1,
                    "chapter_content": "cont 1",
                    "chapter_views_count": 0,
                    "chapter_likes_count": 0
                }
            ]
        }
    ]
}
```

Ответ API при неверном primary key:
```json
{
    "detail": "Not found."
}
```

## Chapter

Получить список всех Chapter: <br> **GET http://0.0.0.0:8000/api/v1/chapters/?per_page=2** <br>
Ответ API:
```json
{
    "count": 6,
    "next": "http://0.0.0.0:8000/api/v1/chapters/?page=2&per_page=2",
    "previous": null,
    "results": [
        {
            "id": 14,
            "chapter_number": 3,
            "chapter_content": "Чаптер 3",
            "chapter_views_count": 0,
            "chapter_likes_count": 0
        },
        {
            "id": 13,
            "chapter_number": 2,
            "chapter_content": "Чаптер 2",
            "chapter_views_count": 0,
            "chapter_likes_count": 0
        }
    ]
}
```

Получить список одного Chapter: <br> **GET http://0.0.0.0:8000/api/v1/chapters/1/** <br>
Ответ API:
```json
{
    "message": "OK",
    "data": {
        "id": 1,
        "chapter_number": 1,
        "chapter_content": "Чаптер 1",
        "chapter_views_count": 3,
        "chapter_likes_count": 1
    }
}
```

Ответ API при неверном primary key:
```json
{
    "message": "Chapter not exists",
    "data": {}
}
```

Добавить лайк к Chapter: <br> **POST http://0.0.0.0:8000/api/v1/chapters/1/** <br>
Ответ API:
```json
{
    "message": "OK"
}
```
Ответ API при неверном primary key:
```json
{
    "message": "Chapter not exists"
}
```

# Пояснения к заданиям
 
## Модели

Все модели находятся в /api/models.py

## API

### Сделать API для получения списка всех книг (Title).
Должна поддерживаться пагинация (постраничная выдача результатов) - сделано с помощью **restframework.pagination**

### Сделать API для получения детальной информации о книге (Title)
Помимо атрибутов книги в ответе должны содержаться все привязанные к ней объекты - сделано с помощью **restframework.serializers**

### При обращении к API с деталями о главе (Chapter) счетчик просмотров увеличиваться на единицу.
1. Нагрузка на данное API предполагается существенная, поэтому желательно непосредственно изменение данных в БД реализовать в фоновой задаче. 
2. Важно обратить внимание, что увеличение счетчика должно происходить строго атомарно. То есть, если две задачи параллельно обновляют счетчик одного объекта, то на выходе всегда должно получаться ”+2”. 

~~Сделано с помощью redis + celery + transaction.atomic. Даже если поступит несколько тасков в 1 время, транзакция не даст зафиксировать результат, и один из тасков перезапустится, когда второй уже завершится. Таким образом проверялось на aiohttp с 1000+ запросами циклом - ни один запрос не потерялся, счетчик увеличивался ровно на число запросов.~~
Впоследствии узнал про метод update и F поля, которыми сделано сейчас

### Сделать отдельный эндпоинт для поставки лайка к главе (Chapter), счетчик лайков увеличивается на еденицу
1. Нагрузка на данное API предполагается существенная, поэтому желательно непосредственно изменение данных в БД реализовать в фоновой задаче. 
2. Важно обратить внимание, что увеличение счетчика должно происходить строго атомарно. То есть, если две задачи параллельно обновляют счетчик одного объекта, то на выходе всегда должно получаться “+2”. 

Сделано также, как предыдущий пункт

### Заведение книг и привязка к ним контента должна выполняться через админку. 
Должен поддерживаться поиск по названиям. - сделано, под поиском показывает поля, по котом идет поиск
Желательно для удобства реализовать привязку и управление контентом на странице в виде inline-блоков в разделе управления страницей (Title) в админке - Сделано

### Для каждой API должно быть минимум по одному положительному автотесту. 
Сделаны тесты: принадлежности к правильному View, отклику от сервера, правильности возвращаемых данных, работоспособности celery тасков. Все тесты хранятся в /api/tests/api_tests.py. Запуск тестов: <br> 
```shell 
python manage.py test --pattern=*_tests.py 
```

### Должны быть миграции для наполнения БД данными, необходимыми для демонстрации. 
Альтернатива: <br>
**GET http://0.0.0.0:8000/api/v1/test_items/** <br>
Полностью удаляет данные с бд и вставляет новые плейсхолдеры

### README.md в корне должен содержать примеры вызовов API. 
Вы его сейчас и читаете :)

### Сервер после запуска должен отвечать по адресу http://0.0.0.0:8000 

Прочитайте блок "Запуск проекта"

### Ожидаемое время выполнения задания в полном объеме 8 часов. 
С учетом перерыва на завтрак - около 4 часов

### Допускается отказ от выполнения некоторых обязательных пунктов требований с подробным обоснованием. 
Выполнены все пункты
