class NabronirovalException(Exception):
    detail: str = "какая-то ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail: str = "Объект не найден"
