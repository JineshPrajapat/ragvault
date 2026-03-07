from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class ChatDocumentResponse(BaseModel):
    cd_id: UUID
    file_name: str
    processing_status: str
    created_at: datetime

    class Config:
        from_attributes = True