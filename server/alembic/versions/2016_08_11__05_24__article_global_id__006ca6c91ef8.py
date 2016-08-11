"""article_global_id

Revision ID: 006ca6c91ef8
Revises: 5c1bda389af9
Create Date: 2016-08-11 05:24:38.694854

"""

# revision identifiers, used by Alembic.
revision = '006ca6c91ef8'
down_revision = '5c1bda389af9'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.add_column('article', sa.Column('global_id', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False))
    op.create_index(op.f('ix_article_global_id'), 'article', ['global_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_article_global_id'), table_name='article')
    op.drop_column('article', 'global_id')
