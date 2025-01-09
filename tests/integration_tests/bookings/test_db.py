from datetime import date

from src.schemas.bookings import BookingAdd

#
# async def test_booking_crud(db):
#     user_id = (await db.users.get_all())[0].id
#     room_id = (await db.rooms.get_all())[0].id
#     booking_data = BookingAdd(
#         user_id=user_id,
#         room_id=room_id,
#         date_from=date(year=2024, month=8, day=10),
#         date_to=date(year=2024, month=8, day=20),
#         price=100,
#     )
#     new_booking = await db.bookings.add(booking_data)
#
#     # получить эту бронь и убедиться что она есть
#     booking = await db.bookings.one_or_none(id=new_booking.id)
#     assert booking
#     assert booking.id == new_booking.id
#     assert booking.room_id == new_booking.room_id
#     assert booking.user_id == new_booking.user_id
#     # а еще можно вот так разом сравнить все параметры
#     assert booking.model_dump(exclude={"id"}) == booking_data.model_dump()
#
#     # обновить бронь
#     updated_date = date(year=2024, month=8, day=25)
#     update_booking_data = BookingAdd(
#         user_id=user_id,
#         room_id=room_id,
#         date_from=date(year=2024, month=8, day=10),
#         date_to=updated_date,
#         price=100,
#     )
#     await db.bookings.edit(update_booking_data, id=new_booking.id)
#     updated_booking = await db.bookings.one_or_none(id=new_booking.id)
#     assert updated_booking
#     assert updated_booking.id == new_booking.id
#     assert updated_booking.date_to == updated_date
#
#     # удалить бронь
#     await db.bookings.delete(id=new_booking.id)
#     booking = await db.bookings.one_or_none(id=new_booking.id)
#     assert not booking


import asyncio
from datetime import date
from src.schemas.bookings import BookingAdd
from src.exception import ObjectNotFoundException


async def test_booking_crud(db):
    # Получаем данные пользователя и комнаты
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id

    # Данные для новой брони
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2024, month=8, day=10),
        date_to=date(year=2024, month=8, day=20),
        price=100,
    )

    # Добавляем новую бронь
    new_booking = await db.bookings.add(booking_data)

    # Получаем эту бронь и проверяем, что она добавилась
    booking = await db.bookings.one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id
    assert booking.room_id == new_booking.room_id
    assert booking.user_id == new_booking.user_id
    assert booking.model_dump(exclude={"id"}) == booking_data.model_dump()

    # Обновляем дату брони
    updated_date = date(year=2024, month=8, day=25)
    update_booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2024, month=8, day=10),
        date_to=updated_date,
        price=100,
    )

    # Обновляем бронь в базе
    await db.bookings.edit(update_booking_data, id=new_booking.id)
    updated_booking = await db.bookings.one_or_none(id=new_booking.id)
    assert updated_booking
    assert updated_booking.id == new_booking.id
    assert updated_booking.date_to == updated_date

    # Удаляем бронь
    await db.bookings.delete(id=new_booking.id)

    # Даем базе немного времени для синхронизации
    await asyncio.sleep(0.1)  # Это может быть полезно, если база данных еще не обновила состояние

    # Проверяем, что бронь удалена
    try:
        booking_after_delete = await db.bookings.one_or_none(id=new_booking.id)
        assert booking_after_delete is None
    except ObjectNotFoundException:
        pass  # Если запись не найдена, это ожидаемое поведение
