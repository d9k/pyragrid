"""order__status

Revision ID: df9db701b083
Revises: ee8719899838
Create Date: 2016-05-17 03:29:14.299379

"""

# revision identifiers, used by Alembic.
revision = 'df9db701b083'
down_revision = 'ee8719899838'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():

    op.add_column(
        'order_',
        sa.Column(
            'status',
            nullable=False,
            default='cart',
            type_=sa.Enum(
                'refunded', 'paid', 'cart', 'refund_failed', 'refund_began', 'goods_sent_back',
                'payment_began', 'payment_failed', 'goods_sent', 'goods_received_back', 'goods_received',
                'partially_paid',
                name='enum_order_status',
                native_enum=False
            ),
            server_default='cart'
        )
    )


def downgrade():
    op.drop_column('order_', 'status')
