from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.db.models.chat_message import ChatMessage
from app.core.session_manager import use_db_async


class ChatMessageRepository:

    @staticmethod
    @use_db_async
    async def create(payload: dict, db: AsyncSession) -> ChatMessage:
        message = ChatMessage(**payload)
        db.add(message)
        await db.commit()
        await db.refresh(message)
        return message

    @staticmethod
    @use_db_async
    async def list_by_session(
        cs_id: UUID,
        limit: int = 20,
        db: AsyncSession = None
    ):
        result = await db.execute(
            select(ChatMessage)
            .where(ChatMessage.cs_id == cs_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
        )

        return result.scalars().all()
    
    @staticmethod
    @use_db_async
    async def list_paginated(
        cs_id: UUID,
        offset: int = 0,
        limit: int = 50,
        db: AsyncSession = None
    ):
        result = await db.execute(
            select(ChatMessage)
            .where(ChatMessage.cs_id == cs_id)
            .order_by(ChatMessage.created_at.asc())
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all()