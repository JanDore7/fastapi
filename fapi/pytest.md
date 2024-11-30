**pytest** — это мощный фреймворк для тестирования Python-приложений. Он поддерживает автоматизацию тестов, позволяет писать их легко и лаконично, и обеспечивает множество возможностей для конфигурации и расширения.
**Установка pytest**

Для установки выполните команду: 
```angular2html
pip install pytest
```

**Структура тестов в pytest**

Тестовые файлы: должны начинаться с test_ или заканчиваться на _test.py.
Тестовые функции: имена функций должны начинаться с test_.

Пример тестов:
```angular2html
# test_example.py
def test_sum():
    assert 1 + 1 == 2

def test_subtract():
    assert 2 - 1 == 1
```

Для запуска всех тестов:
```angular2html
pytest
```

**Файл конфигурации pytest.ini**

Файл pytest.ini позволяет настроить поведение pytest. Он особенно полезен в больших проектах, где необходимо унифицировать параметры запуска тестов.
Пример содержимого pytest.ini:
```angular2html
[pytest]
testpaths = tests
addopts = --verbose --disable-warnings
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    slow: тесты, которые выполняются медленно
    fast: быстрые тесты
minversion = 7.0
```

![Таблица.](images/2024-11-26_06-12.jpg)

Описание параметров
**1. testpaths**

Определяет директории, где pytest будет искать тесты.

По умолчанию: текущая директория и ее подкаталоги.
Пример:
```
testpaths = tests, functional_tests
```
**2. addopts**

Позволяет задавать дополнительные аргументы, которые будут применяться при каждом запуске pytest.

Пример:
```
addopts = --verbose --disable-warnings
```
Этот пример включает подробный вывод и отключает предупреждения.

**3. python_files**

Шаблон имен файлов, которые pytest распознает как тестовые.

По умолчанию: test_*.py.
Пример:
```
python_files = *_test.py
```
**4. python_classes**

Шаблон имен классов, содержащих тестовые функции.

Пример:
```
python_classes = Test*
```
**5. python_functions**

Шаблон имен функций, которые pytest распознает как тесты.

Пример:
```
python_functions = test_*
```
**6. markers**

Определяет пользовательские метки (маркировки) для тестов. Это удобно для группировки тестов по характеристикам.

Пример:
```
markers =
    slow: тесты, которые выполняются медленно
    fast: быстрые тесты
```
**7. minversion**

Указывает минимальную версию pytest, которая должна быть установлена для выполнения тестов.

Пример:
```
minversion = 7.0
```
**8. log_level и log_format**

Позволяют настроить уровень и формат логов, выводимых во время тестирования.

Пример:
```
log_level = DEBUG
log_format = %(asctime)s [%(levelname)s] %(message)s
```
**9. filterwarnings**

Позволяет настроить фильтрацию предупреждений, которые появляются во время тестов.

Пример:
```
filterwarnings =
    ignore::DeprecationWarning
    default::UserWarning
```

**Запуск тестов и команды**
**Основные команды:**

Запуск всех тестов:
```
pytest
```
Запуск тестов в конкретном файле:
```
pytest test_example.py
```
Запуск конкретного теста:
```
pytest test_example.py::test_sum
```
Запуск тестов с определенной маркировкой:
```
pytest -m slow
```
Остановка после первого сбоя:
```
pytest -x
```
Ограничение количества сбоев:
```
pytest --maxfail=3
```
Параллельный запуск тестов (если установлен pytest-xdist):
```
pytest -n 4
```

**Маркировка тестов**

Метки (markers) помогают группировать и фильтровать тесты. Используйте декоратор @pytest.mark.

Пример:
```angular2html
import pytest

@pytest.mark.slow
def test_long_process():
    import time
    time.sleep(5)
    assert True

@pytest.mark.fast
def test_quick():
    assert 1 + 1 == 2

```

Запуск только быстрых тестов:
```angular2html
pytest -m fast
```

