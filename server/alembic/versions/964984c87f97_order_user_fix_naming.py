"""order_user_fix_naming

Revision ID: 964984c87f97
Revises: 14e5f0e24a44
Create Date: 2016-03-29 00:03:15.685882

"""

# revision identifiers, used by Alembic.
revision = '964984c87f97'
down_revision = '14e5f0e24a44'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_constraint('order_good_order_id_fkey', 'order_good', type_='foreignkey')
    op.rename_table('order', 'order_')
    op.create_foreign_key(None, 'order_good', 'order_', ['order_id'], ['id'])
    op.alter_column('user_', 'group', new_column_name='group_')


def downgrade():
    op.drop_constraint('order_good_order_id_fkey', 'order_good', type_='foreignkey')
    op.rename_table('order_', 'order')
    op.alter_column('user_', 'group_', new_column_name='group')
    op.create_foreign_key('order_good_order_id_fkey', 'order_good', 'order', ['order_id'], ['id'])
