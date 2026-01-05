#!/bin/sh
# Obtain a JSON representation of components enabled on this platform.
#
# Expected result should be similar to:
# {
#  "components": [
#    "bird-house/birdhouse-deploy:components/monitoring",
#    "bird-house/birdhouse-deploy:optional-components/canarie-api-full-monitoring",
#    "bird-house/birdhouse-deploy:optional-components/all-public-access",
#    "bird-house/birdhouse-deploy:optional-components/wps-healthchecks",
#    "bird-house/birdhouse-deploy:optional-components/secure-thredds",
#    "bird-house/birdhouse-deploy:optional-components/testthredds",
#    "bird-house/birdhouse-deploy:optional-components/test-weaver",
#    "bird-house/birdhouse-deploy:components/weaver",
#    "bird-house/birdhouse-deploy:components/cowbird",
#    "custom:component-from-another-repo"
#  ]
# }
#

for adir in ${ALL_CONF_DIRS}; do
  [ -d "${adir}" ] || continue
  real_adir="$(readlink -f "${adir}" || realpath "${adir}")"
  if [ "${real_adir}" = "${real_adir#${COMPOSE_DIR%/}/*components/}" ]; then
    # component is not in one of the *components directories in COMPOSE_DIR (not custom)
    component="custom:$(basename ${adir})"
  else
    # component is in one of the *components directories in COMPOSE_DIR (not custom)
    component="bird-house/birdhouse-deploy:${real_adir#${COMPOSE_DIR%/}/}"
  fi
  BIRDHOUSE_DEPLOY_COMPONENTS_LIST="${BIRDHOUSE_DEPLOY_COMPONENTS_LIST}\"${component}\","
done
export BIRDHOUSE_DEPLOY_COMPONENTS_JSON="{\"components\": [${BIRDHOUSE_DEPLOY_COMPONENTS_LIST%,}]}"
