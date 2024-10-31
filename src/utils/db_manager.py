from src.repos.usres import UserRepository
from src.repos.hotels import HotelRepository
from src.repos.rooms import RoomsRepository
from src.repos.booking import BookingRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UserRepository(self.session)
        self.hotels = HotelRepository(self.session)
        self.rooms = RoomsRepository(self.session)
        self.bookings = BookingRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
