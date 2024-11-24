from time import sleep

from src.tasks.celery_app import celery_app_instance


@celery_app_instance.task
def test_task():
    sleep(5)
    print("Я закончил работу")
