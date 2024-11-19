### relationship
создает связь между двумя моделями (таблицами).
Она позволяет загружать связанные объекты, выполнять каскадные операции, 
устанавливать ограничения на связи и многое другое. 
Обычно используется в связке с ForeignKey, 
который задает связь между таблицами на уровне базы данных.  

**Типы связей**

**Один-к-одному (One-to-One)**
Пример: Пользователь имеет один профиль.  

**Один-ко-многим (One-to-Many)**
Пример: Автор может написать множество книг.  

**Многие-ко-многим (Many-to-Many)**
Пример: Студенты записаны на множество курсов,
а курсы включают множество студентов.  

**Основные параметры relationship**

**back_populates:** Настраивает двунаправленную связь.  
**backref:** Упрощенный способ создания обратной связи (альтернатива back_populates).  
**cascade:** Определяет каскадные операции (например, delete, all).  
**lazy:** Задает стратегию загрузки связанных объектов (select, joined, subquery и др.).  
**primaryjoin:** Позволяет указать явное условие соединения для связи.  


Примеры
1. Один-к-одному (One-to-One)
```aiignore
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    profile = relationship("Profile", back_populates="user", uselist=False)

class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    bio = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="profile")

# Создание базы данных и таблиц
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)

# Сессия
Session = sessionmaker(bind=engine)
session = Session()

# Создание объектов
new_user = User(name="John Doe", profile=Profile(bio="Software Developer"))
session.add(new_user)
session.commit()

# Доступ к связанным данным
retrieved_user = session.query(User).first()
print(retrieved_user.profile.bio)  # Вывод: Software Developer

```

2. Один-ко-многим (One-to-Many)
```aiignore
class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship("Author", back_populates="books")

# Создание объектов
author = Author(name="George Orwell", books=[
    Book(title="1984"),
    Book(title="Animal Farm")
])
session.add(author)
session.commit()

# Доступ к данным
retrieved_author = session.query(Author).first()
for book in retrieved_author.books:
    print(book.title)

```

3. Многие-ко-многим (Many-to-Many)  

Для реализации связи "многие-ко-многим" требуется дополнительная
промежуточная таблица.  
```aiignore
from sqlalchemy import Table

# Ассоциативная таблица
student_course = Table(
    'student_course', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    courses = relationship("Course", secondary=student_course, back_populates="students")

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    students = relationship("Student", secondary=student_course, back_populates="courses")

# Создание объектов
student = Student(name="Alice", courses=[Course(title="Math"), Course(title="History")])
session.add(student)
session.commit()

# Доступ к данным
retrieved_student = session.query(Student).first()
for course in retrieved_student.courses:
    print(course.title)

```

Параметр relationship обладает множеством опций,
которые помогают настроить поведение связи между моделями.
Рассмотрим основные параметры, которые позволяют управлять каскадными операциями,
стратегиями загрузки, условиями соединения и обратными ссылками.  

**1. back_populates и backref**

Эти параметры обеспечивают двустороннюю связь между моделями. Например, если связь настроена как один-к-многим (Author → Book), то при доступе к автору можно получить его книги, а из книги — соответствующего автора.
back_populates  

Используется для явного определения связи с двух сторон.  
Обязательно нужно указать в обоих связанных моделях.  

Пример:
```aiignore
class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship("Author", back_populates="books")

```
**backref**

Позволяет создать обратную связь без необходимости
явно определять ее в обоих классах.  
Упрощает код, но менее гибкий, чем back_populates.

Пример:
```aiignore
class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship("Book", backref="author")

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))

```
В этом примере обратная связь book.author автоматически создается через backref.  

**2. cascade**

Параметр cascade определяет, какие действия будут применяться к связанным объектам автоматически при выполнении операций над "родительским" объектом. Это полезно для управления удалением, сохранением, слиянием и другими операциями.
Основные опции cascade:

**all:** Применяет все каскадные операции.  
**save-update:** Сохраняет/обновляет связанные объекты.  
**merge:** Сливает связанные объекты.  
**delete:** Удаляет связанные объекты.  
**delete-orphan:** Удаляет связанные объекты, если они больше не связаны с родительским объектом.  
**refresh-expire:** Обновляет или сбрасывает связанные объекты при загрузке.  
**none:** Отключает каскадные операции.  

Пример:
```aiignore
class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship("Book", cascade="all, delete")

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))

```
Если вы удалите автора, его книги тоже будут удалены:
```aiignore
author = session.query(Author).first()
session.delete(author)
session.commit()

```
**3. lazy**

Параметр lazy определяет стратегию загрузки связанных объектов. Он позволяет управлять тем, как и когда SQLAlchemy загружает связанные данные.
Основные значения lazy:  

**select** (по умолчанию): Отложенная загрузка; связанные данные загружаются при первом обращении.  
**joined:** Использует JOIN, чтобы загрузить связанные данные сразу.  
**subquery:** Использует подзапрос для загрузки связанных данных.  
**dynamic:** Возвращает запрос (Query), который можно использовать для фильтрации.  
**noload: Не загружает связанные данные (просто игнорирует их).  
**raise:** Вызывает ошибку при попытке загрузить связанные данные.  
**selectin:** Использует стратегию "в одном запросе", аналогичную joined.  

Пример:
```aiignore
class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship("Book", lazy="joined")  # Загружает книги сразу с автором

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))

```

**4. uselist**

Определяет, возвращается ли результат как список или единственный объект.

**True (по умолчанию):** Связь возвращает список.
**False:** Связь возвращает один объект.

Пример использования uselist:  

Один-к-одному:
```aiignore
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    profile = relationship("Profile", back_populates="user", uselist=False)

class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    bio = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="profile")

```

**5. secondary**

Используется для настройки связи "многие-ко-многим" через промежуточную таблицу.  

Пример:
```aiignore
association_table = Table(
    'association', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    courses = relationship("Course", secondary=association_table, back_populates="students")

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    students = relationship("Student", secondary=association_table, back_populates="courses")

```

**6. primaryjoin и secondaryjoin**

Эти параметры позволяют вручную указать условия соединения (JOIN) между таблицами.  

Пример:
```aiignore
class Parent(Base):
    __tablename__ = 'parents'
    id = Column(Integer, primary_key=True)

class Child(Base):
    __tablename__ = 'children'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parents.id'))

class SpecialChild(Base):
    __tablename__ = 'special_children'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parents.id'))

Parent.special_children = relationship(
    "SpecialChild",
    primaryjoin="Parent.id==SpecialChild.parent_id"
)

```
**7. order_by**

Определяет порядок, в котором возвращаются связанные объекты.  

Пример:
```aiignore
class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship("Book", order_by="Book.title")

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))

```

**8. viewonly**

Если указать viewonly=True, то связь становится "только для чтения" 
и не изменяет данные в базе.  

Пример:
```aiignore
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    orders = relationship("Order", viewonly=True)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))

```



