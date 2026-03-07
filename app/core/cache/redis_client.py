import json
from typing import Any, List
from uuid import UUID
from redis.asyncio import Redis
from app.core.cache.redis import redis_manager


class RedisClient:

    DEFAULT_TTL = 3600  # 1 hour

    def __init__(self, ):
        
        self._client: Redis = redis_manager.client

    @staticmethod
    def _chat_key(cs_id: UUID) -> str:
        return f"chat:memory:{cs_id}"

    async def append_message(
        self,
        cs_id: UUID,
        message: dict[str, Any],
        ttl: int = DEFAULT_TTL,
    ) -> None:
        """
        Append a message to chat memory.
        """
        key = self._chat_key(cs_id)

        await self._client.rpush(key, json.dumps(message))
        await self._client.expire(key, ttl)

    async def get_recent(
        self,
        cs_id: UUID,
        limit: int = 20,
    ) -> List[dict[str, Any]]:
        """
        Retrieve last N messages from chat memory.
        """
        key = self._chat_key(cs_id)

        data = await self._client.lrange(key, -limit, -1)
        return [json.loads(item) for item in data]

    async def clear_chat(self, cs_id: UUID) -> None:
        """
        Delete chat memory for a given session.
        """
        await self._client.delete(self._chat_key(cs_id))