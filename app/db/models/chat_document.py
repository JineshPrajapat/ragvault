import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Text, UniqueConstraint, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base


class ChatDocument(Base):
    __tablename__ = "chat_documents"

    __table_args__ = (
        UniqueConstraint("cs_id", "file_hash", name="uq_session_filehash"),
    )

    cd_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    cs_id = Column(
        UUID(as_uuid=True),
        ForeignKey("chat_sessions.cs_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    file_name = Column(String(255), nullable=False)
    file_path = Column(Text, nullable=False)

    file_hash = Column(String(64), nullable=False)
    file_size = Column(Integer, nullable=False)

    storage_type = Column(String(20), default="local")

    processing_status = Column(String(20), default="uploaded")

    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())