import shutil
from fastapi import APIRouter, UploadFile

from src.services.images import ImagesService
from src.tasks.tasks import test_task, resize_image

router = APIRouter(prefix="/images", tags=["Изображения отелей"])


# noinspection PyArgumentList
@router.post("")
def upload_image(file: UploadFile):
    ImagesService().upload_image(file)


