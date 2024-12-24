from fastapi import APIRouter
from fastapi import HTTPException

from src.api.dependencies import DBDep
from src.exception import ObjectNotFoundException
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.api.dependencies import UserIdDepends
from src.schemas.rooms import Room

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("", summary="Получение бронирования")
async def get_all_booking(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me", summary="Мои бронирования")
async def get_all_booking_me(user_id: UserIdDepends, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("", summary="Создание бронирования")
async def add_booking(
    db: DBDep,
    user_id: UserIdDepends,
    booking_data: BookingAddRequest,
):
    try:
        room: Room | None = await db.rooms.one_or_none(id=booking_data.room_id)
    except ObjectNotFoundException as ex:
        raise HTTPException(status_code=404, detail="Номер не найден")
    hotel = await db.hotels.get_one(id=room.hotel_id)
    room_price = room.price
    _booking_data = BookingAdd(
        user_id=user_id, price=room_price, **booking_data.model_dump()
    )
    booking = await db.bookings.add_bookings(_booking_data, hotel_id=hotel.id)
    await db.commit()
    return {"status": "OK", "data": booking}
