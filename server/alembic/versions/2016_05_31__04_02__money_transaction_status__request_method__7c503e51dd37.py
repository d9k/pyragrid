"""money_transaction_status__request_method

Revision ID: 7c503e51dd37
Revises: e2ecc778eb49
Create Date: 2016-05-31 04:02:39.557726

"""

# revision identifiers, used by Alembic.
revision = '7c503e51dd37'
down_revision = 'e2ecc778eb49'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'money_transaction_status',
        sa.Column(
            'request_method',
            sa.Enum('GET', 'POST', name='enum_request_method', native_enum=False),
            nullable=False
        )
    )


def downgrade():
    op.drop_column('money_transaction_status', 'request_method')
