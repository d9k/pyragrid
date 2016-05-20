"""transaction__money_shop_delta

Revision ID: 9a3b0f4f4fcd
Revises: 4e9c974bc7ed
Create Date: 2016-05-20 13:43:33.287542

"""

# revision identifiers, used by Alembic.
revision = '9a3b0f4f4fcd'
down_revision = '4e9c974bc7ed'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('money_transaction', sa.Column('shop_money_delta', sa.Numeric(precision=12, scale=2), nullable=False, default=0.0, server_default='0.0'),)


def downgrade():
    op.drop_column('money_transaction', 'shop_money_delta')
