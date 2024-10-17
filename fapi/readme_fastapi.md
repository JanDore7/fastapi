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


Неотъемлемой частью работы с эндпоинтами являются данные передаваемые в запросе.

***Quryset*** - (иногда его называют QuerySet) — это специальный класс, 
предоставляемый FastAPI для работы с параметрами запроса (
query parameters) в ваших маршрутах. 
Query parameters используются для передачи данных через URL. 
В FastAPI они удобны для работы с опциональными и обязательными 
значениями, с типами по умолчанию и валидацией.

***Аргументы Query***

**default**: Значение по умолчанию.  
q: str = Query("default_value")  
Если параметр не передан, будет использоваться значение "default_value".  

**min_length и max_length**: Ограничения на минимальную и максимальную длину строки.  
q: str = Query(None, min_length=3, max_length=50)  
Значение параметра должно быть строкой длиной от 3 до 50 символов.  

**regex**: Регулярное выражение для валидации.  
q: str = Query(None, regex="^fixedpattern$")  
Этот параметр должен соответствовать регулярному выражению ^fixedpattern$.  

**alias**: Альтернативное имя для параметра.  
q: str = Query(None, alias="item-query")  
В запросе параметр должен называться item-query: /items/?item-query=some-query  

**description**: Описание параметра, полезно для генерации документации.  
q: str = Query(None, description="Это параметр запроса для поиска")  
Описание появится в Swagger UI.  

**deprecated**: Пометка параметра как устаревшего.  
q: str = Query(None, deprecated=True)  
Swagger UI покажет, что этот параметр устарел, но его можно продолжать использовать.  


**example**: Пример значения, полезно для документации.  
q: str = Query(None, example="example value")  
ример отображается в пользовательском интерфейсе документации и помогает 
пользователям API понять, какой формат данных ожидается.  


***Использования типов данных***  

FastAPI позволяет работать с различными типами данных для параметров запроса. Рассмотрим использование разных типов, 
включая возможность комбинирования 
типов с помощью оператора объединения |.

```aiignore
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/search/")
async def search_items(data: str | int = Query(...)):
    return {"data": data}

```

**Обязательные параметры**

В этом примере параметр data может быть либо строкой, либо целым числом. FastAPI автоматически выполняет проверку 
типа и преобразование, если это возможно. Параметр является обязательным.

Запросы могут выглядеть так:
>/search/?data=123   # data будет целым числом 123
> 
>/search/?data=text  # data будет строкой "text"

**Опциональные параметры**

Параметры запроса могут быть опциональными (то есть не обязательными). Чтобы сделать параметр опциональным, вы можете 
установить его значение по умолчанию в None:  
```aiignore
@app.get("/optional/")
async def read_optional_items(data: str | None = Query(None)):
    return {"data": data}

```
Этот маршрут будет корректен как при передаче параметра, так и без него:  

>/optional/?data=some-data  # data будет "some-data"
> 
> /optional/                 # data будет None


**Множественные значения**

Вы можете использовать параметры запроса для передачи 
множественных значений с помощью списков. Например:

```aiignore
@app.get("/items/")
async def read_items(q: list[str] = Query([])):
    return {"q": q}
```
Этот запрос:
>/items/?q=item1&q=item2

вернет:

```aiignore
{
    "q": ["item1", "item2"]
}

```

***Body:***

В FastAPI Body — это специальный класс, который используется для извлечения данных из тела HTTP-запроса (body). Он обычно применяется для передачи данных в формате JSON (или других поддерживаемых форматах) в методах POST, PUT, PATCH и других запросах, 
где тело запроса содержит данные.

Зачем используется Body?

Когда клиент отправляет данные на сервер (например, при создании или обновлении ресурса), эти данные обычно передаются в теле запроса. В FastAPI класс Body помогает вам извлекать и обрабатывать эти данные с возможностью их валидации и настройки.

**Основное использование**

Body часто используется с объектами Pydantic для автоматической валидации данных. 
Рассмотрим базовый пример:  

```aiignore
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    return item

```
В этом примере:  

