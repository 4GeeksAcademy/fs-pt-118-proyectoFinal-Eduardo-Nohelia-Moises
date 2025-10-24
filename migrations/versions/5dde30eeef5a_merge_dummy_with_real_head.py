"""merge dummy with real head

Revision ID: 5dde30eeef5a
Revises: 0763d677d453, 0dea30be746a
Create Date: 2025-10-21 16:23:24.728516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5dde30eeef5a'
down_revision = ('0763d677d453', '0dea30be746a')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
