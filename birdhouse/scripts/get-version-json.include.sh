#!/bin/sh

# get the current version of this deployment
RELEASE_FILE="$(dirname "${COMPOSE_DIR}")/RELEASE.txt"

if [ -f "${RELEASE_FILE}" ]; then
  BIRDHOUSE_VERSION="$(head -1 "$RELEASE_FILE" | cut -d" " -f 1)"
  BIRDHOUSE_RELEASE_TIME="$(head -1 "$RELEASE_FILE" | cut -d" " -f 2)"
  BIRDHOUSE_VERSION_JSON="{\"version\": \"${BIRDHOUSE_VERSION}\", \"release_time\": \"${BIRDHOUSE_RELEASE_TIME}\"}"
  export BIRDHOUSE_VERSION_JSON
fi
