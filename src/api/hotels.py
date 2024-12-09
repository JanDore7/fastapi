from datetime import date
from typing import List
from fastapi_cache.decorator import cache
from fastapi import Query, APIRouter, Body

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelPATCH, HotelAdd


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/{hotel_id}", summary="Получение отеля")
@cache(expire=100)
async def get_hotel(hotel_id: int, db: DBDep):
    print("Иду в бд")
    return await db.hotels.one_or_none(id=hotel_id)


@router.get("", summary="Получение списка отелей")
@cache(expire=100)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название или описание отеля"),
    location: str | None = Query(None, description="Адрес отеля"),
    date_from: date | None = Query(
        None, description="Дата заезда", exampls="2024-11-01"
    ),
    date_to: date | None = Query(None, description="Дата выезда", example="2024-11-07"),
):

    page_size = pagination.page_size or 3
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=page_size,
        offset=page_size * (pagination.page_number - 1),
    )


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
    result = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": result}


@router.put("", summary="Редактирование отеля")
async def edit_hotels(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await db.hotels.edit(hotel_data, id=hotel_id)
    return {"status": "OK"}


@router.delete("", summary="Удаление отеля")
async def delete_hotels(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    return {"status": "OK"}


@router.patch(
    "",
    summary="Редактирование отеля",
    description="<h1>Тут можно редактировать отель</h1>",
)
async def partially_edit_hotels(hotel_id: int, hotel_data: HotelPATCH, db: DBDep):
    await db.hotels.partially_edit(hotel_data, exclude_unset=True, id=hotel_id)
    return {"status": "OK"}
