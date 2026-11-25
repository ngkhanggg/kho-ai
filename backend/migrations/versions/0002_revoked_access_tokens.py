"""Persist JWT revocations until the token expires."""

import sqlalchemy as sa
from alembic import op

revision = "0002_revoked_access_tokens"
down_revision = "0001_shops_and_users"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "revoked_access_tokens",
        sa.Column("jti", sa.Uuid(), primary_key=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_revoked_access_tokens_expires_at", "revoked_access_tokens", ["expires_at"]
    )


def downgrade() -> None:
    op.drop_table("revoked_access_tokens")
