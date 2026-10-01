from __future__ import annotations

from app.database import SessionLocal
from app.services.publishing_service import publish_platform_post
from app.tasks.celery_app import celery_app


@celery_app.task(name="publish_platform_post")
def publish_platform_post_task(platform_post_id: int):
    db = SessionLocal()
    try:
        return publish_platform_post(db, platform_post_id)
    finally:
        db.close()
