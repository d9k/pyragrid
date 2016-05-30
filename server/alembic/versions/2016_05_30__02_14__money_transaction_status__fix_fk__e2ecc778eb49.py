"""money_transaction_status__fix_fk

Revision ID: e2ecc778eb49
Revises: 38b2617c4b5b
Create Date: 2016-05-30 02:14:05.049063

"""

# revision identifiers, used by Alembic.
revision = 'e2ecc778eb49'
down_revision = '38b2617c4b5b'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_constraint('money_transaction_status_money_transaction_id_fkey', 'money_transaction_status', type_='foreignkey')
    op.create_foreign_key(None, 'money_transaction_status', 'money_transaction', ['money_transaction_id'], ['id'])


def downgrade():
    op.drop_constraint(None, 'money_transaction_status', type_='foreignkey')
    op.create_foreign_key('money_transaction_status_money_transaction_id_fkey', 'money_transaction_status', 'order_good', ['money_transaction_id'], ['id'])
