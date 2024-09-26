import logging

def setup_logging() -> None:
    """
    Настройка логирования, добавляет обработчики записи логов в файл и в консоль.
    Создает два обработчика:
        - handler_file для записи логов в файл 'app.log' с уровнем DEBUG
        - handler_console для вывода логов в консоль с уровнем INFO
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Устанавливаем уровень логирования для логгера

    # Создание обработчика для записи логов в файл
    handler_file = logging.FileHandler('app.log')
    handler_file.setLevel(logging.WARNING)  # Устанавливаем уровень для файла
    formatter_file = logging.Formatter('%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]')
    handler_file.setFormatter(formatter_file)

    # Создание обработчика для вывода логов в консоль
    handler_console = logging.StreamHandler()
    handler_console.setLevel(logging.INFO)  # Устанавливаем уровень для консоли
    formatter_console = logging.Formatter('%(levelname)s (%(asctime)s): %(message)s')
    handler_console.setFormatter(formatter_console)

    # Добавление обработчиков к логгеру
    logger.addHandler(handler_file)
    logger.addHandler(handler_console)