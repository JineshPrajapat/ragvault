from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from contextlib import asynccontextmanager
from config import settings


class Base(DeclarativeBase):
    pass


class Database:
    def __init__(self):
        self.database_url = settings.DATABASE_URL
        self.engine = self._create_engine()
        self.SessionLocal = self._create_sessionmaker()

    def _create_engine(self):
        return create_async_engine(
            self.database_url,
            echo=False,
            pool_pre_ping=True,
            future=True,
        )

    def _create_sessionmaker(self):
        return async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False,  # important
        )

    @asynccontextmanager
    async def get_session(self):
        async with self.SessionLocal() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


db_instance = Database()