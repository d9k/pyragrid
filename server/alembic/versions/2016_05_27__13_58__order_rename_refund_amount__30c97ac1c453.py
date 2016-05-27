"""order_rename_refund_amount

Revision ID: 30c97ac1c453
Revises: c9f91d568aa1
Create Date: 2016-05-27 13:58:13.218568

"""

# revision identifiers, used by Alembic.
revision = '30c97ac1c453'
down_revision = 'c9f91d568aa1'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column(
        'order_', 'rejected_amount', new_column_name='refund_amount',
        existing_type=sa.NUMERIC(precision=12, scale=2), existing_nullable=True
    )


def downgrade():
    op.alter_column(
        'order_', 'refund_amount', new_column_name='rejected_amount',
        existing_type=sa.NUMERIC(precision=12, scale=2), existing_nullable=True
    )
