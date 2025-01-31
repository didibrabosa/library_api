from fastapi import FastAPI
from app.controller import user_controller

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Library API is up and running!"}


app.include_router(user_controller.router)
