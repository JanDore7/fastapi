import pytest

from src.database import Base
from src.database import engine
from src.models import *


@pytest.fixture(autouse=True)
async def async_main():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
