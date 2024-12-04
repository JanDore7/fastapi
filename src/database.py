from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.config import settings
from sqlalchemy.orm import DeclarativeBase


# Создаем асинхронный движок
engine = create_async_engine(settings.DB_URL)

# Создаем движок для работы с задачами celery pool_class=NullPool — указывает, что движок не будет использовать пул
# подключений, а будет открывать новое соединение для каждого запроса.
engine_null_pool = create_async_engine(settings.DB_URL, poolclass=NullPool)


# Создаем асинхронный фабрикатор сессий
async_session = async_sessionmaker(engine, expire_on_commit=False)

# Создаем асинхронный фабрикатор сессий для работы с задачами celery
async_session_null_pool = async_sessionmaker(engine_null_pool, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
