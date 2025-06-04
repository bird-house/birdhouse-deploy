if [ "$_BIRDHOUSE_ERROR_HANDLING_ENABLED" != "true" ]; then
    BIRDHOUSE_DEBUG_MODE="${BIRDHOUSE_DEBUG_MODE:-false}"
    BIRDHOUSE_FAIL_FAST="${BIRDHOUSE_FAIL_FAST:-true}"

    SHELL_EXEC_FLAGS=""
    [ "$BIRDHOUSE_DEBUG_MODE" = "$true" ] && SHELL_EXEC_FLAGS="$SHELL_EXEC_FLAGS -x"
    [ "$BIRDHOUSE_FAIL_FAST" = "$true" ] && SHELL_EXEC_FLAGS="$SHELL_EXEC_FLAGS -e"

    set ${SHELL_EXEC_FLAGS}

    exit_handler() {
        exit_code="$?"
        [ "$exit_code" -eq 0 ] && exit
        [ "$BIRDHOUSE_EXPECTED_EXIT" = "true" ] && exit "$exit_code"
        err_msg="An unexpected error occurred. See additional messages on stderr for details or rerun this command with BIRDHOUSE_DEBUG_MODE=true."
        if command -v log >/dev/null; then
            log ERROR "$err_msg"
        else
            >&2 echo "The following error occurred before logging could be initialized: $err_msg"
        fi
    }

    expect_exit() {
        exit_code="${1:-$?}"
        export BIRDHOUSE_EXPECTED_EXIT=true
        exit "${exit_code}"
    }

    trap 'exit_handler' EXIT
fi

_BIRDHOUSE_ERROR_HANDLING_ENABLED=true
