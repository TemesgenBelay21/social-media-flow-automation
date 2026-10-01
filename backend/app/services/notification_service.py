from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.models import Notification


def create_notification(db: Session, user_id: int, notification_type: str, title: str, message: str) -> Notification:
    notification = Notification(user_id=user_id, type=notification_type,
                                title=title, message=message, created_at=datetime.utcnow())
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification
