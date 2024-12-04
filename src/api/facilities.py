from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep

from src.schemas.facilities import FacilitiesAdd


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получение списка услуг")
# @cache(expire=10)
async def get_facilities(db: DBDep):
    print("Иду в базу данных")
    return await db.facilities.get_all()


@router.post("", summary="Создание услуги")
async def create_facilities(
    db: DBDep, data: FacilitiesAdd = Body(example='{"title": "Кондиционер"}')
):
    result = await db.facilities.add(data)
    await db.commit()
    return {"status": "OK", "facilities": result}
