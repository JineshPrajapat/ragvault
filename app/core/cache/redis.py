# app/core/cache/redis.py

from typing import Optional
from redis.asyncio import Redis
from config import settings


class RedisManager:
    """
    Manages Redis connection lifecycle.
    Should be initialized on app startup.
    """

    def __init__(self) -> None:
        self._client: Optional[Redis] = None

    async def connect(self) -> None:
        if self._client is None:
            self._client = Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
            )

            # Test connection
            await self._client.ping()

    async def disconnect(self) -> None:
        if self._client:
            await self._client.close()
            self._client = None

    @property
    def client(self) -> Redis:
        if self._client is None:
            raise RuntimeError("Redis not connected. Initialize at startup.")
        return self._client


redis_manager = RedisManager()