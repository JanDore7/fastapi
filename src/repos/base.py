from typing import List
from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel
from src.database import engine


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]

    async def one_or_none(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model)

    async def add(self, data: BaseModel) -> object:

        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        print(add_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(add_stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model)

    async def edit(self, data: BaseModel, **filter_by):
        update_stmt = (
            update(self.model).filter_by(**filter_by).values(**data.model_dump())
        )
        await self.session.execute(update_stmt)

    async def delete(self, **filter_by):
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)

    async def partially_edit(
        self, data: BaseModel, exclude_unset: bool = True, **filter_by
    ):
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(update_stmt)
