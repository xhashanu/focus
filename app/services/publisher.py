"""
Autonomous Publisher Service — services/publisher.py

Handles the complete end-to-end publishing workflow against the production
Laravel MySQL database via its REST API (strictly isolated, HTTP only).

Responsibilities:
  1. Taxonomy resolution: find-or-create category, subcategory, tags, location
  2. Transactional article insertion into tbl_news
  3. Secondary image insertion into tbl_news_image
  4. Optional tbl_breaking_news entry
  5. Optional tbl_notifications push
  6. Optional video_shorts creation

All writes go through the Laravel REST API — we never connect directly
to MySQL (per context.md strict-isolation constraint).
"""
from __future__ import annotations

import json
import logging
from datetime import datetime, date
from typing import Any, Dict, List, Optional

import httpx

from app.config import settings
from app.schemas.schema_models import (
    CategoryPayload,
    SubcategoryPayload,
    TagPayload,
    LocationPayload,
    NewsArticlePayload,
    NewsImagePayload,
    BreakingNewsPayload,
    NotificationPayload,
    VideoShortsPayload,
    CuratedArticlePayload,
    generate_slug,
)

logger = logging.getLogger(__name__)


class PublisherError(Exception):
    """Raised on any failure during autonomous publishing."""
    pass


class LaravelAPIClient:
    """Low-level HTTP client for communicating with the Laravel admin API.

    Every method maps to a Laravel route and returns the decoded JSON
    response body.  All errors are wrapped in PublisherError.
    """

    def __init__(
        self,
        base_url: str = settings.LARAVEL_API_URL,
        api_token: str = settings.LARAVEL_API_TOKEN,
        timeout: float = 30.0,
    ):
        # Strip trailing /api/... paths so we have the domain root
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token
        self.timeout = timeout

    def _headers(self) -> Dict[str, str]:
        h: Dict[str, str] = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if self.api_token:
            h["Authorization"] = f"Bearer {self.api_token}"
        return h

    # -----------------------------------------------------------------
    # Generic request helpers
    # -----------------------------------------------------------------

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            with httpx.Client(timeout=self.timeout) as client:
                resp = client.get(url, headers=self._headers(), params=params)
                resp.raise_for_status()
                return resp.json()
        except Exception as exc:
            logger.error("GET %s failed: %s", url, exc)
            raise PublisherError(f"GET {endpoint}: {exc}") from exc

    def _post(self, endpoint: str, payload: Dict[str, Any]) -> Any:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            with httpx.Client(timeout=self.timeout) as client:
                resp = client.post(url, headers=self._headers(), json=payload)
                resp.raise_for_status()
                return resp.json()
        except httpx.HTTPStatusError as exc:
            logger.error("POST %s → HTTP %d: %s", url, exc.response.status_code, exc.response.text)
            raise PublisherError(f"POST {endpoint} HTTP {exc.response.status_code}: {exc.response.text}") from exc
        except Exception as exc:
            logger.error("POST %s failed: %s", url, exc)
            raise PublisherError(f"POST {endpoint}: {exc}") from exc

    # -----------------------------------------------------------------
    # Taxonomy: find-or-create helpers
    # -----------------------------------------------------------------

    def resolve_category(self, name: str, language_id: int = 1) -> int:
        """Return the category ID for *name*, creating it if it doesn't exist."""
        try:
            data = self._get("api/categories", {"language_id": language_id})
            categories = data if isinstance(data, list) else data.get("data", [])
            for cat in categories:
                if str(cat.get("category_name", "")).strip().lower() == name.strip().lower():
                    logger.info("Resolved existing category '%s' → id=%s", name, cat["id"])
                    return int(cat["id"])
        except PublisherError:
            logger.warning("Category lookup failed; will attempt creation.")

        payload = CategoryPayload(category_name=name, language_id=language_id)
        result = self._post("api/categories", payload.model_dump())
        cat_id = int(result.get("id") or result.get("data", {}).get("id", 0))
        logger.info("Created new category '%s' → id=%d", name, cat_id)
        return cat_id

    def resolve_subcategory(self, name: str, category_id: int, language_id: int = 1) -> int:
        """Return the subcategory ID for *name* under *category_id*."""
        try:
            data = self._get("api/subcategories", {"category_id": category_id, "language_id": language_id})
            subs = data if isinstance(data, list) else data.get("data", [])
            for sub in subs:
                if str(sub.get("subcategory_name", "")).strip().lower() == name.strip().lower():
                    logger.info("Resolved existing subcategory '%s' → id=%s", name, sub["id"])
                    return int(sub["id"])
        except PublisherError:
            logger.warning("Subcategory lookup failed; will attempt creation.")

        payload = SubcategoryPayload(
            subcategory_name=name,
            category_id=category_id,
            language_id=language_id,
        )
        result = self._post("api/subcategories", payload.model_dump())
        sub_id = int(result.get("id") or result.get("data", {}).get("id", 0))
        logger.info("Created new subcategory '%s' → id=%d", name, sub_id)
        return sub_id

    def resolve_tags(self, names: List[str], language_id: int = 1) -> str:
        """Resolve a list of tag names to IDs.

        Returns a comma-separated string of tbl_tag.id values (e.g. '1,5,12')
        which is what tbl_news.tag_id expects.
        """
        if not names:
            return ""

        tag_ids: List[int] = []

        # Fetch all existing tags once
        existing_tags: List[Dict[str, Any]] = []
        try:
            data = self._get("api/tags", {"language_id": language_id})
            existing_tags = data if isinstance(data, list) else data.get("data", [])
        except PublisherError:
            logger.warning("Tag lookup failed; will create all tags.")

        existing_map = {
            str(t.get("tag_name", "")).strip().lower(): int(t["id"])
            for t in existing_tags
            if t.get("id")
        }

        for name in names:
            key = name.strip().lower()
            if key in existing_map:
                tag_ids.append(existing_map[key])
                logger.debug("Resolved tag '%s' → id=%d", name, existing_map[key])
            else:
                payload = TagPayload(tag_name=name.strip(), language_id=language_id)
                result = self._post("api/tags", payload.model_dump())
                tid = int(result.get("id") or result.get("data", {}).get("id", 0))
                tag_ids.append(tid)
                existing_map[key] = tid
                logger.info("Created new tag '%s' → id=%d", name, tid)

        return ",".join(str(i) for i in tag_ids)

    def resolve_location(self, name: str, latitude: str = "0.0", longitude: str = "0.0") -> int:
        """Return the location ID for *name*, creating it if necessary."""
        if not name or not name.strip():
            return 0

        try:
            data = self._get("api/locations")
            locations = data if isinstance(data, list) else data.get("data", [])
            for loc in locations:
                if str(loc.get("location_name", "")).strip().lower() == name.strip().lower():
                    logger.info("Resolved existing location '%s' → id=%s", name, loc["id"])
                    return int(loc["id"])
        except PublisherError:
            logger.warning("Location lookup failed; will attempt creation.")

        payload = LocationPayload(location_name=name.strip(), latitude=latitude, longitude=longitude)
        result = self._post("api/locations", payload.model_dump())
        loc_id = int(result.get("id") or result.get("data", {}).get("id", 0))
        logger.info("Created new location '%s' → id=%d", name, loc_id)
        return loc_id

    # -----------------------------------------------------------------
    # Content insertion
    # -----------------------------------------------------------------

    def insert_news(self, payload: NewsArticlePayload) -> int:
        """Insert a row into tbl_news and return the new record ID."""
        data = payload.model_dump()
        # Convert date/datetime objects to strings for JSON serialisation
        for key in ("date", "published_date", "show_till"):
            if data.get(key) and isinstance(data[key], (datetime, date)):
                data[key] = data[key].isoformat()

        result = self._post("api/news", data)
        news_id = int(result.get("id") or result.get("data", {}).get("id", 0))
        logger.info("Inserted tbl_news row → id=%d, title='%s'", news_id, payload.title[:60])
        return news_id

    def insert_news_image(self, payload: NewsImagePayload) -> int:
        result = self._post("api/news-images", payload.model_dump())
        return int(result.get("id") or result.get("data", {}).get("id", 0))

    def insert_breaking_news(self, payload: BreakingNewsPayload) -> int:
        result = self._post("api/breaking-news", payload.model_dump())
        bn_id = int(result.get("id") or result.get("data", {}).get("id", 0))
        logger.info("Inserted tbl_breaking_news → id=%d", bn_id)
        return bn_id

    def send_notification(self, payload: NotificationPayload) -> int:
        data = payload.model_dump()
        if isinstance(data.get("date_sent"), datetime):
            data["date_sent"] = data["date_sent"].isoformat()
        result = self._post("api/notifications", data)
        notif_id = int(result.get("id") or result.get("data", {}).get("id", 0))
        logger.info("Sent tbl_notifications → id=%d", notif_id)
        return notif_id

    def insert_video_short(self, payload: VideoShortsPayload) -> int:
        data = payload.model_dump()
        if isinstance(data.get("published_date"), datetime):
            data["published_date"] = data["published_date"].isoformat()
        result = self._post("api/video-shorts", data)
        vs_id = int(result.get("id") or result.get("data", {}).get("id", 0))
        logger.info("Inserted video_shorts → id=%d", vs_id)
        return vs_id


