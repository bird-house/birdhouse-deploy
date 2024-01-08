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
    REG_BG_BOLD="$(tput sgr0)$(tput setab 1)$(tput bold)"
    NORMAL=$(tput sgr0)
fi

BIRDHOUSE_LOG_LEVEL=${BIRDHOUSE_LOG_LEVEL:-INFO}
export LOG_DEBUG="${GRAY}DEBUG${NORMAL}:    "
export LOG_INFO="${BLUE}INFO${NORMAL}:     "
export LOG_WARN="${YELLOW}WARNING${NORMAL}:  "
export LOG_ERROR="${RED}ERROR${NORMAL}:    "
export LOG_CRITICAL="${REG_BG_BOLD}CRITICAL${NORMAL}: "  # to report misuse of functions

# Usage: log {LEVEL} "{message}"
log() {
    if [ "${BIRDHOUSE_LOG_LEVEL}" != DEBUG ] \
    && [ "${BIRDHOUSE_LOG_LEVEL}" != INFO ] \
    && [ "${BIRDHOUSE_LOG_LEVEL}" != WARN ] \
    && [ "${BIRDHOUSE_LOG_LEVEL}" != ERROR ]; then
        echo "${LOG_CRITICAL}Invalid log level setting: [BIRDHOUSE_LOG_LEVEL=${BIRDHOUSE_LOG_LEVEL}]."
        exit 2
    fi
    if [ "$2" = "" ]; then
        echo "${LOG_CRITICAL}Invalid log message is missing."
        exit 2
    fi
    if [ "$1" = "DEBUG" ]; then
        if [ "${BIRDHOUSE_LOG_LEVEL}" = DEBUG ]; then
            echo "${LOG_DEBUG}$2"
        fi
    elif [ "$1" = "INFO" ]; then
        if [ "${BIRDHOUSE_LOG_LEVEL}" = DEBUG ] \
        || [ "${BIRDHOUSE_LOG_LEVEL}" = INFO ]; then
            echo "${LOG_INFO}$2"
        fi
    elif [ "$1" = "WARN" ]; then
        if [ "${BIRDHOUSE_LOG_LEVEL}" = DEBUG ] \
        || [ "${BIRDHOUSE_LOG_LEVEL}" = INFO ] \
        || [ "${BIRDHOUSE_LOG_LEVEL}" = WARN ]; then
            echo "${LOG_WARN}$2"
        fi
    elif [ "$1" = "ERROR" ]; then
        echo "${LOG_ERROR}$2"
    else
        echo "${LOG_CRITICAL}Invalid log level: [$1]"
        exit 2
    fi
}
