from typing import List
import logging
from fastapi import APIRouter, HTTPException, Response
from app.services.user_service import UserService
from app.entities.user import User

router = APIRouter()
logger = logging.getLogger(__name__)
user_service = UserService()

@router.post("/users", response_model=User)
def create_user(user : User):
    try:
        logger.info(f"Creating User with this data={user}")
        created_user = user_service.create_user(user)

        logger.info(f"Create User request finished with response={created_user}")
        return created_user
    
    except Exception as ex:
        logger.error(f"An error occurred while creating the User: {ex}")
        raise HTTPException(status_code=500, detail="Failed to create User.")
    
@router.get("/users/{id}", response_model=User)
def get_user_by_id(id: str):
    try:
        logger.info(f"Geting User with id={id}")
        geted_user = user_service.get_user_by_id(id)

        logger.info(f"Geting User request finished with response={geted_user}")
        return geted_user
    
    except ValueError as ex:
        logger.warning(f"User not found: {ex}")
        raise HTTPException(status_code=404, detail="Failed to get User")
    
@router.get("/users/", response_model=List[User])
def get_all_users():
    logger.info(f"Getting all Users")
    geted_users = user_service.get_all_users()

    logger.info(f"Get all Users request finished with response={geted_users}")
    return geted_users
