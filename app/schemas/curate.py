from typing import Optional
from pydantic import BaseModel, HttpUrl, Field


class CurateRequest(BaseModel):
    url: str = Field(..., description="Social media video URL (Instagram, TikTok, X, etc.)")
    auto_publish: Optional[bool] = Field(
        default=None,
        description="Override autonomous publishing. True = publish directly to production; False = draft for human review; None = use system default.",
    )


class CurateResponse(BaseModel):
    task_id: str = Field(..., description="Celery background task ID for tracking progress")
    status: str = Field(default="ACCEPTED", description="Current request status")
    message: str = Field(default="Curation pipeline task dispatched", description="Human-readable status message")
    source_url: str = Field(..., description="The submitted video URL")
    mode: str = Field(default="DEFAULT", description="Execution mode: AUTONOMOUS or HUMAN-REVIEW")

