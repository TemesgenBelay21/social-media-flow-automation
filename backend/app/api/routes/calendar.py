from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_active_user
from app.database import get_db
from app.models.models import Content, PlatformPost, User

router = APIRouter()


@router.get("")
def get_calendar(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    items = db.query(Content).filter(Content.user_id == current_user.id).all()
    result = []
    for item in items:
        for post in item.platform_posts:
            result.append({
                "id": post.id,
                "content_id": item.id,
                "platform": post.platform,
                "status": post.status,
                "scheduled_at": post.scheduled_at,
                "title": item.title,
            })
    return {"items": result, "generated_at": datetime.utcnow().isoformat()}