# =============================================================================
# High-Level Autonomous Publisher
# =============================================================================

class AutonomousPublisher:
    """Orchestrates the full autonomous publishing workflow.

    Accepts a validated `CuratedArticlePayload` (produced by the AI pipeline)
    and executes the complete sequence:
      1. Resolve taxonomy IDs (category → subcategory → tags → location)
      2. Insert the article into tbl_news
      3. Optionally insert into tbl_breaking_news
      4. Optionally send an app notification
      5. Optionally create a video_shorts entry
    """

    def __init__(self, client: Optional[LaravelAPIClient] = None):
        self.client = client or LaravelAPIClient()

    def publish(
        self,
        article: CuratedArticlePayload,
        primary_image_path: Optional[str] = None,
        extra_image_paths: Optional[List[str]] = None,
        source_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Execute the full autonomous publishing pipeline.

        Returns a summary dict with all created resource IDs.
        """
        now = datetime.utcnow()
        results: Dict[str, Any] = {
            "published_at": now.isoformat(),
            "source_url": source_url,
        }

        logger.info("=== Autonomous Publishing Start: '%s' ===", article.title[:60])

        # ---- 1. Resolve taxonomy ----
        category_id = self.client.resolve_category(article.category_name)
        results["category_id"] = category_id

        subcategory_id = 0
        if article.subcategory_name:
            subcategory_id = self.client.resolve_subcategory(
                article.subcategory_name, category_id=category_id,
            )
        results["subcategory_id"] = subcategory_id

        tag_id_str = self.client.resolve_tags(article.tag_names)
        results["tag_ids"] = tag_id_str

        location_id = self.client.resolve_location(
            article.location_name, article.latitude, article.longitude,
        )
        results["location_id"] = location_id

        # ---- 2. Insert main article ----
        news_payload = NewsArticlePayload(
            language_id=1,
            category_id=category_id,
            subcategory_id=subcategory_id,
            tag_id=tag_id_str or "0",
            location_id=location_id,
            title=article.title,
            slug=article.slug,
            image=primary_image_path,
            date=now,
            published_date=now.date(),
            content_type=article.content_type,
            content_value=article.content_value,
            description=article.description,
            summarized_description=article.summarized_description,
            user_id=0,
            admin_id=1,
            status=1,
            is_draft=0,
            is_comment=1,
            meta_title=article.meta_title or article.title,
            meta_description=article.meta_description or article.summarized_description,
            meta_keyword=article.meta_keyword or ",".join(article.tag_names),
            schema_markup=article.schema_markup,
            is_short_news=1 if article.is_short_news else 0,
        )
        news_id = self.client.insert_news(news_payload)
        results["news_id"] = news_id

        # ---- 3. Insert extra images ----
        if extra_image_paths:
            image_ids: List[int] = []
            for img_path in extra_image_paths:
                img_payload = NewsImagePayload(news_id=news_id, other_image=img_path)
                iid = self.client.insert_news_image(img_payload)
                image_ids.append(iid)
            results["news_image_ids"] = image_ids

        # ---- 4. Breaking news (if urgent) ----
        if article.is_breaking_news or article.urgency in ("high", "critical"):
            bn_payload = BreakingNewsPayload(
                language_id=1,
                title=article.title,
                slug=article.slug,
                image=primary_image_path,
                content_type=article.content_type,
                content_value=article.content_value,
                description=article.description,
                summarized_description=article.summarized_description,
                meta_title=article.meta_title,
                meta_description=article.meta_description,
                meta_keyword=article.meta_keyword,
                schema_markup=article.schema_markup,
            )
            bn_id = self.client.insert_breaking_news(bn_payload)
            results["breaking_news_id"] = bn_id

        # ---- 5. Push notification ----
        if article.send_notification or article.urgency == "critical":
            notif_payload = NotificationPayload(
                language_id=1,
                category_id=category_id,
                subcategory_id=subcategory_id,
                news_id=news_id,
                location_id=location_id,
                title=article.title[:191],
                message=article.summarized_description,
                type="news",
                image=primary_image_path,
                date_sent=now,
            )
            notif_id = self.client.send_notification(notif_payload)
            results["notification_id"] = notif_id

        # ---- 6. Video short ----
        if article.create_video_short and article.video_short_url:
            vs_payload = VideoShortsPayload(
                language_id=1,
                category_id=category_id,
                title=article.video_short_title or article.title[:191],
                slug=generate_slug(article.video_short_title or article.title),
                video_type=article.video_short_type,
                video_url=article.video_short_url,
                description=article.summarized_description,
                published_date=now,
                status=1,
            )
            vs_id = self.client.insert_video_short(vs_payload)
            results["video_short_id"] = vs_id

        logger.info(
            "=== Autonomous Publishing Complete: news_id=%d, category=%d, tags='%s' ===",
            news_id, category_id, tag_id_str,
        )
        return results


# Module-level singleton
publisher = AutonomousPublisher()
