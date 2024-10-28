from pydantic import BaseModel, Field, ConfigDict


class RoomsPut(BaseModel):
    title: str  = Field(description="Название комнаты")
    description: str = Field(description="Описание комнаты")
    price: int  = Field(description="Цена комнаты")
    quantity: int = Field(description="Количество комнат")

class RoomsAdd(RoomsPut):
    hotel_id: int = Field(..., description="ID отеля")
    model_config = ConfigDict(from_attributes=True)

class Rooms(RoomsAdd):
    id: int = Field(..., description="ID комнаты")

class RoomsPatch(BaseModel):
    title: str | None = Field(None, description="Название комнаты")
    description: str | None = Field(None, description="Описание комнаты")
    price: int | None = Field(None, description="Цена комнаты")
    quantity: int | None = Field(None, description="Количество комнат")