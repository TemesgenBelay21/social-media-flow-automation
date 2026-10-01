from __future__ import annotations

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.routes import __name__ as _unused
from app.core.security import create_access_token, get_current_active_user, get_password_hash, verify_password
from app.database import get_db
from app.models.models import RefreshToken, User
from app.schemas.schemas import Token, UserCreate, UserLogin, UserOut

router = APIRouter()


@router.post("/register", response_model=UserOut)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(
        User.email == payload.email.lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        name=payload.name,
        email=payload.email.lower(),
        password_hash=get_password_hash(payload.password),
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login_user(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user.id)
    refresh_expiration = datetime.now(timezone.utc) + timedelta(days=7)
    db.add(RefreshToken(user_id=user.id, token_hash=token,
           expires_at=refresh_expiration))
    user.last_login_at = datetime.utcnow()
    db.commit()
    return {"access_token": token, "token_type": "bearer"}


@router.post("/logout")
def logout_user(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    db.query(RefreshToken).filter(
        RefreshToken.user_id == current_user.id).delete()
    db.commit()
    return {"success": True, "message": "Logged out"}


@router.get("/me", response_model=UserOut)
def get_current_user_profile(current_user: User = Depends(get_current_active_user)):
    return current_user
