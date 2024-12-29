from pydantic import BaseModel, EmailStr, Field
import ulid

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(ulid.new()))
    name: str
    email: EmailStr
    password: str