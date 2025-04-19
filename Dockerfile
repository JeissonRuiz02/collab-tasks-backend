FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y build-essential git curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Instala poetry
RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

COPY . .

ENV PYTHONPATH=/app/src
EXPOSE 8080

# 🔥 Aquí está el cambio importante
CMD ["uvicorn", "src.collab_tasks_backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
