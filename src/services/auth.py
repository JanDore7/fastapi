from passlib.context import CryptContext
import jwt
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException
from src.config import settings


class AuthService:
    # Создаем экземпляр класса CryptContext с алгоритмом bcrypt и автоматической проверкой на устаревание хеширования
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        """Создание JWT-токена доступа"""
        # Создаем копию данных словаря data
        to_encode = data.copy()
        # Устанавливаем время истечения токена
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        # Отмечаем время истечения токена путем обновления словаря
        to_encode |= {"exp": expire}  # аналогично to_encode.update({"exp": expire})
        # Кодируем словарь в JWT используя секретный ключ и указанный алгоритм
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        """Хеширование пароля"""
        # Хешируем пароль при помощи CryptContext обратившись к методу hash
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        """Проверка пароля"""
        # Проверяем пароль при помощи CryptContext обратившись к методу verify
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_access_token(self, token: str) -> dict:
        """Декодирование JWT-токена доступа"""
        try:
            # Декодируем JWT-токен указав секретный ключ и алгоритм
            return jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
        except jwt.exceptions.InvalidSignatureError:
            raise HTTPException(status_code=401, detail="Invalid token signature")
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Error decoding token")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
