#!/bin/sh

# support NO_COLOR flag (https://no-color.org/)
if [ -z "${BIRDHOUSE_COLOR}" ] && [ -z "${NO_COLOR}" ]; then
    BIRDHOUSE_COLOR=1
fi 

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
BIRDHOUSE_LOG_FD=${BIRDHOUSE_LOG_FD:-2}
if [ "${BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED}" = 'True' ] || [ "${__BIRDHOUSE_SUPPORTED_INTERFACE}" != 'True' ]; then
    # logs were previously written to stdout for DEBUG and INFO
    # logs were previously intended to be written to stderr for WARN, ERROR, and CRITICAL
    # (this supports backwards compatible scripts that don't use the interface)
    BIRDHOUSE_LOG_DEST_OVERRIDE=${BIRDHOUSE_LOG_DEST_OVERRIDE:-"DEBUG:fd:1:INFO:fd:1:WARN:fd:2:ERROR:fd:2:CRITICAL:fd:2"}
fi
export LOG_DEBUG="${GRAY}DEBUG${NORMAL}:    "
export LOG_INFO="${BLUE}INFO${NORMAL}:     "
export LOG_WARN="${YELLOW}WARNING${NORMAL}:  "
export LOG_ERROR="${RED}ERROR${NORMAL}:    "
export LOG_CRITICAL="${REG_BG_BOLD}CRITICAL${NORMAL}: "  # to report misuse of functions


# Determines where to send log messages:
# - to the file descriptor set by BIRDHOUSE_LOG_FD, or if there is a "fd" option in BIRDHOUSE_LOG_DEST_OVERRIDE for the given log level
# - to the file set by BIRDHOUSE_LOG_FILE, or if there is a "file" option in BIRDHOUSE_LOG_DEST_OVERRIDE for the given log level
# - suppresses writing to a file descriptor if BIRDHOUSE_LOG_QUIET is "True" or if there is a "quiet" option in BIRDHOUSE_LOG_DEST_OVERRIDE for the given log level
#
# The BIRDHOUSE_LOG_DEST_OVERRIDE contains a ':' delimited string that determines how to override the log destination for specific log levels.
# BIRDHOUSE_LOG_DEST_OVERRIDE sections contain '<log-level>:<option>:<argument>', this can be repeated multiple times to allow for different settings for different
# log levels. Accepted values:
# - <log-level>: one of: DEBUG, INFO, WARN, ERROR, CRITICAL
# - <option>: one of: fd, file, quiet
# - <argument>: if the option is fd, this must be a valid file descriptor; if the option is file, this is the path to a log file
#
# Example usage:
# - BIRDHOUSE_LOG_FD=2; BIRDHOUSE_LOG_FILE=test.log
#    - all log levels will be written to stderr and test.log
# - BIRDHOUSE_LOG_FD=2; BIRDHOUSE_LOG_QUIET=True
#    - all log file output will be suppressed (this is the same as setting BIRDHOUSE_LOG_QUIET=True but also demonstrates that it overrides BIRDHOUSE_LOG_FD)
# - BIRDHOUSE_LOG_FD=1, BIRDHOUSE_LOG_DEST_OVERRIDE='DEBUG:file:debug.log'
#    - all log levels will be written to stdout 
#    - DEBUG will also be written to debug.log
# - BIRDHOUSE_LOG_FILE=all.log, BIRDHOUSE_LOG_DEST_OVERRIDE='INFO:file:info.log:ERROR:quiet::WARN:fd:1'
#    - all log levels will be written to all.log except for INFO which will be written to info.log
#    - all log levels will be written to stderr (the default) except for ERROR which will be suppressed and WARN which will be written to stdout
log_dest() {
    level=$1
    option=$2
    read log_line || true
    if [ -n "${log_line}" ]; then
        log_quiet="${BIRDHOUSE_LOG_QUIET}"
        log_fd="${BIRDHOUSE_LOG_FD}"
        log_file="${BIRDHOUSE_LOG_FILE}"
        if [ "${option}" != "NO_OVERRIDE" ]; then
            override_string="${BIRDHOUSE_LOG_DEST_OVERRIDE}"
            override_section="${override_string#*"${level}:"}"
            while [ "${override_string}" != "${override_section}" ]; do
                override="$(echo "${override_section}" | cut -d: -f 1-2)"
                case "${override}" in
                    quiet:*)
                        log_quiet=True
                    ;;
                    fd:*)
                        log_fd="$(echo "${override}" | cut -d: -f 2)"
                    ;;
                    file:*)
                        log_file="$(echo "${override}" | cut -d: -f 2)"
                    ;;
                esac
                override_string="${override_string#*"${level}:${override}"}"
                override_section="${override_string#*"${level}:"}"
            done
        fi
        if [ "${log_quiet}" = "True" ]; then
            echo "$log_line" >> "${log_file:-/dev/null}"
        else
            if [ -n "${log_file}" ]; then
                echo "$log_line" | tee -a "${log_file}" 1>&"${log_fd}"
            else
                echo "$log_line" 1>&"${log_fd}"
            fi
        fi
    fi
}


