"""deleted at for soft deletes

Revision ID: f920b07db2c5
Revises: 6076bfce55f0
Create Date: 2025-01-18 22:35:04.111253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f920b07db2c5'
down_revision: Union[str, None] = '6076bfce55f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('url_shortener', sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('url_shortener', 'deleted_at')
    # ### end Alembic commands ###
