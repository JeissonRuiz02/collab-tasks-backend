from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    assigned_to: Optional[str] = None

class Task(TaskCreate):
    id: str
    user_id: str
    status: str = "pending"
    created_at: datetime
