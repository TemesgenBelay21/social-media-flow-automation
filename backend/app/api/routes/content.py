from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.security import get_current_active_user
from app.database import get_db
from app.models.models import Content, PlatformPost, SocialAccount
from app.schemas.schemas import ContentCreate, ContentOut, PlatformPostCreate, PlatformPostOut
from app.services.content_service import create_content_record, schedule_content_post
from app.services.publishing_service import publish_platform_post

router = APIRouter()


@router.get("", response_model=list[ContentOut])
def list_content(
    db: Session = Depends(get_db),
    current_user: SocialAccount = Depends(get_current_active_user),
    limit: int = Query(default=20, ge=1, le=100),
):
    return db.query(Content).filter(Content.user_id == current_user.id).order_by(Content.created_at.desc()).limit(limit).all()


@router.post("", response_model=ContentOut)
def create_content(
    payload: ContentCreate,
    db: Session = Depends(get_db),
    current_user: SocialAccount = Depends(get_current_active_user),
):
    return create_content_record(db, current_user.id, payload)


@router.get("/{content_id}", response_model=ContentOut)
def get_content(content_id: int, db: Session = Depends(get_db), current_user: SocialAccount = Depends(get_current_active_user)):
    content = db.query(Content).filter(
        Content.id == content_id, Content.user_id == current_user.id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content


@router.put("/{content_id}", response_model=ContentOut)
def update_content(content_id: int, payload: ContentCreate, db: Session = Depends(get_db), current_user: SocialAccount = Depends(get_current_active_user)):
    content = db.query(Content).filter(
        Content.id == content_id, Content.user_id == current_user.id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    content.title = payload.title
    content.base_caption = payload.base_caption
    content.status = payload.status
    content.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(content)
    return content


@router.post("/{content_id}/schedule")
def schedule_content(content_id: int, payload: PlatformPostCreate, db: Session = Depends(get_db), current_user: SocialAccount = Depends(get_current_active_user)):
    return schedule_content_post(db, current_user.id, content_id, payload)


@router.post("/{content_id}/publish")
def publish_content(content_id: int, db: Session = Depends(get_db), current_user: SocialAccount = Depends(get_current_active_user)):
    content = db.query(Content).filter(
        Content.id == content_id, Content.user_id == current_user.id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    linked_posts = db.query(PlatformPost).filter(
        PlatformPost.content_id == content_id).all()
    if not linked_posts:
        raise HTTPException(
            status_code=400, detail="No platform posts available for publishing")

    results = []
    for post in linked_posts:
        post.status = "publishing"
        db.commit()
        results.append({
            "platform_post_id": post.id,
            "platform": post.platform,
            "result": publish_platform_post(db, post.id),
        })

    return {"success": True, "message": "Publishing started", "count": len(results), "results": results}


@router.delete("/{content_id}")
def delete_content(content_id: int, db: Session = Depends(get_db), current_user: SocialAccount = Depends(get_current_active_user)):
    content = db.query(Content).filter(
        Content.id == content_id, Content.user_id == current_user.id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    db.delete(content)
    db.commit()
    return {"success": True, "message": "Content removed"}
