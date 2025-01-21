from datetime import date

from src.exception import check_date_correct, ObjectNotFoundException, HotelNotFoundException, \
    ObjectAlreadyExistsException, RoomsNotFoundException
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomsAdd, RoomsAddRequest, RoomsPatchRequest, RoomsPatch, Room
from src.services.base import BaseService
from src.services.hotels import HotelsService


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
            raise

        rooms_facilities_data = [
            RoomFacilityAdd(rooms_id=result.id, facilities_id=f_id)
            for f_id in (data.facilities_ids or [])
        ]

        if rooms_facilities_data:  # Только если есть данные для добавления
            await self.db.rooms_facilities.add_bulk(rooms_facilities_data)

        await self.db.commit()


    async def edit_room(self, hotel_id: int, room_id: int, room_data: RoomsAddRequest):
        await HotelsService(self.db).get_hotel(hotel_id)
        await self.get_room_with_check(room_id)
        _data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump())
        await self.db.rooms.edit(_data, id=room_id)
        await self.db.rooms_facilities.set_room_facilities(
            room_id, facilities=room_data.facilities_ids
        )
        await self.db.commit()




    async def partially_edit_room(self, room_id: int, hotel_id: int, room_data: RoomsPatchRequest):
        await HotelsService(self.db).get_hotel(hotel_id)
        await self.get_room_with_check(room_id)
        _room_data_dict = room_data.model_dump(exclude_unset=True)
        _data = RoomsPatch(hotel_id=hotel_id, **_room_data_dict)
        await self.db.rooms.partially_edit(
            _data, exclude_unset=True, id=room_id, hotel_id=hotel_id
        )
        if "facilities_ids" in _room_data_dict:
            await self.db.rooms_facilities.set_room_facilities(
                room_id, facilities=_room_data_dict["facilities_ids"]
            )
        await self.db.commit()

    async def delete_room(self, hotel_id: int, room_id: int):
        await HotelsService(self.db).get_hotel(hotel_id)
        await self.get_room_with_check(room_id)
        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)


    async def get_room_with_check(self, room_id: int) -> Room:
        try:
            return await self.db.rooms.one_or_none(id=room_id)
        except ObjectNotFoundException:
            raise RoomsNotFoundException
        