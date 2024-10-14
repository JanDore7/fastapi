**Pydantic** – это мощная библиотека для Python, 
которая предоставляет средства для валидации данных и 
создания моделей данных. Она широко используется для валидации
данных в веб-приложениях, API и других проектах. 
В Pydantic версии 2.0 произошли изменения в API,
и было введено много новых методов, включая model_validate.  


## Основные методы Pydantic моделей

1. **model_validate()**

Метод model_validate() используется для создания экземпляра 
модели Pydantic и валидации входных данных. 
Этот метод принимает данные (обычно в формате словаря или JSON) 
и проверяет, соответствуют ли они схеме модели.  
Аргументы model_validate()  

**data (обязательно)**: входные данные для валидации. 
Это может быть словарь или объект JSON.  
**from_attributes (по умолчанию False)**: определяет, следует 
ли получать значения атрибутов напрямую
из объекта. Полезно при работе с объектами Python,
а не с простыми словарями.  
**context (по умолчанию None)**: произвольный контекст, 
который можно использовать при валидации данных.
Контекст доступен в пользовательских валидаторах.  

**Пример использования:**  
```aiignore
from pydantic import BaseModel, ValidationError

class User(BaseModel):
    id: int
    name: str

try:
    user = User.model_validate({'id': 1, 'name': 'Alice'})
    print(user)
except ValidationError as e:
    print(e)

```
2. **model_dump()**

Метод model_dump() используется для сериализации данных модели обратно 
в формат Python (словарь). Он конвертирует объект модели
в JSON-подобную структуру данных.  
Аргументы model_dump()

**include**: указывает, какие поля включить в сериализацию.  
**exclude**: указывает, какие поля исключить из сериализации.  
**by_alias (по умолчанию False)**: определяет, 
следует ли использовать алиасы (псевдонимы) полей вместо их имен.  
**exclude_unset (по умолчанию False)**: исключает поля,
значения которых не были установлены.  
**exclude_defaults (по умолчанию False)**: исключает поля,
значения которых равны значениям по умолчанию.  
**exclude_none (по умолчанию False)**: исключает поля, 
значения которых равны None.  

**Пример:**
```aiignore
user = User(id=1, name='Alice')
print(user.model_dump(exclude={'id'}))  # {'name': 'Alice'}

```

3. **model_construct()**

Метод **model_construct()** используется для создания модели 
без выполнения валидации данных. Это полезно, когда вы точно знаете,
что данные корректны и не хотите тратить ресурсы на валидацию.  

**Пример:**
```aiignore
user = User.model_construct(id=1, name='Alice')
print(user)

```
4. **model_copy()**

Метод model_copy() создает копию объекта модели с возможностью
изменить некоторые поля.  
Аргументы model_copy()  

**update**: словарь с полями, которые нужно изменить в копии.

**Пример:**
```
user = User(id=1, name='Alice')
new_user = user.model_copy(update={'name': 'Bob'})
print(new_user)  # User(id=1, name='Bob')
```
5. **model_json()**

Этот метод возвращает данные модели в формате JSON. 
Полезен для сериализации данных для передачи через API.   

**Пример:**
```aiignore
json_data = user.model_json()
print(json_data)  # {"id": 1, "name": "Alice"}

```
6. **model_validate_json()**

Аналогично методу model_validate(), но принимает 
строку JSON вместо словаря.  

**Пример:**
```aiignore
user_json = '{"id": 1, "name": "Alice"}'
user = User.model_validate_json(user_json)
print(user)  # User(id=1, name='Alice')

```

7. **__fields_set__**

Это свойство возвращает множество полей,
которые были установлены при создании объекта модели.  

**Пример:**
```aiignore
user = User(id=1, name='Alice')
print(user.__fields_set__)  # {'id', 'name'}

```

## Пользовательские валидаторы

Кроме встроенных методов, Pydantic также поддерживает 
пользовательские валидаторы для валидации значений полей.
Они создаются с помощью декоратора **@field_validator** в 
Pydantic 2.0 (вместо @validator, который использовался ранее).  

**Пример:**
```aiignore
from pydantic import BaseModel, FieldValidationInfo, field_validator

class User(BaseModel):
    id: int
    name: str

    @field_validator('name')
    def validate_name(cls, value: str, info: FieldValidationInfo):
        if len(value) < 3:
            raise ValueError('Name must be at least 3 characters long')
        return value

try:
    user = User(id=1, name='Al')
except ValidationError as e:
    print(e)  # Name must be at least 3 characters long

```

## ConfigDict

