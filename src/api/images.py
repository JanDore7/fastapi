import shutil
from fastapi import APIRouter, UploadFile
from src.tasks.tasks import test_task, resize_image

router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post("")
def upload_image(file: UploadFile):
    with open(f"src/static/images/{file.filename}", "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)
        test_task.delay()
        resize_image.delay(
            "/home/dideb/my_utilities/my_projects/fastapi/src/static/images/Без имени.jpeg"
        )
