
pip install sqlalchemy alembic
pip install asyncpg
pip install greenlet


### Полезные материалы по теме:   
[Sqlalchemy 2.0 ...](https://django.fun/docs/sqlalchemy/2.0/)  
[Изминения в версии 2.0 ...](https://habr.com/ru/articles/735606/)
[Видеоматериалы по SQLAlchemy](https://www.youtube.com/watch?v=LKkn-2FId8w)


**Настройка асинхронного подключения**

Создадим файл db.py, где будет происходить настройка подключения к базе данных.

```aiignore
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# URL подключения для PostgreSQL
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/db_name"

# Создаем асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаем сессию для взаимодействия с базой данных
AsyncSessionLocal = sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Создаем базовый класс для ORM-моделей
Base = declarative_base()

```



**Создание модели**

Для работы с базой данных необходимо создать ORM-модель. Пусть это будет таблица Hotel.
```aiignore
from sqlalchemy import Column, Integer, String

class Hotel(Base):
    __tablename__ = 'hotels'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    stars = Column(Integer)

```

**Асинхронное взаимодействие**

Теперь давайте разберем несколько примеров запросов — как с использованием ORM, так и "сырые" SQL-запросы.
Пример 1: Асинхронная вставка с использованием ORM  
```
from db import AsyncSessionLocal
from models import Hotel

async def add_hotel(name: str, stars: int):
    async with AsyncSessionLocal() as session:
        new_hotel = Hotel(name=name, stars=stars)
        session.add(new_hotel)
        await session.commit()
        await session.refresh(new_hotel)
        return new_hotel

```

В этом примере мы создаем новый объект Hotel, добавляем его в сессию и сохраняем изменения в базу данных с помощью commit().
Пример 2: Сырой запрос на выборку    

Для выполнения "сырого" SQL-запроса используется метод session.execute().   
```aiignore
from db import AsyncSessionLocal
from sqlalchemy import text

async def get_hotels_raw():
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT * FROM hotels"))
        hotels = result.fetchall()
        return hotels

```
Здесь выполняется простой "сырой" SQL-запрос на выборку всех данных из таблицы hotels.  
Пример 3: Обновление данных с использованием ORM   
```aiignore
async def update_hotel(hotel_id: int, stars: int):
    async with AsyncSessionLocal() as session:
        hotel = await session.get(Hotel, hotel_id)
        if hotel:
            hotel.stars = stars
            await session.commit()
            return hotel
        return None

```
В этом примере обновляется информация о количестве звезд отеля.  
Пример 4: Сырой запрос на обновление  
```aiignore
async def update_hotel_raw(hotel_id: int, stars: int):
    async with AsyncSessionLocal() as session:
        await session.execute(
            text("UPDATE hotels SET stars = :stars WHERE id = :hotel_id"),
            {"stars": stars, "hotel_id": hotel_id}
        )
        await session.commit()

```
Этот пример показывает, как выполнять "сырые" SQL-запросы для обновления данных.  
Шаг 5: Инициализация базы данных  

Для создания таблиц необходимо инициализировать базу данных. 
Это можно сделать через специальный метод create_all().  
```aiignore
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

```

Пример использования FastAPI с асинхронным SQLAlchemy  

Теперь давайте рассмотрим, как интегрировать SQLAlchemy с FastAPI:  
```aiignore
from fastapi import FastAPI, Depends
from db import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

@app.post("/hotels/")
async def create_hotel(name: str, stars: int, db: AsyncSession = Depends(get_db)):
    new_hotel = Hotel(name=name, stars=stars)
    db.add(new_hotel)
    await db.commit()
    await db.refresh(new_hotel)
    return new_hotel

@app.get("/hotels/")
async def read_hotels(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM hotels"))
    return result.fetchall()

```  
---
Заметка
Функция для проверки соединения
```aiignore
async def func():
    async with engine.begin() as conn:
        res = await conn.execute(text("SELECT version()"))
        print(res.fetchall())


asyncio.run(func())
```
---

**Модели при помощи Mapped**

Использование Mapped в SQLAlchemy относится к более современному и 
типизированному стилю объявления моделей, который улучшает поддержку 
аннотаций типов в Python. В этой модели Mapped используется для аннотации 
атрибутов классов, а тип столбцов указывается с помощью типа аннотации, 
что делает код более понятным для систем типизации.  

**Создание моделей с использованием Mapped и более современной фабрикой сессии**

Новый более современный метод создания асинхронной сессии:  
```aiignore
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

# Создаем асинхронный движок для PostgreSQL с asyncpg
engine = create_async_engine(
    "postgresql+asyncpg://user:password@localhost/mydatabase", 
    echo=True
)

# Фабрика асинхронных сессий
AsyncSession = async_sessionmaker(
    bind=engine, 
    expire_on_commit=False
)


```


*Пример модели:*
```aiignore
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    age: Mapped[int] = mapped_column(Integer)

```
В этом примере:  

**Mapped[int]** используется для аннотации типа атрибута.  
**mapped_column()** заменяет обычный Column(), обеспечивая более 
чистую интеграцию с аннотациями типов.  

**Типы данных**

Все типы данных остаются такими же, как в обычном подходе с использованием Column, 
но мы аннотируем тип столбца с помощью Mapped:  

**Integer:** Представляет целые числа.
Пример: id: Mapped[int] = mapped_column(Integer)  

**String:** Строки с фиксированной или переменной длиной.
Пример: name: Mapped[str] = mapped_column(String(50))  

**Text:** Неограниченная строка, для хранения больших текстов.
Пример: content: Mapped[str] = mapped_column(Text)  

**Boolean:** Логические значения True или False.
Пример: is_active: Mapped[bool] = mapped_column(Boolean, default=False)  

**Date:** Дата без времени.
Пример: birthdate: Mapped[date] = mapped_column(Date)  

**DateTime:** Хранит дату и время.
Пример: created_at: Mapped[datetime] = mapped_column(DateTime)  

**Float:** Число с плавающей точкой.
Пример: salary: Mapped[float] = mapped_column(Float)  

**DECIMAL:** Точный числовой тип для денежных данных.
Пример: balance: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2))  

**Enum:** Хранение значений перечислений.
Пример: role: Mapped[Role] = mapped_column(Enum(Role))  

**LargeBinary:** Для хранения бинарных данных.
Пример: data: Mapped[bytes] = mapped_column(LargeBinary)  

**Аргументы столбцов**

**primary_key:** Если True, столбец является первичным ключом.
Пример: id: Mapped[int] = mapped_column(Integer, primary_key=True)  

**nullable:** Если False, столбец не может содержать NULL.
Пример: name: Mapped[str] = mapped_column(String(50), nullable=False)  

**unique:** Значения в столбце должны быть уникальными.
Пример: email: Mapped[str] = mapped_column(String(255), unique=True)  

**default:** Значение по умолчанию для столбца.
Пример: is_active: Mapped[bool] = mapped_column(Boolean, default=False)  

**index:** Создание индекса для столбца.
Пример: name: Mapped[str] = mapped_column(String(50), index=True)  

**ForeignKey:** Связывает столбец с другим столбцом (внешний ключ).
Пример: user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))  

