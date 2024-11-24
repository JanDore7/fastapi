# Гайд по работе с Celery

**Celery** — это мощная система управления очередями задач, которая позволяет распределять выполнение задач между несколькими воркерами (работниками). Она активно используется в асинхронной обработке данных, веб-приложениях и автоматизации процессов.  

Ниже представлен подробный гайд с объяснениями и примерами.    

Основные понятия Celery  

**Задача (Task)**
Асинхронная функция, которая добавляется в очередь для выполнения.

**Очередь (Queue)**
Хранилище задач, где задачи ожидают выполнения. Очереди управляются брокером.

**Брокер (Broker)**
Программное обеспечение, обеспечивающее взаимодействие между продюсером задач (приложением) и воркерами. Примеры брокеров: Redis, RabbitMQ.

**Результат (Result Backend)**
Место для хранения результатов выполненных задач (например, база данных, Redis, MongoDB и др.).

**Шаги настройки Celery**
**1. Установка**

Убедитесь, что у вас установлены Python и виртуальное окружение. Установите Celery и брокер:
```angular2html
pip install celery[redis]
pip install redis
```

**2. Настройка брокера (Redis)**

Установите Redis (на Linux, используйте sudo apt install redis), запустите его:
```angular2html
sudo service redis start
```
Убедитесь, что Redis работает:
```angular2html
redis-cli ping
```
Ответ должен быть PONG.  


**3. Настройка Celery**

Создайте базовую структуру проекта:
```angular2html
my_project/
├── tasks.py
├── celery_app.py
├── requirements.txt
```
Файл celery_app.py
```angular2html
from celery import Celery

# Настройка приложения Celery
app = Celery(
    'my_project',
    broker='redis://localhost:6379/0',  # URL брокера
    backend='redis://localhost:6379/0'  # Хранилище результатов
)

# Конфигурация
app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True
)
```
Файл tasks.py
```angular2html
from celery_app import app

# Пример задачи
@app.task
def add(x, y):
    return x + y
```

**4. Запуск воркеров**

Запустите воркера для обработки задач:  
```angular2html
celery -A celery_app worker --loglevel=info
```
Результат должен быть похож на:  
```angular2html
[2024-11-24 12:00:00,000: INFO/MainProcess] Connected to redis://localhost:6379/0
[2024-11-24 12:00:00,000: INFO/MainProcess] Worker: Ready.
```

**5. Выполнение задач**

Создайте Python-скрипт для отправки задач:
```angular2html
from tasks import add

# Отправка задачи в очередь
result = add.delay(4, 6)

# Проверка выполнения
print(f"Task ID: {result.id}")
print(f"Task Status: {result.status}")

# Получение результата
if result.ready():
    print(f"Result: {result.get()}")
```

**Расширенные возможности**
**1. Планировщик задач (Celery Beat)**

Установка:
```angular2html
pip install celery[redis] django-celery-beat
```

Добавьте в проект celery_app.py и установите django-celery-beat. Это позволяет запускать задачи по расписанию (например, каждую минуту или в определенные дни).  

**2. Ретрай задач**

Иногда задачи могут завершаться с ошибками. Вы можете настроить автоматические повторные попытки:  
```angular2html
@app.task(bind=True, max_retries=3, default_retry_delay=10)
def unreliable_task(self):
    try:
        # Код задачи
        pass
    except Exception as exc:
        raise self.retry(exc=exc)
```

**3. Группировка задач**

Выполнение нескольких задач параллельно:  
```angular2html
from celery import group
from tasks import add

# Группа задач
task_group = group(add.s(2, 2), add.s(4, 4), add.s(6, 6))
result = task_group.apply_async()

# Результаты всех задач
print(result.get())

```

**4. Цепочки задач**

Выполнение задач последовательно:  
```angular2html
from celery import chain
from tasks import add

# Цепочка задач
task_chain = chain(add.s(2, 2) | add.s(4) | add.s(6))
result = task_chain.apply_async()

# Результат финальной задачи
print(result.get())
```

**5. Ретрай брокера**

Если брокер недоступен, Celery может настроить ретрай:
```angular2html
app.conf.broker_transport_options = {'visibility_timeout': 3600}
```

**6. Мониторинг (Flower)**

Flower — веб-интерфейс для мониторинга задач Celery.

Установка:
```angular2html
pip install flower
```
Запуск:
```angular2html
celery -A celery_app flower
```
Откройте http://localhost:5555 в браузере.

**Полезные команды**

Проверить подключение к брокеру:
```angular2html
celery -A celery_app inspect ping
```
Очистить очередь задач:
```angular2html
celery -A celery_app purge
```
Остановить воркеры:
```angular2html
celery -A celery_app control shutdown
```

**Базовая команда запуска Celery**
```angular2html
celery --app=<имя_приложения> worker [дополнительные_аргументы]
```

