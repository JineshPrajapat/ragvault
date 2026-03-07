from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.db.models.chat_session import ChatSession
from app.core.session_manager import use_db_async
from uuid import UUID


class ChatSessionRepository:

    @staticmethod
    @use_db_async
    async def create(u_id: UUID, title: str, db: AsyncSession) -> ChatSession:
        session = ChatSession(
            u_id=u_id,
            title=title,
            status="active"
        )
        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session

    @staticmethod
    @use_db_async
    async def get_by_id(cs_id: UUID, db: AsyncSession) -> ChatSession | None:
        result = await db.execute(
            select(ChatSession).where(ChatSession.cs_id == cs_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    @use_db_async
    async def rename(cs_id: UUID, title: str, db: AsyncSession):
        await db.execute(
            update(ChatSession)
            .where(ChatSession.cs_id == cs_id)
            .values(title=title)
        )
        await db.commit()

    @staticmethod
    @use_db_async
    async def list_by_user(u_id: UUID, db: AsyncSession):
        result = await db.execute(
            select(ChatSession)
            .where(ChatSession.u_id == u_id, ChatSession.status != "deleted")
            .order_by(ChatSession.created_at.desc())
        )
        return result.scalars().all()

    @staticmethod
    @use_db_async
    async def soft_delete(cs_id: UUID, db: AsyncSession):
        await db.execute(
            update(ChatSession)
            .where(ChatSession.cs_id == cs_id)
            .values(status="deleted")
        )
        await db.commit()