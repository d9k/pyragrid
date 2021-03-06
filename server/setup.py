import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'pyramid_jinja2',
    'pyramid_beaker',
    'deform==2.0.4',
    'jac==0.16.1',  # jinja-assets-compressor
    'colander',
    'ColanderAlchemy',
    'dictalchemy',
    'repoze.sendmail==4.1',
    'pyramid_mailer',
    'configparser',
    'sqlalchemy-datatables==0.1.7',
    # 'https://github.com/Pegase745/sqlalchemy-datatables/archive/v0.1.7.zip"'
    'psycopg2',
    'alembic',
    'inflection',
    'pygraphviz',
    'eralchemy',
    'pyperclip',
    'dominate',  # html creation
    'formencode'  # MultiDict to dict
]

setup(name='pyragrid',
      version='0.0.6',
      description='pyragrid',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='pyragrid',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = pyragrid:main
      [console_scripts]
      initialize_pyragrid_db = pyragrid.scripts.initializedb:main
      gen_db_erd_schema = pyragrid.scripts.gen_db_erd_schema:main
      """,
      )
