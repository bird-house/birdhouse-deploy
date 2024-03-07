#!/bin/sh

THIS_FILE="$(readlink -f "$0" || realpath "$0")"
THIS_DIR="$(dirname "${THIS_FILE}")"

export BIRDHOUSE_COMPOSE="${BIRDHOUSE_COMPOSE:-"${THIS_FILE}"}"
export BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED=${BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED:-True}

"${THIS_DIR}/birdhouse-compose.sh" "$@"
