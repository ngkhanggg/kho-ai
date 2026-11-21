import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.auth_router import get_user_repo, router
from app.ports import InMemoryUserRepository
from app.security import decode_access_token


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "a" * 64)
    app = FastAPI()
    app.include_router(router)

    repo = InMemoryUserRepository()
    app.dependency_overrides[get_user_repo] = lambda: repo

    return TestClient(app)


@pytest.fixture
def registered_user(client: TestClient):
    register_payload = {
        "full_name": "Nguyen Van A",
        "shop_name": "KhoAI Store 1",
        "email": "user@khoai.vn",
        "password": "Password123",
        "confirm_password": "Password123",
    }

    register_response = client.post("/api/v1/auth/register", json=register_payload)
    assert register_response.status_code == 201
    return register_response.json()


def test_login_successful(client: TestClient, registered_user):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": f" {registered_user['email'].upper()} ",
            "password": "Password123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 1800

    claims = decode_access_token(data["access_token"])
    assert claims["sub"] == registered_user["user_id"]
    assert claims["shop_id"] == registered_user["shop_id"]
    assert claims["email"] == registered_user["email"]
    assert claims["exp"] - claims["iat"] == data["expires_in"]


@pytest.mark.parametrize(
    ("email", "password"),
    [
        pytest.param("user@khoai.vn", "WrongPass123", id="wrong-password"),
        pytest.param("unknown@example.com", "Password123", id="unknown-email"),
    ],
)
def test_login_invalid_credentials(client: TestClient, registered_user, email, password):
    response = client.post(
        "/api/v1/auth/login", json={"email": email, "password": password}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid email or password."}


@pytest.mark.parametrize(
    ("payload", "field"),
    [
        pytest.param(
            {"email": "bad-email", "password": "Password123"},
            "email",
            id="invalid-email",
        ),
        pytest.param({"password": "Password123"}, "email", id="missing-email"),
        pytest.param({"email": "user@khoai.vn"}, "password", id="missing-password"),
    ],
)
def test_login_invalid_request(client: TestClient, payload, field):
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", field]
