from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from app.auth_router import get_user_repo, router
from app.models import RevokedAccessToken
from app.ports import InMemoryUserRepository
from app.security import JWT_ALGORITHM
from app.sessions import get_session_engine


ORIGIN = "http://localhost:5173"


@pytest.fixture
def session_app(tmp_path, monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "a" * 64)
    engine = create_engine(f"sqlite:///{tmp_path / 'sessions.db'}")
    RevokedAccessToken.__table__.create(engine)
    repo = InMemoryUserRepository()

    def make_client():
        app = FastAPI()
        app.include_router(router)
        app.dependency_overrides[get_session_engine] = lambda: engine
        app.dependency_overrides[get_user_repo] = lambda: repo
        return TestClient(app, base_url=ORIGIN)

    yield make_client
    engine.dispose()


def bearer(token):
    return {"Authorization": f"Bearer {token}"}


def test_logout_revokes_only_the_selected_session(session_app):
    credentials = {"email": "user@khoai.vn", "password": "Password123"}
    origin_headers = {"Origin": ORIGIN}
    with session_app() as client, session_app() as other_client:
        registration = client.post(
            "/api/v1/auth/register",
            json={
                **credentials,
                "confirm_password": credentials["password"],
                "full_name": "Nguyen Van A",
                "shop_name": "KhoAI Store",
            },
        )
        assert registration.status_code == 201
        user = registration.json()
        login = client.post("/api/v1/auth/login", headers=origin_headers, json=credentials)
        other_login = other_client.post(
            "/api/v1/auth/login", headers=origin_headers, json=credentials
        )
        assert login.status_code == other_login.status_code == 200
        assert "secure" not in login.headers["Set-Cookie"].lower()
        token = login.cookies["khoai_session"]
        other_token = other_login.cookies["khoai_session"]
        session = client.get("/api/v1/auth/session")
        assert session.status_code == 200
        assert session.headers["Cache-Control"] == "no-store"
        for field in ("user_id", "shop_id", "email"):
            assert session.json()[field] == user[field]
        for headers in ({}, {"Origin": "http://localhost:5174"}):
            assert client.post("/api/v1/auth/logout", headers=headers).status_code == 403
        assert client.get("/api/v1/auth/session").status_code == 200

        logout = client.post("/api/v1/auth/logout", headers=origin_headers)
        assert logout.status_code == 204
        assert logout.content == b""
        assert "Max-Age=0" in logout.headers["Set-Cookie"]
        assert "khoai_session" not in client.cookies
        assert client.get("/api/v1/auth/session").status_code == 401
        assert other_client.get("/api/v1/auth/session").status_code == 200

    with session_app() as client:
        session = client.get("/api/v1/auth/session", headers=bearer(token))
        assert session.status_code == 401
        assert session.headers["WWW-Authenticate"] == "Bearer"
        assert client.post("/api/v1/auth/logout", headers=bearer(token)).status_code == 204
        assert client.get("/api/v1/auth/session", headers=bearer(other_token)).status_code == 200


@pytest.mark.parametrize("case", ["missing", "bad-signature", "expired", "missing-claim"])
def test_session_endpoints_reject_invalid_tokens(session_app, case):
    now = datetime.now(timezone.utc)
    claims = {
        "sub": str(uuid4()),
        "shop_id": str(uuid4()),
        "email": "user@khoai.vn",
        "jti": str(uuid4()),
        "iat": now - timedelta(minutes=2),
        "exp": now + timedelta(minutes=1),
    }
    if case == "expired":
        claims["exp"] = now - timedelta(minutes=1)
    if case == "missing-claim":
        del claims["jti"]
    key = "b" * 64 if case == "bad-signature" else "a" * 64
    headers = {} if case == "missing" else bearer(jwt.encode(claims, key, algorithm=JWT_ALGORITHM))

    with session_app() as client:
        for response in (
            client.get("/api/v1/auth/session", headers=headers),
            client.post("/api/v1/auth/logout", headers=headers),
        ):
            assert response.status_code == 401
            assert response.headers["WWW-Authenticate"] == "Bearer"
