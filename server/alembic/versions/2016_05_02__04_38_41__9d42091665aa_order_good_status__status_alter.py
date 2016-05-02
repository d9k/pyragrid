"""order_good_status__status_alter

Revision ID: 9d42091665aa
Revises: 18192965e0b9
Create Date: 2016-05-02 04:38:41.975364

"""

# revision identifiers, used by Alembic.
revision = '9d42091665aa'
down_revision = '18192965e0b9'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector
# for raw sql:
# from sqlalchemy import text

connection = op.get_bind()
engine_name = connection.engine.name
# WTF!?!? inspector can't inspect check constaints!!111
inspector = Inspector.from_engine(connection.engine)

enum_order_good_status_new = sa.Enum('wanted_add', 'wanted_remove', 'payment_began', 'payment_failed', 'paid', 'refund_began', 'refund_began', 'refund_failed', 'refunded', 'good_sent', 'good_received', 'good_sent_back', name='enum_order_status', native_enum=False)

enum_order_good_status_old = sa.Enum('created', 'excluded', 'payment_began', 'payment_failed', 'paid', 'refund_began',  'refund_failed', 'refunded', name='enum_order_status', native_enum=False)

order_good_status_helper = sa.Table(
    'order_good_status',
    sa.MetaData(),
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('status', sa.String)
)

order_good_helper = sa.Table(
    'order_good',
    sa.MetaData(),
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('status', sa.String)
)

def upgrade():
    # raise Exception('Not implemented yet')
    # @zzzeek, sqlalchemy developer, doesn't want to fix non-native enums
    # (https://bitbucket.org/zzzeek/alembic/issues/363)
    # so here is the hack:

    if engine_name == 'postgresql':
        connection.engine.execute("""
            ALTER TABLE order_good_status DROP CONSTRAINT IF EXISTS enum_order_status;
            ALTER TABLE order_good DROP CONSTRAINT IF EXISTS enum_order_status;
        """)
    #     # TODO fix, check constraint
    #     op.drop_constraint('enum_order_status', 'order_good_status')
    #     op.drop_constraint('enum_order_status', 'order_good')

    op.execute(
        order_good_status_helper.update().
        where(order_good_status_helper.c.status == op.inline_literal('created')).
        values({'status': op.inline_literal('wanted_add')})
        # TODO ENSURE VARCHAR LENGTH SUFFICIENCY!
    )

    op.execute(
        order_good_helper.update().
        where(order_good_helper.c.status == op.inline_literal('created')).
        values({'status': op.inline_literal('wanted_add')})
        # TODO ENSURE VARCHAR LENGTH SUFFICIENCY!
    )

    op.alter_column(
        'order_good_status',
        'status',
        type_=enum_order_good_status_new,
        # existing_nullable=True,
        nullable=False
    )

    op.alter_column(
        'order_good',
        'status',
        type_=enum_order_good_status_new,
        # existing_nullable=True,
        nullable=False
    )


def downgrade():
    # raise Exception('Not implemented yet')
    if engine_name == 'postgresql':
        connection.engine.execute("""
           ALTER TABLE order_good_status DROP CONSTRAINT IF EXISTS enum_order_status;
           ALTER TABLE order_good DROP CONSTRAINT IF EXISTS enum_order_status;
        """)
    #     op.drop_constraint('enum_order_status', 'order_good_status')
    #     op.drop_constraint('enum_order_status', 'order_good')

    op.execute(
        order_good_status_helper.update().
        where(order_good_status_helper.c.status == op.inline_literal('wanted_add')).
        values({'status': op.inline_literal('created')})
    )

    op.execute(
        order_good_helper.update().
        where(order_good_helper.c.status == op.inline_literal('wanted_add')).
        values({'status': op.inline_literal('created')})
    )

    op.alter_column(
        'order_good_status',
        'status',
        type_=enum_order_good_status_old,
        # existing_nullable=False,
        nullable=True
    )

    op.alter_column(
        'order_good',
        'status',
        type_=enum_order_good_status_old,
        # existing_nullable=False,
        nullable=True
    )

