#@IgnoreInspection BashAddShebang
#must be included as `source ./db-params.inc`

#TODO rewrite in python for x-platform etc
#TODO check venv

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SERVER_DIR=$(readlink -f ${THIS_DIR}/..)
SERVER_PACKAGE_DIR=$(readlink -f ${SERVER_DIR}/pyragrid)

if [[ -z "${PYRAGRID_CONFIG_NAME}" ]]; then
	PYRAGRID_CONFIG_NAME="development.ini"
fi

echo "config name is \"${PYRAGRID_CONFIG_NAME}\""

if [[ "${PYRAGRID_CONFIG_NAME}" == "production.ini" ]] || [[ "${PYRAGRID_CONFIG_NAME}" == "production" ]]; then
	read -p "Would you like to continue? (y/n): " answer
	if [[ "${answer}" != "y" ]]; then
		exit
	fi
fi

parse_config="${SERVER_PACKAGE_DIR}/scripts/parse_config.py -c ${PYRAGRID_CONFIG_NAME}"

DB_USER=$(${parse_config} db username)
#DB_PASSWORD=$(${parse_config} db password)
DB_NAME=$(${parse_config} db name)
DB_BACKUP_FILE_NAME="${DB_NAME}.sql"
MODEL_OUTPUT_FILE_NAME=models_.py
