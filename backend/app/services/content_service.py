from __future__ import annotations

from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.models import Content, PlatformPost, ScheduledJob, SocialAccount
from app.schemas.schemas import ContentCreate, PlatformPostCreate
from app.tasks.publish_tasks import publish_platform_post_task


def create_content_record(db: Session, user_id: int, payload: ContentCreate) -> Content:
    content = Content(user_id=user_id, title=payload.title,
                      base_caption=payload.base_caption, status=payload.status)
    db.add(content)
    db.commit()
    db.refresh(content)
    return content


def schedule_content_post(db: Session, user_id: int, content_id: int, payload: PlatformPostCreate):
    content = db.query(Content).filter(
        Content.id == content_id, Content.user_id == user_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    social_account = db.query(SocialAccount).filter(
        SocialAccount.id == payload.social_account_id,
        SocialAccount.user_id == user_id,
    ).first()
    if not social_account:
        raise HTTPException(status_code=404, detail="Social account not found")

    scheduled_at = payload.scheduled_at or datetime.now(timezone.utc)
    platform_post = PlatformPost(
        content_id=content.id,
        social_account_id=social_account.id,
        platform=payload.platform or social_account.platform,
        caption=payload.caption or content.base_caption,
        platform_config=str(
            payload.platform_config) if payload.platform_config else None,
        scheduled_at=scheduled_at,
        status="scheduled",
    )
    db.add(platform_post)
    db.commit()
    db.refresh(platform_post)

    scheduled_job = ScheduledJob(
        platform_post_id=platform_post.id,
        scheduled_at=scheduled_at,
        status="queued",
    )
    db.add(scheduled_job)
    db.commit()
    db.refresh(scheduled_job)

    try:
        publish_platform_post_task.apply_async(
            args=[platform_post.id], eta=scheduled_at)
    except Exception:
        scheduled_job.status = "queued"
        db.commit()

    return {"success": True, "platform_post": platform_post.id, "scheduled_at": platform_post.scheduled_at, "job_id": scheduled_job.id}
