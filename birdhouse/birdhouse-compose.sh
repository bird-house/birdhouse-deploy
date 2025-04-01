#!/bin/sh

# NOTE, this file and all the extra component pre/post scripts that it executes
# is used by the autodeploy mechanism inside a very minimalistic container,
# therefore:
#
# * When making change to this file or any extra component pre/post scripts,
#   should also test that it does not break the autodeploy.
#
# * Try to keep the same behavior/code, inside and outside of the
#   autodeploy container to catch error early with the autodeploy.

# list of all variables to be substituted in templates
#   some of these variables *could* employ provided values in 'default.env',
#   but they must ultimately be defined one way or another for the server to work
VARS='
  $BIRDHOUSE_COMPOSE
  $BIRDHOUSE_FQDN
  $BIRDHOUSE_DOC_URL
  $BIRDHOUSE_SUPPORT_EMAIL
  $BIRDHOUSE_DATA_PERSIST_ROOT
  $BIRDHOUSE_DATA_PERSIST_SHARED_ROOT
  $BIRDHOUSE_LOCAL_ENV
  $BIRDHOUSE_LOG_DIR
  $COMPOSE_DIR
  $COMPOSE_PROJECT_NAME
'

# list of vars to be substituted in template but they do not have to be set in env.local
#   their default values are from 'default.env', so they do not have to be defined in 'env.local' if values are adequate
#   they usually are intended to provide additional features or extended customization of their behavior
#   when the value provided explicitly, it will be used instead of guessing it by inferred values from other variables
OPTIONAL_VARS='
  $BIRDHOUSE_FQDN_PUBLIC
  $BIRDHOUSE_SSL_CERTIFICATE
  $BIRDHOUSE_EXTRA_PYWPS_CONFIG
  $BIRDHOUSE_NAME
  $BIRDHOUSE_DESCRIPTION
  $BIRDHOUSE_INSTITUTION
  $BIRDHOUSE_SUBJECT
  $BIRDHOUSE_TAGS
  $BIRDHOUSE_DOCUMENTATION_URL
  $BIRDHOUSE_RELEASE_NOTES_URL
  $BIRDHOUSE_SUPPORT_URL
  $BIRDHOUSE_LICENSE_URL
  $BASH_IMAGE
'

THIS_FILE="$(readlink -f "$0" || realpath "$0")"
THIS_DIR="$(dirname "${THIS_FILE}")"

export BIRDHOUSE_COMPOSE="${BIRDHOUSE_COMPOSE:-"${THIS_FILE}"}"

# we switch to the real directory of the script, so it still works when used from $PATH
# tip: ln -s /path/to/birdhouse-compose.sh ~/bin/
# Setup PWD for sourcing env.local.
cd "${THIS_DIR}" || exit 1

# Setup COMPOSE_DIR for sourcing env.local.
# Prevent un-expected difference when this script is run inside autodeploy
# container and manually from the host.
COMPOSE_DIR="$(pwd)"

. "${COMPOSE_DIR}/read-configs.include.sh"
read_configs # this sets ALL_CONF_DIRS

. "${COMPOSE_DIR}/scripts/get-components-json.include.sh"
. "${COMPOSE_DIR}/scripts/get-services-json.include.sh"
. "${COMPOSE_DIR}/scripts/get-version-json.include.sh"

check_required_vars || exit $?

# we apply all the templates
if [ x"$1" = x"up" ] || [ x"$1" = x"restart" ] || [ x"${BIRDHOUSE_COMPOSE_TEMPLATE_FORCE}" = x"true" ]; then
  log INFO "Updating template files found across 'BIRDHOUSE_EXTRA_CONF_DIRS' (enabled and default components)."
  find ${ALL_CONF_DIRS} -name '*.template' 2>/dev/null |
  while read FILE
  do
    DEST=${FILE%.template}
    if [ -d "${DEST}" ]; then
      # purposely using 'rmdir' to get an error if the contents are not empty
      # this is only to handle docker-compose early generation of volume mounts
      log WARN "Removing invalid directory for template file [${DEST}]"
      if ! rmdir "${DEST}" 2>/dev/null; then
        log ERROR "Cannot remove non-empty directory [${DEST}]." \
                  "This directory should not exist as it conflicts with destination of [${FILE}]." \
                  "Please remove it and try starting up the birdhouse stack again."
        exit 1
      fi
    fi
    cat "${FILE}" | envsubst "$VARS" | envsubst "$OPTIONAL_VARS" > "${DEST}"
  done
  [ "$?" -eq 1 ] && exit 1  # re-raise the subshell error of the while loop
