from fastapi import APIRouter
from fastapi import Query, APIRouter, Body

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.facilities import FacilitiesAdd, Facilities


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получение списка услуг")
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("", summary="Создание услуги")
async def create_facilities(
        db: DBDep,
        data: FacilitiesAdd = Body(example='{"title": "Кондиционер"}')
        ):
    result = await db.facilities.add(data)
    await db.commit()
    return {"status": "OK", "facilities": result}