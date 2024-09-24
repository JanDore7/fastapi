from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "Сочи"},
    {"id": 2, "title": "Дубай", "name": "Дубай"},
    {"id": 3, "title": "New York", "name": "Нью-Йорк"}
    ]


@app.get("/hotels")
async def get_hotels(name: str | None = Query(None, description="Название отеля" )):
    if name in [hotel["name"] for hotel in hotels]:
        return next(hotel for hotel in hotels if hotel["name"] == name)
    return hotels


@app.delete("/hotels/{hotel_name}")
async def delete_hotel(hotel_name: str):
    global hotels
    print(hotel_name)
    hotels = [hotel for hotel in hotels if hotel["name"] != hotel_name]
    return {"status": "ok"}


@app.post("/hotels")
async def create_hotel(hotel: dict = Body()):
    global hotels
    hotels.append(
        {
            "id": len(hotels) + 1,
            "title": hotel["title"],
            "name": hotel["name"]
        }
    )
    return {"status": "ok"}


@app.put("/hotels/{hotel_id}")
async def update_hotel(hotel_id: int, hotel: dict = Body(..., example={"title": "New York", "name": "Нью-Йорк"})):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    hotels.append(
        {
            "id": hotel_id,
            "title": hotel["title"],
            "name": hotel["name"]
        }
    )
    return {"status": "ok", "hotel": hotel}


@app.patch("/hotels/{hotel_id}")
async def patch_hotel(hotel_id: int, data_hotel: dict = Body(..., description="Новые данные отеля")):
    global hotels
    if len(data_hotel) < 2:
        for hotel in hotels:
            if hotel["id"] == hotel_id:
                if "title" in data_hotel:
                    hotel["title"] = data_hotel["title"]
                if "name" in data_hotel:
                    hotel["name"] = data_hotel["name"]
                    return {"status": "ok", "hotel": hotel }
    else:
        await update_hotel(hotel_id, data_hotel)
        return {"status": "ok", "hotel": hotels}








if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)