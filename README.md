pyragrid README
===============

Installation
------------

http://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/requirements.html

python venv
~~~~~~~~~~~

    # for psycopg2
    sudo apt-get install libpq-dev python-dev

    # ?
    sudo apt-get install python3.4-venv

    sudo apt-get install python3-pip
    sudo pip install virtualenv

    cd server
    virtualenv-3.4 venv
    # or `virtualenv -p $(which python3.4) venv`
    source venv/bin/activate

optional hint:

run after every new package installation (for venv moving ability)

    virtualenv-3.4 --relocatable venv

check after `source venv/bin/activate`:

	which python
	python --version
	which easy_install

main part
~~~~~~~~~

	cd server

	$VENV/bin/python setup.py develop
	# run setup.py with develop param on production too
	# if you experience some dependency missing error, try run command again

        createdb <your_db_name>
	$VENV/bin/initialize_pyragrid_db development.ini
	$VENV/bin/pserve development.ini

//TODO: how to install ColanderAlchemy simplier?

//	pip install ColanderAlchemy
//	cd venv/lib/python3.4/site-packages
//	unzip ColanderAlchemy-0.3.3-py3.4.egg
//	rm -r EGG-INFO

For Jinja asset compiler working
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    sudo npm install -g coffee-script
    sudo npm install -g js2coffee


Type hinting
------------

https://www.jetbrains.com/pycharm/help/type-hinting-in-pycharm.html

ReST docstrings
---------------

https://www.python.org/dev/peps/pep-0287/

PRODUCTION DEPLOYMENT
=====================

    % sudo apt-get install supervisor
    % nano /etc/supervisor/supervisord.conf

To the end:

    [program:mysite]
    autorestart=true
    command=/path/to/mysite/server/venv/bin/pserve /path/to/mysite/server/production.ini http_port=50%(process_num)02d
    process_name=%(program_name)s-%(process_num)01d
    numprocs=2
    numprocs_start=0
    redirect_stderr=true
    stdout_logfile=/var/log/supervisor/%(program_name)s-%(process_num)01d.log

then

    % sudo service supervisor restart

TODO
====

TODO check this:

	pip freeze > requirements.txt
