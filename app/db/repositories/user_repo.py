from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.user import User
from app.schemas.user import UserCreate
from app.core.session_manager import use_db_async
from uuid import UUID

class UserRepository:
    
    @staticmethod
    @use_db_async
    async def get_by_email(email: str, db: AsyncSession, ) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    @staticmethod
    @use_db_async
    async def get_by_id(u_id: UUID, db: AsyncSession) -> User | None:
        result = await db.execute(select(User).where(User.u_id == u_id, User.is_active == True))
        return result.scalar_one_or_none()

    @staticmethod
    @use_db_async
    async def create(payload: UserCreate, password: str, db: AsyncSession, ) -> User:
        user = User(
            email=payload.email,
            name=payload.name,
            role=payload.role,
            is_active=payload.is_active,
            password=password,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
