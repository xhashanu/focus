"""
Celery Background Task — workers/tasks.py

End-to-end news curation pipeline supporting two modes:
  1. **Human-in-the-loop (default):** Download → Extract → Search → AI → Draft → Wait for review
  2. **Autonomous (AUTO_PUBLISH=true):** Download → Extract → Search → AI Curator → Publish directly to production

Mode is controlled by settings.AUTO_PUBLISH and can also be overridden per-task
via the `auto_publish` keyword argument.
"""
import logging
from typing import Dict, Any, Optional
from celery import shared_task
from app.workers.celery_app import celery_app
from app.config import settings
from app.db.session import SessionLocal
from app.models.draft import Draft, DraftStatus
from app.services.media import media_service, MediaProcessingError
from app.services.search import search_service
from app.services.ai import ai_service
from app.services.ai_curator import ai_curator
from app.services.publisher import publisher, PublisherError

logger = logging.getLogger(__name__)


@celery_app.task(
    bind=True,
    name="app.workers.tasks.process_news_link",
    max_retries=3,
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
)
def process_news_link(
    self,
    url: str,
    auto_publish: Optional[bool] = None,
    llm_provider: Optional[str] = None,
) -> Dict[str, Any]:
    """Execute the end-to-end media acquisition, context gathering, and AI news curation pipeline.

    Args:
        url: The social media video URL to process.
        auto_publish: Override settings.AUTO_PUBLISH for this specific task.
                      None = use settings.AUTO_PUBLISH.
        llm_provider: Override settings.DEFAULT_LLM_PROVIDER ('nvidia_nemotron' or 'gemini').
    """
    task_id = self.request.id
    should_auto_publish = auto_publish if auto_publish is not None else settings.AUTO_PUBLISH
    mode = "AUTONOMOUS" if should_auto_publish else "HUMAN-REVIEW"
    active_provider = llm_provider or settings.DEFAULT_LLM_PROVIDER
    logger.info("Executing process_news_link task %s for URL: %s (mode=%s, provider=%s)", task_id, url, mode, active_provider)

    # 1. Pipeline Start / Downloader
    self.update_state(
        state="PROGRESS",
        meta={
            "stage": "DOWNLOADING",
            "progress": 10,
            "mode": mode,
            "provider": active_provider,
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
                "progress": 25,
                "mode": mode,
                "provider": active_provider,
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
                "progress": 40,
                "mode": mode,
                "provider": active_provider,
                "details": "Reverse-searching keyframes on Google Lens to verify location and origin...",
            },
        )
        primary_keyframe = keyframes[0] if keyframes else video_path
        lens_context = search_service.search_keyframe_context(primary_keyframe)

        # =====================================================================
        # BRANCHING POINT: Autonomous vs Human-Review
        # =====================================================================

        if should_auto_publish:
            return _autonomous_pipeline(
                self, task_id, url, db,
                audio_path, video_path, keyframes, lens_context,
                llm_provider=active_provider,
            )
        else:
            return _human_review_pipeline(
                self, task_id, url, db,
                audio_path, video_path, keyframes, lens_context,
                llm_provider=active_provider,
            )

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


# =============================================================================
# Pipeline Branches
# =============================================================================

