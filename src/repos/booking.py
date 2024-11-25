from datetime import date

from sqlalchemy import select

from src.repos.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.schemas.bookings import Booking


class BookingRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking

    async def get_bookings_with_today_checkin(self):
        query = select(BookingsOrm).filter(BookingsOrm.date_from == date.today())
        result = await self.session.execute(query)
