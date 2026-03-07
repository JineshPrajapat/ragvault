from celery import Celery
from config import settings

celery_app = Celery(
    "ragvault",
    broker=settings.RABBITMQ_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
)

import app.tasks.document_tasks