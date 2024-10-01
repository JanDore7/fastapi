
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

**Создание моделей с использованием Mapped**

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



  ## Alembic

Alembic — это инструмент миграций базы данных для SQLAlchemy, который позволяет отслеживать изменения в структуре базы данных и применять их последовательно. Он широко используется для управления схемой базы данных в проектах на Python, особенно в сочетании с FastAPI и SQLAlchemy.
Установка Alembic  

Чтобы установить Alembic, используйте команду pip:  
> pip install alembic  

**Инициализация Alembic**  

После установки необходимо инициализировать проект Alembic:  
> alembic init alembic

Эта команда создаст директорию alembic, а также конфигурационный файл alembic.ini. В папке alembic появится несколько файлов:

**env.py** — основной скрипт, который управляет настройкой миграций.  
**Папка versions** — здесь будут храниться миграции.  


**Конфигурация файла alembic.ini**
Файл alembic.ini отвечает за глобальные настройки Alembic. Вот пример содержимого и подробное объяснение каждой строки:

```aiignore
# A generic, single database configuration.

[alembic]
# Название папки, где хранятся миграции. По умолчанию 'alembic'.
script_location = alembic

# Уровень логирования. INFO для стандартного вывода информации.
# Может быть DEBUG, INFO, WARNING, ERROR, CRITICAL.
log_level = INFO

# Системный путь, который будет добавлен к sys.path перед выполнением env.py
# Это полезно для загрузки кастомных модулей или настройки окружения, если
# ваши модели и бизнес-логика расположены в директориях, которые не включены
# в стандартный sys.path.
prepend_sys_path = .

# Версии миграций могут храниться в нескольких местах, если проект использует
# несколько баз данных или схем. Здесь можно указать дополнительные пути.
# Можно оставить закомментированным, если нет необходимости.
# version_locations = %(here)s/versions

# Указываем версию SQLAlchemy, с которой работает Alembic.
# sqlalchemy_module_prefix = None

# Путь к каталогу шаблонов. Оставляем по умолчанию.
# templates_path = %(here)s/templates

# Список всех URL, с которыми работает Alembic.
# Это строка подключения к базе данных.
# Этот параметр можно задать здесь или передавать через командную строку.
sqlalchemy.url = postgresql+asyncpg://user:password@localhost/dbname

[post_write_hooks]
# Здесь можно настроить пост-процессинг, например, автоматическое форматирование кода.
# python -m black: использовать black для форматирования сгенерированных файлов миграций.
# hooks можно применять для автоматизации после генерации миграций.
# Команда для использования black:
# hooks = python -m black

[logging]
# Управление логированием. В большинстве случаев можно оставить настройки по умолчанию.
# file = %(here)s/alembic.log  # Файл для логирования Alembic.

```

Важные параметры:

**prepend_sys_path** — этот параметр указывает путь, 
который будет добавлен в системный путь Python (sys.path) перед тем, 
как выполняется файл env.py. Это полезно, если у вас есть нестандартные модули или папки, которые необходимо сделать доступными для Alembic. Значение . (точка) указывает на текущую директорию проекта.
Например, если ваша структура проекта содержит директории, 
где хранятся модели или дополнительные настройки, 
вы можете указать их в этом параметре для правильного подключения.  
*Пример использования:*  

>prepend_sys_path = ./src  # Если ваши модели находятся в src/models.py

**script_location **— указывает, где хранятся миграции и конфигурационные файлы. По умолчанию это папка alembic.  

**sqlalchemy.url** — строка подключения к базе данных. Здесь указываются тип базы данных, пользователь, пароль и адрес.  

**log_level **— управляет уровнем детализации логирования. Для отладки можно поставить DEBUG, чтобы видеть больше информации.  

**version_locations** — этот параметр позволяет указать 
дополнительные пути для хранения версий миграций, 
если проект использует несколько баз данных или схем.    

**post_write_hooks** — опциональная настройка, которая позволяет выполнять команды после генерации миграций. 
Это может быть полезно для автоматического форматирования кода миграций 
с использованием таких инструментов, как black.  

**logging** — этот блок позволяет управлять логированием действий Alembic. Можно указать путь к файлу логов и настроить 
уровень логирования.  

**Настройка env.py**

Файл env.py отвечает за настройку контекста миграций. Основные моменты:  

Подключение к базе данных.  
Синхронизация состояния с моделями SQLAlchemy.  

