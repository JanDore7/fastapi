from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, BIGINT
from src.database import Base


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(200))
