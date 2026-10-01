from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_active_user
from app.database import get_db
from app.models.models import SocialAccount, User
from app.schemas.schemas import SocialAccountCreate, SocialAccountOut
from app.services.social_account_service import create_social_account, disconnect_social_account

router = APIRouter()


@router.get("", response_model=list[SocialAccountOut])
def list_social_accounts(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return db.query(SocialAccount).filter(SocialAccount.user_id == current_user.id).all()


@router.post("", response_model=SocialAccountOut)
def create_social_account_route(payload: SocialAccountCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return create_social_account(db, current_user.id, payload)


@router.delete("/{account_id}")
def delete_social_account(account_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    account = db.query(SocialAccount).filter(
        SocialAccount.id == account_id, SocialAccount.user_id == current_user.id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Social account not found")
    disconnect_social_account(db, account)
    return {"success": True, "message": "Social account disconnected"}
