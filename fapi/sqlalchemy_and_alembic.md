
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
[Подробнее ..](foreignKey.md)

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
**values()** – список значений для вставки. Можно передавать либо конкретные значения, либо маппинг (словарь).  
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
---
# Для дебага можно воспользоваться таким принтом:

```aiignore
add_hotel_stmt = insert(HotelsORM).values(**hotel_data.model_dump()).returning(HotelsORM.title)
print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
```
---

## Основы асинхронного SELECT-запроса

В SQLAlchemy для выполнения SELECT-запросов используется функция select(), которая возвращает объект запроса. Чтобы получить результат запроса, его нужно выполнить через сессию. В нашем случае, так как мы работаем с асинхронным кодом, сессия будет асинхронной.
Пример базового SELECT-запроса:  
```aiignore
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

async def get_all_users(session):
    result = await session.execute(select(User))
    users = result.scalars().all()  # scalars() возвращает модели ORM
    return users

```
В данном примере мы создаем запрос select(User), 
который выбирает все записи из таблицы users, связанной с моделью User. 
Функция **scalars()** возвращает результат в виде ORM-объектов. 

Различия между filter_by() и filter()  

SQLAlchemy предлагает два метода для фильтрации данных: 
filter_by() и filter().  
**filter_by()**  

Этот метод используется для простой фильтрации,
где значения передаются через именованные параметры.
Он работает с атрибутами моделей и является упрощённым.  
```aiignore
async def get_users_by_name(session, name):
    result = await session.execute(select(User).filter_by(name=name))
    users = result.scalars().all()
    return users

```
Здесь filter_by(name=name) проверяет, 
что поле name у модели User равно значению переменной name. 
Это удобно, когда у нас простое условие без сложной логики.  

**filter()**  
Метод filter() поддерживает более сложные условия и выражения. 
Он позволяет комбинировать фильтры с помощью логических операторов.  
```aiignore
from sqlalchemy import or_

async def get_users_by_name_or_email(session, name, email):
    result = await session.execute(
        select(User).filter(or_(User.name == name, User.email == email))
    )
    users = result.scalars().all()
    return users

```

Здесь filter(or_(User.name == name, User.email == email)) ищет пользователей, 
у которых либо имя равно name, либо email равен email. 
Метод or_() объединяет условия логическим "ИЛИ" (OR).  

**Использование оператора where()**  

Метод where() — это универсальный способ указать условия фильтрации, подобно filter(), 
но он используется напрямую в SQL-выражениях. 

```aiignore
async def get_users_with_condition(session):
    result = await session.execute(
        select(User).where(User.name == 'John', User.email.like('%example.com'))
    )
    users = result.scalars().all()
    return users

```
В данном примере используется метод where(), 
который задает условия выбора пользователей с именем "John" и email, 
заканчивающимся на "example.com".  

**Работа с подстроками: like() и ilike()**  

**like()**: ищет записи, содержащие определенную подстроку. SQL-запрос строится с использованием оператора LIKE.  
**ilike()**: как и like(), но чувствительность к регистру игнорируется (нечувствителен к регистру).  

Пример с like():  
```aiignore
async def search_users_by_name(session, substring: str):
    result = await session.execute(
        select(User).where(User.name.like(f'%{substring}%'))
    )
    users = result.scalars().all()
    return users

```

Здесь мы ищем всех пользователей, у которых в имени содержится подстрока, заданная в переменной substring.  

Пример с ilike():  
```aiignore
async def search_users_case_insensitive(session, substring: str):
    result = await session.execute(
        select(User).where(User.name.ilike(f'%{substring}%'))
    )
    users = result.scalars().all()
    return users

```
Здесь ilike() игнорирует регистр букв при поиске.  

**Работа с фильтрами: in_(), between()**  


**in_()** - Этот метод позволяет искать записи, 
где поле принадлежит одному из значений в списке.    

```aiignore
async def get_users_by_ids(session, user_ids):
    result = await session.execute(
        select(User).where(User.id.in_(user_ids))
    )
    users = result.scalars().all()
    return users

```
Здесь мы ищем всех пользователей,
чьи идентификаторы находятся в списке user_ids.  

