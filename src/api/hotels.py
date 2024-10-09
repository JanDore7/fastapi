from typing import List

from fastapi import Query, APIRouter, Body
from sqlalchemy import select, insert
from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel
from src.database import async_session, engine
from src.models.hotels import HotelsOrm

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получение списка отелей")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название или описание отеля"),
        location: str | None = Query(None, description="Адрес отеля"),
):
    page_size = pagination.page_size or 3

    async with (async_session() as session):
        query = select(HotelsOrm)
        if title:
            query = query.where(HotelsOrm.title.ilike(f"%{title}%"))
        if location:
            query = query.where(HotelsOrm.location.op("~")(rf"\y{location.capitalize()}\y"))
        query = (
            query
            .limit(page_size)
            .offset((pagination.page_nuber - 1) * page_size)
        )
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await session.execute(query)
        return result.scalars().all()


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
    hotels_orm = []
    async with async_session() as session:
        for hotel in hotel_data:
            add_hotel_stmt = insert(HotelsOrm).values(**hotel.model_dump()).returning(HotelsOrm.title)
            print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
            await session.execute(add_hotel_stmt)
            hotels_orm.append(await session.scalar(add_hotel_stmt))
            await session.commit()

    return {"status": "ok", "hotels": hotels_orm}

#
# @router.put("/{hotel_id}")
# def edit_hotel(hotel_id: int, hotel_data: Hotel):
#     global hotels
#     hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
#     hotel["title"] = hotel_data.title
#     hotel["name"] = hotel_data.name
#     return {"status": "OK"}
#
#
# @router.patch(
#     "/{hotel_id}",
#     summary="Частичное обновление данных об отеле",
#     description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
# )
# def partially_edit_hotel(
#         hotel_id: int,
#         hotel_data: HotelPATCH,
# ):
#     global hotels
#     hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
#     if hotel_data.title:
#         hotel["title"] = hotel_data.title
#     if hotel_data.name:
#         hotel["name"] = hotel_data.name
#     return {"status": "OK"}
#
#
# @router.delete("/{hotel_id}")
# def delete_hotel(hotel_id: int):
#     global hotels
#     hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
#     return {"status": "OK"}


