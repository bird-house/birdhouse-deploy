#!/bin/sh

# default value in case of error or missing definitions

for adir in ${ALL_CONF_DIRS}; do
  [ -f "${adir}/service-config.json" ] || continue
  SERVICES="${SERVICES}$([ -n "${SERVICES}" ] && echo ',') $(cat "${adir}/service-config.json")"
done

if [ -z "${SERVICES}" ]; then
  echo "${YELLOW}Warning: ${NORMAL}No services in DEFAULT_CONF_DIRS and EXTRA_CONF_DIRS. SERVICES JSON list will be empty!"
fi
export BIRDHOUSE_DEPLOY_SERVICES_JSON="{\"services\": [${SERVICES}]}"
