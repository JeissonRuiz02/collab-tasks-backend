from fastapi import FastAPI
from src.collab_tasks_backend.routers import task
from src.collab_tasks_backend.auth.routes import router as auth_router
from dotenv import load_dotenv
import os

load_dotenv()
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if credentials_path:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

app = FastAPI(title="Collab Tasks API")

app.include_router(task.router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "API de tareas colaborativas en GCP"}
