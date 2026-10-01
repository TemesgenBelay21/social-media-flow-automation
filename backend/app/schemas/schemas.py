from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(..., min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True
    timezone: str = "UTC"
    created_at: datetime

    model_config = {"from_attributes": True}


class SocialAccountCreate(BaseModel):
    platform: str
    account_name: Optional[str] = None
    username: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class SocialAccountOut(BaseModel):
    id: int
    user_id: int
    platform: str
    platform_user_id: Optional[str]
    account_name: Optional[str]
    username: Optional[str]
    connection_status: str
    metadata: Optional[Dict[str, Any]] = Field(default=None, alias="metadata_")
    created_at: datetime

    @field_validator("metadata", mode="before")
    @classmethod
    def parse_metadata(cls, value: Any) -> Any:
        if isinstance(value, str):
            try:
                return json.loads(value)
            except (TypeError, ValueError):
                return {"raw": value}
        return value

    model_config = {"from_attributes": True, "populate_by_name": True}


class ContentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    base_caption: Optional[str] = None
    status: str = "draft"


class ContentOut(BaseModel):
    id: int
    user_id: int
    title: str
    base_caption: Optional[str]
    status: str
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}


class MediaCreate(BaseModel):
    file_name: str
    file_type: str
    mime_type: str
    file_size: int
    storage_path: str
    url: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[float] = None


class MediaOut(BaseModel):
    id: int
    user_id: int
    file_name: str
    file_type: str
    mime_type: str
    file_size: int
    storage_path: str
    url: Optional[str]
    width: Optional[int]
    height: Optional[int]
    duration: Optional[float]
    created_at: datetime

    model_config = {"from_attributes": True}


class PlatformPostCreate(BaseModel):
    content_id: Optional[int] = None
    social_account_id: int
    platform: str
    caption: Optional[str] = None
    platform_config: Optional[Dict[str, Any]] = None
    scheduled_at: Optional[datetime] = None
    status: str = "draft"


class PlatformPostOut(BaseModel):
    id: int
    content_id: int
    social_account_id: int
    platform: str
    caption: Optional[str]
    platform_config: Optional[Dict[str, Any]]
    scheduled_at: Optional[datetime]
    published_at: Optional[datetime]
    external_post_id: Optional[str]
    status: str
    error_message: Optional[str]
    retry_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class NotificationOut(BaseModel):
    id: int
    user_id: int
    type: str
    title: str
    message: str
    read_at: Optional[datetime]
    created_at: datetime

    model_config = {"from_attributes": True}


class AnalyticsOut(BaseModel):
    id: int
    user_id: int
    platform: str
    external_post_id: Optional[str]
    impressions: Optional[int]
    reach: Optional[int]
    views: Optional[int]
    likes: Optional[int]
    comments: Optional[int]
    shares: Optional[int]
    saves: Optional[int]
    clicks: Optional[int]
    engagement: Optional[float]
    follower_count: Optional[int]
    captured_at: datetime

    model_config = {"from_attributes": True}


class SettingsUpdate(BaseModel):
    timezone: Optional[str] = None
    notification_preferences: Optional[Dict[str, bool]] = None


class SettingsOut(BaseModel):
    timezone: str = "UTC"
    notification_preferences: Dict[str, bool] = {
        "email": True, "push": True, "sms": False}
