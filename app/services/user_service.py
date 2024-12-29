import logging
from app.repositories.user_repository import UserRepository
from app.entities.user import User

class UserService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.repository = UserRepository()
    
    def create_user(self, user: User):
        self.logger.info(f"Creating User with this data={user}")
        return self.repository.create_user(user)