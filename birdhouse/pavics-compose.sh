#!/bin/sh

THIS_FILE="$(readlink -f "$0" || realpath "$0")"
THIS_DIR="$(dirname "${THIS_FILE}")"

BIRDHOUSE_ALLOW_BACKWARDS_COMPATIBLE=True

. "${THIS_DIR}/birdhouse-compose.sh"
