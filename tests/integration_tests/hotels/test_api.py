async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels",
        params={"date_from": "2023-01-01", "date_to": "2023-01-02"},
    )
    assert response.status_code == 200
