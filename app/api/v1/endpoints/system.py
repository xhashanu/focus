import os
import shutil
from pathlib import Path
from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.config import settings
from app.db.session import get_db
from app.models.draft import Draft, DraftStatus

router = APIRouter()


@router.get(
    "/system/stats",
    summary="Get system health and operational metrics",
    description="Returns aggregate counts of drafts, storage utilization, and service status.",
)
def get_system_stats(db: Session = Depends(get_db)) -> Dict[str, Any]:
    # Draft counts
    total_drafts = db.query(func.count(Draft.id)).scalar() or 0
    pending_count = db.query(func.count(Draft.id)).filter(Draft.status == DraftStatus.PENDING).scalar() or 0
    published_count = db.query(func.count(Draft.id)).filter(Draft.status == DraftStatus.PUBLISHED).scalar() or 0
    rejected_count = db.query(func.count(Draft.id)).filter(Draft.status == DraftStatus.REJECTED).scalar() or 0
    failed_count = db.query(func.count(Draft.id)).filter(Draft.status == DraftStatus.FAILED).scalar() or 0

    # Storage calculation
    temp_dir = Path(settings.STORAGE_TEMP_DIR)
    temp_file_count = 0
    temp_size_bytes = 0
    if temp_dir.exists():
        for f in temp_dir.rglob("*"):
            if f.is_file():
                temp_file_count += 1
                try:
                    temp_size_bytes += f.stat().st_size
                except OSError:
                    pass

    return {
        "status": "healthy",
        "drafts": {
            "total": total_drafts,
            "pending": pending_count,
            "published": published_count,
            "rejected": rejected_count,
            "failed": failed_count,
        },
        "storage": {
            "path": str(temp_dir),
            "file_count": temp_file_count,
            "size_mb": round(temp_size_bytes / (1024 * 1024), 2),
        },
        "integrations": {
            "serpapi_configured": bool(settings.SERPAPI_API_KEY),
            "gemini_configured": bool(settings.GEMINI_API_KEY),
            "laravel_configured": bool(settings.LARAVEL_API_URL and settings.LARAVEL_API_TOKEN),
        },
    }


@router.post(
    "/system/cleanup",
    summary="Purge orphaned temporary media files",
    description="Deletes cached media files from temporary storage to free up disk space.",
)
def cleanup_temp_storage() -> Dict[str, Any]:
    temp_dir = Path(settings.STORAGE_TEMP_DIR)
    deleted_files = 0
    freed_bytes = 0

    if temp_dir.exists():
        for f in temp_dir.glob("*"):
            if f.is_file():
                try:
                    freed_bytes += f.stat().st_size
                    f.unlink(missing_ok=True)
                    deleted_files += 1
                except Exception:
                    pass

    return {
        "success": True,
        "deleted_files": deleted_files,
        "freed_mb": round(freed_bytes / (1024 * 1024), 2),
    }
