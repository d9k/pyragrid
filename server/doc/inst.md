Installation
============

#http://flask.pocoo.org/docs/0.10/tutorial/
http://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/requirements.html

installation:

	virtualenv -p $(which python3.4) venv
	source venv/bin/activate

проверка после `source venv/bin/activate`:

	which python
	python --version
	which easy_install

установка зависимостей:

	//easy_install "pyramid==1.5.7"
	//easy_install nose webtest deform sqlalchemy pyramid_jinja2 pyramid_debugtoolbar waitress pyramid_tm zope.sqlalchemy

	pip install "pyramid==1.5.7"
    pip install nose webtest deform sqlalchemy pyramid_jinja2 pyramid_debugtoolbar waitress pyramid_tm zope.sqlalchemy pyramid_beaker

pyramid_beaker - сессии


https://pypi.python.org/pypi/sqlacodegen:

    pip install psycopg2 sqlacodegen

alembic (https://alembic.readthedocs.org/en/latest/tutorial.html) :

    pip install alembic
    alembic init --template pylons alembic

http://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/scaffolds.html

	hash -r
	pcreate --scaffold starter scaffolds
	cd scaffolds
	python setup.py develop
	pserve development.ini --reload

#Server run (after /venv/bin/activate !):
#python flaskr.py