"""user_add_email_confirmation

Revision ID: 59ba331f80
Revises: 5421692cc2b
Create Date: 2015-10-07 08:00:21.548139

"""

# revision identifiers, used by Alembic.
revision = '59ba331f80'
down_revision = '5421692cc2b'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('active', sa.Boolean(), server_default='false', nullable=False))
    op.add_column('users', sa.Column('email_check_code', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('email_checked', sa.Boolean(), server_default='false', nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'email_checked')
    op.drop_column('users', 'email_check_code')
    op.drop_column('users', 'active')
    ### end Alembic commands ###
