from __future__ import annotations

from app.config import settings
from app.integrations.mock import MockPlatformAdapter


def get_platform_adapter(platform: str, social_account=None):
    if settings.social_platform_mode == "mock":
        return MockPlatformAdapter(platform_name=platform)
    return MockPlatformAdapter(platform_name=platform)
