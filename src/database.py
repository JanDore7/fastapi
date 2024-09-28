import asyncio

from pydantic import with_config
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.config import settings
from sqlalchemy import text


engine = create_async_engine(settings.DB_URL)

async def func():
    async with engine.begin() as conn:
        res = await conn.execute(text("SELECT version()"))
        print(res.fetchall())


asyncio.run(func())