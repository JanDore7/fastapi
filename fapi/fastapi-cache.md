**1. Установка**

Установите библиотеку fastapi-cache вместе с поддержкой нужного backend'а (например, Redis):
```angular2html
pip install fastapi-cache[redis]
```
Если требуется поддержка другого backend'а (например, Memcached), можно использовать соответствующие зависимости.  

**2. Настройка и основные компоненты**
**2.1 Инициализация кэша**

Для начала работы нужно инициализировать провайдер кэша. Пример для Redis:
```angular2html
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import aioredis

app = FastAPI()

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
```
**RedisBackend(redis)**: указывает, что мы используем Redis в качестве хранилища кэша.
**prefix="fastapi-cache"**: задаёт префикс для всех ключей в Redis, чтобы избежать конфликтов.

**2.2 Декоратор @cache**

@cache используется для кэширования результата функции. Пример
```angular2html
from fastapi import APIRouter
from fastapi_cache.decorator import cache

router = APIRouter()

@router.get("/items")
@cache(expire=60)  # Кэширование на 60 секунд
async def get_items():
    return {"items": ["item1", "item2", "item3"]}
```
**expire=60**: задаёт время жизни кэша в секундах.

**3. Подробности использования**
**3.1 Установка времени жизни кэша**

Вы можете указать время жизни кэша (TTL) через параметр expire:

**expire=0**: результат будет кэшироваться без ограничения времени.
**expire=None**: отключает кэширование.

**3.2 Настройка ключей кэша**

Библиотека автоматически генерирует ключи на основе пути запроса и параметров. Вы можете изменить генерацию ключей, передав кастомную функцию:
```angular2html
from fastapi_cache import FastAPICache

def custom_key_builder(function, namespace, request, response):
    return f"{namespace}:{request.url.path}"

FastAPICache.init(backend, key_builder=custom_key_builder)
```
**4. Поддерживаемые backend'ы**

fastapi-cache поддерживает несколько хранилищ, включая:
4.1 Redis

Используйте RedisBackend для кэширования в Redis:
```angular2html
from fastapi_cache.backends.redis import RedisBackend
import aioredis

redis = aioredis.from_url("redis://localhost")
FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
```
**4.2 In-Memory (по умолчанию)**

Для небольших приложений можно использовать кэш в памяти:
```angular2html
from fastapi_cache.backends.inmemory import InMemoryBackend

FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
```
**5. Расширенные функции**
**5.1 Очистка кэша**

Чтобы удалить данные из кэша, используйте метод FastAPICache.clear():
```angular2html
from fastapi import APIRouter
from fastapi_cache import FastAPICache

router = APIRouter()

@router.delete("/cache")
async def clear_cache():
    await FastAPICache.clear()
    return {"message": "Cache cleared"}
```
**5.2 Использование кэша в зависимости**

Вы можете использовать кэш как часть зависимости:
```angular2html
from fastapi import Depends
from fastapi_cache.decorator import cache

async def get_data():
    # Здесь может быть тяжелый запрос к базе данных
    return {"data": "value"}

@router.get("/data")
@cache(expire=30)
async def cached_endpoint(data=Depends(get_data)):
    return data
```
**6. Тестирование**

Для тестирования кэширования можно использовать инструменты вроде pytest с моками или напрямую подключаться к Redis, чтобы убедиться, что ключи создаются правильно.

**7. Полный пример приложения**
```angular2html
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
import aioredis

app = FastAPI()

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="example")

@app.get("/data")
@cache(expire=10)
async def get_data():
    return {"message": "This response is cached for 10 seconds"}

@app.delete("/clear-cache")
async def clear_cache():
    await FastAPICache.clear()
    return {"message": "Cache cleared"}
```

**Подробное объяснение custom_key_builder и всех методов FastAPICache**
**Основные понятия кэширования в FastAPI**

Когда мы используем кэширование, ключ для кэша позволяет определить, какие данные сохранять или извлекать. В библиотеке fastapi-cache ключи создаются автоматически на основе URL, параметров запроса и других данных. Однако, в некоторых случаях вам может понадобиться настроить свой способ генерации ключей (например, чтобы игнорировать определённые параметры или учитывать специфические условия).
**Объяснение custom_key_builder**
Пример кода
```angular2html
from fastapi import FastAPI
from fastapi_cache import FastAPICache

# Функция для создания кастомного ключа
def custom_key_builder(function, namespace, request, response):
    """
    Генерирует ключ для кэширования.
    
    Параметры:
    - function: ссылка на кэшируемую функцию.
    - namespace: пространство имён (например, префикс для ключа).
    - request: объект запроса FastAPI.
    - response: объект ответа FastAPI (может быть None для генерации ключа перед выполнением запроса).

    Возвращает:
    - Строка, которая будет использоваться в качестве ключа.
    """
    # Ключ включает префикс (namespace) и путь запроса
    return f"{namespace}:{request.url.path}"

# Инициализация FastAPICache с кастомным генератором ключей
app = FastAPI()

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(
        backend=RedisBackend(redis), 
        key_builder=custom_key_builder  # Используем кастомный key_builder
    )
```
Пошаговое объяснение

