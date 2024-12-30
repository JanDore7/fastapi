from datetime import date

from fastapi import HTTPException


class NabronirovalException(Exception):
    detail: str = "какая-то ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail: str = "Объект не найден"


class AllRoomsByBookedException(NabronirovalException):
    detail: str = "Нет свободных номеров"


class ObjectAlreadyExistsException(NabronirovalException):
    detail: str = "Объект уже существует"


class DateErrorException(NabronirovalException):
    detail: str = "Ошибка при установке дат!!"


def check_date_correct(date_from: date, date_to: date) -> None:
    if date_from >= date_to:
        raise HTTPException(status_code=422, detail="Ошибка при установке дат")


class NameErrorHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(NameErrorHTTPException):
    status_code = 404
    detail = "Отеля не найден"


class RoomsNotFoundHTTPException(NameErrorHTTPException):
    status_code = 404
    detail = "Комната не найдена"
