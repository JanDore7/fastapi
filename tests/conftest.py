import json

import pytest
from httpx import AsyncClient

from src.config import settings
from src.database import Base, async_session_null_pool
from src.database import engine_null_pool
from src.main import app

from src.models import *
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomsAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="function")
async def db() -> DBManager:
    async with DBManager(session_factory=async_session_null_pool) as db:
        yield db


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_hotels.json", encoding="utf-8") as file_hotels:
        hotels = json.load(file_hotels)
    with open("tests/mock_rooms.json", encoding="utf-8") as file_rooms:
        data_rooms = json.load(file_rooms)

    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels]
    rooms = [RoomsAdd.model_validate(room) for room in data_rooms]

    async with DBManager(session_factory=async_session_null_pool) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def test_add_user(ac, setup_database):
    await ac.post(
        "auth/register",
        json={"email": "ququrusya@pes.com", "password": "12345678"},
    )
