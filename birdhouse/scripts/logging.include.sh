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


# Usage: log {LEVEL} "{message}" [...]
# Any amount of messages can be passed to the function.
log() {
    if [ "${BIRDHOUSE_LOG_LEVEL}" != DEBUG ] \
    && [ "${BIRDHOUSE_LOG_LEVEL}" != INFO ] \
    && [ "${BIRDHOUSE_LOG_LEVEL}" != WARN ] \
    && [ "${BIRDHOUSE_LOG_LEVEL}" != ERROR ]; then
        echo "${LOG_CRITICAL}Invalid log level setting: [BIRDHOUSE_LOG_LEVEL=${BIRDHOUSE_LOG_LEVEL}]."
        exit 2
    fi
    level="$1"
    shift
    if [ "$*" = "" ]; then
        echo "${LOG_CRITICAL}Invalid log message is missing."
        exit 2
    fi
    if [ "${level}" = "DEBUG" ]; then
        if [ "${BIRDHOUSE_LOG_LEVEL}" = DEBUG ]; then
            echo "${LOG_DEBUG}$*"
        fi
    elif [ "${level}" = "INFO" ]; then
        if [ "${BIRDHOUSE_LOG_LEVEL}" = DEBUG ] \
        || [ "${BIRDHOUSE_LOG_LEVEL}" = INFO ]; then
            echo "${LOG_INFO}$*"
        fi
    elif [ "${level}" = "WARN" ]; then
        if [ "${BIRDHOUSE_LOG_LEVEL}" = DEBUG ] \
        || [ "${BIRDHOUSE_LOG_LEVEL}" = INFO ] \
        || [ "${BIRDHOUSE_LOG_LEVEL}" = WARN ]; then
            echo "${LOG_WARN}$*"
        fi
    elif [ "${level}" = "ERROR" ]; then
        echo "${LOG_ERROR}$*"
    else
        echo "${LOG_CRITICAL}Invalid log level: [${level}]"
        exit 2
    fi
}