Мы определяем модель Item с помощью Pydantic, которая описывает структуру данных, ожидаемых в теле запроса.
Маршрут /items/ принимает тело запроса в формате JSON, а FastAPI автоматически выполняет валидацию данных.

***Аргументы Body***

**1. default**: Значение по умолчанию  
```aiignore
from fastapi import FastAPI, Body

app = FastAPI()

@app.post("/items/")
async def create_item(data: dict = Body({"default_key": "default_value"})):
    return data
```
Если тело запроса не передано, значение будет по умолчанию:
```aiignore
{
    "default_key": "default_value"
}

```

**embed**: Вложенность тела запроса  

Когда embed=True, вы можете обернуть тело запроса в дополнительный уровень вложенности, что может быть полезно 
для совместимости с некоторыми клиентами API.
```aiignore
@app.post("/items/")
async def create_item(item: dict = Body(..., embed=True)):
    return item

```
Запрос должен выглядеть так:  

```aiignore
{
  "item": {
    "name": "Sample",
    "price": 10.5
  }
}
```
В отличие от обычного случая, когда тело запроса напрямую передаётся как JSON-объект, здесь оно обёрнуто в ключ "item".  

**description**: Описание параметра
description полезен для генерации документации. Он позволяет добавить подробное описание того, что это 
за данные и для чего они нужны.
```aiignore
@app.post("/items/")
async def create_item(item: dict = Body(..., description="JSON данные о товаре")):
    return item

```
В Swagger UI это описание появится в секции параметров запроса и укажет пользователю, для чего предназначено тело запроса.

**example**: Пример значения  
Как и для параметров запроса, example помогает указать пример данных, который будет отображаться в документации.

```aiignore
@app.post("/items/")
async def create_item(
    item: dict = Body(
        ...,
        examples={
            "example1": {
                "summary": "Простой пример",
                "description": "Пример для простого товара",
                "value": {"name": "Item 1", "price": 20.0}
            },
            "example2": {
                "summary": "Другой пример",
                "description": "Пример для другого товара",
                "value": {"name": "Item 2", "price": 30.0, "tax": 5.0}
            }
        }
    )
):
    return item

```
В документации будут отображены оба примера, и пользователь сможет выбрать подходящий вариант для тестирования API.  

Пример с несколькими параметрами Body
```aiignore
from fastapi import FastAPI, Query, Body

app = FastAPI()

@app.post("/items/")
async def create_item(
    q: str = Query(None, description="Поисковый параметр"),
    item: dict = Body(..., example={"name": "Sample", "price": 10.5})
):
    return {"q": q, "item": item}

```

Здесь:  


q — это необязательный параметр запроса, который можно передать через URL.
    
item — это данные в теле запроса, которые передаются в формате JSON.


--- 
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

## Роутеры

В FastAPI роутеры — это удобный способ организации и управления маршрутизацией в вашем приложении. Они позволяют разбивать ваше приложение на модули, что делает код более структурированным и легко поддерживаемым.
Основные параметры роутеров

Роутер: Основная сущность, которая обрабатывает маршруты.

Создаётся с помощью **APIRouter()**.

Может принимать несколько параметров:  
            **prefix**: строка, добавляемая перед каждым маршрутом, определённым в роутере.  
            **tags**: список строк, который помогает группировать маршруты в документации Swagger UI.  
            **dependencies**: зависимости, которые должны быть выполнены для всех маршрутов этого роутера.  
            **responses**: глобальные ответы для всех маршрутов в роутере.  

**  Пример использования роутера**  
```aiignore
from fastapi import FastAPI, APIRouter

app = FastAPI()
router = APIRouter()

@router.get("/items/{item_id}", tags=["items"])
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

@router.post("/items/", tags=["items"])
async def create_item(item: dict):
    return {"item": item}

# Подключаем роутер к приложению
app.include_router(router, prefix="/api/v1")

```

Как это работает:  

Создание роутера:  
        Сначала создаётся экземпляр APIRouter.  

