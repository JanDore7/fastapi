from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, BIGINT
from src.database import Base


class HotelsOrm(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str]
