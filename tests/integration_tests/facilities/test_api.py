from src.schemas.facilities import FacilitiesAdd


async def test_add_hotel(db):
    facility_data = FacilitiesAdd(
        title="интернет",
    )
    new_facility_data = await db.facilities.add(facility_data)
    print(f"{new_facility_data=}")
    await db.commit()


async def test_get_facilities(ac):
    response = await ac.get(
        "/facilities",
    )
    assert response.status_code == 200
