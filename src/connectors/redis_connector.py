import asyncio
import redis.asyncio as redis
import logging
from redis.exceptions import RedisError

from src.config import settings


class RedisManager:
    def __init__(self, host: str, port: str):
        self.host = host
        self.port = port
        self.redis_url = settings.REDIS_URL
        self.max_retries = 5
        self.retry_delay = 3
        self.redis = None

    async def connect(self):
        retries = 0
        while retries < self.max_retries:
            try:
                logging.info("Подключаюсь к Redis...")
                self.redis = await redis.from_url(self.redis_url)
                logging.info("Успешно подключился к Redis")
                return  # Выход из метода после успешного подключения
            except RedisError as e:
                retries += 1
                print(
                    f"Ошибка подключения к Redis: {e}. Повторная попытка ({retries}/{self.max_retries})..."
                )
                await asyncio.sleep(self.retry_delay)
            except Exception as e:
                retries += 1
                print(
                    f"Неожиданная ошибка: {e}. Повторная попытка ({retries}/{self.max_retries})..."
                )
                await asyncio.sleep(self.retry_delay)

        print("Не удалось подключиться к Redis после нескольких попыток.")

    async def set(self, key: str, value: str, expire: int = None):
        if self.redis is None:
            print("Redis клиент не подключён.")
            return
        try:
            if expire:
                await self.redis.set(key, value, ex=expire)
            else:
                await self.redis.set(key, value)
            print(f"Установлен ключ: {key} со значением: {value}")
        except RedisError as e:
            print(f"Ошибка при установке значения для ключа {key}: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка при установке значения для ключа {key}: {e}")

    async def get(self, key: str):
        if self.redis is None:
            print("Redis клиент не подключён.")
            return None
        try:
            value = await self.redis.get(key)
            print(f"Получен ключ: {key}, значение: {value}")
            return value
        except RedisError as e:
            print(f"Ошибка при получении значения для ключа {key}: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка при получении значения для ключа {key}: {e}")

    async def delete(self, key: str):
        if self.redis is None:
            print("Redis клиент не подключён.")
            return
        try:
            await self.redis.delete(key)
            print(f"Удалён ключ: {key}")
        except RedisError as e:
            print(f"Ошибка при удалении ключа {key}: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка при удалении ключа {key}: {e}")

    async def close(self):
        if self.redis:
            try:
                await self.redis.close()
                print("Соединение с Redis закрыто.")
            except Exception as e:
                print(f"Ошибка при закрытии соединения с Redis: {e}")
