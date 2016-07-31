pyragrid README
===============

Installation
------------

http://docs.pylonsproject.org/projects/pyramid/en/latest/quick_tutorial/requirements.html

### python venv

    # for psycopg2
    sudo apt-get install libpq-dev python-dev

    # ?
    sudo apt-get install python3.4-venv

    sudo apt-get install python3-pip
    sudo pip install virtualenv

    cd server
    virtualenv-3.4 venv

    # or `virtualenv -p $(which python3.4) venv`

    # for ubutu 16.04:
    sudo apt-get install python3.5-venv python3-pip
    pyvenv-3.5 venv
    
    source venv/bin/activate

optional hint:

run after every new package installation (for venv moving ability)

    virtualenv-3.4 --relocatable venv

check after `source venv/bin/activate`:

	which python
	python --version
	which easy_install

### main part

	cd server

	$VENV/bin/python setup.py develop
	# run setup.py with develop param on production too
	# if you experience some dependency missing error, try run command again

    cp development.ini.template development.ini
    cp development_passwords.ini.template development_passwords.ini
    # then edit *.ini files

    createdb <your_db_name>
	$VENV/bin/initialize_pyragrid_db development.ini
	$VENV/bin/pserve development.ini

### For Jinja asset compiler working

install nodejs (for Ubuntu):

    sudo apt-get install -y build-essential

    curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
    sudo apt-get install -y nodejs

then

    sudo npm install -g coffee-script js2coffee

### For assets fix

    # ensure ruby installed, then
    sudo su -c "gem install sass"

    sudo npm i -g gulp bower
    npm i
    gulp bower
    gulp

Type hinting
------------

https://www.jetbrains.com/pycharm/help/type-hinting-in-pycharm.html

ReST docstrings
---------------

https://www.python.org/dev/peps/pep-0287/

SQLAlchemy ER diagram generator
-------------------------------

https://github.com/pygraphviz/pygraphviz/issues/20

http://stackoverflow.com/questions/15661384/python-does-not-see-pygraphviz
sudo apt-get install graphviz libgraphviz-dev pkg-config

https://github.com/pygraphviz/pygraphviz/issues/71
pip install pygraphviz --install-option="--include-path=/usr/include/graphviz" --install-option="--library-path=/usr/lib/graphviz/"

diagrams generator (optional)
-----------------------------

(see https://gist.github.com/NLKNguyen/c39596c205ba1f1866c8)

1. install graphviz package

	sudo apt-get install graphviz

2. Download PlantUML (http://plantuml.sourceforge.net/download.html)
3. Unpack and run PlantUML (`java -jar /path/to/plantuml.jar`)

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

Emacs debug
===========

`Alt+X venv-activate`

http://stackoverflow.com/questions/3734880/getting-pdb-in-emacs-to-use-python-process-from-current-virtualenv
