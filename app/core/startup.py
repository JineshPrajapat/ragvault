from sqlalchemy import text
from app.core.database import Database, Base
from app.core.cache.redis import redis_manager
import logging

logger = logging.getLogger(__name__)

db = Database()
   
async def init_database() -> None:
    try:
        async with db.engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        # print(Base.metadata.tables.keys())
        print("✅ Database connected successfully")
    except Exception as e:
        print("❌ Database connection failed", {e})
        raise e

async def init_redis() -> None:
    try:
        await redis_manager.connect()
        print("✅ Redis connected successfully")
    except Exception as e:
        print("❌ Redis connection failed", {e})
        raise e
    
async def shutdown_redis() -> None:
    await redis_manager.disconnect()
    print("🔌 Redis disconnected")
    
