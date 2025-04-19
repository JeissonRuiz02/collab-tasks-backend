# src/collab_tasks_backend/models/user.py

from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: str
    username: str
    email: EmailStr
    hashed_password: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserInDB(User):
    hashed_password: str