**between()** - Используется для поиска записей, где значение поля попадает в заданный диапазон.  
```aiignore
from sqlalchemy import between

async def get_users_by_id_range(session, start_id: int, end_id: int):
    result = await session.execute(
        select(User).where(between(User.id, start_id, end_id))
    )
    users = result.scalars().all()
    return users

```
Здесь мы выбираем пользователей с идентификаторами в диапазоне от start_id до end_id включительно.  

**Использование options()**

Метод options() в SQLAlchemy — это мощный инструмент для изменения и настройки поведения запросов. Он позволяет указать стратегии выборки данных, такие как предзагрузка связанных объектов, откладывание загрузки данных и другие настройки, которые помогают оптимизировать запросы и минимизировать количество выполняемых SQL-запросов.

1. **joinedload**

Что делает: Предзагружает связанные объекты с помощью SQL-запроса с JOIN.
Это соединяет две таблицы в одном запросе и загружает связанные данные сразу.  
Когда использовать: Когда у вас есть объекты, связанные с текущей моделью, и вы хотите избежать отдельного 
запроса для каждого объекта (избежать "N+1 проблемы").  [N+1 проблема](N+1.md)  
Пример:
```aiignore
from sqlalchemy.orm import joinedload

# Загрузка пользователя вместе с его адресами в одном запросе с JOIN
session.query(User).options(joinedload(User.addresses)).all()

```
Особенности:  

Применяет SQL JOIN, что может быть эффективным для небольших таблиц,
но для больших может привести к увеличению объема передаваемых данных.  

2. **subqueryload**

Что делает: Предзагружает связанные объекты с помощью подзапроса (subquery). 
Этот подход выполняет отдельный запрос для связанных объектов и 
связывает их с основным набором данных.  
Когда использовать: Когда joinedload может привести к слишком
большим результатам, из-за чего запрос будет тяжелым. 
Подзапросы лучше подходят для загрузки данных из больших таблиц.  
Пример:    
```aiignore
from sqlalchemy.orm import subqueryload

# Загрузка пользователя с адресами через подзапрос
session.query(User).options(subqueryload(User.addresses)).all()

```
Особенности:

Выполняется отдельный запрос для связанных объектов, 
что может быть более эффективно для больших объемов данных, 
так как предотвращает создание огромных JOIN.  

3. **selectinload**

Что делает: Похож на subqueryload, но использует SQL-оператор
IN вместо подзапроса. Таким образом, связанные объекты загружаются 
через один SQL-запрос, который выбирает данные с помощью условия IN.   
Когда использовать: Когда нужно загрузить связанные объекты по 
условию с IN оператором. Это эффективно для больших выборок данных, 
когда используется один запрос для нескольких связанных объектов.  
Пример:  
```aiignore
from sqlalchemy.orm import selectinload

# Загрузка адресов пользователей через IN-запрос
session.query(User).options(selectinload(User.addresses)).all()

```
Особенности:  

Это решение может быть быстрее, чем subqueryload в зависимости 
от структуры данных, так как использует одну выборку с IN.  


4. **lazyload**

Что делает: Откладывает загрузку связанных объектов до тех пор,
пока они не будут реально использованы в коде. 
При первом обращении к связанному объекту выполняется отдельный запрос 
для его загрузки.  
Когда использовать: Если вы хотите загружать только те связанные объекты, 
которые действительно понадобятся, чтобы минимизировать 
начальную нагрузку на базу данных.  
Пример:  
```aiignore
from sqlalchemy.orm import lazyload

# Связанные объекты будут загружены только при обращении к ним
session.query(User).options(lazyload(User.addresses)).all()

```
Особенности:  

Предотвращает загруженность базы данных при выполнении 
первоначальных запросов, но может привести к множественным 
отдельным запросам при обращении к связанным данным (N+1 проблема).  

5. **raiseload**

Что делает: Препятствует ленивой загрузке и вызывает исключение, 
если к связанным объектам обращаются лениво (при попытке их загрузить 
после выполнения основного запроса).  
Когда использовать: Чтобы выявить неявные ленивые загрузки в коде, 
которые могут приводить к снижению производительности из-за 
избыточных SQL-запросов.  
Пример:  
```aiignore
from sqlalchemy.orm import raiseload

# Вызовет исключение, если будет попытка лениво загрузить связанные объекты
session.query(User).options(raiseload(User.addresses)).all()

```
Особенности:  

