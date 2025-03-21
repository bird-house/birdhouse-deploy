#!/bin/sh

THIS_FILE="$(readlink -f "$0" || realpath "$0")"
THIS_DIR="$(dirname "${THIS_FILE}")"
COMPOSE_DIR="${COMPOSE_DIR:-$(dirname "${THIS_DIR}")}"

if [ -f "${COMPOSE_DIR}/read-configs.include.sh" ]; then
    . "${COMPOSE_DIR}/read-configs.include.sh"
fi

# default value in case of error or missing definitions

for adir in ${ALL_CONF_DIRS}; do
  [ -f "${adir}/service-config.json" ] || continue
  # read and strip leading/trailing whitespaces
  SERVICE_CONF="$(cat "${adir}/service-config.json" | sed -z 's/^\s*//;s/\s*$//')"
  # remove the leading/trailing [] to get a pseudo-json of nested objects to extend the list
  SERVICE_CONF="$(echo "${SERVICE_CONF}" | sed -z 's/^\s*\[\s*//;s/\s*\]\s*$//')"
  SERVICES="${SERVICES}$([ -n "${SERVICES}" ] && echo ',' || echo '') ${SERVICE_CONF}"
done

if [ -z "${SERVICES}" ]; then
  log WARN "No services in BIRDHOUSE_DEFAULT_CONF_DIRS and BIRDHOUSE_EXTRA_CONF_DIRS. SERVICES JSON list will be empty!"
fi
export BIRDHOUSE_DEPLOY_SERVICES_JSON="{\"services\": [${SERVICES}]}"
