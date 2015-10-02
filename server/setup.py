import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    # 'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'pyramid_jinja2',
    'pyramid_beaker',
    'deform==2.0a2',
    'colander',
    'ColanderAlchemy',
    'dictalchemy',
    'repoze.sendmail==4.1',
    'pyramid_mailer',
    # 'ConfigParser',
    'configparser',

]

setup(name='best_tests_server',
      version='0.0',
      description='best_tests_server',
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
      test_suite='best_tests_server',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = best_tests_server:main
      [console_scripts]
      initialize_best_tests_server_db = best_tests_server.scripts.initializedb:main
      """,
      )