**Полезные плагины**

**pytest-xdist — параллельное выполнение тестов:**
```
pip install pytest-xdist
pytest -n 4
```
**pytest-cov — покрытие кода:**
```
pip install pytest-cov
pytest --cov=имя_пакета
```
**pytest-html — генерация HTML-отчетов:**
```
pip install pytest-html
pytest --html=report.html
```
# Важно
При работе с алхимией стоит переопределить движок .

engine_null_pool = create_async_engine(settings.DB_URL, pool_class=NullPool)
async_session_null_pool = async_sessionmaker(engine_null_pool, expire_on_commit=False)

**NullPool** отключает использование пула соединений. Это значит, что каждый раз при выполнении запроса создаётся новое соединение с базой данных, а после выполнения запроса соединение закрывается.


**ФИКСТУРА**

**Фикстура в Pytest** — это способ подготовки тестовой среды перед выполнением тестов. Фикстуры помогают организовать повторяющиеся действия, такие как настройка базы данных, создание временных файлов или конфигурация тестового окружения, и делают код тестов более читаемым и поддерживаемым.  

Фикстуры определяются с помощью декоратора **@pytest.fixture** и могут возвращать данные, которые затем используются в тестах. 

Определение фикстуры: Используйте декоратор @pytest.fixture перед функцией, чтобы объявить её как фикстуру.
```angular2html
@pytest.fixture
def sample_fixture():
    return {"key": "value"}  # данные, доступные тесту
```

Использование фикстуры в тесте: Передайте имя фикстуры как аргумент функции теста.
```angular2html
def test_example(sample_fixture):
    assert sample_fixture["key"] == "value"
```
Настройка более сложной логики: Если требуется выполнять действия до и после теста, можно использовать конструкцию yield.
```angular2html
@pytest.fixture
def resource():
    # Настройка
    resource = {"status": "ready"}
    yield resource  # Данные для теста
    # Очистка
    resource["status"] = "closed"
```

Декоратор @pytest.fixture поддерживает различные параметры для управления поведением фикстур:  

**scope**: Определяет, как долго будет существовать фикстура. Возможные значения:  
    **"function"** (по умолчанию): фикстура создаётся заново для каждой тестовой функции.  
    **"class"**: фикстура используется для всех тестов в классе.  
    **"module"**: фикстура используется для всех тестов в модуле.  
    **"package"**: фикстура используется для всех тестов в пакете.  
    **"session"**: фикстура используется для всех тестов в сессии.  

```angular2html
@pytest.fixture(scope="module")
def shared_resource():
    return {"data": 42}
```

**autouse**: Если True, фикстура будет автоматически применяться ко всем тестам, без необходимости явного указания её имени.
```angular2html
@pytest.fixture(autouse=True)
def setup_environment():
    print("Фикстура выполнена")
```

**params**: Позволяет передать набор параметров для фикстуры. Каждый тест будет выполнен с каждым параметром.
```angular2html
@pytest.fixture(params=[1, 2, 3])
def param_fixture(request):
    return request.param
```

Использование в тестах:
```angular2html
def test_with_params(param_fixture):
    assert param_fixture in [1, 2, 3]
```

**name**: Позволяет задать кастомное имя фикстуре, которое будет использоваться в тестах.
```angular2html
@pytest.fixture(name="custom_fixture")
def sample_fixture():
    return "custom value"
```

Использование:
```angular2html
def test_custom_fixture(custom_fixture):
    assert custom_fixture == "custom value"
```

**Пример сложной фикстуры**
```angular2html
import pytest

@pytest.fixture(scope="function", autouse=False)
def database():
    # Настройка
    db = {"connection": "open"}
    print("Открытие соединения с базой данных")
    yield db
    # Очистка
    db["connection"] = "closed"
    print("Закрытие соединения с базой данных")

def test_database_operation(database):
    assert database["connection"] == "open"
```
