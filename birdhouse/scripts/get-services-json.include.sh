#!/bin/sh

# default value in case of error or missing definitions
export BIRDHOUSE_DEPLOY_SERVICES_JSON='{}'
if [ -z "${ALL_CONF_DIRS}" ]; then
  echo "No services in DEFAULT_CONF_DIRS and EXTRA_CONF_DIRS. SERVICES JSON list will be empty!"
  return
fi

for adir in $(echo "$ALL_CONF_DIRS" | grep -v " ./core\| ./data"); do
  [ -f "${adir}/service-config.json" ] || continue
  SERVICES="${SERVICES}$([ -n "${SERVICES}" ] && echo ',') $(cat "${adir}/service-config.json")"
done

export BIRDHOUSE_DEPLOY_SERVICES_JSON="{\"services\": [${SERVICES}]}"
