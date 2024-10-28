from fastapi import APIRouter, Body, Query

from src.database import async_session
from src.schemas.rooms import RoomsAdd, RoomsPatch, RoomsAddRequest, RoomsPatchRequest
from src.repos.rooms import RoomsRepository



router = APIRouter(prefix="/hotels", tags=["Комнаты"])


@router.get("/{hotel_id}/rooms", summary="Получение всех номеров")
async def get_rooms(hotel_id: int):
    async with async_session() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение комнаты")
async def get_room(hotel_id: int, room_id: int):
    async with async_session() as session:
        return await RoomsRepository(session).one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms", summary="Создание комнаты")
async def create_room(hotel_id: int, data: RoomsAddRequest ):
    _data = RoomsAdd(hotel_id=hotel_id, **data.model_dump())
    async with async_session() as session:
        result = await RoomsRepository(session).add(_data)
        await session.commit()
    return {"status": "OK", "room": result }


@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменение комнаты")
async def edit_room(hotel_id: int,room_id: int, room_data: RoomsAddRequest = Body(
    openapi_examples={
        "1": {
            "summary": "Редактирование комнаты ",
            "value": {
                "title": "Комната new - 1",
                "description": "Комната new - 1",
                "price": 11500,
                "quantity": 1,
            }
        },
        "2": {
            "summary": "Редактирование комнаты 2",
            "value": {
                "title": "Комната new - 2",
                "description": "Комната new - 2",
                "price": 2000,
                "quantity": 2,
            }
        }
    }
)):
    _data = RoomsAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session() as session:
        await RoomsRepository(session).edit(_data, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Редактирование комнаты")
async def partially_edit_room(
        room_id: int,
        hotel_id: int,
        room_data: RoomsPatchRequest
):
    _data = RoomsPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session() as session:
        await RoomsRepository(session).partially_edit(
            _data,
            exclude_unset=True,
            id=room_id,
            hotel_id=hotel_id
        )
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление комнаты")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}