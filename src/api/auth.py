from fastapi import APIRouter
from passlib.context import CryptContext

from src.repos.usres import UserRepository
from src.database import async_session
from src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Аутентификация и Авторизация"])


pwd_context = CryptContext(schemes=["bcrypt"])


@router.post("/register", summary="Регистрация")
async def register_user(data: UserRequestAdd):
    hashed_password = pwd_context.hash(data.password)
    new_user = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session() as session:
        result = await UserRepository(session).add(new_user)
        await session.commit()
        return {"status": "OK"}
