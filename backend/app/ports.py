import uuid
from datetime import datetime, timezone
from typing import Protocol
from pydantic import BaseModel

class UserRecord(BaseModel):
    user_id: uuid.UUID
    shop_id: uuid.UUID
    full_name: str
    email: str
    password_hash: str
    created_at: datetime
    last_login_at: datetime | None = None

class UserRepositoryProtocol(Protocol):
    def get_by_email(self, email: str) -> UserRecord | None: ...
    def create_user_with_shop(
        self, full_name: str, shop_name: str, email: str, password_hash: str
    ) -> UserRecord: ...

class InMemoryUserRepository:
    def __init__(self) -> None:
        self._users_by_email: dict[str, UserRecord] = {}

    def get_by_email(self, email: str) -> UserRecord | None:
        return self._users_by_email.get(email.strip().lower())

    def create_user_with_shop(
        self, full_name: str, shop_name: str, email: str, password_hash: str
    ) -> UserRecord:
        normalized = email.strip().lower()
        if normalized in self._users_by_email:
            raise ValueError("Duplicate email")
        record = UserRecord(
            user_id=uuid.uuid4(),
            shop_id=uuid.uuid4(),
            full_name=full_name.strip(),
            email=normalized,
            password_hash=password_hash,
            created_at=datetime.now(timezone.utc),
            last_login_at=None,
        )
        self._users_by_email[normalized] = record
        return record