#!/bin/bash

echo "deprecated. must be deleted in future"
exit

if [ -z "$1" ]; then
	echo Usage: db-autogen-migration migration_name
	exit
fi

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SERVER_DIR=$(readlink -f ${THIS_DIR}/..)
cd ${SERVER_DIR}
. ${SERVER_DIR}/venv/bin/activate
source ${THIS_DIR}/db-params.inc.sh
#TODO config from env PYRAGRID_CONFIG_NAME
#alembic -x pyramid_config=${PYRAGRID_CONFIG_NAME} revision --autogenerate -m $1
alembic revision --autogenerate -m $1