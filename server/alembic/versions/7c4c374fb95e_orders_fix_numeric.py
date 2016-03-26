"""orders_fix_numeric

Revision ID: 7c4c374fb95e
Revises: 3ef35b74884
Create Date: 2016-03-22 04:31:38.280967

"""

# revision identifiers, used by Alembic.
revision = '7c4c374fb95e'
down_revision = '3ef35b74884'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('order', 'paid_amount',
               existing_type=sa.REAL(),
               type_=sa.Numeric(precision=12, scale=2),
               existing_nullable=True)
    op.alter_column('order', 'rejected_amount',
               existing_type=sa.REAL(),
               type_=sa.Numeric(precision=12, scale=2),
               existing_nullable=True)
    op.alter_column('order', 'total',
               existing_type=sa.REAL(),
               type_=sa.Numeric(precision=12, scale=2),
               existing_nullable=True)
    op.alter_column('order_good', 'count',
               existing_type=sa.REAL(),
               type_=sa.Numeric(precision=12, scale=4),
               existing_nullable=True)
    op.alter_column('order_good', 'paid_amount',
               existing_type=sa.REAL(),
               type_=sa.Numeric(precision=12, scale=2),
               existing_nullable=True)
    op.alter_column('order_good', 'refund_amount',
               existing_type=sa.REAL(),
               type_=sa.Numeric(precision=12, scale=2),
               existing_nullable=True)
    op.alter_column('order_good', 'refund_count',
               existing_type=sa.REAL(),
               type_=sa.Numeric(precision=12, scale=4),
               existing_nullable=True)
    op.alter_column('order_good', 'total',
               existing_type=sa.REAL(),
               type_=sa.Numeric(precision=12, scale=2),
               existing_nullable=True)
    op.alter_column('order_good_status', 'paid',
               existing_type=sa.REAL(),
               type_=sa.Numeric(precision=12, scale=2),
               existing_nullable=True)
    op.alter_column('order_good_status', 'rejected',
               existing_type=sa.REAL(),
               type_=sa.Numeric(precision=12, scale=2),
               existing_nullable=True)
    op.alter_column('order_good_status', 'shop_money_delta',
               existing_type=sa.REAL(),
               type_=sa.Numeric(precision=12, scale=2),
               existing_nullable=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('order_good_status', 'shop_money_delta',
               existing_type=sa.Numeric(precision=12, scale=2),
               type_=sa.REAL(),
               existing_nullable=True)
    op.alter_column('order_good_status', 'rejected',
               existing_type=sa.Numeric(precision=12, scale=2),
               type_=sa.REAL(),
               existing_nullable=True)
    op.alter_column('order_good_status', 'paid',
               existing_type=sa.Numeric(precision=12, scale=2),
               type_=sa.REAL(),
               existing_nullable=True)
    op.alter_column('order_good', 'total',
               existing_type=sa.Numeric(precision=12, scale=2),
               type_=sa.REAL(),
               existing_nullable=True)
    op.alter_column('order_good', 'refund_count',
               existing_type=sa.Numeric(precision=12, scale=4),
               type_=sa.REAL(),
               existing_nullable=True)
    op.alter_column('order_good', 'refund_amount',
               existing_type=sa.Numeric(precision=12, scale=2),
               type_=sa.REAL(),
               existing_nullable=True)
    op.alter_column('order_good', 'paid_amount',
               existing_type=sa.Numeric(precision=12, scale=2),
               type_=sa.REAL(),
               existing_nullable=True)
    op.alter_column('order_good', 'count',
               existing_type=sa.Numeric(precision=12, scale=4),
               type_=sa.REAL(),
               existing_nullable=True)
    op.alter_column('order', 'total',
               existing_type=sa.Numeric(precision=12, scale=2),
               type_=sa.REAL(),
               existing_nullable=True)
    op.alter_column('order', 'rejected_amount',
               existing_type=sa.Numeric(precision=12, scale=2),
               type_=sa.REAL(),
               existing_nullable=True)
    op.alter_column('order', 'paid_amount',
               existing_type=sa.Numeric(precision=12, scale=2),
               type_=sa.REAL(),
               existing_nullable=True)
    ### end Alembic commands ###