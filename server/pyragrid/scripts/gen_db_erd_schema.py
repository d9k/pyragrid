import os
import os.path as path
import sys
import transaction
import pyragrid.helpers as helpers
import subprocess

from sqlalchemy import engine_from_config
import eralchemy

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from pyragrid.db import (
    DBSession,
    Base
    )

from os.path import dirname, realpath


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

#           server <- pyragrid <- scripts
server_path = dirname(dirname(dirname(realpath(__file__))))

bash_cwd = server_path
erd_file_name = 'erd-from-sqlalchemy.png'


def bash(*command_parts):
    # return subprocess.call(["bash", "-c", " ".join(command_parts)], cwd=bash_cwd, stdout=subprocess.PIPE)
    result = subprocess.check_output(["bash", "-c", " ".join(command_parts)], cwd=bash_cwd)
    return result.decode()


def proc(*command_parts):
    # return subprocess.call(["bash", "-c", " ".join(command_parts)], cwd=bash_cwd, stdout=subprocess.PIPE)
    result = subprocess.check_output(command_parts, cwd=bash_cwd)
    return result.decode()


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)

    settings = get_appsettings(config_uri, options=options)
    # passwords_config_path = helpers.get_passwords_config_path(global_config['__file__'])
    passwords_config_path = helpers.get_passwords_config_path(config_uri)
    if os.path.isfile(passwords_config_path):
        passwords_settings = helpers.load_config(passwords_config_path)
        settings = helpers.dicts_merge(passwords_settings.get('app:main', {}), settings)

    # sql_engine = engine_from_config(settings, 'sqlalchemy.')
    # # DBSession.configure(bind=engine)
    # Base.metadata.bind = sql_engine
    erd_file_path = path.realpath(path.join(server_path, '..', 'dia', erd_file_name))
    eralchemy.render_er(Base, erd_file_path)
    print('file generated. see "' + erd_file_path + '"')
