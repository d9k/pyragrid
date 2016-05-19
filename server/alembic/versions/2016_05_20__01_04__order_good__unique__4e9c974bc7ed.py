"""order_good__unique

Revision ID: 4e9c974bc7ed
Revises: 6df5ae86f1e5
Create Date: 2016-05-20 01:04:38.947685

"""

# revision identifiers, used by Alembic.
revision = '4e9c974bc7ed'
down_revision = '6df5ae86f1e5'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_unique_constraint('order_good_unique', 'order_good', ['order_id', 'good_id', 'price'])


def downgrade():
    op.drop_constraint('order_good_unique', 'order_good', type_='unique')

