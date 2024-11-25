from src.models.bookings import BookingsOrm
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repos.mapper.base import DataMapper
from src.schemas.bookings import Booking
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel


class RoomsDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Room


class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Booking
