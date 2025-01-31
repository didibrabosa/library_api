from typing import List, Annotated
import logging
from fastapi import APIRouter, HTTPException, Response, Depends, Request
from app.services.user_service import UserService
from app.entities.user import User

router = APIRouter()
logger = logging.getLogger(__name__)


def get_user_service(requests: Request):
    return requests.state.user_service


ServiceDep = Annotated[UserService, Depends(get_user_service)]


@router.post("/users", response_model=User)
def create_user(user: User, service: ServiceDep):
    try:
        logger.info(f"Creating User with this data={user}")
        created_user = service.create_user(user)

        logger.info(f"Create User request finished with response={created_user}")
        return created_user

    except Exception as ex:
        logger.error(f"An error occurred while creating the User: {ex}")
        raise HTTPException(status_code=500, detail="Failed to create User.")


@router.get("/users/{id}", response_model=User)
def get_user_by_id(id: str, service: ServiceDep):
    try:
        logger.info(f"Geting User with id={id}")
        geted_user = service.get_user_by_id(id)

        logger.info(f"Geting User request finished with response={geted_user}")
        return geted_user

    except ValueError as ex:
        logger.warning(f"User not found: {ex}")
        raise HTTPException(status_code=404, detail="Failed to get User")


@router.get("/users", response_model=List[User])
def get_all_users(service: ServiceDep):
    logger.info("Getting all Users")
    geted_users = service.get_all_users()

    logger.info(f"Get all Users request finished with response={geted_users}")
    return geted_users


@router.put("/users/{id}", response_model=User)
def update_user(id: str, user: User, service: ServiceDep):
    try:
        logger.info(f"Updating User with this id={id}")
        updated_user = service.update_user(id, user)

        logger.info(f"Update User request finished with response={updated_user}")
        return updated_user

    except ValueError as ex:
        logger.warning(f"User not found: {ex}")
        raise HTTPException(status_code=404, detail="Failed to update User")


@router.delete("/users/{id}")
def delete_user(id: str, service: ServiceDep):
    try:
        logger.info(f"Deleting User with id={id}")
        service.delete_user(id)

        logger.info("Delete custumer request finished with response=204")
        return Response(status_code=204)

    except KeyError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
