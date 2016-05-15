"""good__filepath__to__file_path

Revision ID: 18192965e0b9
Revises: 86df297c8e7c
Create Date: 2016-05-02 02:29:36.374895

"""

# revision identifiers, used by Alembic.
revision = '18192965e0b9'
down_revision = '86df297c8e7c'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

# TODO add existing_type for mysql!


def upgrade():
    op.alter_column('good', 'filepath', new_column_name='file_path')


def downgrade():
    op.alter_column('good', 'file_path', new_column_name='filepath')
