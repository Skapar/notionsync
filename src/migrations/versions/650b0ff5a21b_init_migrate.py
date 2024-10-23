"""init migrate

Revision ID: 650b0ff5a21b
Revises: 5aeade1a752c
Create Date: 2024-10-23 10:39:25.682968

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '650b0ff5a21b'
down_revision: Union[str, None] = '5aeade1a752c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
