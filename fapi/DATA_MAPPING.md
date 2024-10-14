Паттерн Data Mapper – это структурный паттерн
проектирования, используемый для разделения
бизнес-логики приложения от логики взаимодействия с базой данных.
Его основная идея заключается в том, чтобы объекты в приложении
и данные в базе данных были разделены и не зависели друг от друга
напрямую. Data Mapper выступает посредником, который преобразует 
объекты в данные для базы данных и наоборот.  
Основные концепции:    

**Бизнес-объекты (Entities)**: Это объекты, которые содержат данные и логику приложения. Они не знают, как хранятся данные или как происходит их взаимодействие с базой данных.  
**Data Mapper**: Это отдельный слой, который отвечает за преобразование бизнес-объектов в формат, пригодный для хранения в базе данных, и наоборот.  
**Абстракция базы данных**: Data Mapper скрывает детали работы с базой данных (SQL-запросы, соединения, транзакции) от бизнес-логики.  

Зачем нужен Data Mapper?  

**Разделение обязанностей**: Data Mapper разделяет логику приложения и логику доступа к данным, что делает код чище
и легче тестируемым.  
**Тестируемость**: Легче тестировать бизнес-логику, не привязываясь к реальной базе данных.  
**Гибкость**: Легче изменять схему базы данных или структуру объектов в приложении без изменений в обоих местах.  

Пример использования  

Предположим, у нас есть простое приложение для управления пользователями. Мы будем использовать паттерн Data Mapper для
работы с базой данных.  
Бизнес-объект User  
```aiignore
class User:
    def __init__(self, user_id: int, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email

    def __repr__(self):
        return f"User({self.user_id}, {self.name}, {self.email})"

```
Этот объект не имеет никаких зависимостей на базу данных,
он чисто представляет данные и логику пользователя.  

**Data Mapper для пользователя UserMapper**    

Теперь создадим Data Mapper, который будет заниматься 
загрузкой и сохранением объектов User в базу данных:  
```aiignore
import sqlite3

class UserMapper:
    def __init__(self, connection):
        self.connection = connection

    def find_by_id(self, user_id: int) -> User:
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        if result:
            return User(user_id=result[0], name=result[1], email=result[2])
        return None

    def insert(self, user: User):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO users (id, name, email) VALUES (?, ?, ?)",
                       (user.user_id, user.name, user.email))
        self.connection.commit()

    def update(self, user: User):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?",
                       (user.name, user.email, user.user_id))
        self.connection.commit()

    def delete(self, user: User):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user.user_id,))
        self.connection.commit()

```

**Пример использования**
```
# Создание подключения к базе данных
connection = sqlite3.connect(':memory:')

# Создание таблицы пользователей
connection.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)''')

# Создание объекта User
user = User(user_id=1, name="John Doe", email="john.doe@example.com")

# Работа с Data Mapper
mapper = UserMapper(connection)

# Вставка пользователя в базу данных
mapper.insert(user)

# Получение пользователя из базы данных
retrieved_user = mapper.find_by_id(1)
print(retrieved_user)  # User(1, John Doe, john.doe@example.com)

# Обновление данных пользователя
user.name = "John Updated"
mapper.update(user)

# Удаление пользователя
mapper.delete(user)

```
Преимущества паттерна Data Mapper:

**Чистая архитектура**: Код бизнес-логики не зависит от того, как данные хранятся или извлекаются.  
**Повторное использование**: Data Mapper может легко повторно использоваться для разных бизнес-объектов.  
**Тестирование**: Можно легко протестировать бизнес-логику без базы данных, используя мок-объекты.  
**Гибкость**: Легко менять структуру хранения данных в базе данных, не меняя бизнес-логику.  

Недостатки паттерна Data Mapper:

**Сложность реализации**: Реализация Data Mapper требует большего объема кода по сравнению с паттерном Active Record.  
**Больше кода**: Нужно писать дополнительный код для маппинга каждого объекта, что может увеличить размер кода.  
**Перфоманс**: Из-за уровня абстракции могут возникать проблемы с производительностью в сложных сценариях.  

**Сравнение с Active Record**

Паттерн Active Record – это другой подход, в котором бизнес-объект сам содержит логику взаимодействия с базой данных.
В отличие от него, Data Mapper полностью разделяет 
бизнес-логику и работу с базой данных, 
делая каждый компонент более автономным и изолированным. 
**Пример Active Record:**
```aiignore
class User:
    def __init__(self, user_id: int, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email

    def save(self):
        connection = sqlite3.connect('example.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (id, name, email) VALUES (?, ?, ?)",
                       (self.user_id, self.name, self.email))
        connection.commit()

```
В этом случае объект User напрямую знает, как сохранять 
себя в базу данных, что упрощает код, но усложняет 
тестирование и поддержание архитектуры.  
Вывод  

Паттерн Data Mapper особенно полезен в крупных проектах, 
где важно разделить бизнес-логику и логику работы с данными.
Это делает код более модульным, тестируемым и гибким. 
Однако для маленьких проектов Active Record может быть более
удобным решением за счет простоты и меньшего объема кода.  

# [Назад к Алхимии ...](sqlalchemy_and_alembic.md)