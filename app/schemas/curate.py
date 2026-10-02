from typing import Optional, List
from pydantic import BaseModel, HttpUrl, Field


class CurateRequest(BaseModel):
    url: str = Field(..., description="Social media video URL (Instagram, TikTok, X, etc.)")
    auto_publish: Optional[bool] = Field(
        default=None,
        description="Override autonomous publishing. True = publish directly to production; False = draft for human review; None = use system default.",
    )
    llm_provider: Optional[str] = Field(
        default=None,
        description="LLM provider: 'nvidia_nemotron' or 'gemini'. None = use system default.",
    )


class CurateResponse(BaseModel):
    task_id: str = Field(..., description="Celery background task ID for tracking progress")
    status: str = Field(default="ACCEPTED", description="Current request status")
    message: str = Field(default="Curation pipeline task dispatched", description="Human-readable status message")
    source_url: str = Field(..., description="The submitted video URL")
    mode: str = Field(default="DEFAULT", description="Execution mode: AUTONOMOUS or HUMAN-REVIEW")
    llm_provider: Optional[str] = Field(default=None, description="Selected LLM provider")


class BatchCurateRequest(BaseModel):
    urls: List[str] = Field(..., description="List of video URLs to process in batch")
    auto_publish: Optional[bool] = Field(default=None, description="Override auto-publish for all URLs")
    llm_provider: Optional[str] = Field(default=None, description="LLM provider for all URLs")


class BatchCurateResponse(BaseModel):
    total: int = Field(..., description="Total number of URLs submitted")
    accepted: int = Field(0, description="Number of URLs accepted and queued")
    rejected: int = Field(0, description="Number of URLs rejected (invalid)")
    tasks: List[CurateResponse] = Field(default_factory=list, description="Individual task responses")
    rejected_urls: List[str] = Field(default_factory=list, description="List of rejected URLs")

