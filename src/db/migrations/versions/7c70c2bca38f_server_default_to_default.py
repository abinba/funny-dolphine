"""server_default to default

Revision ID: 7c70c2bca38f
Revises: 8b5afc6fb3e6
Create Date: 2024-01-10 14:34:38.896537

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7c70c2bca38f"
down_revision: Union[str, None] = "8b5afc6fb3e6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
