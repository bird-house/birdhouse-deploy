# this is used to mock calls to birdhouse-compose.sh
THIS_FILE="$(readlink -f "$0" || realpath "$0")"
THIS_DIR="$(dirname "${THIS_FILE}")"

. "${THIS_DIR}/../../birdhouse/scripts/logging.include.sh"
log DEBUG test logging debug
log INFO test logging info
log WARN test logging warn
log ERROR test logging error
log invalid-level test invalid level
