
pip install sqlalchemy alembic
pip install asyncpg
pip install greenlet

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

