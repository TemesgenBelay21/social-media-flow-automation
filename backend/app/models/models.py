from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    timezone = Column(String(80), default="UTC")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)

    refresh_tokens = relationship(
        "RefreshToken", back_populates="user", cascade="all, delete-orphan")
    social_accounts = relationship(
        "SocialAccount", back_populates="user", cascade="all, delete-orphan")
    content = relationship("Content", back_populates="user",
                           cascade="all, delete-orphan")
    notifications = relationship(
        "Notification", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship(
        "AuditLog", back_populates="user", cascade="all, delete-orphan")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    token_hash = Column(String(255), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    revoked_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="refresh_tokens")


class SocialAccount(Base):
    __tablename__ = "social_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    platform = Column(String(50), nullable=False, index=True)
    platform_user_id = Column(String(120), nullable=True)
    account_name = Column(String(150), nullable=True)
    username = Column(String(150), nullable=True)
    access_token_encrypted = Column(Text, nullable=True)
    refresh_token_encrypted = Column(Text, nullable=True)
    token_expires_at = Column(DateTime, nullable=True)
    scopes = Column(Text, nullable=True)
    connection_status = Column(String(50), default="connected")
    metadata_ = Column("metadata", Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    user = relationship("User", back_populates="social_accounts")
    platform_posts = relationship(
        "PlatformPost", back_populates="social_account", cascade="all, delete-orphan")


class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    base_caption = Column(Text, nullable=True)
    status = Column(String(50), default="draft", index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    user = relationship("User", back_populates="content")
    media_links = relationship(
        "ContentMedia", back_populates="content", cascade="all, delete-orphan")
    platform_posts = relationship(
        "PlatformPost", back_populates="content", cascade="all, delete-orphan")


class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)
    mime_type = Column(String(120), nullable=False)
    file_size = Column(Integer, nullable=False)
    storage_path = Column(String(500), nullable=False)
    url = Column(String(500), nullable=True)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    duration = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    content_links = relationship(
        "ContentMedia", back_populates="media", cascade="all, delete-orphan")


class ContentMedia(Base):
    __tablename__ = "content_media"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey(
        "content.id", ondelete="CASCADE"), nullable=False)
    media_id = Column(Integer, ForeignKey(
        "media.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    content = relationship("Content", back_populates="media_links")
    media = relationship("Media", back_populates="content_links")

    __table_args__ = (UniqueConstraint(
        "content_id", "media_id", name="uq_content_media"),)


class PlatformPost(Base):
    __tablename__ = "platform_posts"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey(
        "content.id", ondelete="CASCADE"), nullable=False)
    social_account_id = Column(Integer, ForeignKey(
        "social_accounts.id", ondelete="CASCADE"), nullable=False)
    platform = Column(String(50), nullable=False, index=True)
    caption = Column(Text, nullable=True)
    platform_config = Column(Text, nullable=True)
    scheduled_at = Column(DateTime, nullable=True, index=True)
    published_at = Column(DateTime, nullable=True)
    external_post_id = Column(String(255), nullable=True, index=True)
    status = Column(String(50), default="draft", index=True)
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    content = relationship("Content", back_populates="platform_posts")
    social_account = relationship(
        "SocialAccount", back_populates="platform_posts")
    scheduled_jobs = relationship(
        "ScheduledJob", back_populates="platform_post", cascade="all, delete-orphan")


class ScheduledJob(Base):
    __tablename__ = "scheduled_jobs"

    id = Column(Integer, primary_key=True, index=True)
    platform_post_id = Column(Integer, ForeignKey(
        "platform_posts.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(String(255), nullable=True)
    scheduled_at = Column(DateTime, nullable=True, index=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String(50), default="queued", index=True)
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    platform_post = relationship(
        "PlatformPost", back_populates="scheduled_jobs")


class Analytics(Base):
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    platform = Column(String(50), nullable=False, index=True)
    external_post_id = Column(String(255), nullable=True, index=True)
    impressions = Column(Integer, nullable=True)
    reach = Column(Integer, nullable=True)
    views = Column(Integer, nullable=True)
    likes = Column(Integer, nullable=True)
    comments = Column(Integer, nullable=True)
    shares = Column(Integer, nullable=True)
    saves = Column(Integer, nullable=True)
    clicks = Column(Integer, nullable=True)
    engagement = Column(Float, nullable=True)
    follower_count = Column(Integer, nullable=True)
    captured_at = Column(DateTime, default=datetime.utcnow, index=True)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    type = Column(String(50), default="info")
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    read_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="SET NULL"), nullable=True)
    action = Column(String(120), nullable=False, index=True)
    entity_type = Column(String(120), nullable=True)
    entity_id = Column(Integer, nullable=True)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="audit_logs")
