from fastapi import APIRouter, HTTPException
from src.collab_tasks_backend.models.task import Task, TaskCreate
from src.collab_tasks_backend.services.firestore import create_task, list_tasks, update_task, delete_task
from src.collab_tasks_backend.services.pubsub import publish_task_created, publish_task_deleted, publish_task_updated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.collab_tasks_backend.auth.jwt import decode_access_token, create_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")
    return payload

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=Task)
def create_new_task(task: TaskCreate, user=Depends(get_current_user)):
    user_id = user["sub"]
    new_task_dict = create_task(task, user_id=user_id)
    new_task = Task(**new_task_dict)
    publish_task_created(new_task)
    return new_task

@router.put("/{task_id}", response_model=Task)
def update_existing_task(task_id: str, task: Task, user=Depends(get_current_user)):
    updated_task = update_task(task_id, task, user_id=user["sub"])
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    publish_task_updated(updated_task)
    return updated_task

@router.delete("/{task_id}")
def delete_existing_task(task_id: str, user=Depends(get_current_user)):
    deleted_task = delete_task(task_id, user_id=user["sub"])
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    publish_task_deleted(deleted_task)
    return {"msg": "Task deleted successfully"}


@router.get("/", response_model=list[Task])
def get_all_tasks(user=Depends(get_current_user)):
    return list_tasks(user["sub"])
