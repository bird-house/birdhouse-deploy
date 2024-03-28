#!/bin/sh

THIS_FILE="$(readlink -f "$0" || realpath "$0")"
THIS_DIR="$(dirname "${THIS_FILE}")"

export BIRDHOUSE_COMPOSE="${BIRDHOUSE_COMPOSE:-"${THIS_FILE}"}"

"${THIS_DIR}/birdhouse-compose.sh" "$@"
