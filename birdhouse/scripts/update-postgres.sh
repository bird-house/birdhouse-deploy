#!/usr/bin/env sh

# This script updates all postgres databases that are used by components in this repository.
# This includes magpie and all WPS birds that use the postgres component.
# This does not include test component like optional-components/generic_bird and will not update
# custom components (ones not from this repository).
#
# It will update postgres databases to the version specified by the POSTGRES_VERSION_UPDATE
# environment variable.
# All of the old database files will be copied to a temporary directory in case you want to inspect
# them or revert this operation later on. To specify which directory to write these backups to 
# set the DATA_BACKUP_DIR variable (default: ${TMPDIR:-/tmp}/birdhouse-postgres-migrate-backup/)
# Note that backups in the form of database dumps will also be written to the named volume or directory
# specified by the BIRDHOUSE_BACKUP_VOLUME variable.
# 
# For example, to update the current postgres databases to version 18.1 and write backups to /tmp/test/
# 
# $ POSTGRES_VERSION_UPDATE=18.1 DATA_BACKUP_DIR=/tmp/test/ ./update-postgresh.sh

THIS_FILE="$(readlink -f "$0" || realpath "$0")"
THIS_DIR="$(dirname "${THIS_FILE}")"
BIRDHOUSE_EXE="${THIS_DIR}/../../bin/birdhouse"

eval $(${BIRDHOUSE_EXE} configs --print-log-command)

: ${POSTGRES_VERSION_UPDATE:?"$(log ERROR "POSTGRES_VERSION_UPDATE must be set")"}

DATA_BACKUP_DIR="${DATA_BACKUP_DIR:-"${TMPDIR:-/tmp}"/birdhouse-postgres-migrate-backup/}"
POSTGRES_COMPONENTS="-a magpie -a $(birdhouse -q configs -c 'echo $POSTGRES_DATABASES_TO_CREATE' | sed 's/ / -a /g')"

log INFO "Migrating postgres databases to version ${POSTGRES_VERSION_UPDATE}"

log INFO "Starting the birdhouse stack in order to backup existing databases."
${BIRDHOUSE_EXE} compose up -d

log INFO "Backing up postgres databases from the following components: $(echo "${POSTGRES_COMPONENTS}" | sed 's/[[:space:]]*-a[[:space:]]*/ /g')"
${BIRDHOUSE_EXE} backup create --no-restic ${POSTGRES_COMPONENTS}

log INFO "Stopping the birdhouse stack in order to update postgres version"
${BIRDHOUSE_EXE} compose down

log INFO "Backing up all postgres data to ${DATA_BACKUP_DIR}."
eval "$(${BIRDHOUSE_EXE} -q configs -c 'echo "MAGPIE_PERSIST_DIR=$MAGPIE_PERSIST_DIR; POSTGRES_DATA_DIR=$POSTGRES_DATA_DIR"')"

mkdir -p ${DATA_BACKUP_DIR}
mv "${MAGPIE_PERSIST_DIR}" "${DATA_BACKUP_DIR}"
mv "${POSTGRES_DATA_DIR}" "${DATA_BACKUP_DIR}"

MAGPIE_POSTGRES_VERSION=${POSTGRES_VERSION_UPDATE} POSTGRES_VERSION=${POSTGRES_VERSION_UPDATE} ${BIRDHOUSE_EXE} compose up -d

${BIRDHOUSE_EXE} backup restore --no-restic ${POSTGRES_COMPONENTS}

log INFO "Migration is now complete. Please ensure that the data has been upgraded properly.
If you are satisfied that the databases have been updated properly please add the following to your local environment file:

export MAGPIE_POSTGRES_VERSION=${POSTGRES_VERSION_UPDATE} 
export POSTGRES_VERSION=${POSTGRES_VERSION_UPDATE}

If you are not satified that the databases have been updated properly and you wish to revert these changes, you can do so by running:

${BIRDHOUSE_EXE} compose down
rm -r "${MAGPIE_PERSIST_DIR}"
rm -r "${POSTGRES_DATA_DIR}"
mv "${DATA_BACKUP_DIR}/$(basename "${MAGPIE_PERSIST_DIR}")" "${MAGPIE_PERSIST_DIR}" 
mv "${DATA_BACKUP_DIR}/$(basename "${POSTGRES_DATA_DIR}")" "${POSTGRES_DATA_DIR}" 
${BIRDHOUSE_EXE} compose up -d
"
