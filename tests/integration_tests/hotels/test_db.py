from sqlalchemy.ext.asyncio import async_sessionmaker

from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager


async def test_add_hotel():
    hotel_data = HotelAdd(title="Hotel 5 stars", location="Сочи")
    async with DBManager(session_factory=async_sessionmaker) as db:
        new_hotel_data = await db.hotels.add(hotel_data)
        print(f"{new_hotel_data=}")
