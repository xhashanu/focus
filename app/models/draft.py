import enum
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime,
    JSON,
    Enum as SqlEnum,
)
from app.models.base import Base


class DraftStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    PUBLISHED = "PUBLISHED"
    REJECTED = "REJECTED"
    FAILED = "FAILED"


class Draft(Base):
    __tablename__ = "drafts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    task_id = Column(String(128), index=True, nullable=True)
    source_url = Column(String(1024), nullable=False, index=True)

    # AI Generated Content
    headline = Column(String(512), nullable=True)
    summary = Column(Text, nullable=True)
    body_content = Column(Text, nullable=True)  # HTML formatted
    location = Column(String(256), nullable=True)
    tags = Column(JSON, default=list, nullable=True)
    confidence_score = Column(Float, nullable=True)
    ai_notes = Column(Text, nullable=True)

    # Pipeline & Lifecycle
    status = Column(
        SqlEnum(DraftStatus),
        default=DraftStatus.PENDING,
        nullable=False,
        index=True,
    )
    media_paths = Column(JSON, default=dict, nullable=True)
    laravel_post_id = Column(String(128), nullable=True)
    error_message = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Draft id={self.id} status={self.status} headline={self.headline[:30] if self.headline else None}>"
