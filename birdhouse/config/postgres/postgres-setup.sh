#!/usr/bin/env bash

set -e

export PGPASSWORD=${POSTGRES_PASSWORD}

databases_to_create=(
    flyingpigeon
    hummingbird
    malleefowl
    catalog
    finch
    raven
    postgres-pavics
)

echo 'Waiting for postgres database connection'
while ! pg_isready -h postgres -U ${POSTGRES_USER}; do sleep 1; done;

databases=$(psql -h postgres -U ${POSTGRES_USER} -d ${POSTGRES_DB} -t -c 'SELECT datname FROM pg_database WHERE datistemplate = false;')

for db_to_create in ${databases_to_create[*]}
do
    exists=false
    for db in $databases
    do
        if [ "$db_to_create" == "$db" ] ; then
            exists=true
            break
        fi
    done

    if [ $exists == false ] ; then
        echo "Creating database $db_to_create"
        psql -h postgres -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "CREATE DATABASE $db_to_create;"
    fi

done
