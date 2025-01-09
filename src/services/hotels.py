from datetime import date

from src.exception import check_date_correct
from src.schemas.hotels import HotelAdd, HotelPATCH
from src.services.base import BaseService


class HotelsService(BaseService):

    async def get_filtered_by_time(
            self,
            pagination,
            date_from: date,
            date_to: date,
            location: str | None = None,
            title: str | None = None,
    ):
        check_date_correct(date_from, date_to)
        page_size = pagination.page_size or 3
        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=page_size,
            offset=page_size * (pagination.page_number - 1),
        )


    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.one_or_none(id=hotel_id)

    async def add_hotels(self, hotel_data: list[HotelAdd]):
        result = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return result

    async def edit_hotel(self, hotel_id: int, hotel_data: HotelAdd):
        await self.db.hotels.edit(hotel_data, id=hotel_id)
        await self.db.commit()

    async def edit_hotel_partially(self, hotel_id: int, hotel_data: HotelPATCH, exclude_unset: bool = False):
        await self.db.hotels.partially_edit(hotel_data, exclude_unset=exclude_unset, id=hotel_id)
        await self.db.commit()


    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()