Определение маршрутов:  
        Далее, с помощью декораторов (например, @router.get, @router.post и т.д.) добавляются маршруты. В этом примере определены маршруты для получения и создания элементов.

Подключение роутера к приложению:  
        Метод **include_router()** используется для подключения роутера к приложению. Параметр prefix указывает, что все маршруты из роутера будут доступны по пути /api/v1.

Использование зависимостей  

Вы также можете использовать зависимости в роутерах. 
Это позволяет переиспользовать общий код, например,
для авторизации или валидации.  
```aiignore
from fastapi import Depends

async def verify_token(token: str):
    # Проверка токена
    return token

@router.get("/secure-items/", dependencies=[Depends(verify_token)], tags=["secure"])
async def secure_items():
    return {"message": "This is a secure route."}

```

## Схемы данных
В FastAPI схемы данных обычно создаются с помощью библиотеки Pydantic, которая предоставляет мощный способ валидации данных и сериализации. Схемы данных позволяют описывать структуру данных, которые ваше приложение будет принимать и возвращать.

Вот основные моменты, связанные с созданием схем данных в FastAPI:
1. Создание схемы данных  
2. 

Схемы создаются как классы, унаследованные от BaseModel из Pydantic. Каждый атрибут класса будет представлять поле схемы.
```aiignore
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_active: bool = True  # По умолчанию будет True

```
2. Аргументы и типы данных

С помощью Pydantic вы можете использовать различные типы данных, такие как:

**str**: строка  
**int**: целое число  
**float**: число с плавающей запятой  
**bool**: логическое значение  
**List**: список значений  
**Dict**: словарь значений  
**Optional**: для полей, которые могут отсутствовать (или быть None)  
 вы можете использовать конструкцию | None вместо Optional для указания того, что поле может быть None. 
Это стало возможным благодаря улучшениям в аннотациях типов, и использование | делает код более читаемым.

Вот как это выглядит в контексте модели Pydantic:  
Пример с использованием | None  
```
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str
    description: str | None = Field(default=None, description="The description of the item")
    price: float
```

**Использование Field**

Field позволяет добавлять дополнительные параметры и метаданные для полей в вашей модели. Он используется для задания различных атрибутов полей, таких как описание, значения по умолчанию, ограничения и т. д.
Пример использования  
```aiignore
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., title="Item Name", description="The name of the item")
    price: float = Field(..., gt=0, description="The price of the item, must be greater than 0")
    is_active: bool = Field(True, description="Is the item active")

```
Основные параметры Field
**default**  : Значение по умолчанию для поля. Если значение не указано, поле будет обязательным (используя ...).  
**title**  : Заголовок поля, который может быть использован для генерации документации.  
**description**  : Описание поля, также полезно для документации.  
**gt, lt, ge, le**  : Ограничения для числовых полей (больше, меньше и т.д.).  
**max_length**  : Максимальная длина для строковых полей.  
**min_length**  : Минимальная длина для строковых полей.  
**regex**  : Регулярное выражение для проверки формата строки.  
**example**: Указывает пример значения для документации.

## [База данных ...](database.md)

## О Annotated и Depends
**комментарии к коду **
```aiignore
from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(None, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, lt=30)]


PaginationDep = Annotated[PaginationParams, Depends()]


@router.get("")
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    if pagination.page and pagination.per_page:
        return hotels_[pagination.per_page * (pagination.page-1):][:pagination.per_page]
    return hotels_
```
**Annotated**
позволяет добавлять метаданные к типам данных.
Это полезно для валидации данных, а также для того,
чтобы дать дополнительные подсказки FastAPI при создании API-документации.

*Пример*  
```aiignore
page: Annotated[int | None, Query(None, ge=1)]

```
Первый аргумент в **Annotated** — это тип данных.   
В данном случае это **int | None**, что значит: либо это целое число, либо **None**.    
Второй аргумент — это объект **Query**, который добавляет условия для запроса.   
Например, **Query(None, ge=1)** означает, что значение по умолчанию — **None** и параметр должен быть больше или равен 
**None**, и если пользователь передаст параметр, то минимально допустимое   
значение будет 1 **(ge — "greater than or equal to")**.

