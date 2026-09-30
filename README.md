# Focus: AI News Curation Pipeline

A standalone, asynchronous backend pipeline and editorial studio that automates the curation of localized news articles from social media video links (Instagram, TikTok, X).

The system downloads raw video, extracts audio tracks and keyframes, reverse-searches frames on Google Lens for geolocation and context verification, uses Gemini multimodal AI to generate localized news drafts, and provides an internal Streamlit review panel to approve and push articles to a live Flutter/Laravel news app via REST API.

---

## Architecture Overview

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
                           [ Celery + Redis ]
                                     |
    +--------------------------------+--------------------------------+
    |                                |                                |
    v                                v                                v
1. yt-dlp Video Download    2. ffmpeg Audio & Frames    3. SerpApi Lens Geolocation
    |                                |                                |
    +--------------------------------+--------------------------------+
                                     |
                                     v
                   [ Antigravity / Gemini Multimodal AI ]
                   (Structured localized news generation)
                                     |
                                     v
                        [ SQLite Local Drafts DB ]
                                     |
                     +---------------+---------------+
                     |                               |
                     v                               v
         [ Streamlit Approval Panel ]       [ Live Task Progress ]
         - Inspect Keyframes & Notes        - Real-time stage polling
         - Edit Headline/HTML Body          - 0% -> 100% status widget
                     |
                     v (Human Approved)
       [ Laravel REST API Webhook Push ]
         (STRICT ISOLATION - HTTP Only)
```

---

## Directory Structure

```
focus/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── api.py                    # Root v1 router
│   │       └── endpoints/
│   │           ├── curate.py             # POST /api/v1/curate
│   │           ├── drafts.py             # GET/PATCH /api/v1/drafts, POST /publish
│   │           └── tasks.py              # GET /api/v1/tasks/{id} (Live polling)
│   ├── db/
│   │   └── session.py                    # SQLite engine and session dependency
│   ├── models/
│   │   ├── base.py                       # SQLAlchemy Base
│   │   └── draft.py                      # Draft model and statuses
│   ├── schemas/
│   │   ├── ai_article.py                 # Structured AI output schema
│   │   ├── curate.py                     # Ingestion request & response schemas
│   │   ├── draft.py                      # Draft detail, list & publish schemas
│   │   └── task.py                       # Live task status schema
│   ├── services/
│   │   ├── ai.py                         # Multimodal Antigravity/Gemini service
│   │   ├── laravel.py                    # External Laravel REST push client
│   │   ├── media.py                      # yt-dlp & ffmpeg extraction service
│   │   └── search.py                     # SerpApi Google Lens context service
│   ├── workers/
│   │   ├── celery_app.py                 # Celery app configured with Redis
│   │   └── tasks.py                      # process_news_link background task
│   ├── config.py                         # Pydantic Settings configuration
│   └── main.py                           # FastAPI application entrypoint
├── frontend/
│   └── app.py                            # Streamlit Human Editorial & Live Monitor
├── storage/
│   └── temp/                             # Local temporary media workspace
├── .env.example                          # Environment variables template
├── requirements.txt                      # Project dependencies
├── architecture.md                       # System architecture document
├── context.md                            # Development constraints & rules
└── goal.md                               # Project business goals
```

---

## Quickstart Guide

### 1. Requirements & Prerequisites
* **Python 3.11+**
* **Redis Server** (running locally on port 6379 or remote)
* **FFmpeg** (installed and added to system PATH)

### 2. Environment Setup
```bash
# Copy environment configuration
cp .env.example .env

# Install dependencies
pip install -r requirements.txt
```

### 3. Launching Services

#### Step 1: Start Redis
Ensure your local Redis server is active:
```bash
redis-server
```

#### Step 2: Start the FastAPI Backend
```bash
uvicorn app.main:app --reload --port 8000
```
Interactive Swagger docs will be live at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

#### Step 3: Start the Celery Worker
On Windows:
```bash
celery -A app.workers.celery_app worker --loglevel=info -P solo
```
On Linux / macOS:
```bash
celery -A app.workers.celery_app worker --loglevel=info
```

#### Step 4: Start the Streamlit Human Review Panel
```bash
streamlit run frontend/app.py
```
Open your browser at: [http://localhost:8501](http://localhost:8501)

---

## API Endpoints Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/curate` | Submits social link and dispatches background curation pipeline |
| `GET` | `/api/v1/tasks/{task_id}` | Polls live task execution stage and progress (0-100%) |
| `GET` | `/api/v1/drafts` | Lists pending and processed drafts |
| `GET` | `/api/v1/drafts/{id}` | Retrieves full draft data including media paths and Lens notes |
| `PATCH`| `/api/v1/drafts/{id}` | Updates draft headline, summary, location, tags, or body content |
| `POST` | `/api/v1/drafts/{id}/publish` | Pushes approved draft to live Laravel news app via REST API |
| `POST` | `/api/v1/drafts/{id}/reject` | Marks draft as rejected and purges temporary media files |
