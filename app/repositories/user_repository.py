import logging
from psycopg2 import DatabaseError, IntegrityError
from app.services.db import get_db_connection
from app.entities.user import User

class UserRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db = get_db_connection()

    def create_user(self, user: User) -> User:
        self.logger.info("Starting operation to insert User into the database.")
        try:
            with self.db.cursor() as cursor:
                cursor.execute(
                """
                INSERT INTO users (id, name, email, password)
                VALUES (%s, %s, %s, %s)
                """,
            (user.id, user.name, user.email, user.password),
        )
            self.db.commit()
            self.logger.info(f"User {user.name} successfully inserted.")
            return user
        
        except IntegrityError as ex:
            self.db.rollback()
            self.logger.error(f"Integrity error while inserting User. User data: {user}. Details: {ex}")
            raise
        except DatabaseError as ex:
            self.db.rollback()
            self.logger.error(f"Failed to created User in DataBase: {ex}")
            raise
