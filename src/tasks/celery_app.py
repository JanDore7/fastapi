from celery import Celery


from src.config import settings


celery_app_instance = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=[
        "src.tasks.tasks",
    ],
    backend=settings.REDIS_URL,
)

# С помощью beat_schedule вы задаёте, какие задачи и с какой периодичностью должны выполняться.
celery_app_instance.conf.beat_schedule = {
    "luboe-nazvanie": {
        "task": "booking_to_day_checkin",
        "schedule": 30,
    },
}

# Запуск celery --app=src.tasks.celery_app:celery_app_instance worker
# Запуск beat: celery --app=src.tasks.celery_app:celery_app_instance beat
# Для запуска и worker и beat celery --app=src.tasks.celery_app:celery_app_instance worker --beat
# celery --app=src.tasks.celery_app:celery_app_instance worker -l info -B
