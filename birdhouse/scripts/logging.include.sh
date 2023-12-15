#!/bin/sh

BIRDHOUSE_COLOR=${BIRDHOUSE_COLOR:-1}
if [ "${BIRDHOUSE_COLOR}" -eq "1" ]; then
    BLUE=$(tput setaf 12)
    GRAY=$(tput setaf 8)
    CYAN=$(tput setaf 6)
    PURPLE=$(tput setaf 5)
    YELLOW=$(tput setaf 3)
    GREEN=$(tput setaf 2)
    RED=$(tput setaf 1)
    NORMAL=$(tput sgr0)
fi

export MSG_DEBUG="${GRAY}DEBUG${NORMAL}:    "
export MSG_INFO="${BLUE}INFO${NORMAL}:     "
export MSG_WARN="${YELLOW}WARNING${NORMAL}:  "
export MSG_ERROR="${RED}ERROR${NORMAL}:    "
