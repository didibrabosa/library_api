from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
import ulid


class User(BaseModel):
    id: str = Field(default_factory=lambda: str(ulid.new()))
    name: str
    email: EmailStr
    password: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default=None)
    users_status: bool = Field(default=True)
