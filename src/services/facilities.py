from src.schemas.facilities import FacilitiesAdd
from src.services.base import BaseService


class FacilityService(BaseService):
    async def create_facilities(self, data: FacilitiesAdd):
        result = await self.db.facilities.add(data)
        await self.db.commit()
        return result