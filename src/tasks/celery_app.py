from celery import Celery


from src.config import settings


celery_app_instance = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=[
        "src.tasks.tasks",
    ],
)

# Запуск celery --app=src.tasks.celery_app:celery_app_instance worker