**ConfigDict** — это класс, позволяющий настраивать поведение моделей Pydantic. 
Вы можете управлять тем, как происходит валидация данных, сериализация,
и даже контроль над производительностью, используя его параметры.
Этот объект передается как параметр в модели Pydantic через аргумент model_config.  
Как использовать ConfigDict?  

Настройки модели задаются путем передачи объекта ConfigDict в специальное поле 
model_config класса Pydantic:
```aiignore
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=True
    )

```
В данном примере мы настроили модель User с помощью ConfigDict так, чтобы:  

**validate_assignment=True**: При изменении значений полей модели будет проводиться валидация (например, 
если попытаться присвоить некорректное значение полю).  
**use_enum_values=True**: Если модель содержит поля с типами Enum, 
то Pydantic будет использовать их значения (а не сами члены перечислений).  

**Основные атрибуты ConfigDict**
1. **validate_assignment** (по умолчанию False)

Если этот параметр включен, Pydantic будет проверять данные при каждом 
изменении значения атрибутов модели после её создания. 
Это полезно для обеспечения строгой типизации данных даже при изменениях.  

Пример:
```aiignore
class User(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(validate_assignment=True)

user = User(id=1, name='Alice')
user.id = 'invalid_id'  # ValidationError, id должен быть int

```

2. **use_enum_values** (по умолчанию False)

Этот параметр указывает, должны ли использоваться значения 
перечислений (Enum) вместо их имен при сериализации.  

Пример:  
```aiignore
from enum import Enum

class Status(Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'

class User(BaseModel):
    id: int
    status: Status

    model_config = ConfigDict(use_enum_values=True)

user = User(id=1, status=Status.ACTIVE)
print(user.model_dump())  # {'id': 1, 'status': 'active'}

```
3. **extra** (значения: 'allow', 'forbid', 'ignore', по умолчанию 'ignore')

Этот параметр контролирует поведение модели при передаче дополнительных (неожиданных) полей, 
которые не определены в модели.  

**'allow'**: Дополнительные поля разрешены и будут сохранены в модели.  
**'forbid'**: Дополнительные поля запрещены, и если они переданы, то будет выброшена ошибка.  
**'ignore'**: Дополнительные поля игнорируются и не сохраняются.  

Пример:
```aiignore
class User(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(extra='forbid')

try:
    user = User(id=1, name='Alice', age=30)  # ValidationError, age не ожидается
except ValidationError as e:
    print(e)

```

4. **allow_population_by_field_name** (по умолчанию False)

Разрешает и использовать имена полей (а не псевдонимы) для инициализации модели, 
даже если определены алиасы.   

Пример: 
```aiignore
class User(BaseModel):
    id: int
    name: str = Field(alias='username')

    model_config = ConfigDict(allow_population_by_field_name=True)

user = User(id=1, name='Alice')  # Мы можем использовать 'name' вместо 'username'
print(user)

```

5. **frozen** (по умолчанию False)

Делает модель неизменяемой после создания. 
Любая попытка изменить значение поля после инициализации объекта приведет к ошибке.  

Пример:
```aiignore
class User(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(frozen=True)

user = User(id=1, name='Alice')
user.name = 'Bob'  # TypeError, модель неизменяема

```
6. **from_attributes** (по умолчанию False)

Если установлено в True, позволяет создавать модель из объектов Python, 
используя их атрибуты (а не только словари).  

Пример:

```aiignore
class Person:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

class User(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

person = Person(id=1, name='Alice')
user = User.model_validate(person)  # Модель создается из атрибутов объекта person
print(user)  # User(id=1, name='Alice')

```
7. **copy_on_model_validation** (по умолчанию True)  

Если этот параметр установлен в False, модель не будет создавать копию при валидации. 
Это может ускорить работу, если вы уверены, что переданные данные не нужно копировать.  
8. **arbitrary_types_allowed** (по умолчанию False)  

Разрешает использование произвольных (нестандартных) типов данных, 
которые Pydantic по умолчанию не поддерживает.  

Пример:
```aiignore
class CustomType:
    pass

class User(BaseModel):
    id: int
    custom: CustomType

    model_config = ConfigDict(arbitrary_types_allowed=True)

user = User(id=1, custom=CustomType())
print(user)

```
9. **json_encoders**

Позволяет указать собственные методы для сериализации пользовательских типов в JSON.  

Пример:
```aiignore
from datetime import datetime

class User(BaseModel):
    id: int
    created_at: datetime

    model_config = ConfigDict(json_encoders={datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')})

user = User(id=1, created_at=datetime.now())
print(user.model_json())  # Используется кастомный формат для даты

```








## [Полезные материалы...](https://yourtodo.ru/posts/vvedenie-v-pydantic-osnovyi-i-prodvinutyie-vozmozhnosti/)