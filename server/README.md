pyragrid README
===============

Getting Started
---------------

- cd <directory containing this file>

- $VENV/bin/python setup.py develop

- $VENV/bin/initialize_pyragrid_db development.ini

- $VENV/bin/pserve development.ini


TODO: how to install ColanderAlchemy simplier?

	pip install ColanderAlchemy
	cd venv/lib/python3.4/site-packages
	unzip ColanderAlchemy-0.3.3-py3.4.egg
	rm -r EGG-INFO

Type hinting
------------

https://www.jetbrains.com/pycharm/help/type-hinting-in-pycharm.html

ReST docstrings
---------------

https://www.python.org/dev/peps/pep-0287/

Jinja asset compiler
--------------------

sudo npm install -g coffee-script
sudo npm install -g js2coffee

Installation
============

http://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/requirements.html

installation:

	virtualenv -p $(which python3.4) venv
	source venv/bin/activate

run after every new package installation (for venv moving ability)

	virtualenv-3.4 --relocatable venv

TODO check this:

	pip freeze > requirements.txt

check after `source venv/bin/activate`:

	which python
	python --version
	which easy_install

dependancy install:

	//easy_install "pyramid==1.5.7"
	//easy_install nose webtest deform sqlalchemy pyramid_jinja2 pyramid_debugtoolbar waitress pyramid_tm zope.sqlalchemy

	pip install "pyramid==1.5.7"
    pip install nose webtest deform sqlalchemy pyramid_jinja2 pyramid_debugtoolbar waitress pyramid_tm zope.sqlalchemy pyramid_beaker

pyramid_beaker - sessions


https://pypi.python.org/pypi/sqlacodegen:

    pip install psycopg2 sqlacodegen

alembic (https://alembic.readthedocs.org/en/latest/tutorial.html) :

    pip install alembic
    alembic init --template pylons alembic


password hashing (http://www.cyberciti.biz/python-tutorials/securely-hash-passwords-in-python/)

	pip install passlib

http://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/scaffolds.html

	hash -r
	pcreate --scaffold starter scaffolds
	cd scaffolds
	python setup.py develop

#Server run (after /venv/bin/activate !):

	pserve development.ini --reload

TODO
====

<!---

-->