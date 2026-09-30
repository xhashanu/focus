import logging
from typing import Dict, Any
from celery import shared_task
from app.workers.celery_app import celery_app
from app.db.session import SessionLocal
from app.models.draft import Draft, DraftStatus
from app.services.media import media_service, MediaProcessingError
from app.services.search import search_service
from app.services.ai import ai_service

logger = logging.getLogger(__name__)


@celery_app.task(
    bind=True,
    name="app.workers.tasks.process_news_link",
    max_retries=3,
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
)
def process_news_link(self, url: str) -> Dict[str, Any]:
    """Execute the end-to-end media acquisition, context gathering, and AI news curation pipeline."""
    task_id = self.request.id
    logger.info("Executing process_news_link task %s for URL: %s", task_id, url)

    # 1. Pipeline Start / Downloader
    self.update_state(
        state="PROGRESS",
        meta={
            "stage": "DOWNLOADING",
            "progress": 15,
            "details": f"Acquiring video stream via yt-dlp from: {url}",
        },
    )

    db = SessionLocal()
    video_path = None
    audio_path = None
    keyframes = []

    try:
        # Step 1: Download
        video_path = media_service.download_video(url)

        # Step 2: Media Processing (Audio & Keyframes)
        self.update_state(
            state="PROGRESS",
            meta={
                "stage": "EXTRACTING_MEDIA",
                "progress": 35,
                "details": "Extracting audio track and slicing representative keyframes...",
            },
        )
        audio_path = media_service.extract_audio(video_path)
        keyframes = media_service.extract_keyframes(video_path, num_frames=3)

        # Step 3: Context Gathering via Google Lens (SerpApi)
        self.update_state(
            state="PROGRESS",
            meta={
                "stage": "SEARCHING_CONTEXT",
                "progress": 55,
                "details": "Reverse-searching keyframes on Google Lens to verify location and origin...",
            },
        )
        primary_keyframe = keyframes[0] if keyframes else video_path
        lens_context = search_service.search_keyframe_context(primary_keyframe)

        # Step 4: Multimodal AI Generation
        self.update_state(
            state="PROGRESS",
            meta={
                "stage": "GENERATING_ARTICLE",
                "progress": 75,
                "details": "Synthesizing multimodal audio/video and Lens context into localized news draft...",
            },
        )
        ai_article = ai_service.generate_article(
            audio_path=audio_path,
            video_path=video_path,
            lens_context=lens_context,
            source_url=url,
        )

        # Step 5: Save to SQLite Drafts
        self.update_state(
            state="PROGRESS",
            meta={
                "stage": "SAVING_DRAFT",
                "progress": 90,
                "details": "Validating and persisting draft in local database for human review...",
            },
        )

        media_metadata = {
            "video_path": video_path,
            "audio_path": audio_path,
            "keyframes": keyframes,
        }

        draft = Draft(
            task_id=task_id,
            source_url=url,
            headline=ai_article.headline,
            summary=ai_article.summary,
            body_content=ai_article.body_content,
            location=ai_article.location,
            tags=ai_article.tags,
            confidence_score=ai_article.confidence_score,
            ai_notes=ai_article.ai_notes,
            status=DraftStatus.PENDING,
            media_paths=media_metadata,
        )
        db.add(draft)
        db.commit()
        db.refresh(draft)

        result_payload = {
            "draft_id": draft.id,
            "status": "COMPLETED",
            "headline": draft.headline,
            "location": draft.location,
            "confidence_score": draft.confidence_score,
        }

        self.update_state(
            state="SUCCESS",
            meta={
                "stage": "COMPLETED",
                "progress": 100,
                "details": "News curation complete. Ready for human editorial review.",
                "result": result_payload,
            },
        )
        logger.info("Curation successfully finished for task %s, created draft #%d", task_id, draft.id)
        return result_payload

    except Exception as exc:
        logger.error("Curation task %s failed: %s", task_id, exc)
        # Attempt to mark draft as failed if created
        try:
            failed_draft = Draft(
                task_id=task_id,
                source_url=url,
                status=DraftStatus.FAILED,
                error_message=str(exc),
            )
            db.add(failed_draft)
            db.commit()
        except Exception:
            db.rollback()

        # Handle Celery retry with exponential backoff if retries left
        if self.request.retries < self.max_retries:
            logger.warning("Retrying task %s (attempt %d/%d)...", task_id, self.request.retries + 1, self.max_retries)
            raise self.retry(exc=exc)

        # Final failure state update
        self.update_state(
            state="FAILURE",
            meta={
                "stage": "FAILED",
                "progress": 100,
                "details": f"Pipeline failed: {str(exc)}",
                "error": str(exc),
            },
        )
        raise exc

    finally:
        db.close()
