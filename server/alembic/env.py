from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import logging
import os

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

import pyragrid.scripts.parse_config as parse_pyragrid_config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
logging.config.fileConfig(config.config_file_name)

log = logging.getLogger(__name__)

# deprecated block BEGIN (now os.getenv is used instead)
## pyragrid additional BEGIN
## if config.cmd_opts.x is not None:
##     for additional_option in config.cmd_opts.x:
##         by_equal_split = additional_option.split('=')
##         if len(by_equal_split) == 2 and by_equal_split[0] == 'pyramid_config':
##             pyragrid_ini_name = by_equal_split[1]
##
## # TODO (?) get PYRAGRID_CONFIG_NAME from env
## if pyragrid_ini_name is None:
##     pyragrid_ini_name = 'development.ini'
# END deprecated block

pyragrid_ini_name = os.getenv('PYRAGRID_CONFIG_NAME', 'development.ini')
pyragrid_ini_path = parse_pyragrid_config.get_ini_path(pyragrid_ini_name)
log.info('Alembic uses config from "{0}"'.format(pyragrid_ini_path))
# print('db name is ')

pyragrid_ini = parse_pyragrid_config.load_merged_ini(pyragrid_ini_name)
pyragrid_connection_url = parse_pyragrid_config.get_connection_url_from_settings(pyragrid_ini)
db_connection_params = parse_pyragrid_config.db_connection_params_from_url(pyragrid_connection_url)
db_name = db_connection_params.get('name')
log.info('db name is "{0}"'.format(db_name))

if pyragrid_connection_url:
    config.set_main_option('sqlalchemy.url', pyragrid_connection_url)

if config.get_main_option('sqlalchemy.url') is None:
    # raise Exception('sqlalchemy.url is undefined. You should try to provide additional configuration with -x pyramid_config=<config_name.ini>')
    raise Exception('sqlalchemy.url is undefined. Check config "{0}" or use environment variable PYRAGRID_CONFIG_NAME to set proper config name'.format(db_name))
# END pyragrid additional

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None

from pyragrid.db import Base
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
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        # TODO check; from http://stackoverflow.com/questions/17174636/can-alembic-autogenerate-column-alterations
        compare_type=True
    )

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
            target_metadata=target_metadata,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
