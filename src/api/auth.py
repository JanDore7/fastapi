from sqlalchemy.exc import NoResultFound

from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDepends
from src.repos.usres import UserRepository
from src.database import async_session
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService
from src.api.dependencies import DBDep

router = APIRouter(prefix="/auth", tags=["Аутентификация и Авторизация"])


@router.post("/register", summary="Регистрация")
async def register_user(data: UserRequestAdd, db: DBDep):
    hashed_password = AuthService().hash_password(data.password)
    new_user = UserAdd(email=data.email, hashed_password=hashed_password)
    await db.users.add(new_user)
    await db.commit()
    return {"status": "OK"}


@router.post("/login", summary="Аутентификация")
async def login_user(data: UserRequestAdd, response: Response, db: DBDep):

    try:
        user = await db.users.get_user_with_hashed_password(email=data.email)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User не найден")

    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный пароль")

    access_token = AuthService().create_access_token(data={"user_id": user.id})
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return {"access_token": access_token}


@router.get("/me", summary="Только для аутентифицированных")
async def get_me(user_id: UserIdDepends, db: DBDep):
    return await db.users.one_or_none(id=user_id)


@router.post("/logout", summary="Выход")
async def logout(response: Response):
    response.delete_cookie(key="access_token", httponly=True)
    return {"status": "OK"}
