from src.repos.base import BaseRepository
from src.models.facilities import FacilitiesOrm, RoomFacilitiesOrm
from src.schemas.facilities import Facilities, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facilities


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomFacilitiesOrm
    schema = RoomFacility