**server_default:** Устанавливает значение по умолчанию на уровне сервера базы данных.
Пример: created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())  


**Преимущества использования Mapped**

Типизация: Четкая типизация на уровне Python.  
Совместимость: Интеграция с системами типизации (например, mypy).  
Чистота кода: Отделение типа данных и его описания через Mapped, что делает код более читаемым.  

Такой подход делает работу с моделями более современным и удобным, особенно в больших проектах 
с активным использованием аннотаций типов.

## [Alembic ...](alembic.md)

---

## INSERT

Шаги настройки:  

Настройка Async Engine и Async Session  
Создание моделей  
Выполнение INSERT запроса  

1. Настройка Async Engine и Async Session  

Асинхронный движок (engine) настраивается с
помощью **async_engine** и передается в **async_sessionmaker** 
для управления сессиями.  

```aiignore
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

# Определяем базу моделей
Base = declarative_base()

# Создаем асинхронный движок для подключения к базе данных PostgreSQL
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаем асинхронный фабрикатор сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

```

2. Создание моделей  

Определим простую модель, которая будет использоваться для вставки данных.  
```aiignore
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)

```

3. Выполнение **INSERT** запроса    

Теперь давайте рассмотрим, как выполнить **INSERT** запрос с использованием асинхронной сессии и SQLAlchemy 2.0.
Пример 1: **Простой INSERT**  

