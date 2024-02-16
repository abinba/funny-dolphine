"""shelf table

Revision ID: c7732a70780a
Revises: 1dc3739ccc1d
Create Date: 2024-01-28 21:06:08.824311

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "c7732a70780a"
down_revision: Union[str, None] = "1dc3739ccc1d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_shelf",
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("audiobook_id", sa.Integer(), nullable=False),
        sa.Column("archived", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["account.account_id"],
        ),
        sa.ForeignKeyConstraint(
            ["audiobook_id"],
            ["audiobook.audiobook_id"],
        ),
        sa.PrimaryKeyConstraint("account_id", "audiobook_id"),
    )
    op.drop_index("ix_user_audiobook_user_audiobook_id", table_name="user_audiobook")
    op.drop_table("user_audiobook")
    op.drop_index("ix_user_chapter_user_chapter_id", table_name="user_chapter")
    op.drop_table("user_chapter")
    op.add_column(
        "audiobook", sa.Column("first_chapter_id", sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        None, "audiobook", "chapter", ["first_chapter_id"], ["chapter_id"]
    )
    op.drop_column("listening", "start_time")
    op.drop_column("listening", "last_access_time")
    op.drop_column("listening", "is_favorite")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "listening",
        sa.Column("is_favorite", sa.BOOLEAN(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "listening",
        sa.Column(
            "last_access_time",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.add_column(
        "listening",
        sa.Column(
            "start_time", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
    )
    op.drop_constraint(None, "audiobook", type_="foreignkey")
    op.drop_column("audiobook", "first_chapter_id")
    op.create_table(
        "user_chapter",
        sa.Column("user_chapter_id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("account_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("chapter_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("listened_times", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["account_id"], ["account.account_id"], name="user_chapter_account_id_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["chapter_id"], ["chapter.chapter_id"], name="user_chapter_chapter_id_fkey"
        ),
        sa.PrimaryKeyConstraint("user_chapter_id", name="user_chapter_pkey"),
    )
    op.create_index(
        "ix_user_chapter_user_chapter_id",
        "user_chapter",
        ["user_chapter_id"],
        unique=False,
    )
    op.create_table(
        "user_audiobook",
        sa.Column(
            "user_audiobook_id", sa.INTEGER(), autoincrement=True, nullable=False
        ),
        sa.Column("account_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("audiobook_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column(
            "last_listened_chapter_id", sa.INTEGER(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["account.account_id"],
            name="user_audiobook_account_id_fkey",
        ),
        sa.ForeignKeyConstraint(
            ["audiobook_id"],
            ["audiobook.audiobook_id"],
            name="user_audiobook_audiobook_id_fkey",
        ),
        sa.ForeignKeyConstraint(
            ["last_listened_chapter_id"],
            ["chapter.chapter_id"],
            name="user_audiobook_last_listened_chapter_id_fkey",
        ),
        sa.PrimaryKeyConstraint("user_audiobook_id", name="user_audiobook_pkey"),
    )
    op.create_index(
        "ix_user_audiobook_user_audiobook_id",
        "user_audiobook",
        ["user_audiobook_id"],
        unique=False,
    )
    op.drop_table("user_shelf")
    # ### end Alembic commands ###