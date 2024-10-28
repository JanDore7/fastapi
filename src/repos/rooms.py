from sqlalchemy import select

from src.database import engine
from src.repos.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Rooms


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Rooms


    async def get_all(self, hotel_id, title, limit, offset) -> list[Rooms]:
        query = select(RoomsOrm)
        if title:
            query = query.filter(RoomsOrm.title.ilike(f"%{title}%"))
        if hotel_id:
            query = query.filter(RoomsOrm.hotel_id == hotel_id)
        query = query.limit(limit).offset(offset)
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]