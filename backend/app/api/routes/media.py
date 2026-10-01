from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.security import get_current_active_user
from app.database import get_db
from app.models.models import Media, User
from app.schemas.schemas import MediaCreate, MediaOut
from app.services.media_service import save_uploaded_media

router = APIRouter()


@router.get("", response_model=list[MediaOut])
def list_media(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return db.query(Media).filter(Media.user_id == current_user.id).order_by(Media.created_at.desc()).all()


@router.post("", response_model=MediaOut)
async def upload_media(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return save_uploaded_media(db, file, current_user.id)


@router.delete("/{media_id}")
def delete_media(media_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    media = db.query(Media).filter(Media.id == media_id,
                                   Media.user_id == current_user.id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    db.delete(media)
    db.commit()
    return {"success": True, "message": "Media deleted"}
