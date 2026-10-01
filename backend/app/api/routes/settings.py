from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_active_user
from app.database import get_db
from app.models.models import User
from app.schemas.schemas import SettingsOut, SettingsUpdate

router = APIRouter()


@router.get("", response_model=SettingsOut)
def get_settings(current_user: User = Depends(get_current_active_user)):
    return SettingsOut(timezone=current_user.timezone, notification_preferences={"email": True, "push": True, "sms": False})


@router.put("", response_model=SettingsOut)
def update_settings(payload: SettingsUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if payload.timezone:
        current_user.timezone = payload.timezone
    db.commit()
    return SettingsOut(timezone=current_user.timezone, notification_preferences=payload.notification_preferences or {"email": True, "push": True, "sms": False})
