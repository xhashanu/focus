import logging
from typing import Dict, Any, Optional
import httpx
from app.config import settings
from app.models.draft import Draft

logger = logging.getLogger(__name__)


class LaravelPublishError(Exception):
    """Raised when pushing draft to live Laravel API fails."""
    pass


class LaravelIntegrationService:
    def __init__(
        self,
        api_url: str = settings.LARAVEL_API_URL,
        api_token: str = settings.LARAVEL_API_TOKEN,
    ):
        self.api_url = api_url
        self.api_token = api_token

    def format_payload(self, draft: Draft, category_id: int = 1) -> Dict[str, Any]:
        """Format SQLite Draft to match standard CodeCanyon Laravel News API schema."""
        tags_str = ", ".join(draft.tags) if isinstance(draft.tags, list) else str(draft.tags or "")
        return {
            "title": draft.headline or "Untitled News",
            "description": draft.summary or "",
            "content": draft.body_content or "",
            "category_id": category_id,
            "tags": tags_str,
            "location": draft.location or "",
            "source_url": draft.source_url,
            "confidence_score": draft.confidence_score,
            "ai_curated": True,
            "ai_notes": draft.ai_notes,
        }

    def publish_draft(self, draft: Draft, category_id: int = 1) -> Dict[str, Any]:
        """Push approved draft to the live Laravel app via REST API (strictly isolated via HTTP)."""
        if not self.api_url:
            logger.warning("LARAVEL_API_URL not configured. Simulating successful push.")
            return {
                "success": True,
                "simulated": True,
                "post_id": f"simulated_{draft.id}",
                "message": "Laravel API URL not set in .env. Article marked as published locally.",
            }

        payload = self.format_payload(draft, category_id=category_id)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"

        try:
            logger.info("Pushing draft %s to Laravel API: %s", draft.id, self.api_url)
            with httpx.Client(timeout=30.0) as client:
                response = client.post(self.api_url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                logger.info("Successfully published draft %s to Laravel. Response: %s", draft.id, data)
                return data
        except httpx.HTTPStatusError as exc:
            logger.error("Laravel API returned error status %d: %s", exc.response.status_code, exc.response.text)
            raise LaravelPublishError(f"HTTP {exc.response.status_code}: {exc.response.text}") from exc
        except Exception as exc:
            logger.error("Failed to connect to Laravel API for draft %s: %s", draft.id, exc)
            raise LaravelPublishError(f"Connection failure: {str(exc)}") from exc


laravel_service = LaravelIntegrationService()
