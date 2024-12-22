from fastapi import APIRouter
from app.services.db import get_db_connection
from app.entities.user import User

router = APIRouter()

@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()

    if user_data is None:
        return {"error": "User not found"}
    
    return User(id=user_data[0], name=user_data[1], email=user_data[2], password=user_data[3])