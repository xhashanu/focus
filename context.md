# Development Context & Constraints

## 1. Strict Isolation
Do **NOT** attempt to write SQL queries that connect to a Laravel/MySQL database. This system is entirely isolated. All data pushed to the live app must happen via external HTTP requests (`requests` or `httpx`). 

## 2. Media Handling & Failures
*   Social media links frequently fail or require retries due to rate limits. Configure Celery tasks with exponential backoff and a maximum of 3 retries.
*   Always clean up `/tmp` files after a draft is either published or rejected to prevent disk bloat.
*   Wrap `yt-dlp` execution in robust try/except blocks. 

## 3. The Antigravity AI Implementation
*   Use the `google-antigravity` SDK for the AI generation step. 
*   We need the agent to utilize Gemini's multimodal capabilities. Do not use a separate Speech-to-Text API; feed the extracted audio/video directly to the agent alongside the prompt.
*   Force structured output. The agent must return a JSON object containing:
    ```json
    {
      "headline": "string",
      "summary": "string",
      "body_content": "string (HTML formatted)",
      "location": "string",
      "tags": ["string"],
      "confidence_score": 0.95,
      "ai_notes": "string (Why the AI believes this is accurate based on Lens data)"
    }
    ```

## 4. Code Quality
*   Use Python type hinting extensively (`typing` module or Pydantic models).
*   Use Pydantic models to validate the JSON returned by the AI before saving it to SQLite.
*   Keep functions small and composable. Separate the API routes, Celery tasks, AI logic, and external API integrations into distinct modules (e.g., `/api`, `/workers`, `/services`, `/models`).