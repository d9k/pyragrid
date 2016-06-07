"""order_good__wanted_total

Revision ID: c0044c89c220
Revises: 3dd1f2c8641f
Create Date: 2016-06-07 15:31:38.161586

"""

# revision identifiers, used by Alembic.
revision = 'c0044c89c220'
down_revision = '3dd1f2c8641f'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('order_good', 'count', new_column_name='wanted_count',
                    existing_type=sa.Numeric(precision=12, scale=4), existing_nullable=True)


def downgrade():
    op.alter_column('order_good', 'wanted_count', new_column_name='count',
                    existing_type=sa.Numeric(precision=12, scale=4), existing_nullable=True)
