"""datetime_fix

Revision ID: 363785c825fa
Revises: 7c4c374fb95e
Create Date: 2016-03-28 00:22:36.361887

"""

# revision identifiers, used by Alembic.
revision = '363785c825fa'
down_revision = '7c4c374fb95e'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    op.alter_column('article_revision', 'dateTime', new_column_name='created_at')
    op.create_foreign_key(None, 'order', 'user_', ['user_id'], ['id'])
    op.add_column('order_good', sa.Column('good_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'order_good', 'good', ['good_id'], ['id'])
    op.alter_column('order_good_status', 'datetime', new_column_name='created_at')


def downgrade():
    op.alter_column('order_good_status', 'created_at', new_column_name='datetime')
    op.drop_constraint(None, 'order_good', type_='foreignkey')
    op.drop_column('order_good', 'good_id')
    op.drop_constraint(None, 'order', type_='foreignkey')
    op.alter_column('article_revision', 'created_at', new_column_name='dateTime')
