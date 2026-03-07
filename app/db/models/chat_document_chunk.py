import uuid
from sqlalchemy import Column, Text, Integer, ForeignKey, DateTime, String, JSON, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql.base import TSVECTOR
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from app.core.database import Base


class ChatDocumentChunk(Base):
    __tablename__ = "chat_document_chunks"

    cdc_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    cd_id = Column(
        UUID(as_uuid=True),
        ForeignKey("chat_documents.cd_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    cs_id = Column(
        UUID(as_uuid=True),
        ForeignKey("chat_sessions.cs_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    chunk_index = Column(Integer, nullable=False)

    content = Column(Text, nullable=False)

    embedding = Column(Vector(1024), nullable=False)

    content_tsv = Column(TSVECTOR)

    page_number = Column(Integer)

    section_title = Column(String)
    chapter_title = Column(String)

    keywords = Column(ARRAY(String))
    meta = Column(JSON)

    created_at = Column(DateTime(timezone=True), server_default=func.now())