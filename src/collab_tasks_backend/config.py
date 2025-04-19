import os
from dotenv import load_dotenv

# Cargar el archivo .env
load_dotenv()

# Variables de entorno
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Exportar explícitamente la variable para que la use google-auth
if GOOGLE_APPLICATION_CREDENTIALS:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS

TASK_CREATED_TOPIC = "task-created"
TASK_UPDATED_TOPIC = "task-updated"
TASK_DELETED_TOPIC = "task-deleted"


