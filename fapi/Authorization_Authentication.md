Установка библиотек  

**[Гайд](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/?h=jwt)**

Сначала установим необходимые библиотеки:  



>pip install pyjwt passlib[bcrypt]

1. **Работа с pyjwt**  

**pyjwt** — это библиотека для создания и проверки JSON Web Tokens (JWT), 
которые широко используются для аутентификации и авторизации.  
Создание JWT  

Чтобы создать JWT, вы можете использовать следующий код:  
```aiignore
import jwt
import datetime

# Секретный ключ для подписи токена
SECRET_KEY = "your_secret_key"

def create_jwt(user_id: str):
    # Задаем данные для токена
    payload = {
        "sub": user_id,  # subject (идентификатор пользователя)
        "iat": datetime.datetime.utcnow(),  # время создания
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # время истечения
    }
    
    # Создаем JWT
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# Пример использования
token = create_jwt("user123")
print(token)

```

Объяснение:

**payload**: это данные, которые мы хотим сохранить в токене. Обычно это идентификатор пользователя, время создания и время истечения.
**jwt.encode()**: создает JWT, используя данные из payload, секретный ключ и алгоритм подписи (в данном случае HS256).

Проверка JWT  

Чтобы проверить токен, используйте следующий код:  
```aiignore
def decode_jwt(token: str):
    try:
        # Декодируем токен
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        print("Токен истек")
    except jwt.InvalidTokenError:
        print("Неверный токен")

# Пример использования
decoded_payload = decode_jwt(token)
print(decoded_payload)

```
Объяснение:  

**jwt.decode()**: декодирует токен, проверяя подпись и время истечения. 
Если токен истек или неверен, срабатывают исключения, которые можно обработать.  

2. **Работа с passlib[bcrypt]**  

**passlib** — это библиотека для безопасного хранения паролей. Она предоставляет множество хеш-функций, включая bcrypt, который является одним из самых безопасных вариантов.
Хеширование паролей  

Вот как можно хешировать пароль с помощью bcrypt:  
```aiignore
from passlib.context import CryptContext

# Создаем контекст для работы с паролями
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # Хешируем пароль
    return pwd_context.hash(password)

# Пример использования
hashed_password = hash_password("my_secure_password")
print(hashed_password)

```
Объяснение:  

**CryptContext**: создает контекст для работы с хешами паролей. 
Мы указываем, что будем использовать bcrypt.  
**hash()**: хеширует пароль, возвращая строку с хешем.  

Проверка паролей  

Теперь давайте проверим, соответствует ли введенный пароль хешированному паролю:  
```aiignore
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Проверяем, соответствует ли пароль
    return pwd_context.verify(plain_password, hashed_password)

# Пример использования
is_valid = verify_password("my_secure_password", hashed_password)
print("Пароль валиден:", is_valid)

```
Объяснение:  

**verify()**: сравнивает введенный пароль с хешированным паролем,
возвращая True или False.  

Итог  

Теперь у вас есть основные примеры работы с библиотеками pyjwt и passlib[bcrypt].
Вы можете использовать эти инструменты для создания безопасной аутентификации 
в своем приложении. Вот краткий обзор:  

**pyjwt**: используется для создания и проверки JWT, которые могут содержать информацию о пользователе и времени жизни токена.
**passlib[bcrypt]**: используется для безопасного хеширования паролей, что позволяет хранить их без риска утечки.