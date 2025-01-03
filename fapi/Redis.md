[Полезное...](https://help.reg.ru/support/servery-vps/oblachnyye-servery/ustanovka-programmnogo-obespecheniya/kak-ustanovit-i-nastroit-redis-na-linux#2)

Redis (Remote Dictionary Server) — 
это быстрый и высокопроизводительный сервер базы данных,
работающий в оперативной памяти и поддерживающий множество 
структур данных (строки, списки, множества, хэши, и т. д.).
Он широко используется для кэширования, очередей сообщений,
управления сессиями и других задач.  

В этом руководстве мы рассмотрим основные аспекты работы 
с Redis, начиная с базовой установки и заканчивая операциями
с данными.  

**1. Установка и настройка Redis**
Установка сервера Redis  

Linux/MacOS:  
```aiignore
sudo apt update
sudo apt install redis-server
```
Или через brew на MacOS:
```aiignore
brew install redis
```
**Проверка установки**

После установки запустите сервер Redis:  
```aiignore
redis-server
```
И откройте клиент для проверки:
```aiignore
redis-cli
```

Пример команды в клиенте Redis:
```
SET mykey "Hello, Redis!"
GET mykey
```


**2. Установка библиотеки Python для Redis**

Для взаимодействия с Redis в Python используется библиотека 
redis-py. Установим её:  
```aiignore
pip install redis
```

**3. Подключение к Redis**
Пример подключения к Redis из Python:
```aiignore
import redis

# Подключение к Redis-серверу
client = redis.Redis(host='localhost', port=6379, db=0)

# Проверка соединения
try:
    client.ping()
    print("Успешное подключение к Redis!")
except redis.ConnectionError:
    print("Не удалось подключиться к Redis.")
```

Пояснение:  

**host='localhost'** — хост, на котором запущен сервер Redis (по умолчанию localhost).
**port=6379** — порт, на котором слушает сервер Redis (по умолчанию 6379).
**db=0** — номер базы данных Redis
(по умолчанию используется база 0).  

**4. Работа с базами данных**

Redis поддерживает до 16 баз данных по умолчанию
(это можно изменить в конфигурации). 
Выбор базы данных осуществляется через команду SELECT.  

Пример:
```aiignore
# Переключение на базу данных 1
client = redis.Redis(db=1)
client.set("key_in_db1", "value1")

# Переключение обратно на базу данных 0
client = redis.Redis(db=0)
value = client.get("key_in_db1")
print(value)  # None, так как база другая
```

Пояснение:  

**SELECT db_number**: команды в одной базе данных изолированы от другой.  

**5. Операции со строками**
Установка и получение значения
```aiignore
# Установка значения
client.set("name", "Alice")

# Получение значения
name = client.get("name")
print(name.decode())  # Вывод: Alice

```
Пояснение:  

**set** — устанавливает значение ключа.
**get** — извлекает значение по ключу. Redis возвращает значения в формате bytes, поэтому часто требуется их декодирование.

**
Инкремент/декремент**
```aiignore
client.set("counter", 10)

# Увеличение на 1
client.incr("counter")

# Увеличение на заданное значение
client.incrby("counter", 5)

# Уменьшение на 1
client.decr("counter")

# Уменьшение на заданное значение
client.decrby("counter", 3)

# Вывод текущего значения
print(client.get("counter").decode())  # Вывод: 11

```

**6. Работа с префиксами ключей**
Использование префиксов  

Для лучшей организации данных часто 
используется концепция префиксов ключей.  

Пример:
```aiignore
# Пример использования префикса
client.set("user:1001:name", "Alice")
client.set("user:1001:age", 30)

# Извлечение данных
name = client.get("user:1001:name").decode()
age = int(client.get("user:1001:age"))

print(f"Имя: {name}, Возраст: {age}")

```
Пояснение:

**Префикс (user:1001)** позволяет группировать данные, связанные с одним объектом.
**Разделитель** : — это соглашение для читаемости.

**7. Удаление данных**
Удаление одного ключа
```aiignore
client.set("temporary_key", "value")
client.delete("temporary_key")
```
Удаление нескольких ключей
```aiignore
client.mset({"key1": "value1", "key2": "value2"})
client.delete("key1", "key2")
```
Пояснение:  

**delete** — удаляет указанные ключи.

**8. Хранилища сложных структур данных**

Redis поддерживает различные структуры данных:  
списки, хэши, множества, отсортированные множества.  
Работа с хэшами
```aiignore
# Установка данных в хэше
client.hset("user:1001", "name", "Alice")
client.hset("user:1001", "age", 30)

# Получение значения из хэша
name = client.hget("user:1001", "name").decode()
age = int(client.hget("user:1001", "age"))

# Получение всех значений
user_data = client.hgetall("user:1001")
decoded_data = {k.decode(): v.decode() for k, v in user_data.items()}

print(decoded_data)  # Вывод: {'name': 'Alice', 'age': '30'}
```
Работа со списками
```aiignore
# Добавление элементов в список
client.rpush("tasks", "task1", "task2", "task3")

# Извлечение элементов
task = client.lpop("tasks").decode()  # Удаляет первый элемент
all_tasks = client.lrange("tasks", 0, -1)  # Получение всех элементов
decoded_tasks = [t.decode() for t in all_tasks]

print(decoded_tasks)  # Вывод: ['task2', 'task3']
```
**9. TTL (время жизни ключей)**

Redis поддерживает установку времени жизни для ключей.

```aiignore
client.set("session_key", "abc123", ex=60)  # Ключ будет жить 60 секунд

# Проверка оставшегося времени жизни
ttl = client.ttl("session_key")
print(f"Оставшееся время жизни: {ttl} секунд")
```
**10. Очистка базы данных**

Для очистки текущей базы данных используется команда FLUSHDB:
```aiignore
client.flushdb()
```

Очистка всех баз данных:
```aiignore
client.flushall()
```
