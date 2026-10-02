import logging
from typing import List
from fastapi import APIRouter, status, HTTPException, UploadFile, File, Form
from app.schemas.curate import CurateRequest, CurateResponse, BatchCurateRequest, BatchCurateResponse
from app.workers.tasks import process_news_link

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/curate",
    response_model=CurateResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Ingest social video link and trigger AI curation",
    description="Accepts a social media video URL (Instagram, TikTok, X, YouTube, etc.), dispatches a Celery worker task, and returns the task ID for progress tracking.",
)
def curate_video_link(request: CurateRequest) -> CurateResponse:
    url_str = str(request.url).strip()
    if not url_str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A valid video URL must be provided.",
        )

    try:
        from app.config import settings
        effective_provider = request.llm_provider or settings.DEFAULT_LLM_PROVIDER
        task = process_news_link.delay(
            url_str,
            auto_publish=request.auto_publish,
            llm_provider=effective_provider,
        )
        logger.info(
            "Dispatched curation task %s for URL: %s (auto_publish=%s, provider=%s)",
            task.id, url_str, request.auto_publish, effective_provider,
        )
        effective_mode = "AUTONOMOUS" if (request.auto_publish is True or (request.auto_publish is None and settings.AUTO_PUBLISH)) else "HUMAN-REVIEW"
        return CurateResponse(
            task_id=task.id,
            status="ACCEPTED",
            message=f"Media acquisition and AI news curation pipeline dispatched ({effective_mode}, model: {effective_provider}).",
            source_url=url_str,
            mode=effective_mode,
            llm_provider=effective_provider,
        )
    except Exception as exc:
        logger.error("Failed to enqueue curation task for %s: %s", url_str, exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to dispatch background task: {str(exc)}",
        )


def _dispatch_single(url: str, auto_publish, llm_provider) -> CurateResponse:
    """Internal helper — dispatches a single URL to Celery, returns a CurateResponse."""
    from app.config import settings
    effective_provider = llm_provider or settings.DEFAULT_LLM_PROVIDER
    task = process_news_link.delay(url, auto_publish=auto_publish, llm_provider=effective_provider)
    effective_mode = "AUTONOMOUS" if (auto_publish is True or (auto_publish is None and settings.AUTO_PUBLISH)) else "HUMAN-REVIEW"
    return CurateResponse(
        task_id=task.id,
        status="ACCEPTED",
        message=f"Queued ({effective_mode}, {effective_provider}).",
        source_url=url,
        mode=effective_mode,
        llm_provider=effective_provider,
    )


@router.post(
    "/curate/batch",
    response_model=BatchCurateResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Batch-submit multiple video URLs for AI curation",
    description="Accepts a JSON list of URLs and dispatches each as an independent Celery task. Returns a summary of queued tasks.",
)
def batch_curate(request: BatchCurateRequest) -> BatchCurateResponse:
    tasks: List[CurateResponse] = []
    rejected_urls: List[str] = []

    for raw_url in request.urls:
        url = raw_url.strip()
        if not url or not url.startswith("http"):
            rejected_urls.append(url or "(empty)")
            continue
        try:
            resp = _dispatch_single(url, request.auto_publish, request.llm_provider)
            tasks.append(resp)
        except Exception as exc:
            logger.error("Batch curate: failed to queue %s: %s", url, exc)
            rejected_urls.append(url)

    return BatchCurateResponse(
        total=len(request.urls),
        accepted=len(tasks),
        rejected=len(rejected_urls),
        tasks=tasks,
        rejected_urls=rejected_urls,
    )


@router.post(
    "/curate/upload",
    response_model=BatchCurateResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Upload a .txt or .csv file of video URLs for batch curation",
    description="Upload a plaintext file with one URL per line. Each valid URL is dispatched as an independent Celery task.",
)
async def upload_curate(
    file: UploadFile = File(..., description="Text file with one URL per line (.txt or .csv)"),
    auto_publish: bool = Form(default=False),
    llm_provider: str = Form(default=""),
) -> BatchCurateResponse:
    content = await file.read()
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        text = content.decode("latin-1")

    # Parse URLs: one per line, skip empty/comments
    raw_lines = [line.strip() for line in text.replace("\r\n", "\n").split("\n")]
    urls = [line for line in raw_lines if line and not line.startswith("#")]

    tasks: List[CurateResponse] = []
    rejected_urls: List[str] = []
    prov = llm_provider.strip() or None

    for url in urls:
        # Handle CSV: take first column
        if "," in url:
            url = url.split(",")[0].strip()
        if not url.startswith("http"):
            rejected_urls.append(url)
            continue
        try:
            resp = _dispatch_single(url, auto_publish if auto_publish else None, prov)
            tasks.append(resp)
        except Exception as exc:
            logger.error("Upload curate: failed to queue %s: %s", url, exc)
            rejected_urls.append(url)

    return BatchCurateResponse(
        total=len(urls),
        accepted=len(tasks),
        rejected=len(rejected_urls),
        tasks=tasks,
        rejected_urls=rejected_urls,
    )

