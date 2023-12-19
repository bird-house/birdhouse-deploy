#!/bin/bash

THIS_FILE="$(readlink -f "$0" || realpath "$0")"
THIS_DIR="$(dirname "$THIS_FILE")"

if [ -f "${THIS_DIR}/logging.include.sh" ]; then
    . "${THIS_DIR}/logging.include.sh"
fi

function usage(){
  cat <<EOF
Usage $0 <name of the WPS service|list|all> <operation>
Where operation in:
  count: show the count of "running" jobs, as implemented in pywps.dblog:get_running()
  clean: clear all getcapabilities and describeprocess from the pywps_requests table
  vacuum: perform vacuum on the database file
  select: show the content of pywps_requests table
  zap: completely destroy the content of pywps_requests and pywps_stored_requests tables (DANGER!)
  shell: run interactive sqlite3 shell
EOF
  exit 1
}

if [[ $1 == "list" ]]
then
  docker run -i --rm -v birdhouse_data:/data  birdhouse/bird-base ls /data/pywps/db
  exit
fi

if [[ -z $1 || -z $2 ]]
then
  usage
fi

if [[ $1 == "all" ]]
then
  for db in $(docker run -i --rm -v birdhouse_data:/data  birdhouse/bird-base ls /data/pywps/db)
  do
    echo -n "$db: "
    $0 $db $2
  done
  
  exit
fi


DB=/data/pywps/db/$1/sqlite_log.db

case $2 in
  count)
    SQL="select count(*) from pywps_requests where percent_done > -1 and percent_done < 100.0;"
    ;;
  select)
    SQL="select * from pywps_requests;"
    ;;
  clean)
    SQL="delete from pywps_requests where operation in ('getcapabilities', 'describeprocess');"
    ;;
  vacuum)
    SQL="vacuum;"
    ;;
  zap)
    SQL="delete from pywps_requests; delete from pywps_stored_requests;"
    ;;
  shell)
    docker run -ti --rm -v birdhouse_data:/data  birdhouse/bird-base sqlite3 $DB
    ;;
  *)
    echo "${MSG_ERROR}unknown operation: $2"
    usage
    ;;
esac


docker run -i --rm -v birdhouse_data:/data  birdhouse/bird-base bash <<EOF

if [[ ! -f $DB ]]
then
  echo "Error, database $DB doesn't exists, please check the service name"
  exit 1
fi

sqlite3 $DB "$SQL"


EOF
