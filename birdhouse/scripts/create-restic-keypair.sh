#!/usr/bin/env sh

THIS_FILE="$(readlink -f "$0" || realpath "$0")"
THIS_DIR="$(dirname "${THIS_FILE}")"
BIRDHOUSE_EXE="${THIS_DIR}/../../bin/birdhouse"

eval $("${BIRDHOUSE_EXE}" configs -dp)

RESTIC_REPOSITORY="$(env -i sh -ac ". $BIRDHOUSE_BACKUP_RESTIC_ENV_FILE && echo \$RESTIC_REPOSITORY")"
REPOSITORY_HOST_PATH="${RESTIC_REPOSITORY#"sftp:"}"
REPOSITORY_HOST="${REPOSITORY_HOST_PATH%:*}"

USAGE="USAGE: $(basename "$THIS_FILE") {test | create [ssh-keygen-args ...]}"

HELP="$USAGE

Commands:

  create      Create a new keypair. Any additional arguments will be passed to the ssh-keygen command used to create the keypair. 
  test        Test that you can successfully log in to the remote server at '$REPOSITORY_HOST' (specified by the 
              RESTIC_REPOSITORY variable in '$BIRDHOUSE_BACKUP_RESTIC_ENV_FILE').

Warning:
  Do NOT create a passphrase for the SSH key since this must be able to be run without user input.

"

test_repo_type() {
  if [ "${REPOSITORY_HOST_PATH}" = "$RESTIC_REPOSITORY" ]; then
    log ERROR "The restic repository at '${RESTIC_REPOSITORY}' is not accessed using the SFTP protocol."
    log ERROR "A keypair is not necessary to access this repository and it cannot be accessed over SSH."
    expect_exit 1
  fi
}

case "$1" in 
  test)
    log INFO "Testing keypair located in '${BIRDHOUSE_BACKUP_SSH_KEY_DIR}' to SSH to the remote host at '${REPOSITORY_HOST}'"
    log INFO "If this test is successful you will be logged in to the remote host."
    BIRDHOUSE_BACKUP_RESTIC_EXTRA_DOCKER_OPTIONS='--entrypoint=sh -it' "${BIRDHOUSE_EXE}" backup restic -c \"ssh ${REPOSITORY_HOST}\" || expect_exit 0
    ;;
  create)
    log INFO "Creating a keypair in the directory '${BIRDHOUSE_BACKUP_SSH_KEY_DIR}'."
    BIRDHOUSE_BACKUP_RESTIC_EXTRA_DOCKER_OPTIONS='--entrypoint=sh -it' "${BIRDHOUSE_EXE}" backup restic -c ssh-keygen "$@"
    log INFO "After this key is created you should add the generated public key to the authorized_keys file for the user on '${REPOSITORY_HOST}'"
    log INFO "To test if the public key has been successfully added run this script again with the 'test' command."
    ;;
  -h|--help)
    echo "$HELP"
    ;;
  *)
    >&2 echo "$USAGE"
    expect_exit 1
esac
