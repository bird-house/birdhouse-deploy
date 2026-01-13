#!/bin/sh

# default value in case of error or missing definitions

for adir in ${ALL_CONF_DIRS}; do
  [ -f "${adir}/service-config.json" ] || continue
  # remove the leading/trailing [] to get a pseudo-json of nested objects to extend the list
  SERVICE_CONF="$(cat "${adir}/service-config.json" | tr '\n' ' ' | sed 's/^\s*\[\s*//;s/\s*\]\s*$//')"
  SERVICES="${SERVICES}$([ -n "${SERVICES}" ] && echo ',' || echo '') ${SERVICE_CONF}"
done

if [ -z "${SERVICES}" ]; then
  log WARN "No services in BIRDHOUSE_DEFAULT_CONF_DIRS and BIRDHOUSE_EXTRA_CONF_DIRS. SERVICES JSON list will be empty!"
fi
export BIRDHOUSE_DEPLOY_SERVICES_JSON="{\"services\": [${SERVICES}]}"
