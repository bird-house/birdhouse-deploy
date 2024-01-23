#!/bin/sh

THIS_FILE="$(readlink -f "$0" || realpath "$0")"
THIS_DIR="$(dirname "$THIS_FILE")"

if [ -f "${THIS_DIR}/read-configs.include.sh" ]; then
    . "${THIS_DIR}/read-configs.include.sh"
fi

# default value in case of error or missing definitions

for adir in ${ALL_CONF_DIRS}; do
  [ -f "${adir}/service-config.json" ] || continue
  SERVICES="${SERVICES}$([ -n "${SERVICES}" ] && echo ',') $(cat "${adir}/service-config.json")"
done

if [ -z "${SERVICES}" ]; then
  log WARN "No services in DEFAULT_CONF_DIRS and EXTRA_CONF_DIRS. SERVICES JSON list will be empty!"
fi
export BIRDHOUSE_DEPLOY_SERVICES_JSON="{\"services\": [${SERVICES}]}"
