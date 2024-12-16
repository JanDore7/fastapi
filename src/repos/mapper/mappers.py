from src.models import UsersOrm
from src.models.bookings import BookingsOrm
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repos.mapper.base import DataMapper
from src.schemas.bookings import Booking
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room, RoomWithRelationship
from src.schemas.users import UserWithPassword
from src.models.facilities import FacilitiesOrm
from src.schemas.facilities import Facilities


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel


class RoomsDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Room


class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Booking


class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = UserWithPassword


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facilities


class RoomDataWithRelationshipMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomWithRelationship
