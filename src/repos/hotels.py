from typing import List

from src.repos.base import BaseRepository
from src.database import engine
from src.models.hotels import HotelsOrm
from sqlalchemy import select, insert
from src.schemas.hotels import Hotel


class HotelRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(self, location, title, limit, offset) -> list[Hotel]:
        query = select(HotelsOrm)
        if title:
            query = query.filter(HotelsOrm.title.ilike(f"%{title}%"))
        if location:
            query = query.filter(HotelsOrm.location.op("~")(rf"(?i)\y{location}\y"))
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]

    async def add(self, data: List[Hotel]) -> object:
        models_orm = []
        for model in data:
            add_stmt = (
                insert(self.model).values(**model.model_dump()).returning(self.model)
            )
            print(add_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
            result = await self.session.execute(add_stmt)
            models_orm.append(result.scalar())
        return [self.schema.model_validate(model) for model in models_orm]
