from pydantic import BaseModel, UUID4
# from uuid import UUID
from datetime import datetime


class ChatSessionCreate(BaseModel):
    title: str


class ChatSessionResponse(BaseModel):
    cs_id: UUID4
    title: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True