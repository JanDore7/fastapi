from src.schemas.hotels import HotelAdd


async def test_add_hotel(db):
    hotel_data: list[HotelAdd] = [HotelAdd(title="Hotel 5 stars", location="Сочи")]
    new_hotel_data = await db.hotels.add(hotel_data)
    await db.commit()
