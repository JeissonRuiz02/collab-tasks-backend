# 📋 Collab Tasks API

Una API RESTful de gestión de tareas colaborativas construida con **FastAPI**, desplegada en **Google Cloud Run** y respaldada por **Firestore**, **Pub/Sub** y autenticación **JWT**. Este proyecto está diseñado siguiendo buenas prácticas de arquitectura y desarrollo moderno en la nube.

---

## 🚀 Características Principales

- ✅ CRUD de tareas (Create, Read, Update, Delete)
- ✅ Publicación de eventos a **Google Pub/Sub** (`task.created`, `task.updated`, `task.deleted`)
- ✅ Autenticación basada en **JWT**
- ✅ Asociación de tareas al usuario autenticado
- ✅ Almacenamiento en **Google Firestore** (NoSQL)
- ✅ Despliegue automático vía **Cloud Build + Cloud Run**
- ✅ Dockerizado y portable
- ✅ Uso de variables de entorno seguras
- ✅ Estructura modular y limpia

---

## 🧱 Tecnologías

- **Backend**: Python 3.11 + FastAPI
- **Autenticación**: OAuth2PasswordBearer + JWT (JSON Web Tokens)
- **Base de datos**: Firestore (NoSQL - GCP)
- **Mensajería**: Google Pub/Sub (eventos asincrónicos)
- **Despliegue**: Cloud Build + Cloud Run
- **Infraestructura**: Docker
- **CI/CD**: Cloud Build trigger desde GitHub

---

## 🔐 Autenticación

La API utiliza JWT para proteger los endpoints. Los usuarios deben autenticarse mediante:

```bash
POST /auth/login
```

## 📦 Estructura del Proyecto
``` bash
src/
│
├── collab_tasks_backend/
│   ├── main.py                   # Punto de entrada de FastAPI
│   ├── auth/                     # Lógica de autenticación JWT
│   ├── routers/                  # Endpoints /tasks
│   ├── models/                   # Pydantic models (Task, User, etc.)
│   ├── services/                 # Firestore + Pub/Sub logic
│   ├── config.py                 # Carga de variables de entorno
│
├── Dockerfile
├── cloudbuild.yaml              # CI/CD en GCP
```
## ☁️ Google Cloud Integraciones

Servicio | Uso
Cloud Run | Despliegue sin servidor (serverless) de la API
Cloud Build | Pipeline de CI/CD conectado a GitHub
Pub/Sub | Sistema de mensajería asincrónica para eventos de tareas
Firestore | Almacenamiento NoSQL de tareas y usuarios (sujeto a extensión)
IAM Roles | Configuración segura de permisos para servicio y despliegue continuo

## 🧪 Pruebas Locales
1. Ejecutar localmente:

```bash
uvicorn src.collab_tasks_backend.main:app --reload
```
2. Probar vía Swagger:

- Visita: http://localhost:8000/docs

3. Probar con cURL:

```bash
curl -X POST http://localhost:8000/tasks/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test", "description": "Testing"}'
```

## 🐳 Docker
- docker build -t collab-tasks-api .
- docker run -p 8080:8080 collab-tasks-api

## 🛠️ CI/CD en Cloud Build
```bash
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/collab-tasks-api', '.']

  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/collab-tasks-api']

  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: 'gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'collab-tasks-api'
      - '--image'
      - 'gcr.io/$PROJECT_ID/collab-tasks-api'
      - '--region'
      - 'us-central1'
      - '--platform'
      - 'managed'
      - '--allow-unauthenticated'
      - '--set-env-vars'
      - 'GCP_PROJECT_ID=$PROJECT_ID,TASK_CREATED_TOPIC=task-created,TASK_UPDATED_TOPIC=task-updated,TASK_DELETED_TOPIC=task-deleted'
```
- El trigger se ejecuta automáticamente al hacer git push a main.

## ✅ Buenas Prácticas Aplicadas
- Uso de Pydantic para validaciones y serialización clara.

- División clara en routers, services, models y auth.

- Variables sensibles gestionadas con .env y dotenv.

- Evita exposición de secretos (excluidos en .gitignore).

- Eventos desacoplados mediante Pub/Sub.

- API documentada automáticamente con OpenAPI (Swagger).

## 📣 Autor
- Desarrollado por Jeisson Ruiz
- 🚀 Proyecto de práctica full stack en GCP
- 📬 Contacto: jeissonruizdev@gmail.com .