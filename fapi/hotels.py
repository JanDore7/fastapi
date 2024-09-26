from fastapi import  Query, APIRouter, Path, Body
from shemas.hotels import Hotel, HotelPATCH


hotels = [
    {"id": 1, "title": "Сочи", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]

router = APIRouter(prefix='/hotels', tags=["Отели"])


@router.get("", description="Получить список отелей или отель по названию", name="Список отелей")
async def get_hotels(
        hotel_id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
        page: int | None = Query(1, description="Номер страницы"),
        per_page: int | None = Query(3, description="Количество отелей на странице"),
):
    if hotel_id or title:
        hotels_ = []
        for hotel in hotels:
            if hotel_id and hotel["id"] != hotel_id:
                continue
            if title and hotel["title"] != title:
                continue
            hotels_.append(hotel)
        return hotels_

    if page != 1:
        page -= 1
        start = page * per_page
        end = start + per_page
        print(hotels[start:end])
        return hotels[start:end]
    if page == 1:
        print(hotels[0:per_page])
        return hotels[0:per_page]


@router.delete("/{hotel_name}", description="Удалить отель по названию", name="Удалить отель")
async def delete_hotel(hotel_name: str = Path(...,description="Название отеля")):
    global hotels
    print(hotel_name)
    hotels = [hotel for hotel in hotels if hotel["name"] != hotel_name]
    return {"status": "ok"}


@router.post("", description="Создать отель", name="Создать отель")
async def create_hotel(hotel: Hotel):

    global hotels
    hotels.append(
        {
            "id": len(hotels) + 1,
            "title": hotel.title,
            "name": hotel.name
        }
    )
    return {"status": "ok"}



@router.put("/{hotel_id}", description="Обновить отель", name="Обновить отель")
async def update_hotel(hotel: Hotel = Body(openapi_examples={
    "Пример №1": {"summary" : "Сочи", "value":
        {"title": "Сочи у моря", "name": "Sochi u morja"}},
    "Пример №2": {"summary" : "Дубай", "value":
        {"title": "Дубай у фонтана", "name": "Dubai u fonana"}}
}),
                       hotel_id: int = Path(..., description="Идентификатор гостиницы")):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    hotels.append(
        {
            "id": hotel_id,
            "title": hotel.title,
            "name": hotel.name
        }
    )
    return {"status": "ok", "hotel": hotel}


@router.patch("/{hotel_id}", description="Обновить часть информации об отеле", name="Редактировать отель")
async def patch_hotel(
        data_hotel: HotelPATCH,
        hotel_id: int = Path(..., description="Идентификатор гостиницы")
        ):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if data_hotel.name is not None:
                hotel["name"] = data_hotel.name
            if data_hotel.title is not None:
                hotel["title"] = data_hotel.title
            return {"hotels": hotels}  # return all hotels



