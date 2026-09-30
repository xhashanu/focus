import logging
from fastapi import APIRouter
from celery.result import AsyncResult
from app.workers.celery_app import celery_app
from app.schemas.task import TaskStatusResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/tasks/{task_id}",
    response_model=TaskStatusResponse,
    summary="Get background task live status and progress",
    description="Check the execution status, current processing stage, and progress percentage of a news curation task.",
)
def get_task_status(task_id: str) -> TaskStatusResponse:
    res = AsyncResult(task_id, app=celery_app)

    state = res.state
    stage = None
    progress = 0
    details = None
    result = None
    error = None

    if state == "PENDING":
        details = "Task is queued and waiting for an available Celery worker..."
        progress = 5
    elif state == "PROGRESS":
        info = res.info if isinstance(res.info, dict) else {}
        stage = info.get("stage", "PROCESSING")
        progress = info.get("progress", 50)
        details = info.get("details", "Processing media pipeline...")
    elif state == "SUCCESS":
        stage = "COMPLETED"
        progress = 100
        details = "News curation finished successfully. Draft saved."
        result = res.result if isinstance(res.result, dict) else {"data": str(res.result)}
    elif state == "FAILURE":
        stage = "FAILED"
        progress = 100
        error = str(res.result)
        details = "Pipeline execution encountered a fatal error."
    else:
        details = f"Task in state: {state}"

    return TaskStatusResponse(
        task_id=task_id,
        state=state,
        stage=stage,
        progress=progress,
        details=details,
        result=result,
        error=error,
    )
