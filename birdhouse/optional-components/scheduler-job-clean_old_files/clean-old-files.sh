#!/bin/sh

################################################################
# Example call to delete all files in /tmp last modified longer
# than 20 days ago
#
# $ sh clean-old-files.sh 20 mtime /tmp
##################################################################

AGE="$1"
MODE="$2"
LOCATION="$3"

ACCEPTABLE_MODES='|mmin|mtime|ctime|atime|'

if ! echo "$AGE" | grep -q '^[0-9][0-9]*$'; then
    >&2 echo "AGE argument set to '${AGE}'. It must be an unsigned integer"
    exit 1
fi

if [ "${ACCEPTABLE_MODES#*"|${MODE}|"}" = "${ACCEPTABLE_MODES}" ]; then
    >&2 echo "MODE argument set to '${MODE}'. It must be one of 'mmin', 'mtime', 'ctime', or 'atime'"
    exit 1
fi

if [ -z "${LOCATION}" ]; then
    >&2 echo "LOCATION argument is blank or unset. It must refer to a path on disk."
    exit 1
fi

echo "[$(date)] Removing files in ${LOCATION} that have a ${MODE} value greater than ${AGE} days"
find "${LOCATION}" -type f "-${MODE}" +"${AGE}" -print -delete
find "${LOCATION}" -type d "-${MODE}" +"${AGE}" -print -empty -delete
