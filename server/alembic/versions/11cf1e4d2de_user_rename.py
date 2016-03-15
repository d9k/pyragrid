"""user_rename

Revision ID: 11cf1e4d2de
Revises: 49dd5602656
Create Date: 2016-03-15 13:59:36.665180

"""

# revision identifiers, used by Alembic.
revision = '11cf1e4d2de'
down_revision = '49dd5602656'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.rename_table('_user', 'user_')


def downgrade():
    op.rename_table('user_', '_user')
