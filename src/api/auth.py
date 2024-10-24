from sqlalchemy.exc import NoResultFound

from fastapi import APIRouter, HTTPException, Response, Request

from src.repos.usres import UserRepository
from src.database import async_session
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Аутентификация и Авторизация"])


@router.post("/register", summary="Регистрация")
async def register_user(data: UserRequestAdd):
    hashed_password = AuthService().hash_password(data.password)
    new_user = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session() as session:
        result = await UserRepository(session).add(new_user)
        await session.commit()
        return {"status": "OK"}


@router.post("/login", summary="Аутентификация")
async def login_user(data: UserRequestAdd, response: Response):
    async with async_session() as session:
        try:
            user = await UserRepository(session).get_user_with_hashed_password(
                email=data.email
            )
        except NoResultFound:
            raise HTTPException(status_code=404, detail="User не найден")

        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неверный пароль")

        access_token = AuthService().create_access_token(data={"sub": user.id})
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return {"access_token": access_token}


@router.get("/only_auth", summary="Только для аутентифицированных")
async def only_auth(request: Request):
    access_token = request.cookies.get()