from __future__ import annotations

import random
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.integrations.registry import get_platform_adapter
from app.models.models import PlatformPost, SocialAccount


def publish_platform_post(db: Session, platform_post_id: int) -> dict[str, Any]:
    platform_post = db.query(PlatformPost).filter(
        PlatformPost.id == platform_post_id).first()
    if not platform_post:
        return {"success": False, "message": "Platform post not found"}

    social_account = db.query(SocialAccount).filter(
        SocialAccount.id == platform_post.social_account_id).first()
    adapter = get_platform_adapter(platform_post.platform, social_account)
    result = adapter.publish(platform_post)
    platform_post.status = result["status"]
    platform_post.external_post_id = result.get(
        "external_post_id") or f"mock-{platform_post.platform}-{random.randint(1000, 9999)}"
    platform_post.published_at = datetime.utcnow(
    ) if result["status"] == "published" else None
    platform_post.error_message = result.get("error_message")
    db.commit()
    return result
