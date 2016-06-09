"""order_goos_status__money_migration_fields

Revision ID: 6caa144f53bf
Revises: c0044c89c220
Create Date: 2016-06-09 03:03:10.436161

"""

# revision identifiers, used by Alembic.
revision = '6caa144f53bf'
down_revision = 'c0044c89c220'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_constraint('order_good_status_money_transaction_status_id_fkey', 'order_good_status', type_='foreignkey')
    op.alter_column('order_good_status', 'money_transaction_status_id', new_column_name='transaction_status_id',
                    existing_type=sa.Integer(), existing_nullable=True)
    op.create_foreign_key(None, 'order_good_status', 'money_transaction_status', ['transaction_status_id'], ['id'])

    op.add_column('order_good_status', sa.Column('transaction_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'order_good_status', 'money_transaction', ['transaction_id'], ['id'])


def downgrade():
    op.drop_constraint('order_good_status_transaction_status_id_fkey', 'order_good_status', type_='foreignkey')
    op.alter_column('order_good_status', 'transaction_status_id', new_column_name='money_transaction_status_id',
                    existing_type=sa.Integer(), existing_nullable=True)
    op.create_foreign_key(None, 'order_good_status', 'money_transaction_status', ['money_transaction_status_id'], ['id'])

    op.drop_constraint('order_good_status_transaction_id_fkey', 'order_good_status', type_='foreignkey')
    op.drop_column('order_good_status', 'transaction_id')