**Пример на простом языке**:

Представь, что у тебя есть функция, которая получает число от пользователя, и ты хочешь сказать: "Оно может быть не больше 100 и не меньше 1".
С Annotated ты можешь добавить это ограничение как метаданные.

```aiignore
from typing import Annotated

def process_number(number: Annotated[int, Query(ge=1, le=100)]):
    return number

```
Теперь FastAPI проверит число и вернёт ошибку, если оно не соответствует этим условиям.  


**Depends()** — это мощный механизм FastAPI для инъекции зависимостей в маршруты. Это означает, что ты можешь автоматически передавать параметры, функции или объекты в маршруты, без явного создания их в каждом запросе.

Что делает Depends()?

Depends() сообщает FastAPI, что для работы функции нужно выполнить или инжектировать определённую зависимость. Это может быть:

Валидация и обработка данных запроса (например, параметры запроса, пути или тела).  
Подключение к базе данных.  
Авторизация пользователя.  
Любые другие операции, которые ты хочешь выполнить до вызова функции маршрута.  

*Простой пример с Depends()*  
Пример: Авторизация пользователя  

Предположим, что у тебя есть система, где каждый запрос должен проверять, 
авторизован ли пользователь. 
Ты не хочешь писать эту логику в каждом маршруте. 
Вместо этого ты можешь создать отдельную зависимость, 
которая будет проверять токен авторизации, 
и FastAPI будет автоматически вызывать её при каждом запросе.

**Функция для проверки токена:**

```aiignore
from fastapi import Depends, HTTPException, status

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Здесь ты проверяешь токен
    if token != "valid_token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return {"user": "authorized_user"}

```

Здесь Depends(oauth2_scheme) указывает, что FastAPI должно взять токен (например, из заголовка HTTP) и передать его в функцию.
Если токен неверен, выбрасывается ошибка 401.
Если токен верен, функция возвращает данные о пользователе.

**Использование Depends() в маршруте:**
```aiignore
@router.get("/items/")
def read_items(user: dict = Depends(get_current_user)):
    return {"message": f"Hello, {user['user']}!"}

```
Когда клиент делает запрос к /items/, FastAPI автоматически вызывает функцию get_current_user, передаёт в неё токен и либо авторизует пользователя, либо возвращает ошибку.
Если авторизация прошла успешно, маршрут получает данные пользователя через user: dict.

**Резюме:**

**Annotated** добавляет метаданные к типам, чтобы FastAPI мог валидировать и документировать параметры.  

**Depends** используется для инъекции зависимостей, таких как параметры запроса, авторизация, конфигурации и т.д.

---
```aiignore
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
```


Этот импорт и использование конструкции sys.path.append(str(Path(__file__).parent.parent)) часто применяются для настройки путей к модулям, особенно в сложных проектах с вложенной структурой папок. Вот подробное объяснение:
Что делает код?
Импорт sys и Path:  
sys — это встроенный модуль Python, который предоставляет доступ к различным функциям и переменным, связанным с интерпретатором Python, например, к списку путей поиска модулей, запущенным процессам и системным настройкам.  
Path — это класс из модуля pathlib, который предоставляет удобный и современный способ работы с путями к файлам и директориям, позволяя легко оперировать файловой системой.  

sys.path.append:  
В Python sys.path — это список путей, по которым интерпретатор ищет модули, когда выполняется инструкция import. Это, по сути, "поисковый путь" Python.  
Вызов sys.path.append(<путь>) добавляет новый путь в конец этого списка. Это нужно для того, чтобы Python мог искать модули в указанной директории, если они не находятся в стандартных путях.  

Path(__file__).parent.parent:  
__file__ — это встроенная переменная, которая хранит путь к 
текущему исполняемому файлу Python.  
Path(__file__) создает объект пути, представляющий этот файл.  
parent возвращает родительскую директорию текущего файла.  
Второй .parent поднимается на одну директорию выше 
(к директории, в которой находится папка с текущим файлом).  

