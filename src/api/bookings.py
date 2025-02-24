from fastapi import APIRouter
from fastapi import HTTPException

from src.api.dependencies import DBDep
from src.exception import AllRoomsByBookedException
from src.exception import ObjectNotFoundException
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.api.dependencies import UserIdDepends
from src.schemas.rooms import Room
from fastapi_cache.decorator import cache

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("", summary="Получение бронирования")
@cache(expire=50)
async def get_all_booking(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me", summary="Мои бронирования")
@cache(expire=100)
async def get_all_booking_me(user_id: UserIdDepends, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("", summary="Создание бронирования")
async def add_booking(
    db: DBDep,
    user_id: UserIdDepends,
    booking_data: BookingAddRequest,
):
    try:
        room: Room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail=f"Номер не найден ")
    hotel = await db.hotels.get_one(id=room.hotel_id)
    room_price = room.price
    _booking_data = BookingAdd(
        user_id=user_id, price=room_price, **booking_data.model_dump()
    )
    try:
        booking = await db.bookings.add_bookings(_booking_data, hotel_id=hotel.id)
    except AllRoomsByBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    await db.commit()
    return {"status": "OK", "data": booking}
