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
#    "bird-house/birdhouse-deploy:components/cowbird"
#  ]
# }
#

# default value in case of error or missing definitions
export BIRDHOUSE_DEPLOY_COMPONENTS_JSON='{"components": []}'
if [ -z "${ALL_CONF_DIRS}" ]; then
  echo "No components in DEFAULT_CONF_DIRS and EXTRA_CONF_DIRS. Components JSON list will be empty!"
  return
fi

# resolve path considering if sourced or executed, and whether from current dir, pavics-compose include or another dir
BIRDHOUSE_DEPLOY_COMPONENTS_ROOT=$(dirname -- "$(realpath "$0")")
if [ "$(echo "${BIRDHOUSE_DEPLOY_COMPONENTS_ROOT}" | grep -cE "/birdhouse/?\$" 2>/dev/null)" -eq 1 ]; then
  BIRDHOUSE_DEPLOY_COMPONENTS_ROOT=.
else
  BIRDHOUSE_DEPLOY_COMPONENTS_ROOT="${BIRDHOUSE_DEPLOY_COMPONENTS_ROOT}/.."
fi
cd "${BIRDHOUSE_DEPLOY_COMPONENTS_ROOT}" || true  # ignore error for now, empty list expected of known components after

# note: no quotes in 'ls' on purpose to expand glob patterns
BIRDHOUSE_DEPLOY_COMPONENTS_LIST_KNOWN="$( \
  ls -d1 ./*components/*/ ./config/*/ 2>/dev/null \
  | sed -E "s|\./(.*)/|\1|" \
)"
if [ -z "${BIRDHOUSE_DEPLOY_COMPONENTS_LIST_KNOWN}" ]; then
  echo "[WARNING]" \
    "Could not resolve known birdhouse-deploy components." \
    "Aborting to avoid potentially leaking sensible details." \
    "Components will not be reported on the platform's JSON endpoint."
  return
fi
BIRDHOUSE_DEPLOY_COMPONENTS_LIST_ACTIVE=$( \
  echo "${ALL_CONF_DIRS}" \
  | sed '/^[[:space:]]*$/d' \
)

# create a JSON list using the specified components
# each component that starts by './' gets replaced with the below birdhouse prefix to provide contextual information
# other component locations are considered 'custom' and marked as such to provide contextual information
BIRDHOUSE_DEPLOY_COMPONENTS_BASE="bird-house/birdhouse-deploy:"
BIRDHOUSE_DEPLOY_COMPONENTS_LIST=$( \
  echo "${BIRDHOUSE_DEPLOY_COMPONENTS_LIST_ACTIVE}" \
  | grep "${BIRDHOUSE_DEPLOY_COMPONENTS_LIST_KNOWN}" \
  | sed -E 's|^\s*([A-Za-z0-0./_-]+)\s*$|"\1",|g' \
  | sed -E "s|^\"\./(.*)\"|\"${BIRDHOUSE_DEPLOY_COMPONENTS_BASE}\\1\"|g" \
  | sed '/^\n*$/d' \
)
BIRDHOUSE_DEPLOY_COMPONENTS_LIST="${BIRDHOUSE_DEPLOY_COMPONENTS_LIST%?}"  # remove last comma
export BIRDHOUSE_DEPLOY_COMPONENTS_JSON="{\"components\": [${BIRDHOUSE_DEPLOY_COMPONENTS_LIST}]}"
