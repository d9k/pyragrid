"""good_active

Revision ID: 2c2a22c3407
Revises: 3487fa86e0a
Create Date: 2016-01-23 13:31:55.853639

"""

# revision identifiers, used by Alembic.
revision = '2c2a22c3407'
down_revision = '3487fa86e0a'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goods', sa.Column('active', sa.Boolean(), server_default='false', nullable=False))
    op.alter_column('goods', 'name',
               existing_type=sa.TEXT(),
               nullable=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('goods', 'name',
               existing_type=sa.TEXT(),
               nullable=True)
    op.drop_column('goods', 'active')
    ### end Alembic commands ###
