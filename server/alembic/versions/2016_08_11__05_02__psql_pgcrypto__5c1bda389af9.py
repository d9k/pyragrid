"""psql_pgcrypto

Revision ID: 5c1bda389af9
Revises: 6caa144f53bf
Create Date: 2016-08-11 05:02:58.987429

"""

# revision identifiers, used by Alembic.
revision = '5c1bda389af9'
down_revision = '6caa144f53bf'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    import sqlalchemy.exc
    connection = op.get_bind()
    engine_name = connection.engine.name
    if engine_name == 'postgresql':
        try:
            connection.engine.execute("DROP EXTENSION pgcrypto;")
        except sqlalchemy.exc.ProgrammingError:
            pass
        connection.engine.execute("CREATE EXTENSION pgcrypto;")

def downgrade():
    connection = op.get_bind()
    engine_name = connection.engine.name
    if engine_name == 'postgresql':
        connection.engine.execute("DROP EXTENSION pgcrypto;")

