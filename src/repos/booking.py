from datetime import date

from sqlalchemy import select

from src.repos.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.repos.mapper.base import DataMapper
from src.repos.mapper.mappers import BookingDataMapper


class BookingRepository(BaseRepository):
    model = BookingsOrm
    mapper: DataMapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        """
        Получаем список бронирований с датой сегодня
        :return: список бронирований
        """
        query = select(BookingsOrm).filter(BookingsOrm.date_from == date.today())
        result = await self.session.execute(query)
        return [self.mapper.map_to_schema(model) for model in result.scalars().all()]
