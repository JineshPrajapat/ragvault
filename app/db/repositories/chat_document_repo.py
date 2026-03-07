from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.db.models.chat_document import ChatDocument
from app.core.session_manager import use_db_async
from uuid import UUID


class ChatDocumentRepository:

    @staticmethod
    @use_db_async
    async def create(payload: dict, db: AsyncSession) -> ChatDocument:
        document = ChatDocument(**payload)
        db.add(document)
        await db.commit()
        await db.refresh(document)
        return document
    
    @staticmethod
    @use_db_async
    async def get_by_id_sync(cd_id: UUID, db:AsyncSession) ->ChatDocument:
        result = await db.execute(
            select(ChatDocument)
            .where(ChatDocument.cd_id == cd_id)
        )
        print("result", result)
        return result.scalar_one_or_none()

    @staticmethod
    @use_db_async
    async def update_status(cd_id: UUID, status: str, error: str | None, db: AsyncSession):
        await db.execute(
            update(ChatDocument)
            .where(ChatDocument.cd_id == cd_id)
            .values(processing_status=status, error_message=error)
        )
        await db.commit()

    @staticmethod
    @use_db_async
    async def list_by_session(cs_id: UUID, db: AsyncSession):
        result = await db.execute(
            select(ChatDocument)
            .where(ChatDocument.cs_id == cs_id)
        )
        return result.scalars().all()