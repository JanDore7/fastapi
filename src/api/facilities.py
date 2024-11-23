
import json
from fastapi import Query, APIRouter, Body

from src.api.dependencies import PaginationDep, DBDep
from src.init import redis_manager
from src.schemas.facilities import FacilitiesAdd, Facilities


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получение списка услуг")
async def get_facilities(db: DBDep):
    facilities_from_cache = await redis_manager.get("facilities")
    print(f'{facilities_from_cache=}')
    if not facilities_from_cache:
        print("Иду в БД")
        facilities =  await db.facilities.get_all()
        facilities_schema: list[dict] = [f.model_dump() for f in facilities]
        facilities_json = json.dumps(facilities_schema)
        await redis_manager.set("facilities", facilities_json, expire=15)

        return facilities
    else:
        facilities_dicts = json.loads(facilities_from_cache)
        return facilities_dicts



@router.post("", summary="Создание услуги")
async def create_facilities(
        db: DBDep,
        data: FacilitiesAdd = Body(example='{"title": "Кондиционер"}')
        ):
    result = await db.facilities.add(data)
    await db.commit()
    return {"status": "OK", "facilities": result}