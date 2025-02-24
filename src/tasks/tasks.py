import asyncio
import logging
from time import sleep
from PIL import Image
import os

from src.database import async_session_null_pool
from src.tasks.celery_app import celery_app_instance
from src.utils.db_manager import DBManager


@celery_app_instance.task
def test_task():
    sleep(5)
    print("Я закончил работу")


@celery_app_instance.task
def resize_image(image_path: str):
    logging.debug(f"Функция вызывается {image_path=}")
    """
    Изменяет разрешение изображения
    :param image_path:
    :return:
    """
    sizes = [1000, 500, 200]
    output_folder = "src/static/images"

    image = Image.open(image_path)

    # Получаем имя файла и его расширение
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    for size in sizes:
        # сжимаем изображение
        img_resized = image.resize(
            (size, int(image.height * (size / image.width))), Image.Resampling.LANCZOS
        )

        # Формируем новое имя файла
        new_name = f"{name}_{size}px{ext}"

        # Полный путь к новому изображению
        output_path = os.path.join(output_folder, new_name)

        # сохраняем изображение
        img_resized.save(output_path)
    logging.info(
        f"Изображение сохранено в следующих размерах: {sizes} в папке {output_folder}"
    )


async def get_bookings_with_to_day_checkin_helper():
    """
    Функция получения бронирований с сегодняшним заселением
    return:
    """
    logging.info("Запустилась")
    async with DBManager(session_factory=async_session_null_pool) as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()
        logging.debug(f"{bookings=}")


@celery_app_instance.task(name="booking_to_day_checkin")
def send_email_to_users_with_to_day_checkin():
    """
    задача на периодическое получение данных. (Настройка в celery_app.py)
    :return:
    """
    asyncio.run(get_bookings_with_to_day_checkin_helper())
