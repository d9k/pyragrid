"""order_good_status__mod

Revision ID: ee8719899838
Revises: 9d42091665aa
Create Date: 2016-05-16 12:57:06.487868

"""

# revision identifiers, used by Alembic.
revision = 'ee8719899838'
down_revision = '9d42091665aa'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy import or_

enum_order_good_status_new = sa.Enum('wanted_alter', 'payment_began', 'payment_failed', 'paid', 'refund_began', 'refund_failed', 'refunded', 'good_sent', 'good_received', 'good_sent_back', name='enum_order_status', native_enum=False)

enum_order_good_status_old = sa.Enum('wanted_add', 'wanted_remove', 'payment_began', 'payment_failed', 'paid', 'refund_began', 'refund_failed', 'refunded', 'good_sent', 'good_received', 'good_sent_back', name='enum_order_status', native_enum=False)

order_good_status_helper = sa.Table(
    'order_good_status',
    sa.MetaData(),
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('status', sa.String)
)


def upgrade():
    connection = op.get_bind()
    engine_name = connection.engine.name

    op.drop_column('order_good', 'status')

    if engine_name == 'postgresql':
        connection.engine.execute("ALTER TABLE order_good_status DROP CONSTRAINT IF EXISTS enum_order_status;")

    op.execute(
        order_good_status_helper.update().
        where(order_good_status_helper.c.status == op.inline_literal('wanted_add')).
        values({'status': op.inline_literal('wanted_alter')})
        # TODO ENSURE VARCHAR LENGTH SUFFICIENCY!
    )

    op.alter_column('order_good_status', 'status',
                    type_=enum_order_good_status_new,
                    nullable=False)


def downgrade():
    connection = op.get_bind()
    engine_name = connection.engine.name

    op.add_column('order_good', sa.Column('status', type_=enum_order_good_status_new))

    if engine_name == 'postgresql':
        connection.engine.execute("ALTER TABLE order_good_status DROP CONSTRAINT IF EXISTS enum_order_status;")

    op.execute(
        order_good_status_helper.update().
        where(order_good_status_helper.c.status == op.inline_literal('wanted_alter')).
        values({'status': op.inline_literal('wanted_add')})
        # TODO ENSURE VARCHAR LENGTH SUFFICIENCY!
    )

    op.alter_column('order_good_status', 'status',
                    type_=enum_order_good_status_old,
                    nullable=False)


