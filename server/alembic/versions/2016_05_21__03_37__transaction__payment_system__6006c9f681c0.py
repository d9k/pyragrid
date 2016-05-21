"""transaction__payment_system

Revision ID: 6006c9f681c0
Revises: 9a3b0f4f4fcd
Create Date: 2016-05-21 03:37:46.420252

"""

# revision identifiers, used by Alembic.
revision = '6006c9f681c0'
down_revision = '9a3b0f4f4fcd'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('money_transaction', sa.Column('payment_system', sa.String(length=20), nullable=False))


def downgrade():
    op.drop_column('money_transaction', 'payment_system')
