from datetime import date

from src.schemas.bookings import BookingAdd


async def test_CURD(db):
    user_id = (await db.users.get_all())[
        0
    ].id  # await db.users.get_all() отдельная операция и не может быть вызвана по индексу
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(2024, 11, 1),
        date_to=date(2024, 12, 1),
        price=199,
    )
    new_booking = await db.bookings.add(booking_data)

    booking = await db.bookings.one_or_none(id=new_booking.id)

    assert booking
    assert booking.id == new_booking.id
    assert booking.room_id == new_booking.room_id
    assert booking.user_id == new_booking.user_id

    booking_edit_data = BookingAdd(
        user_id=user_id,
        price=200,
        room_id=room_id,
        date_from=date(year=2024, month=9, day=15),
        date_to=date(year=2024, month=9, day=23),
    )

    await db.bookings.edit(booking_edit_data, id=new_booking.id)
    edited_booking = await db.bookings.one_or_none(id=new_booking.id)

    assert edited_booking
    assert edited_booking.id == new_booking.id
    assert edited_booking.price == booking_edit_data.price
    assert edited_booking.date_from == booking_edit_data.date_from
    assert edited_booking.date_to == booking_edit_data.date_to

    await db.bookings.delete(id=new_booking.id)

    booking_data_delete = await db.bookings.one_or_none(id=new_booking.id)
    assert not booking_data_delete

    await db.commit()