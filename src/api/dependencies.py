from typing import Annotated

from fastapi import Depends, Query, Request, HTTPException
from pydantic import BaseModel

from src.database import async_session
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page_number: Annotated[int, Query(default=1, ge=1)]
    page_size: Annotated[int | None, Query(None, ge=1, lt=30)]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request):
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Требуется аутентификация")
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_access_token(token)
    return data["user_id"]


UserIdDepends = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
