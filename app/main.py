import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config.db import get_db_connection
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.controller.user_controller import router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_connection = get_db_connection()
    user_repository = UserRepository(db_connection=db_connection)
    user_service = UserService(user_repository)

    yield {"user_service": user_service}

    logger.info("Shutdown application")


app = FastAPI(
    lifespan=lifespan
)


app.include_router(router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}
