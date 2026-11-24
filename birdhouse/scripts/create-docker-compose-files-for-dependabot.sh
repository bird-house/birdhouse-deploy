#!/usr/bin/env sh

# Generates docker compose files for each component containing only service names and images
# These files can then be monitored and updated by dependabot (through GitHub) in order to keep
# docker dependencies up to date.

THIS_FILE="$(readlink -f "$0" || realpath "$0")"
THIS_DIR="$(dirname "${THIS_FILE}")"
COMPOSE_DIR="${THIS_DIR}/../"
BIRDHOUSE_EXE="${COMPOSE_DIR}/../bin/birdhouse"

OUTPUT_DIR="${OUTPUT_DIR:-"${COMPOSE_DIR}/../.dependabot/"}"
OUTPUT_FILE="${OUTPUT_FILE:-"${OUTPUT_DIR}/docker-compose.yml"}"

cd "${COMPOSE_DIR}"

. scripts/dependabot-scripts.include.sh

export BIRDHOUSE_EXTRA_CONF_DIRS="$(find ./components/ ./optional-components/ -maxdepth 1 -mindepth 1 -type d | grep -v "${EXCLUDE_COMPONENTS_RE}")"
export PROXY_HTTP_PORT=80 # this is required or else `birdhouse compose config` will raise an error

# load environment variables but skip any local environment overrides because we only
# care about the default docker image definitions
eval $("${BIRDHOUSE_EXE}" --quiet -e /dev/null configs --print-config-command)
eval $("${BIRDHOUSE_EXE}" -e /dev/null configs --print-log-command)

echo "services:" > "${OUTPUT_FILE}"
log INFO "Writing compose files to: ${OUTPUT_DIR}"
for conf_dir in ${BIRDHOUSE_EXTRA_CONF_DIRS}; do
    if [ -f "${conf_dir}/docker-compose-extra.yml" ]; then
        content="$(${DOCKER_COMPOSE} -f ./docker-compose.yml -f "${conf_dir}/docker-compose-extra.yml" config --no-consistency --lock-image-digests | sed 's/.*{}.*//' | sed 's/@sha.*$//')"
        if [ -n "$(echo "${content}" | tail -n+2 | tr -d '[:space:]')" ]; then
            log INFO "Writing compose file for component: $(basename "${conf_dir}")"
            echo "${content}" | grep -v '^services:' | sed "s|\(^\s*image:.*\)|\1  # ${conf_dir}|" >> ${OUTPUT_FILE}
        fi
    fi
done
