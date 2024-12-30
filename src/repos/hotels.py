from datetime import date
from typing import List

from src.exception import check_date_correct
from src.models.rooms import RoomsOrm
from src.repos.base import BaseRepository
from src.database import engine
from src.models.hotels import HotelsOrm
from sqlalchemy import select, insert

from src.repos.mapper.base import DataMapper
from src.repos.mapper.mappers import HotelDataMapper
from src.repos.utils import rooms_ids_for_booking


class HotelRepository(BaseRepository):
    model = HotelsOrm
    mapper: DataMapper = HotelDataMapper

    async def add(self, data: List[mapper.schema]) -> object:
        models_orm = []
        for model in data:
            add_stmt = (
                insert(self.model).values(**model.model_dump()).returning(self.model)
            )
            print(add_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
            result = await self.session.execute(add_stmt)
            models_orm.append(result.scalar())
        return [self.mapper.map_to_schema(model) for model in models_orm]

    async def get_filtered_by_time(
        self, date_from: date, date_to: date, location, title, limit, offset
    ) -> List[mapper.schema]:
        check_date_correct(date_from, date_to)
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        query = select(HotelsOrm).filter(HotelsOrm.id.in_(hotels_ids_to_get))
        if title:
            query = query.filter(HotelsOrm.title.ilike(f"%{title}%"))
        if location:
            query = query.filter(HotelsOrm.location.op("~")(rf"(?i)\y{location}\y"))
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [self.mapper.map_to_schema(hotel) for hotel in result.scalars().all()]
