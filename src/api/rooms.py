from datetime import date


from fastapi import APIRouter, Body, Query
from fastapi import HTTPException

from src.exception import HotelNotFoundHTTPException
from src.exception import ObjectAlreadyExistsException
from src.exception import ObjectNotFoundException
from src.exception import RoomsNotFoundHTTPException
from src.schemas.rooms import RoomsAddRequest, RoomsPatchRequest
from src.api.dependencies import DBDep
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Комнаты"])


@router.get("/{hotel_id}/rooms", summary="Получение всех номеров")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2024-11-01"),
    date_to: date = Query(example="2024-11-07"),
):
    return RoomService(db).get_filtered_by_time(hotel_id, date_from, date_to)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение комнаты")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        return await RoomService(db).get_room(hotel_id, room_id)
    except ObjectNotFoundException:
        raise RoomsNotFoundHTTPException


@router.post("/{hotel_id}/rooms", summary="Создание комнаты")
async def create_room(hotel_id: int, data: RoomsAddRequest, db: DBDep):
    try:
        room = await RoomService(db).create_room(hotel_id, data)
    except ObjectAlreadyExistsException:
        raise HTTPException(status_code=409, detail="Объект уже существует")
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK", "room": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменение комнаты")
async def edit_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
    room_data: RoomsAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Редактирование комнаты ",
                "value": {
                    "title": "Комната new - 1",
                    "description": "Комната new - 1",
                    "price": 11500,
                    "quantity": 1,
                    "facilities_ids": [1, 2],
                },
            },
            "2": {
                "summary": "Редактирование комнаты 2",
                "value": {
                    "title": "Комната new - 2",
                    "description": "Комната new - 2",
                    "price": 2000,
                    "quantity": 2,
                    "facilities_ids": [],
                },
            },
        }
    ),
):
    try:
        await RoomService(db).edit_room(hotel_id, room_id, room_data)
    except ObjectNotFoundException:
        raise RoomsNotFoundHTTPException

    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Редактирование комнаты")
async def partially_edit_room(
    room_id: int, hotel_id: int, room_data: RoomsPatchRequest, db: DBDep
):
    try:
        await RoomService(db).partially_edit_room(room_id, hotel_id, room_data)
    except ObjectNotFoundException:
        raise RoomsNotFoundHTTPException

    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление комнаты")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        await RoomService(db).delete_room(hotel_id, room_id)
    except ObjectNotFoundException:
        raise RoomsNotFoundHTTPException
    return {"status": "OK"}
