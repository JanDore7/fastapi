# FASTAPI

## *<u>Зависимости:</u>*  
- ### fastapi
1. ***pip install fastapi***   
Устанавливает только базовый пакет FastAPI, необходимый 
для минимального функционирования фреймворка.
Это включает ядро **FastAPI**, но не включает дополнительные зависимости, 
такие как инструменты для удобного использования, 
валидации или совместимости с другими библиотеками.  
Подходит для случаев, когда у тебя уже есть все необходимые зависимости или ты сам управляешь установкой.



2. ***pip install 'fastapi[standard]'***  
Устанавливает FastAPI с дополнительными зависимостями, которые обычно нужны 
для продвинутого использования.  
Включает пакеты для:  
**Pydantic** — для валидации данных и типов (это и так входит в базовую установку).  
**ujson** — для более быстрого парсинга JSON (ускоряет работу с JSON).  
**email-validator** — для проверки email адресов.  
**python-multipart** — для работы с загрузкой файлов.  
**itsdangerous** — для безопасной работы с временными токенами.  
**jinja2** — для работы с шаблонами (если используешь рендеринг HTML).    

Этот вариант установки рекомендуется для более полного функционала и упрощает настройку проекта.

- ### Сервер с ASGI  
>[^1] ASGI (Asynchronous Server Gateway Interface) — 
это стандарт интерфейса между веб-серверами и 
веб-приложениями на Python, который поддерживает 
асинхронные операции. Он был разработан как более 
современная альтернатива WSGI 
(Web Server Gateway Interface), 
чтобы лучше соответствовать требованиям 
асинхронных приложений.

Для разработки чаще всего используется **uvicorn** :
1. ***pip install uvicorn***  
Эта команда устанавливает только основной пакет 
uvicorn без дополнительных зависимостей. 
Это достаточно для базового использования Uvicorn как ASGI-сервера.


2. ***pip install 'uvicorn[standard]'***  
Эта команда устанавливает uvicorn вместе с набором 
дополнительных зависимостей, которые обеспечивают 
более широкий функционал. В частности, в стандартную установку могут входить:  
**httptools:** для разбора HTTP-запросов.  
**uvloop:** для улучшения производительности за счет использования асинхронного цикла событий, основанного на libuv.  
**websockets:** для поддержки WebSocket-протокола.  

Для продакшена рекомендуется использовать **Hypercorn** :

1. ***pip install hypercorn***

[Несколько слов о работе с серверами ASGI](ASGI_servers.md)  

---

## *<u>Начало работы</u>*

Импортируем необходимые библиотеки

import uvicorn
from fastapi import FastAPI

Создаем экземпляр класса 

app = FastAPI()

**Список аргументов которые может принимать класс:**  
    **title**: Название вашего приложения (строка).  
    **description**: Описание вашего приложения (строка).  
    **version**: Версия вашего приложения (строка).  
    **terms_of_service**: URL с условиями использования (строка).  
    **contact**: Информация о контактах (словарь с ключами name, url, email).  
    **license_info**: Информация о лицензии (словарь с ключами name и url).  
    **openapi_tags**: Список тегов для структурирования документации (список словарей).  
    **docs_url**: URL для Swagger UI (строка).  
    **redoc_url**: URL для ReDoc (строка).  
    **openapi_url**: URL для OpenAPI схемы (строка).  
    **middleware**: Список промежуточного ПО (middleware) (список).  
    **dependencies**: Глобальные зависимости (список).  
    **exception_handlers**: Глобальные обработчики исключений (словарь).  
    **default_response_class**: Класс ответа по умолчанию (например, JSONResponse).  
    **default_status_code**: Код состояния по умолчанию для ответов.  
    **default_headers**: Заголовки по умолчанию для всех ответов (словарь).  
    **debug**: Включить или отключить режим отладки (логическое значение).  
    **root_path**: Корневой путь для приложения (строка).  
    **on_startup**: Список функций, которые будут выполнены при запуске приложения.  
    **on_shutdown**: Список функций, которые будут выполнены при завершении работы приложения.
    **dependencies**: Глобальные зависимости (список).
    **exception_handlers**: Глобальные обработчики исключений (словарь).
    **include_in_schema**: Указывает, включать ли в схему OpenAPI (логическое значение).  


**Запуск FastAPI**  


1. Самый простой способ запустить FastAPI — написать в терминале команду 
>fastapi dev main.py
> 

