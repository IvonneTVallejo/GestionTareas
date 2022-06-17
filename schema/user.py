
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserSchema(BaseModel):
    id: Optional[str]
    name: str
    username: str
    email: EmailStr
    password: str

class DataUser(BaseModel):
    username: str
    password: str