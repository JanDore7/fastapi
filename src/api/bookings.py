from fastapi import APIRouter, Request
from src.api.dependencies import DBDep
from src.database import engine
from src.schemas.bookings import  BookingAddRequest, BookingAdd
from src.api.dependencies import UserIdDepends


router = APIRouter(prefix="/bookings", tags=["Бронирования"])


# noinspection PyTypeChecker
@router.post('/bookings', summary="Создание бронирования")
async def add_booking(
        db: DBDep,
        user_id: UserIdDepends,
        booking_data: BookingAddRequest,
):
    room = await db.rooms.one_or_none(id=booking_data.room_id)
    room_price = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump()
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}


@router.get("/bookings", summary="Получение бронирования")
async def get_all_booking(db: DBDep):
    bookings = await db.bookings.get_all()
    return {"bookings": bookings}


@router.get("/bookings/me", summary="Мои бронирования")
async def get_all_booking_me(user_id: UserIdDepends, db: DBDep):
    bookings = await db.bookings.get_filtered(user_id=user_id)
    return {"bookings": bookings}