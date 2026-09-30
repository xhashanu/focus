"""
Pydantic models mirroring the exact MySQL schema of the production Laravel
news application (CodeCanyon `news-admin` database).

Every model corresponds to a CREATE TABLE in 127_0_0_1.sql and carries the
exact field names, types, defaults, and constraints so that payloads can be
validated locally before being POSTed to the remote Laravel API.
"""

import datetime as _dt
import re
import unicodedata
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


# =============================================================================
# Utility: Slug Generation
# =============================================================================

def generate_slug(text: str, max_length: int = 191) -> str:
    """Generate a URL-safe slug from arbitrary text.

    Mirrors Laravel's Str::slug() behaviour:
      1. Transliterate to ASCII
      2. Lower-case
      3. Replace non-alphanumerics with hyphens
      4. Collapse consecutive hyphens
      5. Trim leading / trailing hyphens
      6. Truncate to max_length
    """
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-{2,}", "-", text)
    text = text.strip("-")
    return text[:max_length]


# =============================================================================
# Taxonomy Models  (tbl_category, tbl_subcategory, tbl_tag, tbl_location)
# =============================================================================

class CategoryPayload(BaseModel):
    """Maps to `tbl_category`."""
    language_id: int = Field(default=1, description="FK → tbl_languages.id")
    category_name: str = Field(..., max_length=191)
    slug: str = Field(default="", max_length=191)
    row_order: int = Field(default=0)
    image: Optional[str] = Field(default=None, max_length=191)
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    meta_keyword: Optional[str] = None
    schema_markup: Optional[str] = None

    @model_validator(mode="after")
    def _ensure_slug(self) -> "CategoryPayload":
        if not self.slug:
            self.slug = generate_slug(self.category_name)
        return self


class SubcategoryPayload(BaseModel):
    """Maps to `tbl_subcategory`."""
    language_id: int = Field(default=1)
    category_id: int = Field(..., description="FK → tbl_category.id")
    subcategory_name: str = Field(..., max_length=191)
    slug: str = Field(default="", max_length=191)
    row_order: int = Field(default=0)
    image: str = Field(default="", max_length=191)

    @model_validator(mode="after")
    def _ensure_slug(self) -> "SubcategoryPayload":
        if not self.slug:
            self.slug = generate_slug(self.subcategory_name)
        return self


class TagPayload(BaseModel):
    """Maps to `tbl_tag`."""
    language_id: int = Field(default=1)
    tag_name: str = Field(..., max_length=100)
    slug: str = Field(default="", max_length=191)
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    meta_keyword: Optional[str] = None
    schema_markup: Optional[str] = None
    og_image: Optional[str] = None

    @model_validator(mode="after")
    def _ensure_slug(self) -> "TagPayload":
        if not self.slug:
            self.slug = generate_slug(self.tag_name)
        return self


class LocationPayload(BaseModel):
    """Maps to `tbl_location`."""
    location_name: str = Field(..., max_length=191)
    latitude: str = Field(default="0.0", max_length=191)
    longitude: str = Field(default="0.0", max_length=191)


# =============================================================================
# Core Content Models
# =============================================================================

class NewsArticlePayload(BaseModel):
    """Maps to `tbl_news`.

    Every field mirrors the MySQL column exactly so the publisher can
    construct INSERT-ready or API-ready payloads with zero transformation.
    """
    language_id: int = Field(default=1)
    category_id: int = Field(...)
    subcategory_id: int = Field(default=0)
    tag_id: str = Field(
        ...,
        description=(
            "Comma-separated string of tbl_tag.id values, e.g. '1,5,12'. "
            "This is how the CodeCanyon schema stores tag associations."
        ),
    )
    location_id: int = Field(default=0)
    title: str = Field(..., description="News headline / title")
    slug: str = Field(default="", max_length=191)
    image: Optional[str] = Field(default=None, max_length=191, description="Primary image path or URL")
    date: Optional[_dt.datetime] = Field(default=None, description="Article datetime")
    published_date: Optional[_dt.date] = Field(default=None, description="Published date (date only)")
    content_type: str = Field(
        default="standard_post",
        max_length=50,
        description="standard_post | video_youtube | video_other | video_upload",
    )
    content_value: Optional[str] = Field(
        default=None,
        description="Video URL or embed value when content_type is not standard_post",
    )
    description: str = Field(..., description="Full article HTML body (longtext)")
    summarized_description: Optional[str] = Field(
        default=None,
        max_length=191,
        description="Short summary ≤ 191 chars for preview cards",
    )
    user_id: int = Field(default=0)
    admin_id: int = Field(default=1, description="FK → admin.id  (bot user = 1)")
    show_till: Optional[_dt.date] = Field(default=None)
    status: int = Field(default=1, description="1 = active, 0 = deactive")
    is_draft: int = Field(default=0, description="0 = published, 1 = draft")
    is_clone: int = Field(default=0)
    is_comment: int = Field(default=1, description="0 = disabled, 1 = enabled")
    counter: int = Field(default=0)
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    meta_keyword: Optional[str] = None
    schema_markup: Optional[str] = Field(
        default=None,
        description="JSON-LD schema markup for SEO",
    )
    is_short_news: int = Field(default=0, description="0 = no, 1 = yes")

    @field_validator("summarized_description", mode="before")
    @classmethod
    def _truncate_summary(cls, v: Optional[str]) -> Optional[str]:
        if v and isinstance(v, str) and len(v) > 191:
            return v[:188] + "..."
        return v

    @model_validator(mode="after")
    def _validate_fields(self) -> "NewsArticlePayload":
        if not self.slug:
            self.slug = generate_slug(self.title)
        return self


