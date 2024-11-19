from pydantic import BaseModel, Field, ConfigDict

from src.schemas.facilities import Facilities


class RoomsAddRequest(BaseModel):
    title: str = Field(description="Название комнаты")
    description: str | None = Field(None, description="Описание комнаты")
    price: int = Field(description="Цена комнаты")
    quantity: int = Field(description="Количество комнат")
    facilities_ids: list[int] | None = Field([], description="ID услуг")


class RoomsAdd(BaseModel):
    title: str = Field(description="Название комнаты")
    description: str | None = Field(None, description="Описание комнаты")
    price: int = Field(description="Цена комнаты")
    quantity: int = Field(description="Количество комнат")
    hotel_id: int = Field(..., description="ID отеля")


class Room(RoomsAdd):
    id: int = Field(..., description="ID комнаты")

    model_config = ConfigDict(from_attributes=True)

class RoomWithRelationship(Room):
    facilities: list[Facilities]


class RoomsPatchRequest(BaseModel):
    title: str | None = Field(None, description="Название комнаты")
    description: str | None = Field(None, description="Описание комнаты")
    price: int | None = Field(None, description="Цена комнаты")
    quantity: int | None = Field(None, description="Количество комнат")
    facilities_ids: list[int] | None = Field([], description="ID услуг")



class RoomsPatch(BaseModel):
    hotel_id: int | None = Field(None, description="ID отеля")
    title: str | None = Field(None, description="Название комнаты")
    description: str | None = Field(None, description="Описание комнаты")
    price: int | None = Field(None, description="Цена комнаты")
    quantity: int | None = Field(None, description="Количество комнат")
