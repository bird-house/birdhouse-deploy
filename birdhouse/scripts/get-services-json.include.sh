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
  # merge whether config is an array or a single service
  if [ "$(echo "${SERVICE_CONF}" | head -n 1)" = "[" ]; then
    # remove the leading/trailing [] to get a pseudo-json to extend the list
    SERVICE_CONF="$(echo "${SERVICE_CONF}" | sed -z 's/^\s*\[\s*//;s/\s*\]\s*$//')"
    SERVICES="${SERVICES}$([ -n "${SERVICES}" ] && echo ',') ${SERVICE_CONF}"
  else
    SERVICES="${SERVICES}$([ -n "${SERVICES}" ] && echo ',') ${SERVICE_CONF}"
  fi
done

if [ -z "${SERVICES}" ]; then
  log WARN "No services in DEFAULT_CONF_DIRS and EXTRA_CONF_DIRS. SERVICES JSON list will be empty!"
fi
export BIRDHOUSE_DEPLOY_SERVICES_JSON="{\"services\": [${SERVICES}]}"
