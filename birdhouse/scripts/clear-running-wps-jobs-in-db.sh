#!/bin/sh

# eg: DB_NAME=finch
DB_NAME="$1"
if [ -z "$DB_NAME" ]; then
    echo "ERROR: please provide a database name, ex: finch" 1>&2
    exit 2
fi
shift

POSTGRES_USER="$1"
if [ -z "$POSTGRES_USER" ]; then
    POSTGRES_USER=birdhouse
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
WARNING: this will crash all the above requests if currently still processing

Clear those jobs? (Ctrl-C to cancel, any keys to continue)"

read a

set -x
docker exec $POSTGRES_CONTAINER_NAME psql -U $POSTGRES_USER $DB_NAME -c "delete from pywps_requests where percent_done > -1 and percent_done < 100.0;"