for level in CRITICAL DEBUG INFO WARN ERROR; do 
    override="$(echo "${BIRDHOUSE_LOG_DEST_OVERRIDE}" | sed "s/\(^\|.*:\)\(${level}:\(quiet\|fd\|file\):[^:]*\).*\|.*/\2/")"
    no_override="$([ "${level}" = "CRITICAL" ] && echo NO_OVERRIDE)"
    if [ -z "${override}" ] && echo "${BIRDHOUSE_LOG_DEST_OVERRIDE}" | grep -q "\(^\|.*:\)${level}:"; then
        echo "${LOG_CRITICAL}Invalid log destination override for level '${level}': [BIRDHOUSE_LOG_DEST_OVERRIDE=${BIRDHOUSE_LOG_DEST_OVERRIDE}]" | log_dest CRITICAL "$no_override"
        exit 2
    fi
    if [ "$(echo "${override}" | cut -d: -f2)" = "fd" ]; then
        override_fd=$(echo "${override}" | cut -d: -f3)
        if [ -z "${override_fd##*[!0-9]*}" ]; then
            echo "${LOG_CRITICAL}Invalid log file descriptor setting (not an integer) for level ${level}: '${override_fd}' [BIRDHOUSE_LOG_DEST_OVERRIDE=${BIRDHOUSE_LOG_DEST_OVERRIDE}]" | log_dest CRITICAL "$no_override"
            exit 2
        fi
    fi
done

if [ -z "${BIRDHOUSE_LOG_FD##*[!0-9]*}" ]; then
    echo "${LOG_CRITICAL}Invalid log file descriptor setting (not an integer): [BIRDHOUSE_LOG_FD=${BIRDHOUSE_LOG_FD}]." | log_dest CRITICAL
    exit 2
fi

# Usage: log {LEVEL} "{message}" [...]
# Any amount of messages can be passed to the function.
log() {
    level="$1"
    shift || true
    case "${BIRDHOUSE_LOG_LEVEL}" in
        DEBUG|INFO|WARN|ERROR)
            if [ "$*" = "" ]; then
                echo "${LOG_CRITICAL}Invalid: log message is missing." | log_dest CRITICAL
                exit 2
            fi
            {
                case "${BIRDHOUSE_LOG_LEVEL}-${level}" in
                    DEBUG-DEBUG)
                        echo "${LOG_DEBUG}$*"
                    ;;
                    DEBUG-INFO|INFO-INFO)
                        echo "${LOG_INFO}$*"
                    ;;
                    DEBUG-WARN|INFO-WARN|WARN-WARN)
                        echo "${LOG_WARN}$*"
                    ;;
                    *-ERROR)
                        echo "${LOG_ERROR}$*"
                    ;;
                    *-DEBUG|*-INFO|*-WARN)
                    ;;
                    *)
                        echo "${LOG_CRITICAL}Invalid log level: [${level}]" | log_dest CRITICAL
                        exit 2
                    ;;
                esac
            } | log_dest ${level}
        ;;
        *)
            echo "${LOG_CRITICAL}Invalid log level setting: [BIRDHOUSE_LOG_LEVEL=${BIRDHOUSE_LOG_LEVEL}]." | log_dest CRITICAL
            exit 2
        ;;
    esac
}
