#!/bin/sh
# This script is meant to be sourced by all scripts needing to read default.env
# or env.local.

# Derive COMPOSE_DIR from the post probable locations.
# This is not meant to be exhautive.
# Caller of this file can simply set COMPOSE_DIR itself.
set_compose_dir() {
    if [ -z "$COMPOSE_DIR" -o ! -e "$COMPOSE_DIR" ]; then
        COMPOSE_DIR="`pwd`"
        if [ -e "./pavics-compose.sh" ]; then
            # Current dir is COMPOSE_DIR
            COMPOSE_DIR="`realpath "$COMPOSE_DIR"`"
        elif [ -e "../pavics-compose.sh" ]; then
            # Parent dir is COMPOSE_DIR
            # Case of all the scripts under deployment/ or scripts/
            COMPOSE_DIR="`realpath "$COMPOSE_DIR/.."`"
        elif [ -e "../birdhouse-deploy/birdhouse/pavics-compose.sh" ]; then
            # Case of sibling checkout at same level as birdhouse-deploy.
            COMPOSE_DIR="`realpath "$COMPOSE_DIR/../birdhouse-deploy/birdhouse"`"
        elif [ -e "../../birdhouse-deploy/birdhouse/pavics-compose.sh" ]; then
            # Case of subdir of sibling checkout at same level as birdhouse-deploy.
            COMPOSE_DIR="`realpath "$COMPOSE_DIR/../../birdhouse-deploy/birdhouse"`"
        elif [ -e "../../../birdhouse-deploy/birdhouse/pavics-compose.sh" ]; then
            # Case of sub-subdir of sibling checkout at same level as birdhouse-deploy.
            COMPOSE_DIR="`realpath "$COMPOSE_DIR/../../../birdhouse-deploy/birdhouse"`"
        elif [ -e "./birdhouse/pavics-compose.sh" ]; then
            # Child dir is COMPOSE_DIR
            COMPOSE_DIR="`realpath "$COMPOSE_DIR/birdhouse"`"
        fi
        export COMPOSE_DIR
    fi
}

read_default_env() {
}

read_components_default_env() {
}

read_env_local() {
}

process_delayed_eval() {
}