def _human_review_pipeline(
    task, task_id, url, db,
    audio_path, video_path, keyframes, lens_context,
    llm_provider: Optional[str] = None,
) -> Dict[str, Any]:
    """Original flow: generate draft → persist for human editorial review."""

    task.update_state(
        state="PROGRESS",
        meta={
            "stage": "GENERATING_ARTICLE",
            "progress": 65,
            "mode": "HUMAN-REVIEW",
            "provider": llm_provider or settings.DEFAULT_LLM_PROVIDER,
            "details": f"Synthesizing multimodal context with {llm_provider or settings.DEFAULT_LLM_PROVIDER}...",
        },
    )
    ai_article = ai_service.generate_article(
        audio_path=audio_path,
        video_path=video_path,
        lens_context=lens_context,
        source_url=url,
        provider=llm_provider,
    )

    task.update_state(
        state="PROGRESS",
        meta={
            "stage": "SAVING_DRAFT",
            "progress": 90,
            "mode": "HUMAN-REVIEW",
            "provider": llm_provider or settings.DEFAULT_LLM_PROVIDER,
            "details": "Persisting draft for human review...",
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
        "mode": "HUMAN-REVIEW",
        "provider": llm_provider or settings.DEFAULT_LLM_PROVIDER,
        "headline": draft.headline,
        "location": draft.location,
        "confidence_score": draft.confidence_score,
    }

    task.update_state(
        state="SUCCESS",
        meta={
            "stage": "COMPLETED",
            "progress": 100,
            "mode": "HUMAN-REVIEW",
            "provider": llm_provider or settings.DEFAULT_LLM_PROVIDER,
            "details": "News curation complete. Ready for human editorial review.",
            "result": result_payload,
        },
    )
    logger.info("Curation complete (HUMAN-REVIEW) for task %s → draft #%d", task_id, draft.id)
    return result_payload


def _autonomous_pipeline(
    task, task_id, url, db,
    audio_path, video_path, keyframes, lens_context,
    llm_provider: Optional[str] = None,
) -> Dict[str, Any]:
    """Autonomous flow: AI Curator → Publisher → Production database (no human review)."""

    # Step 4a: AI Curator produces CuratedArticlePayload
    task.update_state(
        state="PROGRESS",
        meta={
            "stage": "AI_CURATING",
            "progress": 55,
            "mode": "AUTONOMOUS",
            "provider": llm_provider or settings.DEFAULT_LLM_PROVIDER,
            "details": f"AI Curator ({llm_provider or settings.DEFAULT_LLM_PROVIDER}) generating production-ready article with full schema compliance...",
        },
    )
    curated_article = ai_curator.curate(
        audio_path=audio_path,
        video_path=video_path,
        keyframe_paths=keyframes,
        lens_context=lens_context,
        source_url=url,
        provider=llm_provider,
    )

    # Step 4b: Save a local draft record for audit trail
    task.update_state(
        state="PROGRESS",
        meta={
            "stage": "SAVING_AUDIT_DRAFT",
            "progress": 70,
            "mode": "AUTONOMOUS",
            "details": "Saving local audit trail before publishing...",
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
        headline=curated_article.title,
        summary=curated_article.summarized_description,
        body_content=curated_article.description,
        location=curated_article.location_name,
        tags=curated_article.tag_names,
        confidence_score=curated_article.confidence_score,
        ai_notes=curated_article.ai_notes,
        status=DraftStatus.PENDING,
        media_paths=media_metadata,
    )
    db.add(draft)
    db.commit()
    db.refresh(draft)

    # Step 5: Autonomous Publishing to Production
    task.update_state(
        state="PROGRESS",
        meta={
            "stage": "PUBLISHING",
            "progress": 85,
            "mode": "AUTONOMOUS",
            "details": "Publishing to production Laravel database via REST API...",
        },
    )
    try:
        publish_result = publisher.publish(
            article=curated_article,
            primary_image_path=keyframes[0] if keyframes else None,
            extra_image_paths=keyframes[1:] if len(keyframes) > 1 else None,
            source_url=url,
        )

        # Mark draft as approved/published
        draft.status = DraftStatus.APPROVED
        db.commit()

        result_payload = {
            "draft_id": draft.id,
            "status": "PUBLISHED",
            "mode": "AUTONOMOUS",
            "headline": curated_article.title,
            "location": curated_article.location_name,
            "confidence_score": curated_article.confidence_score,
            "category": curated_article.category_name,
            "urgency": curated_article.urgency,
            "publish_result": publish_result,
        }

        task.update_state(
            state="SUCCESS",
            meta={
                "stage": "PUBLISHED",
                "progress": 100,
                "mode": "AUTONOMOUS",
                "details": f"Article published to production. news_id={publish_result.get('news_id')}",
                "result": result_payload,
            },
        )
        logger.info(
            "Autonomous publishing complete for task %s → news_id=%s, draft #%d",
            task_id, publish_result.get("news_id"), draft.id,
        )
        return result_payload

    except PublisherError as pub_exc:
        logger.error("Publishing failed for task %s: %s", task_id, pub_exc)
        draft.status = DraftStatus.FAILED
        draft.error_message = f"Publishing failed: {pub_exc}"
        db.commit()

        # Even if publishing fails, the draft is still saved locally
        return {
            "draft_id": draft.id,
            "status": "PUBLISH_FAILED",
            "mode": "AUTONOMOUS",
            "headline": curated_article.title,
            "error": str(pub_exc),
            "details": "Article curated but publishing to production failed. Draft saved locally for retry.",
        }
