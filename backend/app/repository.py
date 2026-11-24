from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Shop, User
from app.ports import UserRecord

class PostgreUserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    @staticmethod
    def _to_record(user: User) -> UserRecord:
        return UserRecord(
        user_id=user.user_id,
        shop_id=user.shop_id,
        full_name=user.full_name,
        email = user.email,
        password_hash=user.password_hash,
        created_at=user.created_at,
        last_login_at=user.last_login_at
        )

    def get_by_email(self, email: str) -> UserRecord | None:
        normalized = email.strip().lower()
        query = select(User).where(func.lower(User.email) == normalized)
        user = self.db.scalar(query)
        return self._to_record(user) if user else None
    
    def get_by_id(self, user_id: UUID) -> UserRecord | None:
        user = self.db.get(User,user_id)
        return self._to_record(user) if user else None

    def create_user_with_shop(
        self, full_name: str, shop_name: str, email, password_hash:str) -> UserRecord:
        normalized_email = email.strip().lower()
        shop = Shop(name=shop_name.strip())
        self.db.add(shop)
        self.db.flush()

        user = User(
            full_name=full_name.strip(),
            shop_id=shop.shop_id,
            email=normalized_email,
            password_hash=password_hash
            )
        self.db.add(user)

        try:
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise ValueError("Duplicate email") from exc    

        self.db.refresh(user)
        return self._to_record(user)

    def update_last_login(self, user_id: UUID, login_time: datetime) -> None:
        user = self.db.get(User,user_id)
        if user:
            user.last_login_at = login_time
            self.db.commit()
