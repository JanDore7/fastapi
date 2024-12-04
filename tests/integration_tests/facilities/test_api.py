from src.schemas.facilities import FacilitiesAdd


async def test_create_facilities(ac):
    data = FacilitiesAdd(title="Кондиционер")
    response = await ac.post("/facilities", json=dict(**data.model_dump()))
    assert response.status_code == 200


async def test_get_facilities(ac):
    response = await ac.get(
        "/facilities",
    )
    assert response.status_code == 200
