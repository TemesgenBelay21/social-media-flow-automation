from app.models.models import Content, RefreshToken, ScheduledJob, User
from app.main import app
from app.database import SessionLocal
import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite:///./test_socialflow.db"
Path("test_socialflow.db").unlink(missing_ok=True)


@pytest.fixture(autouse=True)
def reset_db():
    db = SessionLocal()
    for model in (ScheduledJob, Content, RefreshToken, User):
        db.query(model).delete()
    db.commit()
    db.close()
    yield
    db = SessionLocal()
    for model in (ScheduledJob, Content, RefreshToken, User):
        db.query(model).delete()
    db.commit()
    db.close()


client = TestClient(app)


def create_user_and_login(email: str = "alice@example.com", password: str = "secret1234"):
    register = client.post(
        "/api/auth/register",
        json={"name": "Alice Example",
              "email": email, "password": password},
    )
    assert register.status_code == 200, register.text

    login = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    assert login.status_code == 200, login.text
    token = login.json()["access_token"]
    assert token
    return token


def test_register_and_login_flow():
    token = create_user_and_login()

    me = client.get(
        "/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200, me.text
    assert me.json()["email"] == "alice@example.com"


def test_create_and_list_content():
    token = create_user_and_login()

    create = client.post(
        "/api/content",
        json={"title": "Launch post",
              "base_caption": "Hello world", "status": "draft"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert create.status_code == 200, create.text
    payload = create.json()
    assert payload["title"] == "Launch post"

    listing = client.get(
        "/api/content", headers={"Authorization": f"Bearer {token}"})
    assert listing.status_code == 200, listing.text
    assert len(listing.json()) >= 1
