from __future__ import annotations

from datetime import datetime
from typing import Any

from app.integrations.base import SocialPlatformAdapter


class MockPlatformAdapter(SocialPlatformAdapter):
    platform_name = "mock"

    def __init__(self, platform_name: str = "mock"):
        self.platform_name = platform_name

    def connect(self, *args, **kwargs) -> dict[str, Any]:
        return {"success": True, "message": f"{self.platform_name} mock connection configured", "status": "connected"}

    def disconnect(self, *args, **kwargs) -> dict[str, Any]:
        return {"success": True, "message": f"{self.platform_name} disconnected"}

    def validate_content(self, content: Any, **kwargs) -> dict[str, Any]:
        return {"valid": True, "platform": self.platform_name, "warnings": []}

    def publish(self, platform_post: Any, **kwargs) -> dict[str, Any]:
        platform_post_status = "published"
        if self.platform_name == "tiktok":
            platform_post_status = "failed"
            return {
                "success": False,
                "status": "failed",
                "message": "Publishing access pending approval",
                "error_message": "TikTok publishing requires app review and approval.",
                "external_post_id": None,
            }

        if self.platform_name == "telegram":
            return {"success": True, "status": "published", "message": "Telegram message sent", "external_post_id": f"telegram-{datetime.utcnow().timestamp()}"}

        return {"success": True, "status": platform_post_status, "message": f"{self.platform_name} content published in mock mode", "external_post_id": f"mock-{self.platform_name}-{datetime.utcnow().timestamp()}"}

    def get_account_info(self, *args, **kwargs) -> dict[str, Any]:
        return {
            "platform": self.platform_name,
            "account_name": f"Demo {self.platform_name.title()} account",
            "status": "connected",
            "mock": True,
        }

    def get_analytics(self, *args, **kwargs) -> dict[str, Any]:
        return {
            "platform": self.platform_name,
            "impressions": 100,
            "reach": 80,
            "engagement": 4.2,
            "views": 90,
            "likes": 15,
            "mock": True,
        }
