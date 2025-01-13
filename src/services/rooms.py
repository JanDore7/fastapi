from datetime import date

from src.exception import check_date_correct, ObjectNotFoundException, HotelNotFoundException, \
    ObjectAlreadyExistsException
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomsAdd, RoomsAddRequest
from src.services.base import BaseService


class RoomService(BaseService):
    async def get_filtered_by_time(
            self,
            hotel_id: id,
            date_from: date,
            date_to: date
    ):
        check_date_correct(date_from, date_to)
        return await self.db.rooms.get_filtered_by_time(
                hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

    async def get_room(self, room_id: int, hotel_id: int):
        return await self.db.rooms.one_or_none1(id=room_id, hotel_id=hotel_id)


    async def create_room(
            self,
            hotel_id: int,
            data: RoomsAddRequest):
        try:
            await self.db.hotels.one_or_none(id=hotel_id)
        except ObjectNotFoundException as ex:
            raise HotelNotFoundException from ex
        _data = RoomsAdd(hotel_id=hotel_id, **data.model_dump())
        try:
            result = await self.db.rooms.add(_data)
        except ObjectAlreadyExistsException:
            raise HTTPException(status_code=409, detail="Комната уже существует")
        except ObjectNotFoundException:
            raise HotelNotFoundHTTPException

        rooms_facilities_data = [
            RoomFacilityAdd(rooms_id=result.id, facilities_id=f_id)
            for f_id in (data.facilities_ids or [])
        ]

        if rooms_facilities_data:  # Только если есть данные для добавления
            await self.db.rooms_facilities.add_bulk(rooms_facilities_data)

        await self.db.commit()