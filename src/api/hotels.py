from datetime import date
from typing import List

from fastapi_cache.decorator import cache
from fastapi import Query, APIRouter, Body

from src.api.dependencies import PaginationDep, DBDep

from src.exception import HotelNotFoundHTTPException
from src.exception import ObjectNotFoundException
from src.schemas.hotels import HotelPATCH, HotelAdd
from src.services.hotels import HotelsService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/{hotel_id}", summary="Получение отеля")
@cache(expire=100)
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelsService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.get("", summary="Получение списка отелей")
@cache(expire=100)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название или описание отеля"),
    location: str | None = Query(None, description="Адрес отеля", example=["Сочи"]),
    date_from: date | None = Query(None, description="Дата заезда", example="2024-11-01"),
    date_to: date | None = Query(None, description="Дата выезда", example="2024-11-07"),
):
    data = await HotelsService(db).get_filtered_by_time(
        pagination, date_from, date_to, location, title
    )
    return {"status": "OK", "data": data}


@router.post("", summary="Создание отеля")
async def create_hotels(
    db: DBDep,
    hotel_data: List[HotelAdd] = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": [
                    {
                        "title": "Отель Сочи 5 звезд у моря",
                        "location": "Сочи,ул.Красная, 5",
                    }
                ],
            },
            "2": {
                "summary": "Дубай",
                "value": [
                    {
                        "title": "Отель Дубай У фонтана",
                        "location": "Дубай, ул.Уфанский, 10",
                    }
                ],
            },
            "3": {
                "summary": "Пакетная загрузка",
                "value": [
                    {
                        "title": "Отель Мальдивы",
                        "location": "Мальдивы, ул.Нагорная , 27",
                    },
                    {
                        "title": "Отель Геленджик",
                        "location": "Геленджик, ул.Морская, 90",
                    },
                ],
            },
        }
    ),
):
    result = HotelsService(db).add_hotels(hotel_data)
    return {"status": "OK", "data": result}


@router.put("", summary="Редактирование отеля")
async def edit_hotels(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await HotelsService(db).edit_hotel(hotel_id, hotel_data)
    return {"status": "OK"}


@router.delete("", summary="Удаление отеля")
async def delete_hotels(hotel_id: int, db: DBDep):
    await HotelsService(db).delete_hotel(hotel_id)
    return {"status": "OK"}


@router.patch(
    "",
    summary="Редактирование отеля",
    description="<h1>Тут можно редактировать отель</h1>",
)
async def partially_edit_hotels(hotel_id: int, hotel_data: HotelPATCH, db: DBDep):
    await HotelsService(db).edit_hotel_partially(hotel_id, hotel_data, exclude_unset=True)
    return {"status": "OK"}
