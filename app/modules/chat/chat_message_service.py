from uuid import UUID
from typing import List
from app.db.repositories.chat_message_repo import ChatMessageRepository


class ChatMessageService:

    @staticmethod
    async def get_messages(
        cs_id: UUID,
        offset: int = 0,
        limit: int = 50
    ):
        return await ChatMessageRepository.list_paginated(
            cs_id=cs_id,
            offset=offset,
            limit=limit
        )

    @staticmethod
    async def get_recent_messages(
        cs_id: UUID,
        limit: int = 20
    ):
        return await ChatMessageRepository.list_by_session(
            cs_id=cs_id,
            limit=limit
        )