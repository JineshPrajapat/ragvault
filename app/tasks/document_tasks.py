from celery import shared_task
from app.modules.embedding.embedding_service import EmbeddingService
from uuid import UUID
from asgiref.sync import async_to_sync


@shared_task
def process_document(cd_id: str):
    """
    Background task to process uploaded document
    """
    async_to_sync(EmbeddingService.process_document)(UUID(cd_id))