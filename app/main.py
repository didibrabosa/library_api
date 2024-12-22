from fastapi import FastAPI
from app.controller import users

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Library API is up and running!"}

app.include_router(users.router)


