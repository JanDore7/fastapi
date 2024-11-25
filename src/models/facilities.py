from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from src.database import Base


class FacilitiesOrm(Base):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    rooms: Mapped[list["RoomsOrm"]] = relationship(
        back_populates="facilities", secondary="rooms_facilities"
    )


class RoomFacilitiesOrm(Base):
    __tablename__ = "rooms_facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    rooms_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    facilities_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))
