#!/bin/sh

# get the current version of this deployment
RELEASE_FILE="$(dirname "${COMPOSE_DIR}")/RELEASE.txt"

if [ -f "${RELEASE_FILE}" ]; then
  BIRDHOUSE_VERSION="$(head -1 "$RELEASE_FILE" | cut -d" " -f 1)"
  export BIRDHOUSE_VERSION
fi
