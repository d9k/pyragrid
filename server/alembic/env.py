from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

import pyragrid.scripts.parse_config as parse_pyragrid_config

# pyragrid additional BEGIN
for additional_option in config.cmd_opts.x:
    by_equal_split = additional_option.split('=')
    if len(by_equal_split) == 2 and by_equal_split[0] == 'pyramid_config':
        pyragrid_ini_name = by_equal_split[1]
        pyragrid_ini_path = parse_pyragrid_config.get_ini_path(pyragrid_ini_name)
        pyragrid_connection_url = parse_pyragrid_config.get_connection_url_from_ini(pyragrid_ini_path)
        if pyragrid_connection_url:
            config.set_main_option('sqlalchemy.url', pyragrid_connection_url)
# END pyragrid additional

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None

from pyragrid.models import Base
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
