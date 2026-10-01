from __future__ import annotations

from celery import Celery

from app.config import settings

celery_app = Celery(
    "socialflow",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.tasks.publish_tasks"],
)

celery_app.conf.task_serializer = "json"
celery_app.conf.result_serializer = "json"
celery_app.conf.accept_content = ["json"]
celery_app.conf.task_track_started = True
