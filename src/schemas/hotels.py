from pydantic import BaseModel, Field


class Hotel(BaseModel):
    title: str
    location: str

class HotelPATCH(BaseModel):
    title: str | None = Field(None, description="Описание отеля")
    location: str | None = Field(None, description="Адрес отеля")

