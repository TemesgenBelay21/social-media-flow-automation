from __future__ import annotations

from pathlib import Path

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.config import settings
from app.models.models import Media

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".mp4", ".mov", ".webm"}
ALLOWED_MIME_TYPES = {"image/png", "image/jpeg",
                      "image/gif", "video/mp4", "video/quicktime", "video/webm"}


def save_uploaded_media(db: Session, file: UploadFile, user_id: int):
    data = file.filename or "upload"
    suffix = Path(data).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    if file.content_type and file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Invalid MIME type")

    storage_root = Path(settings.storage_path)
    storage_root.mkdir(parents=True, exist_ok=True)
    target_path = storage_root / f"user_{user_id}_{file.filename}"

    content = file.file.read()
    if len(content) > 20 * 1024 * 1024:
        raise HTTPException(
            status_code=400, detail="File exceeds maximum allowed size")

    with open(target_path, "wb") as handle:
        handle.write(content)

    media = Media(
        user_id=user_id,
        file_name=file.filename or "upload",
        file_type=suffix.lstrip("."),
        mime_type=file.content_type or "application/octet-stream",
        file_size=len(content),
        storage_path=str(target_path),
        url=f"/storage/user_{user_id}_{file.filename}",
    )
    db.add(media)
    db.commit()
    db.refresh(media)
    return media