Аргументы и их описание:  
**1. --app=<имя_приложения>**

Указывает путь к объекту Celery, который инициализирует приложение.  

**Формат**:  
<имя_модуля>: имя файла без .py, например, celery_app, если объект находится в celery_app.py.  
<имя_модуля>:<имя_объекта>: если объект Celery в модуле имеет отличное имя, например, celery_app:custom_celery.

**Примеры**:
--app=celery_app  
--app=project.celery:app

**2. worker**

Команда для запуска Celery Worker.  
Обязательный аргумент: сообщает Celery, что мы запускаем именно worker (рабочий процесс для выполнения задач).  

**3. --loglevel=<уровень>**

Указывает уровень детализации логов.  
Доступные значения:  
**debug**: максимальная детализация (для отладки).  
**info** (по умолчанию): общая информация о задачах.  
**warning**: предупреждения.  
**error**: ошибки.  
**critical**: только критические ошибки.  
Пример:
```angular2html
celery --app=celery_app worker --loglevel=debug
```
**4. -Q, --queues=<очереди>**

Указывает конкретные очереди, которые должен обслуживать worker.  
Зачем:  
Если в вашем проекте есть несколько очередей, worker может обслуживать только те, которые вы указали.
Пример:
```angular2html
celery --app=celery_app worker --queues=default,high_priority
```

**5. -c, --concurrency=<число>**

Указывает число параллельных потоков/процессов worker.  
По умолчанию: количество ядер процессора.  
Пример:
```angular2html
celery --app=celery_app worker --concurrency=4
```

**6. -n, --hostname=<имя>**

Устанавливает уникальное имя для worker.  
Зачем:  
Если вы запускаете несколько worker на одном сервере, каждому нужно задать уникальное имя.  
Пример:
```angular2html
celery --app=celery_app worker --hostname=worker1@%h
```

**7. --autoscale=<макс>,<мин>**

Динамически меняет количество рабочих потоков.  
Формат: максимум_потоков,минимум_потоков.  
Пример:
```angular2html
celery --app=celery_app worker --autoscale=10,3
```

**8. --detach**

Запускает worker как фоновый процесс (демон).  
Пример:
```angular2html
celery --app=celery_app worker --detach
```

**9. --pidfile=<путь>**

Указывает путь для сохранения PID-файла worker.  
Зачем:  
Удобно для управления процессами worker.  
Пример:  
```angular2html
celery --app=celery_app worker --detach --pidfile=/var/run/celery/%n.pid
```


**10. --time-limit=<секунды>**

Устанавливает максимальное время выполнения задачи.  
Пример:
```angular2html
celery --app=celery_app worker --time-limit=300
```

**11. --soft-time-limit=<секунды>**

Устанавливает мягкий лимит времени выполнения задачи. После его истечения задача будет прервана аккуратно.  
Пример:
```angular2html
celery --app=celery_app worker --soft-time-limit=200
```

Полный пример команды
```angular2html
celery --app=celery_app worker \
  --loglevel=info \
  --concurrency=4 \
  --queues=default,priority \
  --hostname=worker1@%h \
  --autoscale=8,2 \
  --detach \
  --pidfile=/var/run/celery/%n.pid \
  --time-limit=300 \
  --soft-time-limit=200

```

Другие команды для Celery

Запуск задач в фоне:
```angular2html
celery --app=celery_app beat --loglevel=info
```
**beat**: запускает планировщик задач для выполнения периодических задач.

Очистка сообщений worker:
```angular2html
celery --app=celery_app purge
```

Мониторинг worker:
```angular2html
celery --app=celery_app status

```
Отмена выполнения задачи:
```angular2html
celery --app=celery_app control revoke <task_id>
```
**Пример проекта**
Файловая структура:
```angular2html
project/
├── celery_app.py  # Конфигурация Celery
└── tasks.py       # Определение задач

```

celery_app.py:
```angular2html
from celery import Celery

app = Celery('project_name', broker='redis://localhost:6379/0')

app.conf.update(
    result_backend='redis://localhost:6379/0',
    task_routes={
        'tasks.high_priority_task': {'queue': 'high_priority'},
        'tasks.default_task': {'queue': 'default'},
    }
)

app.autodiscover_tasks(['tasks'])

```

tasks.py:
```angular2html
from celery_app import app

@app.task
def default_task():
    print("Default task executed.")

@app.task
def high_priority_task():
    print("High priority task executed.")

```
Запуск worker:
```angular2html
celery --app=celery_app worker --loglevel=info --queues=default
```


**Заключение**

Celery — это мощный инструмент для асинхронной обработки задач. В этом гайде мы рассмотрели основы и продвинутые возможности. Вы можете настроить Celery под свои нужды, используя различные брокеры и бекенды, а также управлять сложными зависимостями задач.



