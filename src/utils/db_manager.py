from src.repos.facilities import FacilitiesRepository, RoomsFacilitiesRepository
from src.repos.usres import UserRepository
from src.repos.hotels import HotelRepository
from src.repos.rooms import RoomsRepository
from src.repos.booking import BookingRepository


class DBManager:
    """
    Класс DBManager управляет сессией базы данных и предоставляет доступ к репозиториям для различных сущностей.

    Он используется для управления сессией базы данных и обеспечивания транзакций с использованием асинхронных
    методов. Класс создаёт репозитории для работы с пользователями, отелями, номерами, бронированиями и удобствами,
    используя сессию базы данных.

    Атрибуты:
        session_factory (callable): Фабрика для создания сессий с базой данных.
        session (AsyncSession): Асинхронная сессия для взаимодействия с базой данных.
        users (UserRepository): Репозиторий для работы с пользователями.
        hotels (HotelRepository): Репозиторий для работы с отелями.
        rooms (RoomsRepository): Репозиторий для работы с номерами.
        bookings (BookingRepository): Репозиторий для работы с бронированиями.
        facilities (FacilitiesRepository): Репозиторий для работы с удобствами.
        rooms_facilities (RoomsFacilitiesRepository): Репозиторий для работы с удобствами номеров.
    """

    def __init__(self, session_factory):
        """
        Инициализация DBManager с фабрикой сессий.
        Args: session_factory (callable): Фабрика для создания сессий с базой данных.
        """
        self.session_factory = session_factory

    async def __aenter__(self):
        """
        Метод для асинхронного входа в контекстный менеджер.
        Создаёт сессию базы данных и инициализирует репозитории для работы с различными сущностями.
        Returns: DBManager: Возвращает сам объект DBManager с доступом к репозиториям.
        """
        # Создаём асинхронную сессию базы данных
        self.session = self.session_factory()

        # Инициализируем репозитории
        self.users = UserRepository(self.session)
        self.hotels = HotelRepository(self.session)
        self.rooms = RoomsRepository(self.session)
        self.bookings = BookingRepository(self.session)
        self.facilities = FacilitiesRepository(self.session)
        self.rooms_facilities = RoomsFacilitiesRepository(self.session)

        # Возвращаем объект DBManager для использования в контекстном менеджере
        return self

    async def __aexit__(self, *args):
        """
        Метод для асинхронного выхода из контекстного менеджера.
        Осуществляет откат изменений в сессии и закрытие сессии после выполнения операций.
        """
        # Откат всех изменений в сессии
        await self.session.rollback()
        # Закрытие сессии
        await self.session.close()

    async def commit(self):
        """
            Метод для коммита транзакции в базе данных.
            Сохраняет изменения в базе данных, сделанные в рамках текущей сессии.
        """
        await self.session.commit()
