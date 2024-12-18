from datetime import date

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy import literal
from sqlalchemy import select

from src.models import RoomsOrm
from src.repos.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.repos.mapper.base import DataMapper
from src.repos.mapper.mappers import BookingDataMapper
from src.repos.utils import rooms_ids_for_booking
from src.schemas.bookings import BookingAdd
from src.schemas.bookings import BookingAddRequest


class BookingRepository(BaseRepository):
    model = BookingsOrm
    mapper: DataMapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        """
        Получаем список бронирований с датой сегодня
        :return: список бронирований
        """
        query = select(self.model).filter(BookingsOrm.date_from == date.today())
        result = await self.session.execute(query)
        return [self.mapper.map_to_schema(model) for model in result.scalars().all()]

    async def add_bookings(self, data: BookingAdd, hotel_id: int):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=data.date_from, date_to=data.date_to, hotel_id=hotel_id
        )
        rooms_ids_to_book_res = await self.session.execute(rooms_ids_to_get)
        rooms_ids_to_book: list[int] = rooms_ids_to_book_res.scalars().all()

        if data.room_id not in rooms_ids_to_book:
            raise HTTPException(status_code=500, detail="Нет свободны комнат")
        new_booking = await self.add(data)
        return new_booking