```aiignore
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

async def create_user(session: AsyncSession, name: str, email: str):
    # Создаем запрос на вставку
    stmt = insert(User).values(name=name, email=email)
    
    # Выполняем запрос
    await session.execute(stmt)
    await session.commit()

# Пример использования сессии
async def main():
    async with AsyncSessionLocal() as session:
        await create_user(session, "John Doe", "john.doe@example.com")

```
В этом примере используется метод insert() для создания запроса, который затем выполняется с помощью session.execute(stmt). Важно вызывать commit(), чтобы зафиксировать изменения.
Пример сырого SQL:

sql  
>INSERT INTO users (name, email) VALUES ('John Doe', 'john.doe@example.com');

4. Использование дополнительных параметров  

SQLAlchemy поддерживает различные параметры для insert() и execute():  

**values()** – указывает значения для вставки. Можно передавать либо конкретные значения, либо маппинг (словарь).
**prefix_with()** – добавляет префиксы к SQL-запросу. Используется для специфических модификаторов SQL (например, INSERT OR IGNORE).
**returning()** – позволяет вернуть определенные колонки после вставки.

Пример 2: **INSERT с returning()**  
```aiignore
async def create_user_returning_id(session: AsyncSession, name: str, email: str):
    # Создаем запрос на вставку с возвратом id
    stmt = insert(User).values(name=name, email=email).returning(User.id)
    
    # Выполняем запрос и получаем результат
    result = await session.execute(stmt)
    await session.commit()
    
    # Извлекаем id созданного пользователя
    user_id = result.scalar()
    return user_id

# Пример использования
async def main():
    async with AsyncSessionLocal() as session:
        user_id = await create_user_returning_id(session, "Jane Doe", "jane.doe@example.com")
        print(f"Created user with ID: {user_id}")

```

Пример сырого SQL:  

sql  
>INSERT INTO users (name, email) VALUES ('Jane Doe', 'jane.doe@example.com') RETURNING id;

5. Выполнение нескольких вставок  

Для массовой вставки можно передать список значений в values().  
Пример 3: **Массовая вставка**  
```aiignore
async def bulk_insert_users(session: AsyncSession, users: list[dict]):
    # Создаем запрос на массовую вставку
    stmt = insert(User).values(users)
    
    # Выполняем запрос
    await session.execute(stmt)
    await session.commit()

# Пример использования
async def main():
    async with AsyncSessionLocal() as session:
        users = [
            {"name": "Alice", "email": "alice@example.com"},
            {"name": "Bob", "email": "bob@example.com"},
        ]
        await bulk_insert_users(session, users)

```

Пример сырого SQL:

sql
>INSERT INTO users (name, email) VALUES 
('Alice', 'alice@example.com'), 
('Bob', 'bob@example.com');


Аргументы для insert():  

**table** – таблица, в которую выполняется вставка.
**values** – значения, которые вставляются в таблицу.
**prefix_with** – префиксы SQL-запроса (например, для специфичных конструкций базы данных).
**returning** – список полей, которые должны быть возвращены после вставки.

Асинхронное использование транзакций  

Для больших операций, состоящих из нескольких запросов, 
важно управлять транзакциями. Вот пример использования транзакций.  
Пример 4: **Транзакция**

```aiignore
async def create_multiple_users(session: AsyncSession, users: list[dict]):
    async with session.begin():  # Запуск транзакции
        stmt = insert(User).values(users)
        await session.execute(stmt)

# Пример использования
async def main():
    async with AsyncSessionLocal() as session:
        users = [
            {"name": "Charlie", "email": "charlie@example.com"},
            {"name": "Dave", "email": "dave@example.com"},
        ]
        await create_multiple_users(session, users)

```
В этом примере сессия находится в контексте транзакции, которая автоматически завершается после
выхода из контекстного менеджера.  
