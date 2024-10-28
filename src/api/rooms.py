from fastapi import APIRouter, Body, Query

from src.database import async_session
from src.schemas.rooms import RoomsAdd, RoomsPatch, RoomsPut
from src.repos.rooms import RoomsRepository
from src.api.dependencies import PaginationDep


router = APIRouter(prefix="/rooms", tags=["Комнаты"])


@router.get("/{room_id}", summary="Получение комнаты")
async def get_room(room_id: int):
    async with async_session() as session:
        return await RoomsRepository(session).one_or_none(id=room_id)


@router.get("", summary="Получение комнат")
async def get_rooms(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Название или описание отеля"),
    hotel_id: int | None = Query(None, description="ID отеля"),
):
    page_size = pagination.page_size or 3
    async with async_session() as session:
        return await RoomsRepository(session).get_all(
            hotel_id=hotel_id,
            title=title,
            limit=page_size,
            offset=page_size * (pagination.page_number - 1))



@router.post("", summary="Создание комнаты")
async def create_room(data: RoomsAdd = Body(
    openapi_examples={
        "1": {
            "summary": "Создание комнаты 1",
            "value": {
                "title": "Комната 1",
                "description": "Комната 1",
                "price": 1000,
                "quantity": 1,
                "hotel_id": 1
            }
        },
        "2": {
            "summary": "Создание комнаты 2",
            "value": {
                "title": "Комната 2",
                "description": "Комната 2",
                "price": 2000,
                "quantity": 2,
                "hotel_id": 1
            }

    }}
)):
    async with async_session() as session:
        result = await RoomsRepository(session).add(data)
        await session.commit()
        return {"status": "OK", "room": result }

@router.put("", summary="Редактирование комнаты")
async def edit_hotels(hotel_id: int, hotel_data: RoomsPut = Body(
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
    async with async_session() as session:
        await RoomsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch(
    "",
    summary="Редактирование данных о комнате",
    description="<h1>Тут можно редактировать данные о комнате</h1>",
)
async def partially_edit_hotels(hotel_id: int, hotel_data: RoomsPatch):
    async with async_session() as session:
        await RoomsRepository(session).partially_edit(
            hotel_data, exclude_unset=True, id=hotel_id
        )
        await session.commit()
    return {"status": "OK"}


@router.delete("", summary="Удаление комнаты")
async def delete_room(room_id: int):
    async with async_session() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
    return {"status": "OK"}