import os

from fastapi import HTTPException

import firestore

from src.collab_tasks_backend import config
from google.cloud import firestore
from datetime import datetime
import uuid

from src.collab_tasks_backend.auth.security import pwd_context
from src.collab_tasks_backend.models.task import Task
from src.collab_tasks_backend.models.user import UserCreate

db = firestore.Client(
    project=os.getenv("GCP_PROJECT_ID"),
    database="(default)"
)
collection = db.collection("tasks")

def create_task(task_data, user_id: str):
    task_id = str(uuid.uuid4())
    task_dict = task_data.dict()
    task_dict.update({
        "id": task_id,
        "user_id": user_id,
        "status": "pending",
        "created_at": datetime.utcnow()
    })
    collection.document(task_id).set(task_dict)
    return task_dict

def update_task(task_id: str, updated_data: Task, user_id: str):
    doc_ref = collection.document(task_id)
    doc = doc_ref.get()

    if not doc.exists:
        return None

    task = doc.to_dict()
    if task["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="No autorizado para modificar esta tarea")

    doc_ref.update(updated_data.dict())
    updated_task = doc_ref.get().to_dict()
    return updated_task

def list_tasks(user_id: str):
    tasks_ref = collection.where("user_id", "==", user_id).stream()
    return [doc.to_dict() for doc in tasks_ref]

def delete_task(task_id: str, user_id: str):
    doc_ref = collection.document(task_id)
    doc = doc_ref.get()

    if not doc.exists:
        return None

    task = doc.to_dict()
    if task["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="No autorizado para eliminar esta tarea")

    doc_ref.delete()
    return task

def create_user(user_create: UserCreate):
    user_id = str(uuid.uuid4())
    hashed_password = pwd_context.hash(user_create.password)
    user_data = {
        "id": user_id,
        "username": user_create.username,
        "email": user_create.email,
        "hashed_password": hashed_password
    }
    db.collection("users").document(user_id).set(user_data)
    return user_data

def get_user_by_email(email: str):
    users = db.collection("users").where("email", "==", email).get()
    if users:
        return users[0].to_dict()
    return None