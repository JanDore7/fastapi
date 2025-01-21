import shutil
from tempfile import NamedTemporaryFile
from fastapi import UploadFile

from src.services.base import BaseService
from src.tasks.tasks import test_task, resize_image


class ImagesService(BaseService):
    def upload_image(self, image_path: str, file: UploadFile):
        image_path = f"src/static/images/{file.filename}"
        with NamedTemporaryFile() as tmp_file:
            tmp_file.write(file.file.read())
            tmp_file.flush()
            shutil.copyfile(tmp_file.name, image_path)
        test_task.delay()
        resize_image.delay(image_path)