Полезно при отладке запросов и улучшении их производительности, 
так как предотвращает незамеченные ленивые загрузки.


6. **defer**

Что делает: Откладывает загрузку конкретных столбцов 
до момента их реального использования. Это позволяет исключить 
ненужные данные из основного запроса, тем самым снижая нагрузку 
на базу данных.  
Когда использовать: Если есть большие или редко используемые столбцы,
которые не нужно загружать при каждом запросе.  
Пример:  

```aiignore
from sqlalchemy.orm import defer

# Колонка large_column не будет загружена сразу
session.query(User).options(defer(User.large_column)).all()

```
Особенности:  
Полезно для оптимизации запросов, если 
данные некоторых колонок загружаются редко.  

7. **undefer**

Что делает: Принудительно загружает те столбцы, 
загрузка которых была отложена с помощью defer.
Это используется для предзагрузки отложенных колонок.  
Когда использовать: Если вам нужно принудительно загрузить 
отложенные колонки в конкретном запросе, 
например, для предотвращения ленивой загрузки.  
Пример:
```aiignore
from sqlalchemy.orm import undefer

# Колонка large_column будет загружена, несмотря на отложенную загрузку
session.query(User).options(undefer(User.large_column)).all()

```

Особенности:  

Может использоваться для оптимизации в тех случаях,
когда необходимо управлять загрузкой отложенных данных.  

8. **contains_eager**

Что делает: Используется для указания, что
связанные объекты уже были загружены (например, 
с помощью отдельного запроса или другого метода),
и их не нужно загружать повторно.  
Когда использовать: Если вы уже выполнили отдельный запрос, 
который загрузил связанные данные, и хотите использовать 
их в основном запросе, избегая повторной загрузки.  
    Пример:  

```aiignore
from sqlalchemy.orm import contains_eager

# Связанные адреса уже загружены, не нужно их загружать заново
session.query(User).join(User.addresses).options(contains_eager(User.addresses)).all()

```

Особенности:  

Полезно при сложных запросах, когда данные уже загружены
через другие механизмы.  

---
Эти опции можно комбинировать, 
чтобы тонко настраивать запросы в зависимости от потребностей 
вашего приложения. Выбор подходящей стратегии загрузки данных зависит от 
структуры данных и количества связанных объектов. Например,
для небольших наборов данных joinedload может быть эффективным, 
а для больших данных лучше использовать subqueryload или selectinload.

## Обработка резултатов

1. **Метод scalars()**  

Метод scalars() используется для извлечения ORM-объектов из 
результатов SQLAlchemy-запросов. Когда вы выполняете запрос 
через session.execute(), результат может содержать строки 
(в виде кортежей), которые соответствуют столбцам в базе данных. 
scalars() помогает преобразовать эти строки в ORM-объекты, 
связанные с моделью.  
Пример использования scalars():   
```aiignore
async def get_all_users(session):
    result = await session.execute(select(User))
    users = result.scalars().all()  # scalars() возвращает ORM-объекты, вместо кортежей
    return users

```
Объяснение:

**scalars()** извлекает значения первой колонки в каждой 
строке запроса и преобразует их в объекты ORM. 
Это особенно полезно, когда ваш запрос возвращает объекты модели, 
например, User, вместо простых данных.  

**Метод all()** возвращает все результаты запроса в виде списка.  

Пример без scalars():  

Если не использовать scalars(), результатом запроса могут быть кортежи:  
```aiignore
async def get_all_users_without_scalars(session):
    result = await session.execute(select(User))
    users = result.all()  # Вернется список кортежей
    return users

```
В таком случае каждый элемент в users будет кортежем, 
содержащим один объект User. Например, 
users[0] будет (User(id=1, name='John'),),
что требует дополнительных шагов для извлечения данных.  

2. **Метод all()**  

**Метод all()** возвращает все результаты запроса в виде списка.
Его можно использовать как с scalars(), так и без него.  
Пример:  
```aiignore
async def get_all_users(session):
    result = await session.execute(select(User))
    users = result.scalars().all()  # Возвращает все результаты как список объектов User
    return users

```
all() удобен, когда вы хотите получить все записи из базы данных и сразу же обработать их.  


3. **Метод first()**  

