import logging
from fastapi import APIRouter, status, HTTPException
from app.schemas.curate import CurateRequest, CurateResponse
from app.workers.tasks import process_news_link

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/curate",
    response_model=CurateResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Ingest social video link and trigger AI curation",
    description="Accepts a social media video URL (Instagram, TikTok, X), dispatches a Celery worker task, and returns the task ID for progress tracking.",
)
def curate_video_link(request: CurateRequest) -> CurateResponse:
    url_str = str(request.url).strip()
    if not url_str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A valid video URL must be provided.",
        )

    try:
        task = process_news_link.delay(url_str, auto_publish=request.auto_publish)
        logger.info("Dispatched curation task %s for URL: %s (auto_publish=%s)", task.id, url_str, request.auto_publish)
        effective_mode = "AUTONOMOUS" if (request.auto_publish is True or (request.auto_publish is None and False)) else "HUMAN-REVIEW"
        from app.config import settings
        if request.auto_publish is None:
            effective_mode = "AUTONOMOUS" if settings.AUTO_PUBLISH else "HUMAN-REVIEW"
        return CurateResponse(
            task_id=task.id,
            status="ACCEPTED",
            message=f"Media acquisition and AI news curation pipeline dispatched ({effective_mode}).",
            source_url=url_str,
            mode=effective_mode,
        )
    except Exception as exc:
        logger.error("Failed to enqueue curation task for %s: %s", url_str, exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to dispatch background task: {str(exc)}",
        )
