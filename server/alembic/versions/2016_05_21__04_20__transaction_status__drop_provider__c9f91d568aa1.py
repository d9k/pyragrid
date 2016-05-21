"""transaction_status__drop_provider

Revision ID: c9f91d568aa1
Revises: 6006c9f681c0
Create Date: 2016-05-21 04:20:12.889792

"""

# revision identifiers, used by Alembic.
revision = 'c9f91d568aa1'
down_revision = '6006c9f681c0'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('money_transaction_status', 'provider')


def downgrade():
    op.add_column('money_transaction_status', sa.Column('provider', sa.TEXT(), autoincrement=False, nullable=True))
