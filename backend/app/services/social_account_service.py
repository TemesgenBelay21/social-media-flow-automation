from __future__ import annotations

import json

from sqlalchemy.orm import Session

from app.models.models import SocialAccount
from app.schemas.schemas import SocialAccountCreate


def create_social_account(db: Session, user_id: int, payload: SocialAccountCreate) -> SocialAccount:
    account = SocialAccount(
        user_id=user_id,
        platform=payload.platform,
        account_name=payload.account_name or payload.platform.title(),
        username=payload.username,
        connection_status="connected",
        metadata_=json.dumps(payload.metadata or {"mode": "mock"}),
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def disconnect_social_account(db: Session, account: SocialAccount) -> None:
    account.connection_status = "disconnected"
    db.commit()
