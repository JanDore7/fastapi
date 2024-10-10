from typing import List
from pydantic import constr
from fastapi import Query, APIRouter, Body

from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel
from src.database import async_session, engine

from src.repos.hotels import HotelRepository

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получение списка отелей")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название или описание отеля"),
        location: str | None = Query(None, description="Адрес отеля"),
):
    page_size = pagination.page_size or 3
    async with (async_session() as session):
        return await HotelRepository(session).get_all(
            location=location,
            title=title,
            limit=page_size,
            offset=page_size * (pagination.page_nuber - 1))


@router.post("", summary="Создание отеля")
async def create_hotels(hotel_data: List[Hotel] = Body(openapi_examples={
    "1": {
        "summary": "Сочи",
        "value": [{
            "title": "Отель Сочи 5 звезд у моря",
            "location": "Сочи,ул.Красная, 5",
        }]
    },
    "2": {
        "summary": "Дубай",
        "value": [{
            "title": "Отель Дубай У фонтана",
            "location": "Дубай, ул.Уфанский, 10",
        }]
    },
    "3": {
        "summary": "Пакетная загрузка",
        "value": [{
            "title": "Отель Мальдивы",
            "location": "Мальдивы, ул.Нагорная , 27",
        }, {
            "title": "Отель Геленджик",
            "location": "Геленджик, ул.Морская, 90",
        }]
    }
})
):
    async with async_session() as session:
        result = await HotelRepository(session).add(hotel_data)
        await session.commit()
        return {"status": "OK", "data": result}


@router.put("", summary="Редактирование отеля")
async def edit_hotels(hotel_data: List[Hotel],
                      title: constr(max_length=100) | None = Query(None, description="Название или описание отеля"),
                      location: constr(max_length=500) | None = Query(None, description="Адрес отеля"),
                      ):
    async with (async_session() as session):
        result = await HotelRepository(session).edit(hotel_data, title=title, location=location)
        await session.commit()
        return result


@router.delete("", summary="Удаление отеля")
async def delete_hotels(
        title: constr(max_length=100) | None = Query(None, description="Название или описание отеля"),
        location: constr(max_length=500) | None = Query(None, description="Адрес отеля")
):
    async with (async_session() as session):
        result = await HotelRepository(session).delete(title=title, location=location)
        await session.commit()
        return result
