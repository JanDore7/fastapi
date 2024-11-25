# Подробный гайд о фоновых задачах в FastAPI

Фоновые задачи в FastAPI позволяют выполнять действия в фоновом режиме без блокировки обработки HTTP-запросов. Это полезно, например, для отправки email, записи логов, обработки данных или взаимодействия с внешними сервисами.    
**1. Что такое фоновые задачи в FastAPI?**

FastAPI предоставляет класс BackgroundTasks для простого выполнения задач в фоновом режиме. Суть работы заключается в передаче функции и аргументов, которые будут выполнены после обработки текущего запроса, но не будут блокировать возвращение ответа клиенту.  
**2. Установка и настройка**

Для работы с фоновыми задачами вам понадобится стандартная установка FastAPI. Убедитесь, что у вас установлены FastAPI и Uvicorn:
```angular2html
pip install fastapi uvicorn
```
**3. Простейший пример фоновой задачи**
```angular2html
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def write_log(message: str):
    with open("log.txt", "a") as log_file:
        log_file.write(f"{message}\n")

@app.post("/send-task/")
async def send_task(background_tasks: BackgroundTasks, message: str):
    background_tasks.add_task(write_log, message)
    return {"message": "Task submitted"}
```
Как это работает:

Параметр background_tasks автоматически передается FastAPI в обработчик запроса.  
Метод add_task добавляет функцию write_log с аргументом message в очередь задач.  
После завершения обработки запроса FastAPI выполняет задачу в фоновом режиме.  

**4. Расширение функциональности**
**4.1. Передача нескольких задач**

Вы можете добавлять несколько задач для одного запроса:
```angular2html
@app.post("/multiple-tasks/")
async def multiple_tasks(background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, "First task")
    background_tasks.add_task(write_log, "Second task")
    return {"message": "Multiple tasks submitted"}
```

Задачи будут выполнены последовательно.
**4.2. Использование асинхронных функций**

Если ваша фоновая задача использует асинхронные операции, вы можете передать асинхронную функцию:
```angular2html
import asyncio

async def async_task(message: str):
    await asyncio.sleep(2)  # Имитируем длительную операцию
    print(f"Async task: {message}")

@app.post("/async-task/")
async def async_background_task(background_tasks: BackgroundTasks, message: str):
    background_tasks.add_task(async_task, message)
    return {"message": "Async task submitted"}
```

**5. Интеграция с зависимостями**

Вы можете использовать фоновые задачи в комбинации с зависимостями:
```angular2html
from fastapi import Depends

def dependency_function():
    return "Data from dependency"

@app.post("/task-with-dependency/")
async def task_with_dependency(
    background_tasks: BackgroundTasks, 
    data: str = Depends(dependency_function)
):
    background_tasks.add_task(write_log, data)
    return {"message": "Task with dependency submitted"}
```

**6. Реальные сценарии использования**
**6.1. Отправка email**

```angular2html
from smtplib import SMTP

def send_email(to: str, subject: str, body: str):
    with SMTP("localhost") as smtp:
        smtp.sendmail("noreply@example.com", to, f"Subject: {subject}\n\n{body}")

@app.post("/send-email/")
async def send_email_task(background_tasks: BackgroundTasks, to: str, subject: str, body: str):
    background_tasks.add_task(send_email, to, subject, body)
    return {"message": "Email task submitted"}
```

**6.2. Обновление кэша**
```angular2html
cache = {}

def update_cache(key: str, value: str):
    cache[key] = value

@app.post("/update-cache/")
async def update_cache_task(background_tasks: BackgroundTasks, key: str, value: str):
    background_tasks.add_task(update_cache, key, value)
    return {"message": "Cache update task submitted"}
```

**7. Советы по использованию**

Не используйте задачи для критичных операций. Если выполнение фоновой задачи необходимо для корректного завершения запроса (например, запись в базу данных), лучше сделать это синхронно или асинхронно до возвращения ответа.
Контроль ошибок. Фоновые задачи не предоставляют встроенного механизма для обработки ошибок. Оберните вашу задачу в try/except, чтобы избежать неожиданного завершения.
Мониторинг. Используйте логи или инструменты мониторинга для отслеживания выполнения фоновых задач.


**Заключение**

Фоновые задачи в FastAPI — это удобный инструмент для выполнения простых операций в фоне. Для более сложных сценариев рекомендуется использовать интеграцию с очередями задач. Используйте BackgroundTasks для оптимизации работы приложений без значительного усложнения кода.