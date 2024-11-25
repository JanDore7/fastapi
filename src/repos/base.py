from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel
from src.database import engine
from src.repos.mapper.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.mapper.map_to_schema(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def one_or_none(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_schema(model)

    async def add(self, data: BaseModel) -> object:
        add_stmt = (
            insert(self.model)
            .values(**data.model_dump(exclude_unset=True))
            .returning(self.model)
        )
        print(add_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(add_stmt)
        model = result.scalars().one()
        return self.mapper.map_to_schema(model)

    async def add_bulk(self, data: list[BaseModel]) -> None:
        add_stmt = (
            insert(self.model)
            .values([item.model_dump(exclude_unset=True) for item in data])
            .returning(self.model)
        )  # insert(self.model).values(**item.model_dump(exclude_unset=True)).returning(self.model)
        print(add_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await self.session.execute(add_stmt)

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