class NewsImagePayload(BaseModel):
    """Maps to `tbl_news_image`."""
    news_id: int = Field(...)
    other_image: str = Field(..., max_length=191)


class BreakingNewsPayload(BaseModel):
    """Maps to `tbl_breaking_news`."""
    language_id: int = Field(default=1)
    title: str = Field(...)
    slug: str = Field(default="", max_length=191)
    image: Optional[str] = Field(default=None, max_length=191)
    content_type: Optional[str] = Field(default=None, max_length=50)
    content_value: Optional[str] = None
    description: Optional[str] = None
    summarized_description: Optional[str] = Field(default=None, max_length=191)
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    meta_keyword: Optional[str] = None
    schema_markup: Optional[str] = None

    @field_validator("summarized_description", mode="before")
    @classmethod
    def _truncate_summary(cls, v: Optional[str]) -> Optional[str]:
        if v and isinstance(v, str) and len(v) > 191:
            return v[:188] + "..."
        return v

    @model_validator(mode="after")
    def _validate_fields(self) -> "BreakingNewsPayload":
        if not self.slug:
            self.slug = generate_slug(self.title)
        return self


class NotificationPayload(BaseModel):
    """Maps to `tbl_notifications`."""
    language_id: int = Field(default=1)
    category_id: int = Field(default=0)
    subcategory_id: int = Field(default=0)
    news_id: int = Field(...)
    location_id: int = Field(default=0)
    title: Optional[str] = Field(default=None, max_length=191)
    message: Optional[str] = None
    type: Optional[str] = Field(default=None, max_length=12)
    image: Optional[str] = Field(default=None, max_length=191)
    category_preference: int = Field(default=0)
    date_sent: _dt.datetime = Field(default_factory=_dt.datetime.utcnow)


class VideoShortsPayload(BaseModel):
    """Maps to `video_shorts`."""
    language_id: Optional[int] = Field(default=1)
    category_id: Optional[int] = None
    title: str = Field(..., max_length=191)
    slug: str = Field(default="", max_length=191)
    video_type: str = Field(
        default="video_upload",
        max_length=191,
        description="video_upload | video_youtube | video_other",
    )
    video_url: str = Field(..., max_length=191)
    description: Optional[str] = None
    published_date: Optional[_dt.datetime] = Field(default=None)
    status: int = Field(default=1)

    @model_validator(mode="after")
    def _ensure_slug(self) -> "VideoShortsPayload":
        if not self.slug:
            self.slug = generate_slug(self.title)
        return self


# =============================================================================
# Composite AI Output Model
# =============================================================================

class CuratedArticlePayload(BaseModel):
    """The complete structured output the AI pipeline must produce.

    This is the single payload that drives the entire autonomous publishing
    flow — taxonomy resolution, article insertion, optional breaking news,
    notification, and video short creation.
    """
    # Article core
    title: str = Field(..., description="Compelling headline")
    slug: str = Field(default="", max_length=191)
    description: str = Field(..., description="Full HTML body content")
    summarized_description: str = Field(
        ...,
        max_length=191,
        description="≤ 191 char summary for mobile preview cards",
    )

    # Taxonomy (names, not IDs — the publisher resolves these)
    category_name: str = Field(..., description="e.g. 'Politics', 'Sports', 'Local News'")
    subcategory_name: Optional[str] = Field(default=None)
    tag_names: List[str] = Field(default_factory=list, description="SEO tags as strings")
    location_name: str = Field(default="", description="Geo-location string")
    latitude: str = Field(default="0.0")
    longitude: str = Field(default="0.0")

    # Content type
    content_type: str = Field(
        default="standard_post",
        description="standard_post | video_youtube | video_other | video_upload",
    )
    content_value: Optional[str] = Field(
        default=None,
        description="Video URL when content_type is not standard_post",
    )

    # SEO
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    meta_keyword: Optional[str] = None
    schema_markup: Optional[str] = Field(
        default=None,
        description="JSON-LD structured data markup",
    )

    # Classification
    is_breaking_news: bool = Field(default=False, description="Publish to tbl_breaking_news as well")
    is_short_news: bool = Field(default=False, description="Mark as short/quick news")
    urgency: str = Field(
        default="normal",
        description="normal | high | critical — determines breaking news + notification",
    )
    send_notification: bool = Field(default=False, description="Push app notification on publish")

    # Video short (optional)
    create_video_short: bool = Field(default=False)
    video_short_title: Optional[str] = None
    video_short_url: Optional[str] = None
    video_short_type: str = Field(default="video_upload")

    # AI Provenance
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    ai_notes: str = Field(..., description="AI reasoning and Lens verification notes")

    @field_validator("summarized_description", mode="before")
    @classmethod
    def _truncate_summary(cls, v: Optional[str]) -> Optional[str]:
        if v and isinstance(v, str) and len(v) > 191:
            return v[:188] + "..."
        return v

    @model_validator(mode="after")
    def _validate_fields(self) -> "CuratedArticlePayload":
        if not self.slug:
            self.slug = generate_slug(self.title)
        return self
