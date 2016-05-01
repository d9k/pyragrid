"""sum__to__wanted_sum

Revision ID: 86df297c8e7c
Revises: 92cd6c37e6e2
Create Date: 2016-05-02 02:05:42.657269

"""

# revision identifiers, used by Alembic.
revision = '86df297c8e7c'
down_revision = '92cd6c37e6e2'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('order_good', 'total', new_column_name='wanted_total')
    op.alter_column('order_', 'total', new_column_name='wanted_total')


def downgrade():
    op.alter_column('order_good', 'wanted_total', new_column_name='total')
    op.alter_column('order_', 'wanted_total', new_column_name='total')

