from google.cloud import firestore
from uuid import uuid4
from passlib.context import CryptContext
from src.collab_tasks_backend.models.user import UserCreate

db = firestore.Client()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(user_create: UserCreate):
    user_id = str(uuid4())
    hashed_password = pwd_context.hash(user_create.password)
    user_data = {
        "id": user_id,
        "username": user_create.username,
        "email": user_create.email,
        "hashed_password": hashed_password,
    }
    db.collection("users").document(user_id).set(user_data)
    return {"msg": "Usuario registrado", "user_id": user_id}

def get_user_by_email(email: str):
    users = db.collection("users").where("email", "==", email).get()
    if users:
        return users[0].to_dict()
    return None
