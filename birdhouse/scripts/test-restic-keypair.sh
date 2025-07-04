#!/usr/bin/env sh

THIS_FILE="$(readlink -f "$0" || realpath "$0")"
THIS_DIR="$(dirname "${THIS_FILE}")"
BIRDHOUSE_EXE="${THIS_DIR}/../../bin/birdhouse"

eval $("${BIRDHOUSE_EXE}" configs -dp)

RESTIC_REPOSITORY="$(env -i sh -ac ". $BIRDHOUSE_BACKUP_RESTIC_ENV_FILE && echo \$RESTIC_REPOSITORY")"
REPOSITORY_HOST_PATH="${RESTIC_REPOSITORY#"sftp:"}"
REPOSITORY_HOST="${REPOSITORY_HOST_PATH%:*}"

if [ "${REPOSITORY_HOST_PATH}" = "$RESTIC_REPOSITORY" ]; then
  log WARNING "The restic repository at '${RESTIC_REPOSITORY}' is not accessed using the SFTP protocol."
  log WARNING "A keypair is not necessary to access this repository and it cannot be accessed over SSH."
fi

log INFO "Testing keypair located in '${BIRDHOUSE_BACKUP_SSH_KEY_DIR}' to SSH to the remote host at '${REPOSITORY_HOST}'"
log INFO "If this test is successful you will be logged in to the remote host without the need to enter a passphrase or password."
BIRDHOUSE_BACKUP_RESTIC_EXTRA_DOCKER_OPTIONS='--entrypoint=sh -it' "${BIRDHOUSE_EXE}" --log-level ERROR backup restic -c \"ssh ${REPOSITORY_HOST} \|\| true\"
