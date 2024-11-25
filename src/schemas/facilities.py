from pydantic import BaseModel, Field, ConfigDict


class FacilitiesAdd(BaseModel):
    title: str = Field(..., description="Описание услуги")


class Facilities(FacilitiesAdd):
    id: int


class RoomFacilityAdd(BaseModel):
    rooms_id: int
    facilities_id: int


class RoomFacility(RoomFacilityAdd):
    id: int
