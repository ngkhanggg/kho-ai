"""Create shops and Owner accounts."""

import sqlalchemy as sa
from alembic import op

revision = "0001_shops_and_users"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "shops",
        sa.Column("shop_id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table(
        "users",
        sa.Column("user_id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("shop_id", sa.Uuid(), sa.ForeignKey("shops.shop_id"), nullable=False),
        sa.Column("full_name", sa.Text(), nullable=False),
        sa.Column("email", sa.Text(), nullable=False),
        sa.Column("password_hash", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("shop_id", name="users_one_account_per_shop"),
    )
    op.create_index("users_email_lower_uidx", "users", [sa.text("lower(email)")], unique=True)


def downgrade() -> None:
    op.drop_table("users")
    op.drop_table("shops")
