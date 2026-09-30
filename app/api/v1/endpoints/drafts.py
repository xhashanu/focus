import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.draft import Draft, DraftStatus
from app.schemas.draft import DraftResponse, DraftUpdate, DraftPublishResponse
from app.services.laravel import laravel_service, LaravelPublishError
from app.services.media import media_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/drafts",
    response_model=List[DraftResponse],
    summary="List news drafts",
    description="Retrieve a list of news drafts with optional status filtering.",
)
def list_drafts(
    status_filter: Optional[DraftStatus] = Query(None, alias="status", description="Filter by draft status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
) -> List[Draft]:
    query = db.query(Draft)
    if status_filter:
        query = query.filter(Draft.status == status_filter)
    else:
        # By default, prioritize pending drafts
        pass
    drafts = query.order_by(Draft.created_at.desc()).offset(skip).limit(limit).all()
    return drafts


@router.get(
    "/drafts/{draft_id}",
    response_model=DraftResponse,
    summary="Get single draft details",
)
def get_draft(draft_id: int, db: Session = Depends(get_db)) -> Draft:
    draft = db.query(Draft).filter(Draft.id == draft_id).first()
    if not draft:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Draft with ID {draft_id} not found.",
        )
    return draft


@router.patch(
    "/drafts/{draft_id}",
    response_model=DraftResponse,
    summary="Update draft content (human editing)",
)
def update_draft(
    draft_id: int,
    update_data: DraftUpdate,
    db: Session = Depends(get_db),
) -> Draft:
    draft = db.query(Draft).filter(Draft.id == draft_id).first()
    if not draft:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Draft with ID {draft_id} not found.",
        )

    for field, val in update_data.model_dump(exclude_unset=True).items():
        setattr(draft, field, val)

    db.commit()
    db.refresh(draft)
    return draft


@router.post(
    "/drafts/{draft_id}/publish",
    response_model=DraftPublishResponse,
    summary="Approve draft and push to live Laravel app",
    description="Triggers the webhook to publish the approved draft to the live Flutter/Laravel app via REST API, then cleans up temporary media storage.",
)
def publish_draft(
    draft_id: int,
    category_id: int = Query(1, description="Laravel news category ID"),
    db: Session = Depends(get_db),
) -> DraftPublishResponse:
    draft = db.query(Draft).filter(Draft.id == draft_id).first()
    if not draft:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Draft with ID {draft_id} not found.",
        )

    if draft.status == DraftStatus.PUBLISHED:
        return DraftPublishResponse(
            id=draft.id,
            status=draft.status,
            laravel_post_id=draft.laravel_post_id,
            message="Draft has already been published previously.",
        )

    try:
        # Push to live Laravel REST API (Strict HTTP isolation)
        response_data = laravel_service.publish_draft(draft, category_id=category_id)
        post_id = str(response_data.get("post_id") or response_data.get("id") or "published")

        draft.status = DraftStatus.PUBLISHED
        draft.laravel_post_id = post_id
        db.commit()
        db.refresh(draft)

        # Cleanup media files to prevent disk bloat (per context.md rules)
        if draft.media_paths and isinstance(draft.media_paths, dict):
            video = draft.media_paths.get("video_path")
            audio = draft.media_paths.get("audio_path")
            frames = draft.media_paths.get("keyframes", [])
            all_media = [p for p in [video, audio] + frames if p]
            media_service.cleanup_media(*all_media)

        return DraftPublishResponse(
            id=draft.id,
            status=draft.status,
            laravel_post_id=post_id,
            message="Draft successfully published to Laravel news application.",
        )
    except LaravelPublishError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Laravel webhook publication failed: {str(exc)}",
        )
    except Exception as exc:
        logger.error("Unexpected error publishing draft %s: %s", draft_id, exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error during publishing: {str(exc)}",
        )


@router.post(
    "/drafts/{draft_id}/reject",
    response_model=DraftResponse,
    summary="Reject draft and clean up media",
)
def reject_draft(draft_id: int, db: Session = Depends(get_db)) -> Draft:
    draft = db.query(Draft).filter(Draft.id == draft_id).first()
    if not draft:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Draft with ID {draft_id} not found.",
        )

    draft.status = DraftStatus.REJECTED
    db.commit()
    db.refresh(draft)

    # Cleanup media files per context.md
    if draft.media_paths and isinstance(draft.media_paths, dict):
        video = draft.media_paths.get("video_path")
        audio = draft.media_paths.get("audio_path")
        frames = draft.media_paths.get("keyframes", [])
        all_media = [p for p in [video, audio] + frames if p]
        media_service.cleanup_media(*all_media)

    return draft
