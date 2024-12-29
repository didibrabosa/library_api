import logging
from fastapi import APIRouter, HTTPException, Response
from app.services.user_service import UserService
from app.entities.user import User

router = APIRouter()
logger = logging.getLogger(__name__)
user_service = UserService()

@router.post("/users", response_model=User)
def create_user(user_data : User):
    try:
        logger.info(f"Creating user with this data={user_data}")
        created_user = user_service.create_user(user_data)
        logger.info(f"Create user request finished with response={created_user}")
        return created_user
    except Exception as e:
        logger.error(f"An error occurred while creating the user: {e}")
        raise HTTPException(status_code=500, detail="Failed to create user.")