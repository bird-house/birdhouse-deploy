#!/bin/sh

# default value in case of error or missing definitions
export BIRDHOUSE_DEPLOY_SERVICES_JSON='{"components": []}'
if [ -z "${ALL_CONF_DIRS}" ]; then
  echo "No services in DEFAULT_CONF_DIRS and EXTRA_CONF_DIRS. Components JSON list will be empty!"
  return
fi

for adir in $(echo "$ALL_CONF_DIRS" | grep -v " ./core\| ./data"); do
  [ -f "${adir}/docker-compose-extra.yml" ] || continue
  SERVICES="${SERVICES}, \"$(basename adir)\": \"/$(basename adir)\""
done

export BIRDHOUSE_DEPLOY_SERVICES_JSON="{\"components\": [${SERVICES}]}"
