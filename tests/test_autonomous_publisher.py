"""
Unit and Integration Tests for Autonomous Publishing Architecture.

Tests:
1. Pydantic schema validation & SQL compatibility (127_0_0_1.sql)
2. Slug generation & 191-char summary truncation
3. Taxonomy resolution (Category, Subcategory, Tags, Location)
4. Transactional publishing workflow via AutonomousPublisher
5. AI Curator payload hydration & validation
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
from unittest.mock import MagicMock, patch
from datetime import datetime, date

from app.schemas.schema_models import (
    generate_slug,
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
)
from app.services.publisher import LaravelAPIClient, AutonomousPublisher, PublisherError
from app.services.ai_curator import AICuratorService, CURATOR_SYSTEM_PROMPT


# =============================================================================
# 1. Slug & Truncation Utility Tests
# =============================================================================

def test_generate_slug():
    assert generate_slug("Breaking: Fire in Central Market!") == "breaking-fire-in-central-market"
    assert generate_slug("   Multiple   Spaces   -- and symbols @#$ ") == "multiple-spaces-and-symbols"
    # Max length truncation
    long_title = "a" * 300
    slug = generate_slug(long_title, max_length=191)
    assert len(slug) <= 191


def test_auto_slug_in_models():
    cat = CategoryPayload(category_name="Local News")
    assert cat.slug == "local-news"

    sub = SubcategoryPayload(category_id=1, subcategory_name="Howrah District")
    assert sub.slug == "howrah-district"

    tag = TagPayload(tag_name="Emergency Response")
    assert tag.slug == "emergency-response"

    news = NewsArticlePayload(
        category_id=1,
        tag_id="1,2",
        title="Dramatic Rescue at Hooghly Bridge",
        description="<p>Full story</p>",
    )
    assert news.slug == "dramatic-rescue-at-hooghly-bridge"


def test_summary_truncation_under_191():
    long_summary = "A" * 250
    article = CuratedArticlePayload(
        title="Test Headline",
        description="<p>Body</p>",
        summarized_description=long_summary,
        category_name="Crime",
        confidence_score=0.9,
        ai_notes="Test note",
    )
    assert len(article.summarized_description) <= 191
    assert article.summarized_description.endswith("...")


# =============================================================================
# 2. Schema Model Validation (Matching 127_0_0_1.sql)
# =============================================================================

def test_news_article_payload_exact_fields():
    now = datetime.utcnow()
    payload = NewsArticlePayload(
        language_id=1,
        category_id=5,
        subcategory_id=12,
        tag_id="3,7,9",
        location_id=2,
        title="Municipal Corporation Announces New Metro Extension",
        image="uploads/news/metro_ext.jpg",
        date=now,
        published_date=now.date(),
        content_type="standard_post",
        description="<p>The municipal corporation approved line 3.</p>",
        summarized_description="Municipal corporation approves new metro extension.",
        user_id=0,
        admin_id=1,
        status=1,
        is_draft=0,
        is_comment=1,
        meta_title="Metro Extension Approved",
        meta_description="Details on new metro line",
        meta_keyword="metro, transport, city",
        schema_markup='{"@context": "https://schema.org"}',
        is_short_news=0,
    )
    data = payload.model_dump()
    assert data["status"] == 1
    assert data["is_draft"] == 0
    assert data["admin_id"] == 1
    assert data["tag_id"] == "3,7,9"
    assert data["slug"] == "municipal-corporation-announces-new-metro-extension"


def test_breaking_news_payload():
    bn = BreakingNewsPayload(
        language_id=1,
        title="Flash Floods Alert Issued for Coastal Belt",
        image="uploads/alert.jpg",
        description="<p>Residents advised to stay indoors.</p>",
        summarized_description="Flash flood warning issued for coastal belt.",
    )
    assert bn.slug == "flash-floods-alert-issued-for-coastal-belt"
    assert bn.language_id == 1


def test_video_shorts_payload():
    vs = VideoShortsPayload(
        language_id=1,
        category_id=3,
        title="30s Look at Heritage Tram Ride",
        video_type="video_upload",
        video_url="uploads/shorts/tram_30s.mp4",
        description="Quick tram ride clip",
        status=1,
    )
    assert vs.status == 1
    assert vs.slug == "30s-look-at-heritage-tram-ride"


def test_notification_payload():
    notif = NotificationPayload(
        news_id=42,
        title="Emergency Weather Warning",
        message="Severe squall anticipated within 2 hours.",
        type="news",
    )
    assert notif.news_id == 42
    assert notif.date_sent is not None


# =============================================================================
# 3. Taxonomy Resolution Tests (Mocked Laravel API Client)
# =============================================================================

def test_resolve_existing_category():
    client = LaravelAPIClient(base_url="http://test.local", api_token="test-token")
    client._get = MagicMock(return_value={"data": [{"id": 10, "category_name": "Politics"}]})

    cat_id = client.resolve_category("Politics")
    assert cat_id == 10
    client._get.assert_called_once()


def test_create_new_category_when_not_found():
    client = LaravelAPIClient(base_url="http://test.local", api_token="test-token")
    client._get = MagicMock(return_value={"data": []})
    client._post = MagicMock(return_value={"id": 45, "category_name": "Artificial Intelligence"})

    cat_id = client.resolve_category("Artificial Intelligence")
    assert cat_id == 45
    client._post.assert_called_once()


def test_resolve_tags_batch_mapping():
    client = LaravelAPIClient(base_url="http://test.local", api_token="test-token")
    # Tag 1 exists (id=1), Tag 2 doesn't exist
    client._get = MagicMock(return_value={"data": [{"id": 1, "tag_name": "weather"}]})
    client._post = MagicMock(return_value={"id": 88, "tag_name": "cyclone"})

    tag_ids = client.resolve_tags(["weather", "cyclone"])
    assert tag_ids == "1,88"


def test_resolve_location():
    client = LaravelAPIClient(base_url="http://test.local", api_token="test-token")
    client._get = MagicMock(return_value={"data": [{"id": 5, "location_name": "Kolkata"}]})

    loc_id = client.resolve_location("Kolkata")
    assert loc_id == 5


# =============================================================================
# 4. End-to-End Autonomous Publishing Workflow Test
# =============================================================================

def test_autonomous_publisher_full_flow():
    client = LaravelAPIClient(base_url="http://mock-laravel.test", api_token="secret")

    # Mock taxonomy resolution
    client.resolve_category = MagicMock(return_value=7)
    client.resolve_subcategory = MagicMock(return_value=14)
    client.resolve_tags = MagicMock(return_value="3,9,11")
    client.resolve_location = MagicMock(return_value=2)

    # Mock content insertions
    client.insert_news = MagicMock(return_value=501)
    client.insert_news_image = MagicMock(return_value=1001)
    client.insert_breaking_news = MagicMock(return_value=201)
    client.send_notification = MagicMock(return_value=301)
    client.insert_video_short = MagicMock(return_value=401)

    publisher = AutonomousPublisher(client=client)

    article = CuratedArticlePayload(
        title="High Alert: Industrial Warehouse Fire Contained in North Port",
        slug="high-alert-industrial-warehouse-fire-contained",
        description="<p>Over 12 fire tenders responded promptly.</p>",
        summarized_description="Major warehouse fire contained in North Port with zero casualties reported.",
        category_name="Breaking News",
        subcategory_name="Industrial Incidents",
        tag_names=["Fire", "Emergency", "NorthPort", "Safety"],
        location_name="North Port Dockyard",
        latitude="22.585",
        longitude="88.332",
        content_type="standard_post",
        meta_title="Warehouse Fire Contained",
        meta_description="North Port warehouse fire under control.",
        schema_markup='{"@context":"https://schema.org","@type":"NewsArticle"}',
        is_breaking_news=True,
        urgency="critical",
        send_notification=True,
        create_video_short=True,
        video_short_title="Raw Scene: Firefighters Battling Flames",
        video_short_url="https://storage.local/clips/fire_raw.mp4",
        confidence_score=0.97,
        ai_notes="Verified against regional emergency dispatch logs and Google Lens imagery.",
    )

    result = publisher.publish(
        article=article,
        primary_image_path="storage/temp/keyframe_0.jpg",
        extra_image_paths=["storage/temp/keyframe_1.jpg", "storage/temp/keyframe_2.jpg"],
        source_url="https://x.com/localreporter/status/189283719",
    )

    # Verify all components were invoked correctly
    assert result["news_id"] == 501
    assert result["category_id"] == 7
    assert result["subcategory_id"] == 14
    assert result["tag_ids"] == "3,9,11"
    assert result["location_id"] == 2
    assert result["breaking_news_id"] == 201
    assert result["notification_id"] == 301
    assert result["video_short_id"] == 401
    assert len(result["news_image_ids"]) == 2

    client.insert_news.assert_called_once()
    client.insert_breaking_news.assert_called_once()
    client.send_notification.assert_called_once()
    client.insert_video_short.assert_called_once()
    assert client.insert_news_image.call_count == 2


# =============================================================================
# 5. AI Curator Prompt & Fallback Payload Test
# =============================================================================

def test_ai_curator_system_prompt_rules():
    assert "tbl_news" in CURATOR_SYSTEM_PROMPT or "Laravel" in CURATOR_SYSTEM_PROMPT
    assert "191 characters" in CURATOR_SYSTEM_PROMPT
    assert "schema_markup" in CURATOR_SYSTEM_PROMPT
    assert "urgency" in CURATOR_SYSTEM_PROMPT


def test_ai_curator_dev_fallback_validates_cleanly():
    service = AICuratorService()
    fallback = service._dev_fallback(
        lens_context={"clues": ["Howrah Station", "Crowd gathering"], "knowledge_graph": {}},
        source_url="https://instagram.com/reel/demo123",
    )
    assert isinstance(fallback, CuratedArticlePayload)
    assert len(fallback.summarized_description) <= 191
    assert fallback.category_name != ""
    assert fallback.confidence_score > 0.0
    # Check JSON serialization of the model
    dumped = fallback.model_dump_json()
    assert isinstance(dumped, str)


if __name__ == "__main__":
    import inspect
    tests = [fn for name, fn in list(globals().items()) if name.startswith("test_") and callable(fn)]
    passed = 0
    failed = 0
    print(f"Running {len(tests)} test functions...")
    for t in tests:
        try:
            t()
            passed += 1
            print(f"  [PASS] {t.__name__}")
        except Exception as e:
            failed += 1
            print(f"  [FAIL] {t.__name__}: {e}")
            import traceback
            traceback.print_exc()

    print(f"\nTest Results: {passed} passed, {failed} failed.")
    if failed > 0:
        exit(1)
    else:
        print("ALL TESTS PASSED SUCCESSFULLY!")

