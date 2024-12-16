from sqlalchemy.exc import NoResultFound

from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDepends
from src.schemas.users import UserRequestAdd, UserAdd, User
from src.services.auth import AuthService
from src.api.dependencies import DBDep

router = APIRouter(prefix="/auth", tags=["Аутентификация и Авторизация"])


@router.post("/register", summary="Регистрация")
async def register_user(
    # Принимаем pydantic-схему
    data: UserRequestAdd,
    # Используем зависимость см. src/api/dependencies.py
    db: DBDep,
):
    try:
        # Хеширование пароля
        hashed_password = AuthService().hash_password(data.password)
        # Создание пользователя на основе pydantic-схемы
        new_user = UserAdd(email=data.email, hashed_password=hashed_password)
        # Добавление в БД
        await db.users.add(new_user)
        # Сохранение в БД
        await db.commit()
    except:  # noqa
        raise HTTPException(status_code=400)
    return {"status": "OK"}


@router.post("/login", summary="Аутентификация")
async def login_user(
    # Принимаем pydantic-схему
    data: UserRequestAdd,
    # Инструмент настройки ответа
    response: Response,
    # Используем зависимость см. src/api/dependencies.py
    db: DBDep,
):

    try:
        # Получаем пользователя из БД по email
        user = await db.users.get_user_with_hashed_password(email=data.email)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User не найден")
    # Проверяем пароль пользователя
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный пароль")

    # Генерируем JWT-токен
    access_token = AuthService().create_access_token(data={"user_id": user.id})
    # Устанавливаем куки
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return {"access_token": access_token}


@router.get("/me", summary="Только для аутентифицированных")
async def get_me(
    # Используем зависимость см. src/api/dependencies.py
    user_id: UserIdDepends,
    # Используем зависимость см. src/api/dependencies.py
    db: DBDep,
):
    """Если пользователь аутентифицирован, то возвращаем его данные"""
    # Ищем пользователя в БД
    user = await db.users.one_or_none(id=user_id)
    user = User(**user.model_dump())
    return user


@router.post("/logout", summary="Выход")
async def logout(
    # Инструмент настройки ответа
    response: Response,
):
    """Удаление токена"""
    # Удаляем куку по ключу
    response.delete_cookie(key="access_token", httponly=True)
    return {"status": "OK"}
