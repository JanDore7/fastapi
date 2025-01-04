import logging
from typing import Sequence

from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound
from pydantic import BaseModel
from src.database import engine
from src.exception import ObjectAlreadyExistsException
from src.exception import ObjectNotFoundException
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

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_schema(model)

    async def one_or_none(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            raise ObjectNotFoundException
        return self.mapper.map_to_schema(model)

    async def add(self, data: BaseModel) -> object:
        add_stmt = (
            insert(self.model)
            .values(**data.model_dump(exclude_unset=True))
            .returning(self.model)
        )
        # print(add_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        try:
            result = await self.session.execute(add_stmt)
            model = result.scalars().one()
            return self.mapper.map_to_schema(model)
        except IntegrityError as ex:
            logging.error(
                f"Не удалось добавить объект: {ex.orig.__cause__}, входные данные: {data}"
            )
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from ex
            elif isinstance(ex.orig.__cause__, ForeignKeyViolationError):
                logging.error(
                    f"Не удалось добавить объект: {ex.orig.__cause__}, входные данные: {data}"
                )
                raise ObjectNotFoundException from ex
            else:
                logging.error(f"Не известная ошибка: тип ошибки {ex.orig.__cause__}")
                raise ex

    async def add_bulk(self, data: Sequence[BaseModel]) -> None:
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
