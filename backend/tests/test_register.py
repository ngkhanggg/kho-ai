import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.auth_router import get_user_repo, router
from app.ports import InMemoryUserRepository


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(router)

    repo = InMemoryUserRepository()
    app.dependency_overrides[get_user_repo] = lambda: repo

    return TestClient(app)


def test_register_success(client: TestClient):
    payload = {
        "full_name": "  Nguyen Van A  ",
        "shop_name": "  KhoAI Store 1  ",
        "email": "User@KhoAI.vn ",
        "password": "Password123",
        "confirm_password": "Password123",
    }
    res = client.post("/api/v1/auth/register", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["email"] == "user@khoai.vn"
    assert data["full_name"] == "Nguyen Van A"
    assert "user_id" in data
    assert "shop_id" in data
    assert "password_hash" not in data


def test_register_duplicate_email_blocked(client: TestClient):
    payload = {
        "full_name": "Nguyen Van A",
        "shop_name": "KhoAI Store 1",
        "email": "dup@khoai.vn",
        "password": "Password123",
        "confirm_password": "Password123",
    }
    first = client.post("/api/v1/auth/register", json=payload)
    assert first.status_code == 201

    second = client.post("/api/v1/auth/register", json=payload)
    assert second.status_code == 409


def test_register_password_mismatch_fails(client: TestClient):
    res = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Nguyen Van B",
            "shop_name": "KhoAI Store 2",
            "email": "b@khoai.vn",
            "password": "Password123",
            "confirm_password": "DifferentPassword123",
        },
    )
    assert res.status_code == 422


def test_register_weak_password_and_blank_fields_fail(client: TestClient):
    res = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "   ",
            "shop_name": "   ",
            "email": "not-an-email",
            "password": "weak",
            "confirm_password": "weak",
        },
    )
    assert res.status_code == 422