# Гайд по созданию кастомных исключений в Python

Исключения в Python используются для обработки ошибок и ситуаций, которые нарушают нормальный поток выполнения программы. Помимо встроенных исключений, таких как `ValueError`, `TypeError`, и `KeyError`, Python позволяет создавать свои собственные (кастомные) исключения для обработки специфичных ситуаций.

Этот гайд объяснит, как создавать кастомные исключения и использовать конструкцию `raise ... from ...` для управления связями между исключениями.

---

## Основы создания кастомных исключений

### Шаг 1: Определение кастомного исключения
Создавать кастомные исключения в Python можно, унаследовав класс от встроенного `Exception` или его подкласса. 

Пример:
```python
class CustomException(Exception):
    """Базовый класс для пользовательских исключений."""
    pass

class InvalidInputError(CustomException):
    """Исключение, вызываемое при недопустимом вводе."""
    def __init__(self, message, input_value):
        # Используем super(), чтобы вызвать инициализацию базового класса Exception
        # Это позволяет задать стандартное сообщение для исключения
        super().__init__(message)
        self.input_value = input_value  # Сохраняем дополнительную информацию об ошибке
```

### Шаг 2: Использование кастомного исключения

```python
def process_input(value):
    # Проверяем, является ли ввод целым числом
    if not isinstance(value, int):
        # Выбрасываем наше кастомное исключение, если условие не выполнено
        raise InvalidInputError("Ожидалось целое число.", value)

try:
    process_input("текст")
except InvalidInputError as e:
    # Обрабатываем кастомное исключение и выводим информацию об ошибке
    print(f"Ошибка: {e}. Неверное значение: {e.input_value}")
```

**Вывод:**
```
Ошибка: Ожидалось целое число.. Неверное значение: текст
```

---

## Конструкция `raise ... from ...`

Python предоставляет механизм связывания исключений через конструкцию `raise ... from ...`. Она используется, чтобы указать, что одно исключение было вызвано другим. Это полезно для отладки и улучшения читаемости стек-трейса.

### Зачем это нужно?
1. Улучшает контекст ошибок.
2. Показывает причину, по которой возникло новое исключение.
3. Позволяет передавать первопричину ошибки в новый контекст.

### Пример использования `raise ... from ...`

```python
class ObjectNotFoundException(Exception):
    """Исключение для ситуации, когда объект не найден."""
    pass

class HotelNotFoundException(Exception):
    """Исключение для отсутствия отеля."""
    pass

def find_hotel(hotel_id):
    # Словарь с доступными отелями
    hotels = {1: "Hotel California", 2: "Grand Budapest Hotel"}
    if hotel_id not in hotels:
        # Выбрасываем исключение, если отель не найден
        raise ObjectNotFoundException(f"Отель с ID {hotel_id} не найден.")
    return hotels[hotel_id]

try:
    find_hotel(3)  # Пытаемся найти отель с ID 3, которого нет
except ObjectNotFoundException as ex:
    # Преобразуем одно исключение в другое для более специфичного контекста
    raise HotelNotFoundException("Ошибка поиска отеля.") from ex
```

### Анализ примера
1. Исключение `ObjectNotFoundException` указывает на отсутствие объекта (например, отеля).
2. Исключение `HotelNotFoundException` более специфично для доменной области приложения.
3. Конструкция `raise ... from ...` передаёт контекст исходного исключения `ObjectNotFoundException`, что делает диагностику более точной.

**Вывод стек-трейса:**
```
Traceback (most recent call last):
  File "example.py", line 11, in find_hotel
    raise ObjectNotFoundException(f"Отель с ID {hotel_id} не найден.")
ObjectNotFoundException: Отель с ID 3 не найден.

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "example.py", line 15, in <module>
    raise HotelNotFoundException("Ошибка поиска отеля.") from ex
HotelNotFoundException: Ошибка поиска отеля.
```

---

## Рекомендации по созданию кастомных исключений
1. **Иерархия исключений:**
   - Создайте базовый класс для исключений вашей библиотеки или модуля.
   - Унаследуйте более специфичные исключения от базового класса.

   ```python
   class MyBaseError(Exception):
       """Базовый класс для всех ошибок в модуле."""
       pass

   class FileFormatError(MyBaseError):
       """Ошибка формата файла."""
       pass

   class NetworkError(MyBaseError):
       """Ошибка сети."""
       pass
   ```

2. **Полезная информация:**
   - Добавляйте атрибуты в кастомные исключения, чтобы передавать больше данных об ошибке.

   ```python
   class DatabaseError(Exception):
       """Ошибка базы данных с дополнительной информацией."""
       def __init__(self, message, db_name):
           # Инициализируем базовый класс с сообщением об ошибке
           super().__init__(message)
           self.db_name = db_name  # Сохраняем имя базы данных
   ```

3. **Документация:**
   - Добавьте комментарии и docstring, чтобы другие разработчики понимали назначение исключений.

4. **Использование `raise ... from ...`:**
   - Используйте эту конструкцию для связывания контекстов ошибок, особенно при преобразовании исключений между уровнями абстракции.

---

## Полный пример

```python
class ApplicationError(Exception):
    """Базовый класс для ошибок приложения."""
    pass

class ServiceError(ApplicationError):
    """Ошибка в сервисном слое."""
    def __init__(self, message, service_name):
        # Используем super(), чтобы правильно инициализировать базовый класс
        super().__init__(message)
        self.service_name = service_name  # Сохраняем имя сервиса, где произошла ошибка

class DatabaseError(ApplicationError):
    """Ошибка взаимодействия с базой данных."""
    pass

def fetch_data():
    try:
        # Симулируем ошибку базы данных
        raise DatabaseError("Не удалось подключиться к базе данных.")
    except DatabaseError as ex:
        # Преобразуем исключение в ошибку на уровне сервиса
        raise ServiceError("Ошибка в слое сервиса.", "DatabaseService") from ex

try:
    fetch_data()  # Вызываем функцию, которая вызывает исключение
except ServiceError as e:
    # Обрабатываем исключение и выводим его информацию
    print(f"{e} (Сервис: {e.service_name})")
```

**Вывод:**
```
Ошибка в слое сервиса. (Сервис: DatabaseService)
```
