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
            "nvidia_configured": bool(settings.NVIDIA_API_KEY),
            "laravel_configured": bool(settings.LARAVEL_API_URL and settings.LARAVEL_API_TOKEN),
            "default_llm_provider": settings.DEFAULT_LLM_PROVIDER,
            "nvidia_model": settings.NVIDIA_MODEL,
        },
    }


def _mask(key: str) -> str:
    if not key or len(key) < 8:
        return "********" if key else ""
    return key[:4] + "..." + key[-4:]


@router.get(
    "/system/config",
    summary="Get current external API configuration and active model provider",
)
def get_system_config() -> Dict[str, Any]:
    return {
        "default_llm_provider": settings.DEFAULT_LLM_PROVIDER,
        "nvidia_model": settings.NVIDIA_MODEL,
        "nvidia_base_url": settings.NVIDIA_BASE_URL,
        "nvidia_api_key_masked": _mask(settings.NVIDIA_API_KEY),
        "nvidia_api_key_set": bool(settings.NVIDIA_API_KEY),
        "serpapi_api_key_masked": _mask(settings.SERPAPI_API_KEY),
        "serpapi_api_key_set": bool(settings.SERPAPI_API_KEY),
        "gemini_api_key_masked": _mask(settings.GEMINI_API_KEY),
        "gemini_api_key_set": bool(settings.GEMINI_API_KEY),
        "auto_publish": settings.AUTO_PUBLISH,
    }


from pydantic import BaseModel
from typing import Optional


class ConfigUpdateRequest(BaseModel):
    default_llm_provider: Optional[str] = None
    nvidia_api_key: Optional[str] = None
    nvidia_model: Optional[str] = None
    serpapi_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    auto_publish: Optional[bool] = None


@router.post(
    "/system/config",
    summary="Update API keys and active model provider dynamically",
)
def update_system_config(req: ConfigUpdateRequest) -> Dict[str, Any]:
    if req.default_llm_provider:
        settings.DEFAULT_LLM_PROVIDER = req.default_llm_provider
    if req.nvidia_api_key is not None and req.nvidia_api_key.strip():
        settings.NVIDIA_API_KEY = req.nvidia_api_key.strip()
    if req.nvidia_model:
        settings.NVIDIA_MODEL = req.nvidia_model.strip()
    if req.serpapi_api_key is not None and req.serpapi_api_key.strip():
        settings.SERPAPI_API_KEY = req.serpapi_api_key.strip()
        from app.services.search import search_service
        search_service.api_key = settings.SERPAPI_API_KEY
    if req.gemini_api_key is not None and req.gemini_api_key.strip():
        settings.GEMINI_API_KEY = req.gemini_api_key.strip()
        from app.services.ai_curator import ai_curator
        ai_curator.api_key = settings.GEMINI_API_KEY
    if req.auto_publish is not None:
        settings.AUTO_PUBLISH = req.auto_publish

    # Optionally persist updates to .env if it exists
    env_path = Path(".env")
    if env_path.exists():
        try:
            content = env_path.read_text(encoding="utf-8")
            updates = {
                "DEFAULT_LLM_PROVIDER": f'"{settings.DEFAULT_LLM_PROVIDER}"',
                "NVIDIA_MODEL": f'"{settings.NVIDIA_MODEL}"',
                "AUTO_PUBLISH": str(settings.AUTO_PUBLISH),
            }
            if req.nvidia_api_key and req.nvidia_api_key.strip():
                updates["NVIDIA_API_KEY"] = f'"{settings.NVIDIA_API_KEY}"'
            if req.serpapi_api_key and req.serpapi_api_key.strip():
                updates["SERPAPI_API_KEY"] = f'"{settings.SERPAPI_API_KEY}"'
            if req.gemini_api_key and req.gemini_api_key.strip():
                updates["GEMINI_API_KEY"] = f'"{settings.GEMINI_API_KEY}"'

            import re
            for k, v in updates.items():
                pattern = rf'^{k}=.*$'
                if re.search(pattern, content, flags=re.MULTILINE):
                    content = re.sub(pattern, f"{k}={v}", content, flags=re.MULTILINE)
                else:
                    content += f"\n{k}={v}"
            env_path.write_text(content, encoding="utf-8")
        except Exception:
            pass

    return {
        "success": True,
        "message": "Configuration updated successfully.",
        "config": get_system_config(),
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