2. Для запуска uvicorn достаточно установить библиотеку в виртуальное окружение, перейти в директорию с проектом и запустить веб-сервер в терминале через команду 
>uvicorn main:app --reload

которая запустит наше FastAPI приложение на порту 8000 по адресу 
http://localhost:8000/. Перейдя по этой ссылке в браузере, 
вы должны увидеть сообщение   
**{"detail": "Not found"}**.  
Для перехода к документации API необходимо зайти по адресу http://localhost:8000/docs или http://localhost:8000/redoc.



3. Этот способ используют в production коде. 
Для запуска приложения необходимо прописать в файле main.py следующий код:
```
if name == "main":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
```
В таком случае приложение запускают через привычный вам
python main.py
В таком случае команда максимально лаконична, а все параметры запуска (а их может быть более 10 штук), 
конфигурируются внутри файла main.py

<u>Параметры конфигурации:</u>  


**app**: Объект приложения (например, app, если это ваше FastAPI приложение).  
**host**: Адрес, на котором будет запущен сервер (например, "127.0.0.1").  
**port**: Порт, на котором будет запущен сервер (например, 8000).  
**reload**: Включить перезагрузку сервера при изменении кода (логическое значение, по умолчанию False).  
**reload_dirs**: Список директорий для отслеживания при перезагрузке (по умолчанию - текущая директория).  
**workers**: Количество рабочих процессов (по умолчанию 1).  
**log_level**: Уровень логирования (например, 'info', 'debug', 'warning').  
**access_log**: Включить или отключить логирование запросов (логическое значение, по умолчанию True).  
**use_colors**: Включить или отключить цветное логирование (логическое значение, по умолчанию True).  
**timeout_keep_alive**: Время в секундах для поддержания соединения (по умолчанию 5).  
**ssl**: Настройки SSL для запуска сервера с HTTPS (словарь с параметрами keyfile и certfile).  
**interface**: Используемый интерфейс (например, 'asgi', 'http').  
**lifespan**: Указание на функцию жизненного цикла (по умолчанию None).  
**limit_concurrency**: Ограничение на количество одновременных запросов (по умолчанию None).  
**limit_max_requests**: Максимальное количество запросов, после которого рабочий процесс будет перезапущен 
add(по умолчанию None).  
**proxy_headers**: Указывать, нужно ли использовать заголовки прокси (логическое значение, по умолчанию False).  
**headers**: Заголовки, которые будут добавлены ко всем ответам (словарь).   


**Эндпоинты**

В FastAPI эндпоинты (или "ручки") представляют собой URL-пути, к которым клиент (например, браузер или инструмент вроде curl) может делать запросы. 
Эти эндпоинты обрабатывают запросы и возвращают ответы с данными. 
Каждая ручка в FastAPI связывается с конкретным HTTP-методом, 
таким как **GET, POST, PUT, DELETE** и т.д.
Основные HTTP-методы и их использование в FastAPI:

**GET**: Используется для получения данных с сервера. Например, если вы хотите запросить список объектов (например, товаров, пользователей), то вы используете GET.
*Пример:*
```
    @app.get("/items/{item_id}")
    async def read_item(item_id: int):
        return {"item_id": item_id}
```
В этом примере по пути **/items/{item_id}** можно сделать запрос для получения элемента по его id.
Пример запроса:  
**GET /items/42.**

