import logging
from typing import List
from psycopg2 import DatabaseError, IntegrityError
from psycopg2._psycopg import connection
from app.entities.user import User


class UserRepository:
    def __init__(self, db_connection: connection):
        self.logger = logging.getLogger(__name__)
        self.db = db_connection()

    def create_user(self, user: User) -> User:
        self.logger.info("Starting operation to insert User in DataBase.")
        try:
            with self.db.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO users (id, name, email, password, created_at, users_status)
                    VALUES (%s, %s, %s, %s, NOW(), TRUE);
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

    def get_user_by_id(self, id: str) -> User:
        self.logger.info("Getting an User in DataBase")
        try:
            with self.db.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, name, email, password, created_at, updated_at, users_status
                    FROM users
                    WHERE id = %s
                    """,
                    (id,),
                )
                result = cursor.fetchone()

                if result == None:
                    raise ValueError(f"User not found with id {id}")
                
                return self.map_user_row_to_model(result)
        except DatabaseError as ex:
            self.logger.error(f"Failed to get User by id={id} in DataBase. Error: {ex}")
            raise

    def get_all_users(self) -> List[User]:
        self.logger.info("Getting all Users in DataBase")
        try:
            with self.db.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, name, email, password, created_at, updated_at, users_status
                    FROM users
                    """
                )
                result = cursor.fetchall()

                return [self.map_user_row_to_model(row) for row in result]
        except DatabaseError as ex:
            self.logger.error(f"Failed to get all Users in DataBase. Error: {ex}")
            raise

    def update_user(self, id: str, user: User) -> User:
        self.logger.info("Updating User in DataBase")
        try:
            with self.db.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE users
                    SET name = %s, email = %s, password = %s, updated_at = NOW(), users_status = %s
                    WHERE id = %s 
                    RETURNING id, name, email, password, created_at, updated_at, users_status;
                    """,
                    (user.name, user.email, user.password, user.users_status, id)
                )
                result = cursor.fetchone()

                if not result:
                    raise ValueError(f"User not found with id={id}")
                self.db.commit()
                self.logger.info(f"User {user.name} successfully updated")
                return self.map_user_row_to_model(result)
        except IntegrityError as ex:
            self.db.rollback()
            self.logger.error(f"Integrity error while updating User. User data: {user}. Details: {ex}")
            raise
        except DatabaseError as ex:
            self.db.rollback()
            self.logger.error(f"Failed to updating User in DataBase: {ex}")
            raise

    def delete_user(self, id: str):
        self.logger.info("Deleting User in DataBase")
        try:
            with self.db.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE users
                    SET users_status = FALSE, updated_at = NOW()
                    WHERE id = %s AND users_status = TRUE;
                    """,
                    (id,),
                )
                self.db.commit()
                if cursor.rowcount == 0:
                    raise KeyError(f"User id={id} not fund or alredy inactive.")
        except DatabaseError as ex:
            self.db.rollback()
            self.logger.error(f"Failed to delete in DataBase: {ex}")
            raise

    def map_user_row_to_model(self, row: List) -> User:
        return User(id=row[0], name=row[1], email=row[2], password=row[3], created_at=row[4], updated_at=row[5], users_status=row[6])
