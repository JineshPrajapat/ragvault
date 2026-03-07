from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    cm_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cs_id = Column(UUID(as_uuid=True), ForeignKey("chat_sessions.cs_id", ondelete="CASCADE"), nullable=False)

    role = Column(String(20), nullable=False) # user | assistant | system
    content = Column(JSONB, nullable=False)
    meta = Column(JSONB, nullable=True)

    created_at = Column(DateTime, server_default=func.now())