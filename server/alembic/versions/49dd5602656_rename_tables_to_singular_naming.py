"""rename_tables_to_singular_naming

Revision ID: 49dd5602656
Revises: 2c2a22c3407
Create Date: 2016-03-14 15:31:55.470882

"""

# revision identifiers, used by Alembic.
revision = '49dd5602656'
down_revision = '2c2a22c3407'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    op.rename_table('users', '_user')
    op.rename_table('articles', 'article')
    op.rename_table('articles_revisions', 'article_revision')
    op.rename_table('goods', 'good')


def downgrade():
    op.rename_table('_user', 'users')
    op.rename_table('article', 'articles')
    op.rename_table('article_revision', 'articles_revisions')
    op.rename_table('good', 'goods')
