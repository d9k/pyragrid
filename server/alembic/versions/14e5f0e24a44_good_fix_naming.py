"""good_fix_naming

Revision ID: 14e5f0e24a44
Revises: a1cfe3e46441
Create Date: 2016-03-28 23:55:51.893126

"""

# revision identifiers, used by Alembic.
revision = '14e5f0e24a44'
down_revision = 'a1cfe3e46441'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('good', 'isEgood', new_column_name='is_egood')
    op.alter_column('good', 'filePath', new_column_name='filepath')


def downgrade():
    op.alter_column('good', 'is_egood', new_column_name='isEgood')
    op.alter_column('good', 'filepath', new_column_name='filePath')
