from typing import List
from fastapi import HTTPException
from sqlalchemy import select, insert
from pydantic import BaseModel
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

    async def add(self, hotel_data: List[BaseModel]):
        hotels_orm = []
        for hotel in hotel_data:
            add_stmt = insert(self.model).values(**hotel.model_dump()).returning(self.model)
            print(add_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
            result = await self.session.execute(add_stmt)
            hotels_orm.append(result.scalar())
        return hotels_orm

    async def edit(self, hotel_data: BaseModelPydantic, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        result = result.scalars().all()

        if len(result) > 1:
            raise HTTPException(status_code=400, detail="Найдено несколько отелей.")
        elif len(result) == 0:
            raise HTTPException(status_code=404, detail="Отель не найден.")

        hotel = result[0]

        for hotel_update in hotel_data:
            data_dict = hotel_update.model_dump()
            for key, value in data_dict.items():
                setattr(hotel, key, value)
        self.session.add(hotel)
        return {"hotel": hotel}

    async def delete(self, **filter_by):
        filters = {key: value for key, value in filter_by.items() if value}
        query = select(self.model).filter_by(**filters)

        result = await self.session.execute(query)
        result = result.scalars().all()

        if len(result) > 1:
            raise HTTPException(status_code=400, detail="Найдено несколько отелей.")
        elif len(result) == 0:
            raise HTTPException(status_code=404, detail="Отель не найден.")

        hotel = result[0]
        print(hotel)
        await self.session.delete(hotel)
        return {"hotel": hotel}
