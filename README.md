# SocialFlow Automation

SocialFlow Automation is a full-stack social media management and automation platform for Instagram, Facebook, TikTok, and Telegram. It provides a dashboard for connecting accounts, creating content, scheduling posts, publishing through official APIs, monitoring status, and reviewing analytics.

## Features

- User registration and secure authentication
- Protected dashboard and route guards
- Social account connection management for all supported platforms
- Content composer with draft and scheduling workflows
- Media library with validation and reuse
- Publishing engine with backend workers and retries
- Calendar views and notification center
- Mock mode for local development without live platform credentials
- API documentation via FastAPI
- MySQL-driven relational data model and Alembic migrations
- Docker Compose setup for local development

## Technology stack

- React
- Vite
- TypeScript
- Python
- FastAPI
- SQLAlchemy
- MySQL
- Redis
- Celery
- Docker

## Supported platforms

- Instagram
- Facebook
- TikTok
- Telegram

## Architecture

The system includes a React frontend, a FastAPI backend, a MySQL database, and a Redis/Celery worker system for scheduled publishing. Platform-specific logic is isolated behind adapter/service patterns so each social platform can be extended independently.
