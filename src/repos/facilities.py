from sqlalchemy import select, delete, insert

from src.repos.base import BaseRepository
from src.models.facilities import FacilitiesOrm, RoomFacilitiesOrm
from src.schemas.facilities import Facilities, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facilities


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomFacilitiesOrm
    schema = RoomFacility

    async def set_room_facilities(self, room_id: int, facilities: list[int]):
        get_current_facilities_ids_query = select(self.model.facilities_id).filter_by(rooms_id=room_id)
        result = await self.session.execute(get_current_facilities_ids_query)
        current_facilities_ida: list[int] = result.scalars().all()
        ids_to_delite: list[int] = list(set(current_facilities_ida) - set(facilities))
        ids_to_insert = list(set(facilities) - set(current_facilities_ida))

        if ids_to_delite:
            delite_m2m_facilities_stmt = (
                delete(self.model)
                .filter(
                    self.model.rooms_id == room_id,
                    self.model.facilities_id.in_(ids_to_delite))
            )
            await self.session.execute(delite_m2m_facilities_stmt)

        if ids_to_insert:
            insert_m2m_facilities_stmt = (
                insert(self.model)
                .values(
                    [{"rooms_id": room_id, "facilities_id": f_id} for f_id in ids_to_insert]
                )
            )
            await self.session.execute(insert_m2m_facilities_stmt)