Метод **first()** возвращает первый результат запроса. Если в выборке нет результатов, то он вернёт None.  
Пример:  
```aiignore
async def get_first_user(session):
    result = await session.execute(select(User))
    user = result.scalars().first()  # Возвращает первый объект User
    return user

```
Использование first() эффективно, если вас интересует только один 
результат и вы хотите избежать лишних вычислений для остальных данных.  

4. Метод **one()** и **one_or_none()**  

Метод **one()** гарантирует, что результатом запроса будет ровно одна запись. Если запрос вернёт 
больше одной записи или не найдёт ни одной, то будет вызвано исключение.  
Пример с one():
```aiignore
async def get_exactly_one_user(session):
    result = await session.execute(select(User).where(User.name == 'John'))
    user = result.scalars().one()  # Возвращает объект User, если он ровно один
    return user

```
Если результатом запроса будет больше одной записи, 
выбросится MultipleResultsFound.  
Если не будет ни одной записи, выбросится NoResultFound.  

Если есть вероятность, что результата может не быть, и это нормально для вашего случая, 
лучше использовать one_or_none().  
Пример с one_or_none():
```aiignore
async def get_one_user_or_none(session):
    result = await session.execute(select(User).where(User.name == 'John'))
    user = result.scalars().one_or_none()  # Возвращает объект User или None
    return user

```
Если результат один, то возвращается объект.  
Если результата нет, возвращается None.  
Если результатом будет больше одной записи, выбросится MultipleResultsFound.

5. Метод **fetchall()** и **fetchone()**

Эти методы используются для получения необработанных данных (сырых строк), как они пришли из базы данных, в отличие от scalars(), который возвращает ORM-объекты.
fetchall()  

Возвращает все результаты запроса в виде списка строк.  

```aiignore
async def get_raw_results(session):
    result = await session.execute(select(User))
    rows = result.fetchall()  # Возвращает все строки результата
    return rows

```
Каждый элемент в списке rows будет кортежем, содержащим данные строк. Например, rows[0] может выглядеть как (1, 'John', 'john@example.com'), где 1 — это id, 'John' — это имя пользователя, а 'john@example.com' — это email.
fetchone()  

Возвращает только одну строку результата.  

```aiignore
async def get_one_raw_result(session):
    result = await session.execute(select(User))
    row = result.fetchone()  # Возвращает одну строку результата
    return row

```

Этот метод используется, когда вам нужно получить
одну строку из базы данных, но в виде сырого формата (кортежа).  


6. Метод **partitions()**

Метод partitions() используется для итерации по результатам запроса
с использованием "разбиений" данных (порциями). 
Это полезно, когда у вас есть большое количество данных 
и вы хотите обрабатывать их небольшими 
блоками, чтобы избежать большого потребления памяти.  
Пример использования partitions():   
```aiignore
async def get_users_in_partitions(session):
    result = await session.execute(select(User))
    for partition in result.partitions(10):  # Итерация по результатам с шагом 10
        users = partition.scalars().all()  # Обрабатываем 10 пользователей за раз
        # Дальнейшая логика обработки

```

Заключение

Вот основные методы, которые можно использовать для работы с 
результатами запросов в SQLAlchemy:  

**scalars()** — извлекает ORM-объекты (обычно первую колонку из каждой строки).
**all()** — возвращает все результаты запроса в виде списка.
**first()** — возвращает первый результат запроса или None, если результатов нет.
**one()** — возвращает один результат и выбрасывает исключение, если результатов больше одного или нет вовсе.
**one_or_none()** — возвращает один результат или None, но выбрасывает исключение, если найдено более одной записи.
**fetchall()** и fetchone() — возвращают сырые данные запроса в виде кортежей (все строки или одну строку соответственно).
**partitions()** — обрабатывает результаты запроса порциями.


### [Паттерн DAO ...](DAO.md)
### [Паттерн DATA MAPPING ...](DATA_MAPPING.md)

## Common Table Expressions

CTE (Common Table Expressions, или «Общие табличные выражения»)
в SQL используются для создания временных наборов данных, 
которые можно повторно использовать в одном запросе. 
CTE особенно удобны, если требуется разбить сложный запрос на отдельные части 
или выполнить рекурсивные запросы.
В SQLAlchemy также можно использовать CTE для упрощения сложных 
запросов и повышения их читабельности.  
**1. Использование CTE в чистом SQL** 

