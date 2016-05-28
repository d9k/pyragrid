"""money_transaction_status__additional_data

Revision ID: 7d43288ab025
Revises: 30c97ac1c453
Create Date: 2016-05-28 22:44:06.602051

"""

# revision identifiers, used by Alembic.
revision = '7d43288ab025'
down_revision = '30c97ac1c453'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    op.add_column('money_transaction_status', sa.Column('additional_data', postgresql.JSON(), nullable=True))


def downgrade():
    op.drop_column('money_transaction_status', 'additional_data')
