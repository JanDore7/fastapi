from typing import Callable, Any, Union, Sequence
import functools
import time
import asyncio
import logging
from logger_config import setup_logging


setup_logging()
logger = logging.getLogger(__name__)


def meta_func(func: Callable[..., Any], *args: Any, **kwargs: Any) -> str:
    """Возвращает строку с именем функции и ее аргументами.
    Parameters:
        func (callable): Функция, для которой выводится имя.
        *args: Позиционные аргументы, переданные в функцию. Не обязательный аргумент
        **kwargs: Именованные аргументы, переданные в функцию. Не обязательный аргумент
    Returns:
        str: Имя функции с аргументами, если они есть, иначе только имя функции."""

    if args:
        return f"{func.__name__}{args}"
    elif kwargs:
        return f"{func.__name__}{kwargs}"
    else:
        return f"{str(func.__name__).upper()}"


# Универсальный декоратор (см. Readme)
def decor(func: Callable[..., Any]) -> Callable[..., Any]:
    """Декоратор для измерения времени выполнения функции.

      :param func: Функция, которую нужно обернуть декоратором.
    Returns:
      str: лог с информацией о том для какой функции происходило измерение и какие аргументы были функцией приняты
    """

    @functools.wraps(func)
    async def timekeeping_async(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = await func(*args, **kwargs)
        logger.info(
            f"Обработка запроса для {meta_func(func, *args, **kwargs)} заняла {time.time() - start_time:.2f} сек"
        )

        return result

    @functools.wraps(func)
    def timekeeping(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        logger.info(
            f"Обработка запроса для {meta_func(func, *args, **kwargs)} заняла {time.time() - start_time:.2f} сек"
        )

        return result

    if asyncio.iscoroutinefunction(func):
        return timekeeping_async

    else:
        return timekeeping


@decor
def exemple(query: str) -> None:
    """Имитирует запрос к базе данных
    Parameters:
        query (str): Запрос, для которого нужно получить данные. Могут быть следующие значения:
            - 'Сочи': вызывает задержку в 5 секунд
            - 'Москва': вызывает задержку в 9 секунд
            - 'Уфа': вызывает задержку в 3 секунды
    Returns:
        None: Функция ничего не возвращает. Она только выводит сообщения на экран.
    """

    print(f"Запрашиваю данные для {query}")
    if query == "Сочи":
        time.sleep(5)
    if query == "Москва":
        time.sleep(9)
    if query == "Уфа":
        time.sleep(3)

    return print(f"Получены данные для {query}")


# ---------------Sync----------------


@decor
def main() -> None:
    """Основная функция для выполнения запросов.
    Returns:
        None
    """
    try:
        exemple("Уфа")
        exemple(query="Москва")
        exemple()
    except Exception as e:
        logger.error(f"Error {e}", exc_info=True)


# ----------------Async----------------
# ---gather---


@decor
async def exemple_async(query: str) -> Union[str, None]:
    """Имитирует асинхронный запрос к базе данных
    Parameters:
        query (str): Запрос, для которого нужно получить данные. Могут быть следующие значения:
            - 'Сочи': вызывает задержку в 5 секунд
            - 'Москва': вызывает задержку в 9 секунд
            - 'Уфа': вызывает задержку в 3 секунды
    Returns:
        None: Функция ничего не возвращает. Она только выводит сообщения на экран.
    """
    print(f"Запрашиваю данные для {query}")
    if query == "Сочи":
        await asyncio.sleep(5)
    if query == "Москва":
        await asyncio.sleep(9)
    if query == "Уфа":
        await asyncio.sleep(3)

    return print(f"Получены данные для {query}")


@decor
async def async_gather() -> Sequence[Any]:
    """Асинхронная основная функция для выполнения запросов при помощи asyncio.gather().
    Returns:
        List[Union[str, None]]: Список результатов асинхронных запросов,
        где каждый элемент может быть строкой или None.
    """
    result = await asyncio.gather(
        exemple_async("Москва"),
        exemple_async(),
        exemple_async("Уфа"),
        return_exceptions=True,
    )
    print(f"Результат работы функции {__name__}: {result}, {type(result)}")
    return result


# ---create_task---


@decor
async def async_task() -> Union[str, None]:
    """Асинхронная функция, создающая и выполняющая две задачи с использованием asyncio.create_task.
    Задачи имитируют асинхронные запросы к базе данных с различными задержками. После создания задач выводится
    информация о том, завершены ли задачи, затем задачи дожидаются завершения.
    Returns:
        None
    """

    task_1 = asyncio.create_task(exemple_async("Москва"), name="Москва")
    task_2 = asyncio.create_task(exemple_async("Уфа"), name="Уфа")
    task_3 = asyncio.create_task(exemple_async(), name="Ошибка")
    task_4 = asyncio.create_task(exemple_async("Сочи"), name="Сочи")

    print(f"Отменяем задачу №3 {task_3.cancel()}, {task_3.done()}")
    try:
        await task_3  # Ожидание завершения задачи
    except asyncio.CancelledError:
        logger.warning("Задача была отменена")

    if task_4.done():
        res4 = task_4.result()
        print(f"Результат работы задачи №4 {res4}")
    else:
        print("Задача №4 еще обрабатывается")

    logger.info(
        f"Состояние задачи №1 {task_1.done()} | Состояние задачи №2 {task_2.done()} | Состояние задачи №4 {task_4.done()}"
    )
    res2 = await task_2

    logger.info(
        f"Состояние задачи №1 {task_1.done()} | Состояние задачи №2 {task_2.done()} | Состояние задачи №4 {task_4.done()}"
    )
    res1 = await task_1

    if task_4.done():
        res4 = task_4.result()
        print(f"Результат работы задачи №4 {res4}")
        return print(
            f"РЕЗУЛЬТАТЫ РАБОТЫ ФУНКЦИИ {__name__} ЗАДАЧА№1 {res1}, ЗАДАЧА№2 {res2}, ЗАДАЧА№4 {res4}"
        )


# ---as_completed---


@decor
async def as_complete_main() -> None:
    tasks = [
        exemple_async("Москва"),
        exemple_async("Уфа"),
        # exemple_async(),
        exemple_async("Сочи"),
    ]

    try:
        for task in asyncio.as_completed(tasks):
            result = await task
            print(f"Задача выполнена {result}")
    except Exception as e:
        logger.error(f"Ошибка {e}")


# ---wait---


@decor
async def wait_man() -> None:
    tasks = [
        asyncio.create_task(exemple_async("Москва"), name="Москва"),
        asyncio.create_task(exemple_async("Уфа"), name="Уфа"),
        # asyncio.create_task(exemple_async(), name='Ошибка'),
        asyncio.create_task(exemple_async("Сочи"), name="Сочи"),
    ]

    done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
    print(f"{done=}")
    print(f"{pending=}")

    for task in done:
        print(f"Задача выполнена {task}")


if __name__ == "__main__":
    # main()
    # asyncio.run(async_gather())
    # asyncio.run(async_task())
    # asyncio.run(as_complete_main())
    asyncio.run(wait_man())
