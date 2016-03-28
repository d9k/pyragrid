"""article_columns_naming

Revision ID: 4411cbb7f8a4
Revises: 363785c825fa
Create Date: 2016-03-28 13:39:58.430181

"""

# revision identifiers, used by Alembic.
revision = '4411cbb7f8a4'
down_revision = '363785c825fa'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('article', 'activeRevisionId', new_column_name='active_revision_id')
    op.alter_column('article', 'systemName', new_column_name='system_name')
    op.alter_column('article', 'isTemplate', new_column_name='is_template')
    op.drop_constraint('articles_systemName_key', 'article', type_='unique')
    op.create_unique_constraint(None, 'article', ['system_name'])


def downgrade():
    op.alter_column('article', 'active_revision_id', new_column_name='activeRevisionId')
    op.alter_column('article', 'system_name', new_column_name='systemName')
    op.alter_column('article', 'is_template', new_column_name='isTemplate')
    op.drop_constraint('article_system_name_key', 'article', type_='unique')
    op.create_unique_constraint('articles_systemName_key', 'article', ['systemName'])
