import logging
from typing import List
from app.repositories.user_repository import UserRepository
from app.entities.user import User


class UserService:
    def __init__(self, storage: UserRepository):
        self.logger = logging.getLogger(__name__)
        self.repository = storage

    def create_user(self, user: User):
        self.logger.info(f"Creating User with this data={user}")
        return self.repository.create_user(user)

    def get_user_by_id(self, id: str) -> User:
        self.logger.info(f"Getting customer with this id={id}")
        return self.repository.get_user_by_id(id)

    def get_all_users(self) -> List[User]:
        self.logger.info(f"Getting all Users")
        return self.repository.get_all_users()

    def update_user(self, id: str, user: User) -> User:
        self.logger.info(f"Updated User with this id={id}")
        return self.repository.update_user(id, user)

    def delete_user(self, id: str):
        self.logger.info(f"Deleting User with id={id}")
        self.repository.delete_user(id)
