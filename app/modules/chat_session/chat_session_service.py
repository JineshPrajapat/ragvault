from fastapi import HTTPException
from uuid import UUID
from app.db.repositories.chat_session_repo import ChatSessionRepository


class ChatSessionService:

    @staticmethod
    async def create_session(u_id: UUID, title: str):
        return await ChatSessionRepository.create(u_id=u_id, title=title)

    @staticmethod
    async def list_sessions(u_id: UUID):
        return await ChatSessionRepository.list_by_user(u_id=u_id)

    @staticmethod
    async def rename_session(cs_id: UUID, title: str):
        await ChatSessionRepository.rename(cs_id, title)

    @staticmethod
    async def get_session(u_id: UUID, cs_id: UUID):
        session = await ChatSessionRepository.get_by_id(cs_id)

        if not session or session.u_id != u_id or session.status == "deleted":
            raise HTTPException(status_code=404, detail="Session not found")

        return session

    @staticmethod
    async def delete_session(u_id: UUID, cs_id: UUID):
        session = await ChatSessionRepository.get_by_id(cs_id)

        if not session or session.u_id != u_id:
            raise HTTPException(status_code=404, detail="Session not found")

        await ChatSessionRepository.soft_delete(cs_id)