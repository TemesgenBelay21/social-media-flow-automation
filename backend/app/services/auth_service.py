from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.models import User


def create_user(db: Session, name: str, email: str, password: str) -> User:
    user = User(name=name, email=email.lower(),
                password_hash=get_password_hash(password), is_active=True)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
