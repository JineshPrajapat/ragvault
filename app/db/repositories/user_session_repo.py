from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.user_session import UserSession
from app.schemas.user_session import UserSessionCreate
from app.core.session_manager import use_db_async

class UserSessionRepository:

    @use_db_async
    async def create(payload: UserSessionCreate, db: AsyncSession) -> UserSession:
        session = UserSession(
            u_id=payload.u_id,
            refresh_token=payload.refresh_token,
            expires_at=payload.expires_at,
        )
        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session
    
    @use_db_async
    async def get_by_refresh_token(token: str, db: AsyncSession) -> UserSession | None:
        result = await db.execute(select(UserSession).where(UserSession.refresh_token == token))
        return result.scalar_one_or_none()
