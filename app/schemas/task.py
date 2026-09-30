from typing import Optional, Any, Dict
from pydantic import BaseModel, Field


class TaskStatusResponse(BaseModel):
    task_id: str
    state: str = Field(..., description="Celery task state (PENDING, PROGRESS, SUCCESS, FAILURE, RETRY)")
    stage: Optional[str] = Field(None, description="Detailed pipeline stage (e.g. DOWNLOADING, EXTRACTING_MEDIA, etc.)")
    progress: int = Field(default=0, ge=0, le=100, description="Estimated completion percentage")
    details: Optional[str] = Field(None, description="Current activity description")
    result: Optional[Dict[str, Any]] = Field(None, description="Task completion payload, e.g., created draft ID")
    error: Optional[str] = Field(None, description="Error message if the task failed")
