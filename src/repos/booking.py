from datetime import date


from sqlalchemy import func
from sqlalchemy import literal
from sqlalchemy import select

from src.models import RoomsOrm
from src.repos.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.repos.mapper.base import DataMapper
from src.repos.mapper.mappers import BookingDataMapper
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

    async def add_bookings(self, data: BookingAddRequest):
        # Подзапрос для подсчета количества бронирований
        booking_count_subquery = (
            select(func.count(self.model.id))
            .filter(
                self.model.room_id == data.room_id,
                self.model.date_from < data.date_to,
                self.model.date_to > data.date_from,
            )
            .scalar_subquery()
        )

        # Основной запрос
        query = select(
            RoomsOrm.quantity
            - func.coalesce(booking_count_subquery, literal(0)).label("free_rooms")
        ).filter(RoomsOrm.id == data.room_id)

        print(query.compile(compile_kwargs={"literal_binds": True}))

        # Выполнение запроса
        result = await self.session.execute(query)
        result = result.scalar()
        return result
