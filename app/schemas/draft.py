from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from app.models.draft import DraftStatus


class DraftBase(BaseModel):
    source_url: str
    headline: Optional[str] = None
    summary: Optional[str] = None
    body_content: Optional[str] = None
    location: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    confidence_score: Optional[float] = None
    ai_notes: Optional[str] = None
    status: DraftStatus = DraftStatus.PENDING


class DraftUpdate(BaseModel):
    headline: Optional[str] = None
    summary: Optional[str] = None
    body_content: Optional[str] = None
    location: Optional[str] = None
    tags: Optional[List[str]] = None


class DraftResponse(DraftBase):
    id: int
    task_id: Optional[str] = None
    media_paths: Optional[Dict[str, Any]] = None
    laravel_post_id: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DraftPublishResponse(BaseModel):
    id: int
    status: DraftStatus
    laravel_post_id: Optional[str] = None
    message: str
