from celery import shared_task
from app.modules.embedding.embedding_service import EmbeddingService
from uuid import UUID
from asgiref.sync import async_to_sync
from ..core.celery_app import celery_app


# @shared_task
# def process_document(cd_id: str):
#     """
#     Background task to process uploaded document
#     """
#     async_to_sync(EmbeddingService.process_document)(UUID(cd_id))


@celery_app.task
async def process_document(cd_id: str):
    """
    Async Celery task to process uploaded document
    """
    await EmbeddingService.process_document(UUID(cd_id))