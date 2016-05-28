"""money_transaction_status__url

Revision ID: 38b2617c4b5b
Revises: 7d43288ab025
Create Date: 2016-05-29 00:59:29.667634

"""

# revision identifiers, used by Alembic.
revision = '38b2617c4b5b'
down_revision = '7d43288ab025'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('money_transaction_status', sa.Column('url', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('money_transaction_status', 'url')
