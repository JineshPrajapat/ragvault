from uuid import UUID
from app.db.repositories.chat_message_repo import ChatMessageRepository
from app.core.cache.redis_client import RedisClient
from app.modules.chat.chat_message_service import ChatMessageService


class ChatMemoryService:

    def __init__(self):
        self.redis = RedisClient()

    async def get_history(self, cs_id: UUID, limit: int = 10):

        # 1️. Try Redis first
        cached = await self.redis.get_recent(cs_id, limit)

        if cached:
            return cached

        # 2️. Fallback to DB
        db_messages = await ChatMessageService.get_recent_messages(
            cs_id=cs_id,
            limit=limit
        )

        formatted = [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in reversed(db_messages)
        ]

        return formatted

    async def save_message(
        self,
        cs_id: UUID,
        role: str,
        content: dict,
        meta: dict | None = None
    ):

        payload = {
            "cs_id": cs_id,
            "role": role,
            "content": content,
            "meta": meta
        }

        await ChatMessageRepository.create(payload)

        await self.redis.append_message(
            cs_id,
            {
                "role": role,
                "content": content,
                "meta": meta
            }
        )