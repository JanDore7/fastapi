import pytest

from src.database import async_session_null_pool
from src.utils.db_manager import DBManager


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2025-08-01", "2025-08-10", 200),
        (1, "2025-08-01", "2025-08-10", 200),
        (1, "2025-08-01", "2025-08-10", 200),
        (1, "2025-08-01", "2025-08-10", 200),
        (1, "2025-08-01", "2025-08-10", 200),
        (1, "2025-08-01", "2025-08-10", 500),
        (1, "2025-09-01", "2025-09-10", 200),
    ],
    # Даем название тесту
    ids=[
        "Valid case 1",
        "Valid case 2",
        "Valid case 3",
        "Valid case 4",
        "Valid case 5",
        "Invalid case (500 status)",
        "Valid case with different dates",
    ],
)
async def test_add_booking(
    db, authenticated_ac, room_id, date_from, date_to, status_code
):
    room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    print(f"{response.text=}")
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res


@pytest.fixture(scope="session")
async def delete_all_bookings():
    async with DBManager(session_factory=async_session_null_pool) as db_:
        await db_.bookings.delete()
        await db_.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, amount",
    [
        (1, "2024-08-01", "2024-08-10", 1),
        (1, "2024-08-02", "2024-08-11", 2),
        (1, "2024-08-01", "2024-08-05", 3),
    ],
)
async def test_add_and_get_bookings(
    room_id, date_from, date_to, amount, db, authenticated_ac, delete_all_bookings
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    res = response.json()
    assert isinstance(res, dict)
    assert res["status"] == "OK"
    assert "data" in res
