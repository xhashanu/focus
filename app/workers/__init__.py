from app.workers.celery_app import celery_app
from app.workers.tasks import process_news_link

__all__ = ["celery_app", "process_news_link"]