Что такое key_builder? Это функция, которая принимает 4 параметра:
**function**: Ссылка на функцию, для которой генерируется ключ.
**namespace**: Пространство имён (определяется при инициализации FastAPICache через параметр prefix).
**request**: Объект запроса Request, содержащий информацию о текущем запросе (например, URL, заголовки, параметры и т.д.).
**response**: Объект ответа Response. Может быть None, если ключ генерируется до выполнения запроса.

Возвращаемое значение — строка, которая будет использоваться в качестве ключа в хранилище кэша.

Как работает пример custom_key_builder? В данном случае ключ создаётся на основе двух параметров:  
        Пространства имён namespace (например, "fastapi-cache").  
        Пути запроса request.url.path (например, "/items").  

Таким образом, если запрос идёт на /items, ключ будет выглядеть как "fastapi-cache:/items".

Когда использовать custom_key_builder? Вы можете использовать его в следующих случаях:
Нужно исключить определённые параметры запроса (например, игнорировать query-параметры).  
Нужно добавить уникальные атрибуты, такие как токены аутентификации.  
Вы хотите стандартизировать формат ключей.  

**Подробное описание методов FastAPICache**

Класс FastAPICache предоставляет несколько полезных методов. Рассмотрим их детально:
**1. FastAPICache.init(backend, key_builder=None, prefix="fastapi-cache")**

Используется для инициализации кэширования в приложении.
Параметры:  

backend: Указывает, какое хранилище использовать. Пример: RedisBackend, InMemoryBackend.  
key_builder: (Опционально) Функция для кастомной генерации ключей кэша. По умолчанию используется автоматическая генерация.  
prefix: (Опционально) Пространство имён для ключей. Помогает избежать конфликтов, если один Redis используется несколькими приложениями.  

**2. FastAPICache.get_backend()**

Возвращает текущий backend, используемый для кэширования.  
Пример:
```angular2html
backend = FastAPICache.get_backend()
print(f"Current backend: {backend}")
```
**3. FastAPICache.get_key_builder()**

Возвращает текущую функцию генерации ключей.  
Пример:  
```angular2html
key_builder = FastAPICache.get_key_builder()
print(f"Key builder function: {key_builder}")
```

**4. FastAPICache.clear(namespace=None)**

Удаляет все записи из кэша.  
Параметры:  

**namespace**: (Опционально) Пространство имён, в котором будут удалены ключи. Если не указано, очищается весь кэш.  

Пример:
```angular2html
from fastapi import FastAPI
from fastapi_cache import FastAPICache

app = FastAPI()

@app.delete("/clear-cache")
async def clear_cache():
    await FastAPICache.clear(namespace="fastapi-cache")
    return {"message": "Cache cleared"}
```
**5. FastAPICache.set(key, value, expire)**

Сохраняет значение в кэш вручную.  
Параметры:  

**key**: Ключ, по которому сохраняется значение.
**value**: Данные для сохранения.
**expire**: Время жизни кэша в секундах.

Пример: 
```angular2html
await FastAPICache.set("custom-key", {"data": "value"}, expire=60)
```

**6. FastAPICache.get(key)**

Возвращает данные из кэша по ключу.  
Параметры:  

**key**: Ключ, по которому извлекаются данные. 

Пример:
```angular2html
cached_data = await FastAPICache.get("custom-key")
if cached_data:
    print("Data from cache:", cached_data)
```
**7. FastAPICache.delete(key)**

Удаляет запись из кэша по ключу.  
Параметры:  

**key**: Ключ для удаления.  

Пример:
```angular2html
await FastAPICache.delete("custom-key")
```

**Полный пример использования всех методов**
```angular2html
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
import aioredis

app = FastAPI()

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(
        RedisBackend(redis), 
        prefix="example",
        key_builder=lambda f, ns, req, res: f"{ns}:{req.url.path}?{req.query_params}"
    )

@app.get("/data")
@cache(expire=10)
async def get_data():
    return {"message": "This response is cached for 10 seconds"}

@app.get("/cache-manual")
async def manual_cache():
    key = "manual:key"
    cached_data = await FastAPICache.get(key)
    if cached_data:
        return {"cached": True, "data": cached_data}
    # Сохраняем данные вручную
    data = {"message": "Manually cached data"}
    await FastAPICache.set(key, data, expire=30)
    return {"cached": False, "data": data}

@app.delete("/clear-cache")
async def clear_cache():
    await FastAPICache.clear()
    return {"message": "Cache cleared"}
```

