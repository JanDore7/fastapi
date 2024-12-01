import json

import pytest
from httpx import AsyncClient

from src.config import settings
from src.database import Base, engine_null_pool
from src.main import app

from src.models import *


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def async_main(check_test_mode):

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


def read_json(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


@pytest.fixture(scope="session", autouse=True)
async def test_add_data(async_main):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        hotels_data = read_json("tests/mock_hotels.json")
        rooms_data = read_json("tests/mock_rooms.json")
        response = await ac.post(
            "/hotels",
            json=hotels_data,
        )

        for room in rooms_data:
            print(f"Данные комнаты: {room}")
            response = await ac.post(f"/{room['hotel_id']}/rooms", json=room)
            print(
                f"Ответ сервера при добавлении комнаты {room['hotel_id']}: {response.status_code}, {response.json()}"
            )


@pytest.fixture(scope="session", autouse=True)
async def test_add_user(test_add_data):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(
            "auth/register",
            json={"email": "ququrusya@pes.com", "password": "12345678"},
        )
