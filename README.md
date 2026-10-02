# 📰 Focus: Autonomous AI News Curation & Editorial Pipeline

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![Celery](https://img.shields.io/badge/Celery-5.4.0-37814A.svg?logo=celery)](https://docs.celeryq.dev)
[![Redis](https://img.shields.io/badge/Redis-Queue-DC382D.svg?logo=redis)](https://redis.io)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35.0-FF4B4B.svg?logo=streamlit)](https://streamlit.io)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-2.0+-E92063.svg?logo=pydantic)](https://docs.pydantic.dev)
[![NVIDIA NIM](https://img.shields.io/badge/NVIDIA-Nemotron--3--Ultra-76B900.svg?logo=nvidia)](https://build.nvidia.com/nvidia/nemotron-3-ultra-550b-a55b)
[![SerpApi](https://img.shields.io/badge/SerpApi-Google%20Lens-4285F4.svg?logo=google)](https://serpapi.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Focus** is an end-to-end, asynchronous media intelligence pipeline that transforms unstructured social media video clips (from **Instagram Reels**, **TikTok**, and **X / Twitter**) into fully verified, localized, SEO-optimized news articles and broadcasts them to production news mobile apps and websites.

The engine supports two operational modes:
1. 🚀 **Fully Autonomous Publishing**: Zero human intervention. Multimodal extraction, reverse visual verification via Google Lens, AI-powered structured schema hydration (NVIDIA Nemotron-3-Ultra or Gemini 1.5 Pro — switchable from the dashboard), taxonomy auto-resolution, and immediate transactional publishing to production.
2. ✍️ **Human-in-the-Loop Editorial Desk**: Interactive internal Streamlit workspace for journalists and editors to inspect evidence, preview audio/keyframes, refine content, and approve publication with one click.

---

## 📑 Table of Contents

- [System Architecture](#-system-architecture)
- [Key Features](#-key-features)
- [Operational Modes](#-operational-modes)
- [Database Schema Alignment (`127_0_0_1.sql`)](#-database-schema-alignment-127_0_0_1sql)
- [Project Directory Structure](#-project-directory-structure)
- [Services & Core Components](#-services--core-components)
- [Streamlit Editorial Studio](#-streamlit-editorial-studio)
- [REST API Reference](#-rest-api-reference)
- [Installation & Quickstart](#-installation--quickstart)
- [Running the Test Suite](#-running-the-test-suite)
- [Environment Configuration](#-environment-configuration)
- [Architecture Principles & Strict Isolation](#-architecture-principles--strict-isolation)

---

## 🏗 System Architecture

```
                               +-----------------------------+
                               |   Social Video URL (IG/X)   |
                               +--------------+--------------+
                                              |
                                              v
                                [ FastAPI Ingestion Endpoint ]
                                     (POST /api/v1/curate)
                                              |
                                              v
                                    [ Celery Task Queue ]
                                              | (via Redis)
             +--------------------------------+--------------------------------+
             |                                |                                |
             v                                v                                v
     1. yt-dlp Bypass                 2. ffmpeg Slicing               3. SerpApi Lens
     (Direct Video Stream)           (MP3 Track & Keyframes)          (Visual Geolocation)
             |                                |                                |
             +--------------------------------+--------------------------------+
                                              |
                                              v
                          [ AI Curator (Switchable Engine) ]
                     - NVIDIA Nemotron-3-Ultra-550B (Default)
                     - Gemini 1.5 Pro (Fallback/Alternative)
                        - Structured CuratedArticlePayload Output
                        - JSON-LD NewsArticle Schema Markup
                        - Slug Generation & ≤ 191 Char Summaries
                        - Urgency Classification (normal/high/critical)
                                              |
                      +-----------------------+-----------------------+
                      |                                               |
        [ Mode: AUTONOMOUS ]                            [ Mode: HUMAN-REVIEW ]
                      |                                               |
                      v                                               v
        [ Autonomous Publisher ]                         [ SQLite Local Queue ]
        - Auto-resolve Categories/Tags                   - Audit trail storage
        - Insert tbl_news (status=1)                     - Pending editorial review
        - Insert tbl_news_image                                       |
        - Optional tbl_breaking_news                                  v
        - Push tbl_notifications                         [ Streamlit Studio ]
        - Optional video_shorts                          - Evidence Inspection
                      |                                  - HTML & Meta Editor
                      |                                  - 1-Click Approve & Push
                      |                                               |
                      +-----------------------+-----------------------+
                                              |
                                              v
                               [ Production Laravel REST API ]
                                (STRICT ISOLATION - HTTP Only)
                                              |
                                              v
                           [ Production MySQL DB & Flutter Apps ]
```

---

## ⚡ Key Features

- **Dual LLM Engine with Dashboard Switcher**: Choose between **NVIDIA Nemotron-3-Ultra-550B** (free via NIM API) and **Google Gemini 1.5 Pro** directly from the Streamlit sidebar. The active engine is shown in real-time badges and can be switched per-request or globally.
- **Multimodal Video Processing**: Uses `yt-dlp` with spoofed mobile user-agents to bypass social platform scraping walls, and `ffmpeg` to extract audio tracks and representative keyframe bursts.
- **Reverse Visual Geolocation**: Integrates with [SerpApi Google Lens](https://serpapi.com/manage-api-key) to cross-reference keyframes against global visual databases, pinpointing real-world locations, landmarks, and contextual corroboration.
- **Production MySQL Schema Alignment**: Models strictly mirror the CodeCanyon Laravel news schema (`127_0_0_1.sql`), ensuring zero payload transformation issues when inserting into `tbl_news`, `tbl_category`, `tbl_subcategory`, `tbl_tag`, `tbl_location`, `tbl_news_image`, `tbl_breaking_news`, `tbl_notifications`, and `video_shorts`.
- **Automatic Taxonomy Resolution**: Find-or-create workflow for categories, subcategories, tags (resolved to comma-separated ID strings, e.g. `"1,5,12"`), and geographic locations.
- **SEO & Structured Data Automation**: Generates clean, URL-safe slugs, meta descriptions, and Google-compliant JSON-LD `NewsArticle` schema markup.
- **Urgency-Driven Publishing**: Automatically classifies stories as `normal`, `high`, or `critical`. High/critical events trigger `tbl_breaking_news` entries and mobile push notifications (`tbl_notifications`).
- **Shorts / Quick News Detection**: Videos under 60 seconds are formatted into `video_shorts` and flagged with `is_short_news=1`.
- **Live Worker Polling**: Streamlit frontend polls Celery task states in real-time, displaying a dynamic 5-stage progress stepper and live execution logs.
- **Reasoning Token Stripping**: NVIDIA Nemotron models may emit `<think>...</think>` reasoning traces; these are automatically stripped before Pydantic validation, ensuring clean JSON parsing.

---

## 🔄 Operational Modes

### 1. 🚀 Fully Autonomous Mode (`AUTO_PUBLISH=True`)
Ideal for automated newsrooms and rapid breaking alerts:
- The worker executes all stages automatically.
- The AI Curator synthesizes a publication-ready JSON payload.
- The `AutonomousPublisher` resolves all taxonomy IDs over HTTP and executes transactional publishing into the live database.
- A local record is saved in SQLite for audit history with `status = APPROVED`.

### 2. ✍️ Human-in-the-Loop Mode (`AUTO_PUBLISH=False`)
Designed for editorial oversight and fact-checking:
- The worker executes media extraction, Lens geolocation, and initial drafting.
- The draft is saved in local SQLite with `status = PENDING`.
- Journalists open the Streamlit Editorial Studio, review visual evidence, listen to audio, refine headlines or HTML content, and click **"Approve & Push to Laravel"**.

> **Note:** The operational mode can be overridden per request via the `auto_publish` parameter in the API payload or selected directly from the Streamlit UI.

---

## 🗄 Database Schema Alignment (`127_0_0_1.sql`)

All Pydantic models in [`app/schemas/schema_models.py`](file:///c:/Users/sanan/OneDrive/Desktop/focus/app/schemas/schema_models.py) map 1:1 to the production Laravel database tables:

| MySQL Table | Pydantic Schema Model | Key Columns & Mappings |
| :--- | :--- | :--- |
| `tbl_news` | `NewsArticlePayload` | `id`, `language_id=1`, `category_id`, `subcategory_id`, `tag_id` (CSV string), `location_id`, `title`, `slug`, `image`, `date`, `published_date`, `content_type`, `content_value`, `description` (HTML), `summarized_description` (auto-truncated ≤ 191 chars), `user_id=0`, `admin_id=1`, `status=1`, `is_draft=0`, `is_comment=1`, `counter=0`, `meta_title`, `meta_description`, `meta_keyword`, `schema_markup`, `is_short_news` |
| `video_shorts` | `VideoShortsPayload` | `language_id`, `category_id`, `title`, `slug`, `video_type` (`video_upload`/`video_youtube`), `video_url`, `description`, `published_date`, `status=1` |
| `tbl_breaking_news` | `BreakingNewsPayload` | `language_id`, `title`, `slug`, `image`, `content_type`, `content_value`, `description`, `summarized_description`, `schema_markup` |
| `tbl_notifications` | `NotificationPayload` | `language_id`, `category_id`, `subcategory_id`, `news_id`, `location_id`, `title`, `message`, `type`, `image`, `date_sent` |
| `tbl_category` | `CategoryPayload` | `language_id`, `category_name`, `slug` (auto-generated), `row_order=0`, `image`, `schema_markup` |
| `tbl_subcategory` | `SubcategoryPayload` | `language_id`, `category_id`, `subcategory_name`, `slug`, `row_order=0`, `image` |
| `tbl_tag` | `TagPayload` | `language_id`, `tag_name`, `slug`, `meta_title`, `schema_markup` |
| `tbl_location` | `LocationPayload` | `location_name`, `latitude`, `longitude` |
| `tbl_news_image` | `NewsImagePayload` | `news_id`, `other_image` |
| Composite Schema | `CuratedArticlePayload` | Unified AI output payload containing all content, taxonomy names, and urgency flags |

---

## 📁 Project Directory Structure

```
focus/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── api.py                    # Root v1 APIRouter combining endpoints
│   │       └── endpoints/
│   │           ├── curate.py             # POST /api/v1/curate (Ingestion & trigger)
│   │           ├── drafts.py             # GET/PATCH /api/v1/drafts, POST /publish
│   │           ├── system.py             # GET /stats, POST /cleanup
│   │           └── tasks.py              # GET /api/v1/tasks/{id} (Live polling)
│   ├── db/
│   │   └── session.py                    # SQLAlchemy SQLite engine & sessionmaker
│   ├── models/
│   │   ├── base.py                       # SQLAlchemy Declarative Base
│   │   └── draft.py                      # Draft entity, status enum, and media paths
│   ├── schemas/
│   │   ├── ai_article.py                 # Editorial AI draft response model
│   │   ├── curate.py                     # CurateRequest (with auto_publish) & Response
│   │   ├── draft.py                      # Draft update & detail schemas
│   │   ├── schema_models.py              # Production MySQL Pydantic models (127_0_0_1.sql)
│   │   └── task.py                       # Celery task progress response schema
│   ├── services/
│   │   ├── ai.py                         # Multimodal draft synthesis service
│   │   ├── ai_curator.py                 # Structured Gemini 1.5 Pro curator service
│   │   ├── laravel.py                    # Manual approval webhook push service
│   │   ├── media.py                      # yt-dlp & ffmpeg extraction service
│   │   ├── publisher.py                  # Autonomous publisher & taxonomy resolver
│   │   └── search.py                     # SerpApi Google Lens visual context service
│   ├── workers/
│   │   ├── celery_app.py                 # Celery app configured with Redis
│   │   └── tasks.py                      # process_news_link dual-mode pipeline task
│   ├── config.py                         # Pydantic BaseSettings configuration
│   └── main.py                           # FastAPI application entrypoint & static mount
├── frontend/
│   └── app.py                            # Streamlit Human Editorial & Live Monitor Studio
├── storage/
│   └── temp/                             # Local temporary media scratch workspace
├── tests/
│   └── test_autonomous_publisher.py      # Unit & integration test suite (14 test cases)
├── 127_0_0_1.sql                         # Production MySQL schema reference dump
├── .env.example                          # Environment configuration template
├── requirements.txt                      # Python dependencies
├── architecture.md                       # High-level architecture specification
├── context.md                            # Development rules & strict isolation constraints
└── goal.md                               # Project mission & acceptance criteria
```

---

## ⚙️ Services & Core Components

### 1. Autonomous Publisher ([`app/services/publisher.py`](file:///c:/Users/sanan/OneDrive/Desktop/focus/app/services/publisher.py))
- **`LaravelAPIClient`**: Low-level HTTP client handling communication with the production Laravel REST API.
- **Taxonomy Resolution**:
  - `resolve_category(name)`: Queries `/api/categories`; creates category if not present.
  - `resolve_subcategory(name, category_id)`: Queries `/api/subcategories`; creates if missing.
  - `resolve_tags(names)`: Queries `/api/tags`; creates missing tags and formats comma-separated ID string (e.g., `"1,4,8"`).
  - `resolve_location(name, lat, lon)`: Queries `/api/locations`; creates if missing.
- **Transactional Content Insertion**:
  - Inserts article into `tbl_news`.
  - Inserts sliced keyframes into `tbl_news_image`.
  - Inserts urgent articles into `tbl_breaking_news`.
  - Dispatches push alerts via `tbl_notifications`.
  - Inserts short video records into `video_shorts`.

### 2. AI Curation Engine ([`app/services/ai_curator.py`](file:///c:/Users/sanan/OneDrive/Desktop/focus/app/services/ai_curator.py))
- **`CURATOR_SYSTEM_PROMPT`**: Enforces strict output compliance matching `CuratedArticlePayload`.
- **Dual LLM Provider Support**:
  - **`nvidia_nemotron`** (default): Calls NVIDIA NIM API (`https://integrate.api.nvidia.com/v1/chat/completions`) with model `nvidia/nemotron-3-ultra-550b-a55b`. Reasoning tokens (`<think>...</think>`) are auto-stripped.
  - **`gemini`**: Calls Google Gemini 1.5 Pro via `google.generativeai` SDK.
- **Multi-Tier Execution Fallback**:
  1. Selected LLM provider (NVIDIA Nemotron or Gemini).
  2. Automatic fallback to the alternate provider on failure.
  3. Offline development mock with full schema validation for local testing.
- **Provider Selection**: Controlled via `DEFAULT_LLM_PROVIDER` env var, dashboard sidebar toggle, or per-request `llm_provider` parameter.

### 3. Media Processing Pipeline ([`app/services/media.py`](file:///c:/Users/sanan/OneDrive/Desktop/focus/app/services/media.py))
- **`download_video(url)`**: Uses `yt-dlp` with randomized user-agents and format selection to acquire raw MP4 streams.
- **`extract_audio(video_path)`**: Uses `ffmpeg` to extract a 128kbps mono MP3 track for speech transcription.
- **`extract_keyframes(video_path, num_frames=3)`**: Extracts evenly spaced JPG keyframes across the video timeline.

### 4. Visual Verification Service ([`app/services/search.py`](file:///c:/Users/sanan/OneDrive/Desktop/focus/app/services/search.py))
- **`search_keyframe_context(image_path)`**: Uploads primary keyframes to SerpApi Google Lens reverse search to extract visual match clues, entity names, and Google Knowledge Graph facts.

---

## 🖥 Streamlit Editorial Studio

The internal newsroom panel is built with **Streamlit** and features a cyber-dark aesthetic designed for high information density:

```bash
py -m streamlit run frontend/app.py --server.port 8501
```

### Studio Features:
1. **Sidebar — AI Engine Switcher & API Credentials**:
   - **Active Model Switcher**: Radio toggle between `🤖 NVIDIA Nemotron` and `🧠 Gemini 1.5 Pro` with a quick-switch button. The selected engine is passed to every pipeline invocation.
   - **API Credentials Manager**: Expandable panel to view/update SerpApi, NVIDIA, and Gemini API keys live — with direct links to get free keys.
2. **Live Pipeline & Ingestion Monitor (Tab 1)**:
   - Paste video URLs or select quick demo presets (Instagram Reel, TikTok, X clip).
   - Toggle **Curation Mode**:
     - `🚀 Fully Autonomous (Live DB)`: Publishes directly to production.
     - `✍️ Editorial Review (Draft)`: Generates draft for editorial review.
   - **AI Engine** dropdown per-ingestion: Override the global engine for individual jobs.
   - Live visual step tracker across all 5 pipeline stages, branded with the active engine.
   - Embedded streaming terminal displaying real-time worker logs.
3. **Editorial Desk & Approval Panel (Tab 2)**:
   - Split-screen workspace: Left panel shows keyframe carousel, embedded audio player, and Lens evidence; right panel offers headline, category, location, and HTML body editors.
   - Dual preview: HTML source editor and live mobile app simulation preview.
   - Action bar: Save edits, reject, or approve & push live to Laravel.
4. **Published Articles Archive (Tab 3)**:
   - Searchable history of all articles with live post IDs, timestamps, and categories.
5. **System Diagnostics (Tab 4)**:
   - Connection status, SQLite draft counts, storage disk usage, and one-click media cache cleaner.

---

## 📡 REST API Reference

### Ingestion & Pipeline Control
- **`POST /api/v1/curate`**
  - **Request Body**:
    ```json
    {
      "url": "https://www.instagram.com/reel/C8xyz_sample/",
      "auto_publish": true
    }
    ```
  - **Response (202 Accepted)**:
    ```json
    {
      "task_id": "c1f7b04a-718d-4299-8ea5-055f6920b72c",
      "status": "ACCEPTED",
      "message": "Media acquisition and AI news curation pipeline dispatched (AUTONOMOUS).",
      "source_url": "https://www.instagram.com/reel/C8xyz_sample/",
      "mode": "AUTONOMOUS"
    }
    ```

### Live Progress Polling
- **`GET /api/v1/tasks/{task_id}`**
  - **Response**:
    ```json
    {
      "task_id": "c1f7b04a-718d-4299-8ea5-055f6920b72c",
      "state": "PROGRESS",
      "stage": "AI_CURATING",
      "progress": 70,
      "details": "AI Curator generating production-ready article with full schema compliance...",
      "mode": "AUTONOMOUS"
    }
    ```

### Editorial Draft Management
- **`GET /api/v1/drafts`**: List drafts with optional `?status=PENDING` filter.
- **`GET /api/v1/drafts/{id}`**: Fetch full draft detail, including media paths and Lens notes.
- **`PATCH /api/v1/drafts/{id}`**: Update headline, summary, body content, category, or location.
- **`POST /api/v1/drafts/{id}/publish`**: Manually approve and push draft to Laravel.
- **`DELETE /api/v1/drafts/{id}`**: Reject draft and purge local scratch media.

### System Configuration & Diagnostics
- **`GET /api/v1/system/config`**: Retrieve current API key status (masked) and active LLM provider.
- **`POST /api/v1/system/config`**: Dynamically update API keys (`serpapi_api_key`, `nvidia_api_key`, `gemini_api_key`) and `default_llm_provider` at runtime without restarting.
- **`GET /api/v1/system/stats`**: Backend health, database counts, active LLM provider, and storage metrics.
- **`POST /api/v1/system/cleanup`**: Delete orphaned temporary media files.

---

## 🚀 Installation & Quickstart

### 1. Prerequisites
- **Python 3.11+**
- **FFmpeg**: Must be installed and accessible on system `PATH`
- **Redis Server**: Running locally or via Docker (`docker run -p 6379:6379 redis:alpine`)

### 2. Environment Setup
```bash
# Clone the repository
git clone https://github.com/xhashanu/focus.git
cd focus

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate       # On Linux/macOS
.venv\Scripts\activate          # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env` and provide your credentials:
```bash
cp .env.example .env
```
Key settings:
```ini
# Search & Visual Geolocation (free: https://serpapi.com/manage-api-key)
SERPAPI_API_KEY="your_serpapi_key"

# LLM Provider: "nvidia_nemotron" (default) or "gemini"
DEFAULT_LLM_PROVIDER="nvidia_nemotron"

# NVIDIA NIM API (free: https://build.nvidia.com/nvidia/nemotron-3-ultra-550b-a55b)
NVIDIA_API_KEY="your_nvidia_api_key"
NVIDIA_BASE_URL="https://integrate.api.nvidia.com/v1"
NVIDIA_MODEL="nvidia/nemotron-3-ultra-550b-a55b"

# Google Gemini (alternative LLM)
GEMINI_API_KEY="your_gemini_api_key"

# Laravel Production API
LARAVEL_API_URL="https://your-news-admin-domain.com/api"
LARAVEL_API_TOKEN="your_secure_bearer_token"

AUTO_PUBLISH=False
```

> **💡 Tip:** Both NVIDIA NIM and SerpApi offer free API keys. You can also update keys live from the Streamlit sidebar without restarting any services.

### 4. Start the Application Services (Single Command)

We have provided a unified startup script that automatically launches the **FastAPI Backend**, **Celery Worker**, and **Streamlit Studio** all at once in a single terminal.

```bash
py start.py
```

- **Streamlit Studio**: `http://localhost:8501`
- **FastAPI Interactive Docs**: `http://127.0.0.1:8000/docs`

*(To shut down the entire pipeline, simply press `Ctrl+C` in the terminal).*

---

## 🧪 Running the Test Suite

The test suite thoroughly verifies the entire pipeline: slug generation, summary truncation under 191 characters, strict Pydantic model validation against `127_0_0_1.sql`, mock taxonomy resolution, and end-to-end publisher workflows.

Execute the test suite directly with Python:
```bash
py tests/test_autonomous_publisher.py
```

### Test Results:
```
Running 14 test functions...
  [PASS] test_generate_slug
  [PASS] test_auto_slug_in_models
  [PASS] test_summary_truncation_under_191
  [PASS] test_news_article_payload_exact_fields
  [PASS] test_breaking_news_payload
  [PASS] test_video_shorts_payload
  [PASS] test_notification_payload
  [PASS] test_resolve_existing_category
  [PASS] test_create_new_category_when_not_found
  [PASS] test_resolve_tags_batch_mapping
  [PASS] test_resolve_location
  [PASS] test_autonomous_publisher_full_flow
  [PASS] test_ai_curator_system_prompt_rules
  [PASS] test_ai_curator_dev_fallback_validates_cleanly

Test Results: 14 passed, 0 failed.
ALL TESTS PASSED SUCCESSFULLY!
```

---

## 🔒 Architecture Principles & Strict Isolation

1. **Strict Database Isolation**: Focus **never** connects directly to the production MySQL database via direct socket or raw SQL credentials. All mutations occur exclusively through authenticated HTTP REST API calls to the Laravel backend.
2. **Ephemeral Media Storage**: Raw video streams, extracted MP3 audio files, and keyframes are written to `./storage/temp` and automatically purged once articles are published or rejected.
3. **Resilience & Graceful Degradation**:
   - If Google Lens returns no matches, the AI curator uses extracted audio and video metadata.
   - If external AI APIs are unreachable, the system utilizes a verified offline fallback schema ensuring the pipeline never crashes.
   - Network requests to the Laravel API feature exponential backoff retry mechanisms with clear audit logs in SQLite.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
