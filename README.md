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

## Requirements

- Docker and Docker Compose
- Python 3.12+
- Node.js 20+
- MySQL 8+
- Redis

## Installation

From the project root:

1. Copy the example environment file:
   `cp .env.example .env`
2. Update credentials and secret values in `.env`.
3. Start the stack:
   `docker compose up --build`

## Environment variables

The application reads configuration from `.env` at the project root. See `.env.example` for the required variables. Do not commit real secrets to the repository.

## Database setup

Run migrations from the backend directory:

```bash
cd backend
alembic upgrade head
```

To create a new migration:

```bash
cd backend
alembic revision --autogenerate -m "describe change"
```

## Running the application

Backend development server:

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Frontend development server:

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

Celery worker:

```bash
cd backend
celery -A app.tasks.celery_app worker --loglevel=info
```

## API documentation

The backend exposes Swagger UI and Redoc automatically:

- http://localhost:8000/api/docs
- http://localhost:8000/api/redoc

## Social API configuration

Each platform requires its own developer application and credentials. The app is designed around the official platform APIs, with mock mode used for local development when credentials or approval are not available.

## Mock mode

Set `SOCIAL_PLATFORM_MODE=mock` in the environment file to simulate account connections, publishing, and analytics without hitting live APIs. The mock implementations are clearly marked as development data and are not intended for production use.

## Testing

Backend tests:

```bash
cd backend
pytest
```

Frontend build verification:

```bash
cd frontend
npm install
npm run build
```

## Security

- Never commit `.env` files or secrets.
- Store passwords only as hashes.
- Use JWT access and refresh tokens.
- Validate input and file uploads.
- Keep platform credentials encrypted at rest when stored.

## Deployment

This project is designed for containerized deployment in Docker environments or a managed hosting stack with MySQL, Redis, and a Python application server. Real platform integrations require their own approved developer apps and the appropriate OAuth or bot configuration.

## Notes on unsupported platform capabilities

Some official APIs do not support all social-media actions through a single mechanism. The app is structured to surface those limitations and expose mock or status-based behavior clearly rather than bypassing platform restrictions.
