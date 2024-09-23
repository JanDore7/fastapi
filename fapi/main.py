from fastapi import FastAPI, Query
import uvicorn

my_app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "Сочи"},
    {"id": 2, "title": "Дубай", "name": "Дубай"},
    {"id": 3, "title": "New York", "name": "Нью-Йорк"}
    ]

@my_app.get("/hotels/{id_hotel}")
def get_hotels(
        title: str = Query(..., description="Название отеля")
):
    for hotel in hotels:
        if hotel["title"] == title:
            print(hotel)
            return hotel





if __name__ == "__main__":
    uvicorn.run("main:my_app", host="127.0.0.1", port=8000, reload=True, log_level="debug")