В SQL CTE создаются с помощью ключевого слова WITH.
Это позволяет объявить временную таблицу, которая будет использоваться только в этом запросе.
**Пример 1. Простое CTE**

Предположим, у нас есть таблица employees с информацией о сотрудниках,
где хранятся id, name и department_id.
Мы хотим найти всех сотрудников из конкретного департамента и отсортировать их по имени.
```aiignore
WITH department_employees AS (
    SELECT id, name
    FROM employees
    WHERE department_id = 2
)
SELECT *
FROM department_employees
ORDER BY name;

```
Здесь department_employees — временная таблица,
созданная на основе результата запроса. 
Во втором SELECT мы уже ссылаемся на неё как на отдельную таблицу.  

**Пример 2. Рекурсивное CTE**

Рекурсивные CTE полезны, когда нужно, например, получить данные о структуре компании 
(например, иерархию сотрудников).
```aiignore
WITH RECURSIVE employee_hierarchy AS (
    SELECT id, name, manager_id
    FROM employees
    WHERE manager_id IS NULL  -- Начинаем с начальников без руководителей
    
    UNION ALL
    
    SELECT e.id, e.name, e.manager_id
    FROM employees e
    INNER JOIN employee_hierarchy eh ON e.manager_id = eh.id
)
SELECT *
FROM employee_hierarchy;

```
В этом примере employee_hierarchy используется для получения всех сотрудников 
вместе с их подчиненными.

**2. Использование CTE в SQLAlchemy**

SQLAlchemy поддерживает CTE через метод cte().
Давайте рассмотрим, как работать с CTE в SQLAlchemy на примере аналогичных запросов.
Подготовка  

Предположим, что у нас уже настроено асинхронное соединение с базой данных
и определена таблица employees через SQLAlchemy ORM.

```aiignore
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    department_id = Column(Integer, ForeignKey('departments.id'))
    manager_id = Column(Integer, ForeignKey('employees.id'), nullable=True)

    manager = relationship('Employee', remote_side=[id], backref='subordinates')

```
**Пример 1. Простое CTE с SQLAlchemy**  

Создадим CTE для выборки сотрудников из определенного департамента и сортировки по имени.

```aiignore
from sqlalchemy.future import select
from sqlalchemy import cte

async def get_department_employees(session: AsyncSession, department_id: int):
    # Создаем CTE
    department_employees = (
        select(Employee.id, Employee.name)
        .where(Employee.department_id == department_id)
        .cte("department_employees")
    )
    
    # Используем CTE в основном запросе
    stmt = select(department_employees).order_by(department_employees.c.name)
    
    result = await session.execute(stmt)
    return result.fetchall()

```
Здесь cte("department_employees") создает временную таблицу, 
которую можно использовать в других запросах. Этот пример аналогичен простому CTE из SQL.  
### ВАЖНО, обращение к столбцам из временной таблицы должно быть через cte.c.

Пример 2. Рекурсивное CTE с SQLAlchemy  

Для построения иерархии сотрудников с помощью рекурсивного CTE 
в SQLAlchemy нужно задать объединение union_all.  

```aiignore
from sqlalchemy import union_all

async def get_employee_hierarchy(session: AsyncSession):
    # Базовый запрос для начального уровня (руководителей без менеджеров)
    base_query = select(Employee.id, Employee.name, Employee.manager_id).where(Employee.manager_id == None)
    
    # Рекурсивный запрос для подчиненных сотрудников
    recursive_query = select(Employee.id, Employee.name, Employee.manager_id).join(
        employee_hierarchy, Employee.manager_id == employee_hierarchy.c.id
    )
    
    # Объединяем запросы
    employee_hierarchy = base_query.union_all(recursive_query).cte(recursive=True)
    
    # Основной запрос для выборки иерархии
    stmt = select(employee_hierarchy)
    
    result = await session.execute(stmt)
    return result.fetchall()

```
Здесь:  

**base_query** выбирает всех сотрудников, у которых нет менеджера.
**recursive_query** присоединяет подчиненных к базовому запросу.
**employee_hierarchy** объединяет базовый и рекурсивный запросы через union_all.