Пример настройки env.py для асинхронного использования с FastAPI и SQLAlchemy:  
```aiignore
from alembic import context
from sqlalchemy import engine_from_config, pool
from myapp.models import Base  # Импортируем вашу базу
from logging.config import fileConfig
import asyncio

config = context.config
fileConfig(config.config_file_name)

# Ваша база моделей
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section), prefix="sqlalchemy.", poolclass=pool.NullPool
    )

    async with connectable.connect() as connection:
        await connection.run_sync(context.run_migrations)

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())

```
---
***Важно переменной target_metadata присвоить методанные вашей базы данных.
Предварительно импортировав его в файл env.py.  
Не менее важный момент это импорт всех ваших моделей 
в файле env.py не важно, что сама модель больше нигде не упоминается кроме импорта.***

sqlalchemy.url = нужно обязательно указывать драйвер подключения к базе данных.  
Если вы используете SQLite, то этот параметр можно не указывать.  

В нашем проекте мы для этого переопределим config в env.py:  
config = context.config  
config.set_main_option("sqlalchemy.url", f'{settings.DB_URL}?async_fallback=True')  

**config = context.config:**  
**context.config** — это объект конфигурации Alembic, который загружается из файла alembic.ini и предоставляет доступ к различным параметрам настройки.  
Эта строка присваивает объект конфигурации переменной config, чтобы можно было работать с параметрами Alembic напрямую через объект config.  

**config.set_main_option("sqlalchemy.url", ...):**
Метод set_main_option позволяет программно изменить или задать параметры конфигурации Alembic. В данном случае меняется значение для опции sqlalchemy.url, которая отвечает за строку подключения к базе данных.  
Обычно sqlalchemy.url задается в файле alembic.ini, но этот метод позволяет переопределить значение программно, что может быть полезно для динамической подстановки строки подключения.  

**f'{settings.DB_URL}?async_fallback=True'**:
Это строка формата (f-string), которая подставляет значение переменной settings.DB_URL в строку подключения к базе данных.
**settings.DB_URL** — это, скорее всего, строка подключения к базе данных (например, PostgreSQL, SQLite), которая хранится в вашем файле настроек (например, в Pydantic-модели settings).  
Параметр ?async_fallback=True добавляется

к строке подключения. Он может быть использован для баз данных с асинхронным драйвером (например, asyncpg для PostgreSQL) и означает, что если асинхронная поддержка недоступна, следует попытаться использовать синхронный режим (это зависит от того, как реализован драйвер или фреймворк).  

Что это даёт:

Динамическая конфигурация: Позволяет гибко менять строку подключения к базе данных на основе внешних настроек, например, переменных окружения или значений в коде. Это удобно для работы с разными окружениями (локальная разработка, тестирование, продакшн).

**Асинхронная поддержка: Добавление параметра ?async_fallback=True может использоваться в асинхронных фреймворках (например, FastAPI) для поддержки асинхронного подключения к базе данных. Если асинхронное подключение не удается установить, драйвер может переключиться на синхронный режим (если этот механизм поддерживается).

Таким образом, данный код позволяет гибко управлять строкой подключения к базе данных с поддержкой асинхронного режима.

---










**Создание миграций**

Автоматическое создание миграций — Alembic может отслеживать 
изменения в моделях SQLAlchemy и автоматически 
генерировать миграции. Для этого нужно ввести команду:  

>alembic revision --autogenerate -m "Добавление новых таблиц"

Применение миграций — Чтобы применить миграции к базе данных, выполните:  
>alembic upgrade head

Либо по ключу 
>alembic upgrade ключ

Откат миграций — Для отката последней миграции:  
>alembic downgrade -1

Удаление миграций — Чтобы удалить миграцию, выполните:
>alembic revision --autogenerate -m "Удаление таблицы" --delete

Полный список команд Alembic:  

**alembic init [directory]** — инициализация проекта для работы с Alembic.  
**alembic revision -m "Комментарий"** — создание новой ревизии (миграции) с комментариями.  
**alembic revision --autogenerate -m "Комментарий"**— автоматическая генерация миграции на основе изменений моделей.  
**alembic upgrade [version]** — обновление до указанной версии.  
**alembic upgrade head**— обновление до последней миграции.  
**alembic upgrade +1**— применение следующей миграции.  
**alembic downgrade [version]**— откат до указанной версии.  
**alembic downgrade -1**— откат на одну версию назад.  
**alembic downgrade base**— откат ко всем миграциям.  
**alembic current**— показать текущую версию базы данных.  
**alembic history**— показать историю миграций.  
**alembic heads**— показать все доступные версии миграций.  
**alembic branches**— показать ветвления миграций, если есть несколько путей.  
**alembic show [revision]**— показать детали миграции.  
**alembic stamp [revision]**— отметить базу как соответствующую определенной миграции без фактического
выполнения миграций.  