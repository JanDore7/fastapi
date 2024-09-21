from fastapi import FastAPI
import uvicorn

my_app = FastAPI()





if __name__ == "__main__":
    uvicorn.run("main:my_app", host="0.0.0.0", port=8000, reload=True, log_level="debug")