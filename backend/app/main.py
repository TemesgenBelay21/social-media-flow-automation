from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.api.routes import analytics as analytics_routes
from app.api.routes import auth as auth_routes
from app.api.routes import calendar as calendar_routes
from app.api.routes import content as content_routes
from app.api.routes import media as media_routes
from app.api.routes import notifications as notifications_routes
from app.api.routes import settings as settings_routes
from app.api.routes import social_accounts as social_accounts_routes
from app.config import settings
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SocialFlow Automation",
    description="Centralized social media management and automation platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, prefix="/api/auth", tags=["auth"])
app.include_router(content_routes.router,
                   prefix="/api/content", tags=["content"])
app.include_router(media_routes.router, prefix="/api/media", tags=["media"])
app.include_router(social_accounts_routes.router,
                   prefix="/api/social-accounts", tags=["social_accounts"])
app.include_router(analytics_routes.router,
                   prefix="/api/analytics", tags=["analytics"])
app.include_router(notifications_routes.router,
                   prefix="/api/notifications", tags=["notifications"])
app.include_router(settings_routes.router,
                   prefix="/api/settings", tags=["settings"])
app.include_router(calendar_routes.router,
                   prefix="/api/calendar", tags=["calendar"])


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok", "service": "socialflow-backend"}
