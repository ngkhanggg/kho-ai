from datetime import UTC, datetime
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from app.db import Base
from app.models import Shop, User
from app.repository import PostgreUserRepository


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")

    # Enable foreign key enforcement in SQLite
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, _connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def repo(db_session: Session) -> PostgreUserRepository:
    return PostgreUserRepository(db_session)


def test_create_user_with_shop_persists_both_records(
    repo: PostgreUserRepository, db_session: Session
):
    created = repo.create_user_with_shop(
        full_name="  Nguyen Van A  ",
        shop_name="  KhoAI Store  ",
        email="  Owner@KhoAI.vn  ",
        password_hash="hashed_secret",
    )

    assert created.full_name == "Nguyen Van A"
    assert created.email == "owner@khoai.vn"
    assert created.password_hash == "hashed_secret"
    assert created.last_login_at is None

    shop = db_session.get(Shop, created.shop_id)
    assert shop is not None
    assert shop.name == "KhoAI Store"

    user = db_session.get(User, created.user_id)
    assert user is not None
    assert user.shop_id == shop.shop_id


def test_get_by_email_is_case_insensitive(repo: PostgreUserRepository):
    created = repo.create_user_with_shop(
        full_name="Nguyen Van A",
        shop_name="KhoAI Store",
        email="owner@khoai.vn",
        password_hash="hashed_secret",
    )

    found = repo.get_by_email("  OWNER@KHOAI.VN ")
    assert found is not None
    assert found.user_id == created.user_id
    assert repo.get_by_email("missing@khoai.vn") is None


def test_get_by_id_returns_record_or_none(repo: PostgreUserRepository):
    created = repo.create_user_with_shop(
        full_name="Nguyen Van A",
        shop_name="KhoAI Store",
        email="owner@khoai.vn",
        password_hash="hashed_secret",
    )

    found = repo.get_by_id(created.user_id)
    assert found is not None
    assert found.email == "owner@khoai.vn"
    assert repo.get_by_id(uuid4()) is None


def test_duplicate_email_raises_value_error(repo: PostgreUserRepository):
    repo.create_user_with_shop(
        full_name="Nguyen Van A",
        shop_name="KhoAI Store",
        email="owner@khoai.vn",
        password_hash="hashed_secret",
    )

    with pytest.raises(ValueError, match="Duplicate email"):
        repo.create_user_with_shop(
            full_name="Another Owner",
            shop_name="Second Shop",
            email="OWNER@khoai.vn",
            password_hash="other_hash",
        )


def test_update_last_login_updates_timestamp(repo: PostgreUserRepository):
    created = repo.create_user_with_shop(
        full_name="Nguyen Van A",
        shop_name="KhoAI Store",
        email="owner@khoai.vn",
        password_hash="hashed_secret",
    )
    login_time = datetime(2026, 11, 24, 15, 0, tzinfo=UTC)

    repo.update_last_login(created.user_id, login_time)

    updated = repo.get_by_id(created.user_id)
    assert updated is not None
    assert updated.last_login_at is not None
    assert updated.last_login_at.replace(tzinfo=UTC) == login_time
@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")

    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, _connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
        dbapi_connection.create_function("gen_random_uuid", 0, lambda: str(uuid4()))

    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session