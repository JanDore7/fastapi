from datetime import datetime, timezone, timedelta
from sqlalchemy.exc import NoResultFound

from fastapi import APIRouter, HTTPException, Response
from passlib.context import CryptContext
import jwt

from src.repos.usres import UserRepository
from src.database import async_session
from src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Аутентификация и Авторизация"])


pwd_context = CryptContext(schemes=["bcrypt"])
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode |= {"exp": expire} # аналогично to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/register", summary="Регистрация")
async def register_user(data: UserRequestAdd):
    hashed_password = pwd_context.hash(data.password)
    new_user = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session() as session:
        result = await UserRepository(session).add(new_user)
        await session.commit()
        return {"status": "OK"}


@router.post("/login", summary="Аутентификация")
async def login_user(data: UserRequestAdd,
                     response: Response):
    async with async_session() as session:
        try:
            user = await UserRepository(session).get_user_with_hashed_password(email=data.email)
        except NoResultFound:
            raise HTTPException(status_code=404, detail="User не найден")

        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неверный пароль")

        access_token = create_access_token(data={"sub": user.id})
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return {"access_token": access_token}

