from datetime import datetime
from uuid import UUID,uuid4

from sqlalchemy import DateTime, ForeignKey, Index, Text, UniqueConstraint, func, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Shop(Base):
    __tablename__ = "shops"

    shop_id: Mapped[UUID] = mapped_column(
        primary_key=True, default=uuid4, server_default=text("gen_random_uuid()")
    )
    name: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[UUID] = mapped_column(
        primary_key=True,default=uuid4, server_default=text("gen_random_uuid()")
    )
    shop_id: Mapped[UUID] = mapped_column(ForeignKey("shops.shop_id"))
    full_name: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(Text)
    password_hash: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint("shop_id", name="users_one_account_per_shop"),
        Index("users_email_lower_uidx", func.lower(email), unique=True),
    )


class RevokedAccessToken(Base):
    __tablename__ = "revoked_access_tokens"

    jti: Mapped[UUID] = mapped_column(primary_key=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
