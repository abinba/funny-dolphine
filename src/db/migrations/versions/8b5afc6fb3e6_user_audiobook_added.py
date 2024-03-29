"""user_audiobook added

Revision ID: 8b5afc6fb3e6
Revises: 08473aef612a
Create Date: 2024-01-10 14:03:09.715745

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8b5afc6fb3e6"
down_revision: Union[str, None] = "08473aef612a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_audiobook",
        sa.Column("user_audiobook_id", sa.Integer(), nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=True),
        sa.Column("audiobook_id", sa.Integer(), nullable=True),
        sa.Column("last_listened_chapter_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["account.account_id"],
        ),
        sa.ForeignKeyConstraint(
            ["audiobook_id"],
            ["audiobook.audiobook_id"],
        ),
        sa.ForeignKeyConstraint(
            ["last_listened_chapter_id"],
            ["chapter.chapter_id"],
        ),
        sa.PrimaryKeyConstraint("user_audiobook_id"),
    )
    op.create_index(
        op.f("ix_user_audiobook_user_audiobook_id"),
        "user_audiobook",
        ["user_audiobook_id"],
        unique=False,
    )
    op.alter_column(
        "chapter",
        "chapter_ordered_id",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=100),
        existing_nullable=False,
    )
    op.drop_column("user_chapter", "explored")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user_chapter",
        sa.Column("explored", sa.BOOLEAN(), autoincrement=False, nullable=True),
    )
    op.alter_column(
        "chapter",
        "chapter_ordered_id",
        existing_type=sa.String(length=100),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.drop_index(
        op.f("ix_user_audiobook_user_audiobook_id"), table_name="user_audiobook"
    )
    op.drop_table("user_audiobook")
    # ### end Alembic commands ###
