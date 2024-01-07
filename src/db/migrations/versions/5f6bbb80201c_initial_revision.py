"""initial revision

Revision ID: 5f6bbb80201c
Revises: 
Create Date: 2024-01-07 18:01:12.097681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5f6bbb80201c"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "account",
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("account_id"),
    )
    op.create_index(
        op.f("ix_account_account_id"), "account", ["account_id"], unique=False
    )
    op.create_index(op.f("ix_account_username"), "account", ["username"], unique=True)
    op.create_table(
        "category",
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("category_id"),
    )
    op.create_index(
        op.f("ix_category_category_id"), "category", ["category_id"], unique=False
    )
    op.create_index(op.f("ix_category_name"), "category", ["name"], unique=False)
    op.create_table(
        "audiobook",
        sa.Column("audiobook_id", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=120), nullable=False),
        sa.Column("author", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=1000), nullable=False),
        sa.Column("duration", sa.Integer(), nullable=False),
        sa.Column("cover_image", sa.String(length=2048), nullable=False),
        sa.Column("listened_times", sa.Integer(), nullable=True),
        sa.Column("rating", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["category.category_id"],
        ),
        sa.PrimaryKeyConstraint("audiobook_id"),
    )
    op.create_index(
        op.f("ix_audiobook_audiobook_id"), "audiobook", ["audiobook_id"], unique=False
    )
    op.create_index(op.f("ix_audiobook_author"), "audiobook", ["author"], unique=False)
    op.create_index(op.f("ix_audiobook_title"), "audiobook", ["title"], unique=False)
    op.create_table(
        "user_settings",
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("theme", sa.String(length=40), nullable=True),
        sa.Column("profile_picture", sa.String(length=2048), nullable=True),
        sa.Column("language", sa.String(length=40), nullable=True),
        sa.Column("wifi_only", sa.Boolean(), nullable=True),
        sa.Column("auto_play", sa.Boolean(), nullable=True),
        sa.Column("notifications_enabled", sa.Boolean(), nullable=True),
        sa.Column("adult_content_enabled", sa.Boolean(), nullable=True),
        sa.Column("explicit_phrases", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["account.account_id"],
        ),
        sa.PrimaryKeyConstraint("account_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_settings")
    op.drop_index(op.f("ix_audiobook_title"), table_name="audiobook")
    op.drop_index(op.f("ix_audiobook_author"), table_name="audiobook")
    op.drop_index(op.f("ix_audiobook_audiobook_id"), table_name="audiobook")
    op.drop_table("audiobook")
    op.drop_index(op.f("ix_category_name"), table_name="category")
    op.drop_index(op.f("ix_category_category_id"), table_name="category")
    op.drop_table("category")
    op.drop_index(op.f("ix_account_username"), table_name="account")
    op.drop_index(op.f("ix_account_account_id"), table_name="account")
    op.drop_table("account")
    # ### end Alembic commands ###
