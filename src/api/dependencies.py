from typing import Annotated

from fastapi import Depends, Query, Request, HTTPException
from pydantic import BaseModel

from src.database import async_session
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    """Параметры пагинации"""

    # Тип int со значением по умолчанию 1 и ограничениями больше или равно 1
    page_number: Annotated[int, Query(default=1, ge=1)]
    # Тип int со значением по умолчанию None и ограничениями больше или равно 1 и меньше 30
    page_size: Annotated[int | None, Query(None, ge=1, lt=30)]


# Создаем зависимость
PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(
    # HTTP-запрос, поступивший от клиента.
    request: Request,
):
    """
    Функция для получения токена из куки
    :return: Токен
    """
    # Проверяем наличие токена в куках, если нет вернем None
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Требуется аутентификация")
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    """Функция для получения идентификатора текущего пользователя"""
    # Декодируем токен
    data = AuthService().decode_access_token(token)
    return data["user_id"]


# Создаем зависимость
UserIdDepends = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    """Функция-зависимость для получения сессии базы данных"""
    # Контекстный менеджер для работы с DBManager, который управляет соединением с базой данных.
    # 'async with' гарантирует, что сессия будет закрыта после выхода из блока кода.
    async with DBManager(session_factory=async_session) as db:
        # 'yield' передает объект сессии 'db' в FastAPI для дальнейшего использования в обработчиках.
        yield db


# Создаем зависимость
DBDep = Annotated[DBManager, Depends(get_db)]
