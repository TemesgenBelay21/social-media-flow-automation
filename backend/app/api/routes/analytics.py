from __future__ import annotations

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_active_user
from app.database import get_db
from app.models.models import Analytics, User
from app.schemas.schemas import AnalyticsOut

router = APIRouter()


@router.get("", response_model=list[AnalyticsOut])
def get_analytics(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    window_start = datetime.utcnow() - timedelta(days=30)
    return db.query(Analytics).filter(Analytics.user_id == current_user.id, Analytics.captured_at >= window_start).order_by(Analytics.captured_at.desc()).limit(20).all()
