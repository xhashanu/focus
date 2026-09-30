# System Architecture

## Tech Stack
*   **Language:** Python 3.12+
*   **Web Framework:** FastAPI (for ingestion, review API, and task monitoring).
*   **Frontend (Human Approval Panel):** Streamlit (internal dashboard for live processing tracking and human draft review/approval).
*   **Task Queue:** Celery with a Redis broker (for long-running media tasks).
*   **Database:** SQLite (local, temporary storage for drafts and AI metadata).
*   **Media Tools:** 
    *   `yt-dlp` (for downloading videos).
    *   `ffmpeg-python` (for audio extraction and keyframe slicing).
*   **AI Engine:** Google Antigravity Python SDK (`google-antigravity`) / Gemini API (for multimodal processing and structured JSON generation).
*   **Search API:** SerpApi (Google Lens endpoint for keyframe context).

## Component Flow

### 1. API Layer (FastAPI)
*   `POST /api/v1/curate` -> Accepts `{ "url": "https://instagram.com/..." }`. Returns `202 Accepted` and a `task_id`. Dispatches a Celery task.
*   `GET /api/v1/tasks/{task_id}` -> Returns live pipeline status and progress for real-time tracking.
*   `GET /api/v1/drafts` -> Returns a list of pending articles from the SQLite database.
*   `GET /api/v1/drafts/{id}` -> Returns detailed draft information.
*   `POST /api/v1/drafts/{id}/publish` -> Triggers the webhook to push the approved draft to the live Laravel app.

### 2. Frontend Layer (Streamlit)
*   **Live Ingestion & Processing:** Submit video links and monitor stage-by-stage pipeline progress live (Download -> Extract -> Lens Context -> AI Generation -> Draft Saved).
*   **Approval & Review Panel:** Browse drafts, inspect keyframes and audio, review AI confidence score and notes, edit headline/body, and push to Laravel with one click.

### 3. Worker Layer (Celery)
The background worker executes the `process_news_link` pipeline:
1.  **Download:** Execute `yt-dlp` to fetch the `.mp4`. Save to local `/tmp` storage.
2.  **Process:** Use `ffmpeg` to extract an `.mp3` audio file and 3 keyframe `.jpg` images.
3.  **Search:** Send the best keyframe to SerpApi (Google Lens) to retrieve contextual clues (e.g., "Protest at Howrah Bridge").
4.  **AI Generation:** Initialize the Antigravity Agent. Pass the `.mp3`, the `.mp4`, the Lens context, and the system prompt. Instruct the agent to output strict JSON matching the Laravel API schema.
5.  **Save:** Store the generated JSON, original media paths, and AI confidence score in the SQLite `drafts` table.

### 4. Integration Layer
*   A utility class that takes an approved draft from SQLite, formats it to match the CodeCanyon Laravel API requirements (e.g., `title`, `description`, `category_id`), and executes an authenticated `requests.post()` to the live server.