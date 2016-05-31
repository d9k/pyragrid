"""money_transaction__fix__order_id__fk

Revision ID: 3dd1f2c8641f
Revises: 7c503e51dd37
Create Date: 2016-05-31 05:07:04.715278

"""

# revision identifiers, used by Alembic.
revision = '3dd1f2c8641f'
down_revision = '7c503e51dd37'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_constraint('money_transaction_order_id_fkey', 'money_transaction', type_='foreignkey')
    op.create_foreign_key(None, 'money_transaction', 'order_', ['order_id'], ['id'])


def downgrade():
    op.drop_constraint('money_transaction_order_id_fkey', 'money_transaction', type_='foreignkey')
    op.create_foreign_key('money_transaction_order_id_fkey', 'money_transaction', 'user_', ['order_id'], ['id'])
