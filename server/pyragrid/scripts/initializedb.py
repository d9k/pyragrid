import os
import sys
import transaction
import pyragrid.helpers as helpers

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from pyragrid.models import (
    DBSession,
    # MyModel,
    Base,
    User,
    ADMIN_GROUP
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


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

    sql_engine = engine_from_config(settings, 'sqlalchemy.')
    # DBSession.configure(bind=engine)
    Base.metadata.create_all(sql_engine)
    Base.metadata.bind = sql_engine
    # transaction.commit()

    # with transaction.manager:
    admin = User()
    admin.login = 'admin'
    admin.set_password('changeme')
    admin.group = ADMIN_GROUP
    admin.email = 'noemail@changeme.org'
    admin.active = True
    admin.email_checked = True
    #     model = MyModel(name='one', value=1)
    DBSession.add(admin)
    transaction.commit()
