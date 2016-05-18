"""alter_enum_transaction_status

Revision ID: 6df5ae86f1e5
Revises: df9db701b083
Create Date: 2016-05-19 02:02:47.315546

"""

# revision identifiers, used by Alembic.
revision = '6df5ae86f1e5'
down_revision = 'df9db701b083'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

enum_money_transaction_status_new = sa.Enum(
    'init_request_sent', 'init_answer_received', 'redirect_to_payment_form',
    'confirmation_request_received', 'confirmation_answer_permit',
    'confirmation_answer_deny', 'notification_received',
    'notification_answered', 'failed', 'request_sent',
    name='enum_money_transaction_status',
    native_enum=False
)

enum_money_transaction_status_old = sa.Enum(
    'created', 'canceled', 'requestSent', 'succeed', 'error',
    name='enum_money_transaction_status',
    native_enum=False
)


connection = None
engine_name = None


def init():
    global connection, engine_name
    connection = op.get_bind()
    engine_name = connection.engine.name


def psql_drop_contraint(table, constraint):
    if engine_name == 'postgresql':
        connection.engine.execute("ALTER TABLE " + table + " DROP CONSTRAINT IF EXISTS " + constraint)


def upgrade():
    init()
    psql_drop_contraint(table='money_transaction', constraint='enum_money_transaction_status')
    psql_drop_contraint(table='money_transaction_status', constraint='enum_money_transaction_status')
    # in case of bizzare db state:
    psql_drop_contraint(table='money_transaction_status', constraint='enum_order_status')
    op.alter_column('money_transaction', 'status',
                    type_=enum_money_transaction_status_new,
                    existing_nullable=True)

    op.alter_column('money_transaction_status', 'status',
                    type_=enum_money_transaction_status_new,
                    existing_nullable=True)


def downgrade():
    init()
    psql_drop_contraint(table='money_transaction', constraint='enum_money_transaction_status')
    psql_drop_contraint(table='money_transaction_status', constraint='enum_money_transaction_status')
    op.alter_column('money_transaction_status', 'status',
                    type_=enum_money_transaction_status_old,
                    existing_nullable=True)

    op.alter_column('money_transaction', 'status',
                    type_=enum_money_transaction_status_old,
                    existing_nullable=True)