str(Path(...)):  
Преобразование объекта Path в строку необходимо, 
потому что sys.path.append() ожидает строковый путь.  

Когда это используется?  

Вложенные проекты: Если у вас есть проект с вложенными директориями, 
и вы хотите импортировать модули из родительской или другой верхнеуровневой директории, добавление пути через sys.path.append() может быть полезным. Например, если структура проекта выглядит так:  

```

project/
├── main.py
└── app/
    └── submodule/
        └── script.py

```
Если вы хотите импортировать модуль из директории app в файле script.py, вам нужно добавить путь к этой директории в sys.path.

Упрощение импорта: Без добавления пути, вам пришлось бы писать сложные относительные импорты, такие как:

python

from .. import some_module

Это может быть трудно поддерживать, особенно при глубоко вложенных структурах.

Использование скриптов в качестве модулей: Если вы хотите запускать отдельные файлы в качестве скриптов (например, для тестирования), но при этом сохранить возможность импорта из других частей проекта, вам может понадобиться модифицировать sys.path.

Пример

Предположим, у вас есть следующая структура:

```

project/
├── main.py
└── app/
    └── utils.py

```

Чтобы использовать код из utils.py в main.py, вы можете сделать следующее в main.py:

```
python

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "app"))

import utils
```
Этот код добавляет директорию app в пути поиска модулей, 
позволяя импортировать модуль utils.py.




**[pydantic_sattings...](pydantic_sattings.md)**

## Response

В FastAPI класс Response используется для управления тем, как ответы возвращаются клиенту.
По умолчанию, FastAPI автоматически создает объект Response на основе возвращаемых данных, 
но вы можете вручную настроить ответ, если вам нужен контроль над его содержимым, заголовками, 
статус-кодом, и т.д.  

**Как работает Response в FastAPI**

Когда вы пишете обработчик (эндпоинт), FastAPI возвращает объект Response, который включает:    
**Тело ответа (content):** данные, которые передаются клиенту (например, JSON, HTML, текст и т.д.).
**Заголовки (headers)**: HTTP-заголовки, передающие метаданные об ответе (например, Content-Type, Cache-Control).  
**Статус-код (status_code):** код состояния HTTP (например, 200 OK, 404 Not Found), который говорит о результате
выполнения запроса.  
**Куки (cookies):** механизм передачи данных между клиентом и сервером, хранящихся на стороне клиента.  

FastAPI сам создает ответ, когда вы возвращаете данные, например, словарь или список. 
Однако, вы можете возвращать объекты Response, чтобы явно контролировать содержимое и поведение ответа.  

### Основные классы для работы с Response

1. **Response** - базовый класс для создания кастомных ответов. Вы можете передать текст, HTML, JSON,
и указать тип содержимого (media_type).  
Пример: 
```aiignore
from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/custom")
def custom_response():
    return Response(content="Custom plain text", media_type="text/plain")

```
2. **JSONResponse** -  класс для отправки JSON-ответов. Это стандартный тип ответа, если вы возвращаете словарь.  

Пример:  
```
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/json")
def get_json_response():
    data = {"message": "This is a JSON response"}
    return JSONResponse(content=data)
```
3. **HTMLResponse** -  используется для отправки HTML-документов.

Пример:
```aiignore
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/html")
def get_html_response():
    html_content = "<h1>Hello, FastAPI!</h1>"
    return HTMLResponse(content=html_content)

```
4. **PlainTextResponse** -  используется для отправки текста.

Пример:
```aiignore
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/text")
def get_text_response():
    return PlainTextResponse(content="This is plain text")

```
### Работа с куками

Куки используются для хранения небольших фрагментов данных на стороне клиента.
В FastAPI вы можете управлять куками через Response и Request.  
Установка куки  

Для установки куки используется метод set_cookie() у объекта Response.
Вы можете задать параметры, такие как имя, значение, время жизни куки и другие.

Пример установки куки:  
```aiignore
from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/set-cookie/")
def set_cookie(response: Response):
    response.set_cookie(key="my_cookie", value="cookie_value", max_age=3600)  # кука будет жить 1 час
    return {"message": "Cookie set"}

```

