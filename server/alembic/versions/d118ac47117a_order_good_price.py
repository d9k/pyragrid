"""order_good_price

Revision ID: d118ac47117a
Revises: 615d69ab1b64
Create Date: 2016-04-15 03:07:33.899579

"""

# revision identifiers, used by Alembic.
revision = 'd118ac47117a'
down_revision = '615d69ab1b64'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_good', sa.Column('price', sa.Numeric(precision=12, scale=2), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order_good', 'price')
    ### end Alembic commands ###