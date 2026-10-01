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
