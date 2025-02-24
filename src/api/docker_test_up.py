from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Проверка контейнера"])


@router.get("/health")
def health():
    return {"status": "ok"}