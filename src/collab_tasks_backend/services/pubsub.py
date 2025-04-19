from google.cloud import pubsub_v1
from src.collab_tasks_backend.config import (
    GCP_PROJECT_ID,
    TASK_CREATED_TOPIC,
    TASK_UPDATED_TOPIC,
    TASK_DELETED_TOPIC
)
from src.collab_tasks_backend.models.task import Task


publisher = pubsub_v1.PublisherClient()

def publish_event(task: Task, topic_name: str):
    topic_path = publisher.topic_path(GCP_PROJECT_ID, topic_name)
    data = task.model_dump_json().encode("utf-8")
    future = publisher.publish(topic_path, data=data)
    print(f"[PubSub] Published message to {topic_name} with ID: {future.result()}")

def publish_task_created(task: Task):
    publish_event(task, TASK_CREATED_TOPIC)

def publish_task_updated(task: Task):
    publish_event(task, TASK_UPDATED_TOPIC)

def publish_task_deleted(task: Task):
    publish_event(task, TASK_DELETED_TOPIC)
