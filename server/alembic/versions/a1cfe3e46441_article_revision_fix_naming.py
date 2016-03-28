"""article_revision_fix_naming

Revision ID: a1cfe3e46441
Revises: 4411cbb7f8a4
Create Date: 2016-03-28 23:46:12.702935

"""

# revision identifiers, used by Alembic.
revision = 'a1cfe3e46441'
down_revision = '4411cbb7f8a4'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_constraint('articles_revisions_authorId_fkey', 'article_revision', type_='foreignkey')
    op.drop_constraint('articles_revisions_articleId_fkey', 'article_revision', type_='foreignkey')
    op.alter_column('article_revision', 'articleId', new_column_name='article_id')
    op.alter_column('article_revision', 'authorId', new_column_name='author_id')
    op.alter_column('article_revision', 'parentRevisionId', new_column_name='parent_revision_id')
    op.create_foreign_key(None, 'article_revision', 'user_', ['author_id'], ['id'])
    op.create_foreign_key(None, 'article_revision', 'article', ['article_id'], ['id'])


def downgrade():
    op.drop_constraint('article_revision_author_id_fkey', 'article_revision', type_='foreignkey')
    op.drop_constraint('article_revision_article_id_fkey', 'article_revision', type_='foreignkey')
    op.alter_column('article_revision', 'article_id', new_column_name='articleId')
    op.alter_column('article_revision', 'author_id', new_column_name='authorId')
    op.alter_column('article_revision', 'parent_revision_id', new_column_name='parentRevisionId')
    op.create_foreign_key('articles_revisions_articleId_fkey', 'article_revision', 'article', ['articleId'], ['id'])
    op.create_foreign_key('articles_revisions_authorId_fkey', 'article_revision', 'user_', ['authorId'], ['id'])

