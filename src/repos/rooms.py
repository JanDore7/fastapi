from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from src.repos.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.repos.utils import rooms_ids_for_booking
from src.schemas.rooms import Room, RoomWithRelationship


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        result = await self.session.execute(query)
        return [RoomWithRelationship.model_validate(model) for model in result.unique().scalars().all()]


    async def one_or_none1(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
        )
        result = await self.session.execute(query)
        return RoomWithRelationship.model_validate(model)