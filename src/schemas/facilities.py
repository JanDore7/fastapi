from pydantic import BaseModel, Field, ConfigDict


class FacilitiesAdd(BaseModel):
    title: str = Field(..., description="Описание услуги")

class Facilities(FacilitiesAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
