from repos.base import BaseRepository
from src.models.hotels import HotelsOrm
from sqlalchemy import select
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
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]

