from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class UserSessionBase(BaseModel):
    u_id: UUID
    refresh_token: str
    expires_at: datetime

class UserSessionCreate(UserSessionBase):
    pass
