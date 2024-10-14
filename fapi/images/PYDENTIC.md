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



## [Полезные материалы...](https://yourtodo.ru/posts/vvedenie-v-pydantic-osnovyi-i-prodvinutyie-vozmozhnosti/)