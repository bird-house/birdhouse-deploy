#!/bin/sh

THIS_FILE="`readlink -f "$0" || realpath "$0"`"
THIS_DIR="`dirname "$THIS_FILE"`"
COMPOSE_DIR="`dirname "$THIS_DIR"`"

if [ -f "${COMPOSE_DIR}/scripts/logging.include.sh" ]; then
    . "${COMPOSE_DIR}/scripts/logging.include.sh"
fi

# eg: DB_NAME=finch
DB_NAME="$1"
if [ -z "$DB_NAME" ]; then
    echo "${MSG_ERROR}please provide a database name, ex: finch" 1>&2
    exit 2
fi
shift

POSTGRES_USER="$1"
if [ -z "$POSTGRES_USER" ]; then
    POSTGRES_USER=pavics
else
    shift
fi

if [ -z "$POSTGRES_CONTAINER_NAME" ]; then
    POSTGRES_CONTAINER_NAME=postgres
fi

set -x
docker exec $POSTGRES_CONTAINER_NAME psql -U $POSTGRES_USER $DB_NAME -c "select * from pywps_requests where percent_done > -1 and percent_done < 100.0;"

set +x
echo "
${MSG_WARN}This will crash all the above requests if currently still processing

Clear those jobs? (Ctrl-C to cancel, any keys to continue)"

read a

set -x
docker exec $POSTGRES_CONTAINER_NAME psql -U $POSTGRES_USER $DB_NAME -c "delete from pywps_requests where percent_done > -1 and percent_done < 100.0;"