else
  log DEBUG "Skipping template files update (\"$1\" not \"up\", \"restart\", or forced by BIRDHOUSE_COMPOSE_TEMPLATE_FORCE)"
fi

SHELL_EXEC_FLAGS=
if [ "${BIRDHOUSE_LOG_LEVEL}" = "DEBUG" ]; then
  SHELL_EXEC_FLAGS=-x
fi

create_compose_conf_list # this sets COMPOSE_CONF_LIST
log INFO "Displaying resolved compose configurations:"
log INFO "COMPOSE_CONF_LIST="
log INFO ${COMPOSE_CONF_LIST} | tr ' ' '\n' | grep -v '^-f'

if [ x"$1" = x"info" ]; then
  log INFO "Stopping before execution of docker-compose command."
  exit 0
fi

COMPOSE_EXTRA_OPTS=""
if [ x"$1" = x"up" ]; then
  COMPOSE_EXTRA_OPTS="${BIRDHOUSE_COMPOSE_UP_EXTRA_OPTS}"
fi

if [ x"$1" = x"up" ] || [ x"$1" = x"restart" ]; then
  for adir in $ALL_CONF_DIRS; do
    COMPONENT_PRE_COMPOSE_UP="$adir/pre-docker-compose-up"
    if [ -x "$COMPONENT_PRE_COMPOSE_UP" ]; then
      log INFO "Executing '$COMPONENT_PRE_COMPOSE_UP'"
      sh ${SHELL_EXEC_FLAGS} "$COMPONENT_PRE_COMPOSE_UP"
    fi
    COMPONENT_PRE_COMPOSE_UP_INCLUDE="$adir/pre-docker-compose-up.include"
    if [ -f "$COMPONENT_PRE_COMPOSE_UP_INCLUDE" ]; then
      log INFO "Sourcing '$COMPONENT_PRE_COMPOSE_UP_INCLUDE'"
      . "$COMPONENT_PRE_COMPOSE_UP_INCLUDE"
    fi
  done
fi

log INFO "Executing docker-compose with extra options: $@ ${COMPOSE_EXTRA_OPTS}"
# the PROXY_HTTP_PORT is a little trick to make the compose file invalid without the usage of this wrapper script
PROXY_HTTP_PORT=80 HOSTNAME=${BIRDHOUSE_FQDN} ${DOCKER_COMPOSE} ${COMPOSE_CONF_LIST} "$@" ${COMPOSE_EXTRA_OPTS}
ERR=$?
if [ ${ERR} -gt 0 ]; then
  log ERROR "docker-compose error, exit code ${ERR}"
  exit ${ERR}
fi

# execute post-compose function if exists and no error occurred
type post-compose 2>&1 | grep 'post-compose is a function' > /dev/null
if [ $? -eq 0 ]
then
  [ ${ERR} -gt 0 ] && { log ERROR "Error occurred with docker-compose, not running post-compose"; exit $?; }
  post-compose "$@"
fi


while [ $# -gt 0 ]
do
  if [ x"$1" = x"up" ]; then
    # we restart the proxy after an up to make sure nginx continue to work if any container IP address changes
    PROXY_HTTP_PORT=80 HOSTNAME=${BIRDHOUSE_FQDN} ${DOCKER_COMPOSE} ${COMPOSE_CONF_LIST} restart proxy

    # run postgres post-startup setup script
    # Note: this must run before the post-docker-compose-up scripts since some may expect postgres databases to exist
    postgres_id=$(PROXY_HTTP_PORT=80 HOSTNAME=${BIRDHOUSE_FQDN} ${DOCKER_COMPOSE} ${COMPOSE_CONF_LIST} ps -q postgres 2> /dev/null)
    if [ ! -z "$postgres_id" ]; then
      docker exec ${postgres_id} /postgres-setup.sh
    fi

    for adir in $ALL_CONF_DIRS; do
      COMPONENT_POST_COMPOSE_UP="$adir/post-docker-compose-up"
      if [ -x "$COMPONENT_POST_COMPOSE_UP" ]; then
        log INFO "Executing '$COMPONENT_POST_COMPOSE_UP'"
        sh ${SHELL_EXEC_FLAGS} "$COMPONENT_POST_COMPOSE_UP"
      fi
    done

    # Note: This command should stay last, as it can take a while depending on network and drive speeds
    # immediately cache the new notebook images for faster startup by JupyterHub
    for IMAGE in ${JUPYTERHUB_DOCKER_NOTEBOOK_IMAGES}
    do
      docker pull $IMAGE
    done

  fi
  shift
done


# vi: tabstop=8 expandtab shiftwidth=2 softtabstop=2