**POST**: Используется для создания нового ресурса. Когда вы хотите отправить данные на сервер, чтобы создать новый объект (например, создать пользователя или товар), используйте POST.
*Пример:*
```
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.post("/items/")
async def create_item(item: Item):
    return item
```
В этом примере можно отправить данные для создания нового элемента через POST /items/.
Пример запроса:   
**POST /items/** с JSON-данными тела запроса:
```
    json

        {
          "name": "Item Name",
          "price": 100.5
        }
```

**PUT**: Используется для обновления существующего ресурса. Полная замена данных объекта.
*Пример:*
```
    @app.put("/items/{item_id}")
    async def update_item(item_id: int, item: Item):
        return {"item_id": item_id, **item.dict()}
```
В этом примере вы можете обновить существующий элемент с указанным item_id через PUT /items/{item_id}.
Пример запроса:  
**PUT /items/42** с JSON-данными для обновления.

**PATCH**: Используется для частичного обновления ресурса. В отличие от PUT, он не заменяет весь объект, а только обновляет переданные поля.
*Пример:*
```
    @app.patch("/items/{item_id}")
    async def update_partial_item(item_id: int, item: Item):
        return {"item_id": item_id, **item.dict()}
```
Пример запроса:  
**PATCH /items/42** с изменёнными полями в JSON (например, только цена).

**DELETE**: Используется для удаления ресурса с сервера.
*Пример:*
```
    @app.delete("/items/{item_id}")
    async def delete_item(item_id: int):
        return {"msg": f"Item {item_id} deleted"}
```
В этом примере элемент с указанным item_id удаляется через DELETE /items/{item_id}.
Пример запроса:   
**DELETE /items/42.**

**OPTIONS**: Используется для получения информации о параметрах взаимодействия с ресурсом (например, какие методы поддерживаются).
*Пример:*
```
    @app.options("/items/")
    async def options_item():
        return {"methods": ["GET", "POST", "OPTIONS"]}
```

**HEAD**: Похож на **GET**, но возвращает только заголовки, 
без тела ответа.  
*Пример:*
```
        @app.head("/items/")
        async def head_items():
            return
```

Параметры для настройки эндпоинтов.  
Каждый метод-декоратор (@app.get, @app.post и т.д.) поддерживает несколько полезных параметров:

**path**: Путь URL, по которому будет доступен эндпоинт.
Например, @app.get("/items/{item_id}").  
**tags**: Список строк для группировки эндпоинтов в документации.  
*Пример:*
```
    @app.get("/items/", tags=["items"])
    async def get_items():
        return [{"item_id": "foo"}]
```
**summary**: Краткое описание эндпоинта, отображаемое в документации.  
*Пример:*
```
    @app.get("/items/", summary="Get all items")
    async def get_items():
        return [{"item_id": "foo"}]
```
*description*: Полное описание эндпоинта (отображается в Swagger UI).
*Пример:*
```
    @app.get("/items/", description="Retrieve a list of all items")
    async def get_items():
        return [{"item_id": "foo"}]
```
*response_model*: Модель ответа, которая указывает на структуру возвращаемых данных.
*Пример:*
```
    from pydantic import BaseModel

    class Item(BaseModel):
        name: str
        price: float

    @app.get("/items/", response_model=Item)
    async def get_items():
        return {"name": "foo", "price": 42.0}
```
*status_code*: Код состояния HTTP, который будет возвращен по умолчанию (например, 200 или 201).
*Пример:*
```
    @app.post("/items/", status_code=201)
    async def create_item(item: Item):
        return item
```
*deprecated*: Помечает эндпоинт как устаревший. В документации это будет отмечено специальным значком.
*Пример:*
```
        @app.get("/old-items/", deprecated=True)
        async def get_old_items():
            return [{"item_id": "foo"}]
```
*Пример полного кода:*

```
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    description: str = None

@app.get("/items/{item_id}", tags=["items"], summary="Get an item by ID", response_model=Item)
async def read_item(item_id: int):
    return {"name": "Sample Item", "price": 10.0, "description": "A sample item"}

@app.post("/items/", tags=["items"], summary="Create a new item", status_code=201)
async def create_item(item: Item):
    return item

@app.put("/items/{item_id}", tags=["items"], summary="Update an existing item", response_model=Item)
async def update_item(item_id: int, item: Item):
    return {"name": item.name, "price": item.price, "description": item.description}

@app.delete("/items/{item_id}", tags=["items"], summary="Delete an item", status_code=204)
async def delete_item(item_id: int):
    return
```
Как делать запросы:

    GET: Получение элемента по ID — GET /items/42.
    POST: Создание нового элемента — POST /items/ с JSON-данными.
    PUT: Полное обновление элемента — PUT /items/42.
    DELETE: Удаление элемента — DELETE /items/42.

Документацию можно увидеть, запустив FastAPI и перейдя по адресу http://127.0.0.1:8000/docs.


***Параметры декораторов (@app.get, @app.post, @app.put, и т.д.):***

**path**:  
        Тип: str  
        Описание: Путь URL, по которому будет доступен эндпоинт.  
        Пример: @app.get("/items/{item_id}")    
**tags**:  
        Тип: List[str]  
        Описание: Список строк для группировки эндпоинтов в документации. Эти теги помогают структурировать вашу документацию, разделяя эндпоинты по категориям.  
        Пример: @app.get("/items/", tags=["items"])  
**summary**:  
        Тип: str  
        Описание: Краткое описание эндпоинта, отображаемое в документации.
        Пример: @app.get("/items/", summary="Retrieve a list of items")    
**description**:    
        Тип: str  
        Описание: Полное описание эндпоинта, отображаемое в Swagger UI и ReDoc. Это поле может быть длинным и описывать цель и поведение эндпоинта.  
        Пример: @app.get("/items/", description="Retrieve a list of all items from the database.")    
**response_model**:    
        Тип: Pydantic-модель  
        Описание: Модель данных, описывающая структуру ответа. FastAPI автоматически конвертирует и валидирует данные перед отправкой клиенту, исходя из этой модели.  
        Пример:  
```
    class Item(BaseModel):
        name: str
        price: float

    @app.get("/items/", response_model=Item)
    async def get_items():
        return {"name": "Sample Item", "price": 10.0}
```

**response_model_exclude_unset**:  
Тип: bool   
    Описание: Исключает поля, которые не были установлены явно (если используется Pydantic-модель для ответа). Это может быть полезно, если вы не хотите отправлять значения по умолчанию.  
    Пример: @app.get("/items/", response_model_exclude_unset=True)  

**status_code**:  
Тип: int  
    Описание: HTTP-код состояния по умолчанию, возвращаемый эндпоинтом. Например, для успешных POST-запросов часто используется код 201 Created.  
    Пример: @app.post("/items/", status_code=201)  

**response_class**:  
Тип: Класс ответа  
    Описание: Указывает класс, используемый для отправки ответа (например, JSONResponse, HTMLResponse, PlainTextResponse). По умолчанию FastAPI использует JSONResponse.  
    Пример:  
```
    from fastapi.responses import HTMLResponse

    @app.get("/items/", response_class=HTMLResponse)
    async def get_items():
        return "<h1>Item List</h1>"
```

**response_description**:  
Тип: str  
    Описание: Описание тела ответа для документации OpenAPI. Обычно используется, чтобы описать, что означает успешный ответ.  
    Пример: @app.get("/items/", response_description="List of items successfully retrieved")  

**responses**:  
Тип: Dict[int, Dict[str, Any]]  
    Описание: Словарь, описывающий возможные HTTP-ответы для эндпоинта. Ключи — это коды состояния HTTP, а значения — это дополнительные описания или примеры.  
    Пример:  
```
    @app.get("/items/", responses={404: {"description": "Item not found"}})
    async def get_items(item_id: int):
        return {"item_id": item_id}
```
**deprecated**:  
Тип: bool  
    Описание: Помечает эндпоинт как устаревший. В Swagger UI и ReDoc это будет отмечено специальным значком.  
    Пример: @app.get("/old-items/", deprecated=True)  

**include_in_schema**:  
Тип: bool  
    Описание: Определяет, включать ли эндпоинт в документацию (Swagger UI, ReDoc и схему OpenAPI). Если установлено в False, эндпоинт будет доступен для запросов, но не будет отображаться в документации.  
    Пример:  
```
        @app.get("/internal-items/", include_in_schema=False)
        async def get_internal_items():
            return {"item_id": "internal"}
```

**name**:  
        Тип: str  
        Описание: Человеко-читаемое имя для эндпоинта, которое можно использовать для внутренних целей (например, для ссылок в коде).  
        Пример: @app.get("/items/", name="get_items_endpoint")  

Пример использования всех параметров:  
```
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.get("/items/{item_id}", 
         tags=["items"], 
         summary="Get an item by ID", 
         description="Retrieve a specific item by its unique ID from the database.", 
         response_model=Item, 
         status_code=200, 
         response_description="Item successfully retrieved",
         response_class=JSONResponse, 
         responses={404: {"description": "Item not found"}},
         deprecated=False,
         include_in_schema=True,
         name="get_item_by_id")
async def get_item(item_id: int):
    return {"name": "Sample Item", "price": 20.0}
```
Что происходит в этом примере:
Эндпоинт доступен по пути /items/{item_id}.  
У него есть теги для группировки ("items").  
Он возвращает JSON-ответ с моделью Item.  
У него есть краткое описание (summary) и полное описание (description).  
Он возвращает HTTP-код 200 при успехе и код 404, если элемент не найден.  
Этот эндпоинт включен в документацию (include_in_schema=True).  
Имя эндпоинта внутри кода будет get_item_by_id.  

Все эти параметры позволяют детально настраивать как само поведение эндпоинтов, так и их представление в документации.