Чтение куки  

Чтобы прочитать куки, используйте объект Request из FastAPI. Куки доступны через свойство cookies.  

Пример:
```aiignore
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/get-cookie/")
def get_cookie(request: Request):
    my_cookie = request.cookies.get("my_cookie")
    return {"my_cookie": my_cookie}

```
Удаление куки  

Для удаления куки нужно вызвать delete_cookie() у объекта Response.  

Пример удаления куки:
```aiignore
from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/delete-cookie/")
def delete_cookie(response: Response):
    response.delete_cookie(key="my_cookie")
    return {"message": "Cookie deleted"}

```
Методы Response  

Класс Response предоставляет следующие важные методы для работы с ответами:  

***set_cookie(key, value, max_age, expires, path, domain, secure, httponly)*** — устанавливает куки.  
key (обязательный):  

Это имя куки, которое будет храниться на стороне клиента.
Например: "session_id", "user_token".

value (обязательный):  

Значение куки, которое будет ассоциировано с ключом.
Например: уникальный идентификатор сессии, токен доступа.

Пример:  


>response.set_cookie(key="session_id", value="abc123")

max_age (необязательный):  

Указывает время жизни куки в секундах. По истечении этого времени кука удаляется.
Если параметр не указан, то кука будет сохраняться до закрытия браузера (сессионная кука).
Например: 3600 (кука будет жить 1 час).

Пример:  


>response.set_cookie(key="session_id", value="abc123", max_age=3600)  # Кука живет 1 час

expires (необязательный):  

Альтернативный способ задать время жизни куки через конкретную дату и время, после которого она истекает. Дата указывается в формате UNIX timestamp или строкой в формате HTTP Date.
Обычно используется либо max_age, либо expires, но не оба сразу.

Пример:  

```
from datetime import datetime, timedelta

expires = (datetime.utcnow() + timedelta(days=1)).strftime("%a, %d %b %Y %H:%M:%S GMT")
response.set_cookie(key="session_id", value="abc123", expires=expires)
```
path (необязательный):  

Определяет путь на сервере, к которому привязана кука. Только страницы, соответствующие этому пути, будут иметь доступ к куке.
По умолчанию — /, что означает, что кука доступна на всех страницах сайта.

Пример:  


>response.set_cookie(key="session_id", value="abc123", path="/admin")  # Кука будет доступна только на страницах под "/admin"

domain (необязательный):  

Определяет домен, на котором доступна кука. Полезно для работы с поддоменами.
Например, если указано domain=".example.com", кука будет доступна как на example.com, так и на всех его поддоменах (например, app.example.com).

Пример:  


>response.set_cookie(key="session_id", value="abc123", domain=".example.com")  # Кука доступна на поддоменах

secure (необязательный)  :

Если установлено в True, кука будет отправляться только по защищенному соединению (через HTTPS). Это помогает защитить куку от перехвата через незащищенные соединения.
По умолчанию False.

Пример:  


>response.set_cookie(key="session_id", value="abc123", secure=True)  # Кука будет отправляться только по HTTPS

httponly (необязательный):  

Если установлено в True, кука не будет доступна через JavaScript (то есть она не может быть прочитана или изменена с помощью document.cookie). Это помогает защитить куку от атак XSS (межсайтовый скриптинг).
По умолчанию False.

Пример:  


>response.set_cookie(key="session_id", value="abc123", httponly=True)  # Кука не доступна через JavaScript
  

***delete_cookie(key)*** — удаляет куки.
***headers*** — атрибут, который можно использовать для добавления/изменения заголовков в ответе.
***status_code*** — можно задать код состояния HTTP для ответа.

Пример использования Response с настройкой куки и заголовков  
```aiignore
from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/custom-response/")
def custom_response(response: Response):
    response.set_cookie(key="test_cookie", value="test_value")
    response.headers["X-Custom-Header"] = "CustomHeaderValue"
    return {"message": "Custom Response with Cookie and Header"}

```

