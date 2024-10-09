from sqlalchemy import select, insert
from src.api.dependencies import BaseModelPaydantic
from src.database import engine


class BaseRepository:
    model = None
    def __init__(self, session):
        self.session = session

    async def get_all(self,*args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def one_or_none(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, hotel_data: BaseModelPaydantic):
        hotels_orm = []
        for hotel in hotel_data:
            add_hotel_stmt = insert(self.model).values(**hotel.model_dump()).returning(self.model)
            print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
            result = await self.session.execute(add_hotel_stmt)
            hotels_orm.append(result.scalar())
        return hotels_orm

