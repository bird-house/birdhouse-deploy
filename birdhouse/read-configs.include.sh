#!/bin/sh
# This script is meant to be sourced by all scripts needing to read default.env
# or env.local.
#
# Normally only read_configs() is needed, but for any special needs, each step
# can be called individually.
#
# When not using read_configs(), caller is responsible for knowing the proper
# sequence to read the config files, for hiding password when reading env.local
# and to call process_delayed_eval() to have fully usable resolved variable
# values.
#
# USAGE:
#  # Set variable COMPOSE_DIR to the dir containing pavics-compose.sh and
#  # docker-compose.yml.
#
#  # Source the script providing function read_configs.
#  # read_configs uses COMPOSE_DIR to find default.env and env.local.
#  . $COMPOSE_DIR/read-configs.include.sh
#
#  # Call function read_configs to read the various config files in the
#  # appropriate order and process delayed eval vars properly.
#  read_configs


# Derive COMPOSE_DIR from the most probable locations.
# This is NOT meant to be exhautive.
# Caller of this file can simply set COMPOSE_DIR itself.
discover_compose_dir() {
    if [ -z "$COMPOSE_DIR" ] || [ ! -e "$COMPOSE_DIR" ]; then
        if [ -f "./pavics-compose.sh" ]; then
            # Current dir is COMPOSE_DIR
            COMPOSE_DIR="$(realpath .)"
        elif [ -f "../pavics-compose.sh" ]; then
            # Parent dir is COMPOSE_DIR
            # Case of all the scripts under deployment/ or scripts/
            COMPOSE_DIR="$(realpath ..)"
        elif [ -f "../birdhouse-deploy/birdhouse/pavics-compose.sh" ]; then
            # Case of sibling checkout at same level as birdhouse-deploy.
            COMPOSE_DIR="$(realpath "../birdhouse-deploy/birdhouse")"
        elif [ -f "../../birdhouse-deploy/birdhouse/pavics-compose.sh" ]; then
            # Case of subdir of sibling checkout at same level as birdhouse-deploy.
            COMPOSE_DIR="$(realpath "../../birdhouse-deploy/birdhouse")"
        elif [ -f "../../../birdhouse-deploy/birdhouse/pavics-compose.sh" ]; then
            # Case of sub-subdir of sibling checkout at same level as birdhouse-deploy.
            COMPOSE_DIR="$(realpath "../../../birdhouse-deploy/birdhouse")"
        elif [ -f "./birdhouse/pavics-compose.sh" ]; then
            # Child dir is COMPOSE_DIR
            COMPOSE_DIR="$(realpath birdhouse)"
        fi
        echo "$COMPOSE_DIR"
        export COMPOSE_DIR
    fi
}


read_default_env() {
    if [ -e "$COMPOSE_DIR/default.env" ]; then
        . "$COMPOSE_DIR/default.env"
    else
        echo "WARNING: '$COMPOSE_DIR/default.env' not found" 1>&2
    fi
}


read_env_local() {
    # we don't use usual .env filename, because docker-compose uses it

    if [ -e "$COMPOSE_DIR/env.local" ]; then
        saved_shell_options="$(set +o)"
        set +xv  # hide passwd in env.local in logs

        . "$COMPOSE_DIR/env.local"

        # restore saved shell options
        eval "$saved_shell_options"

    else
        echo "WARNING: '$COMPOSE_DIR/env.local' not found" 1>&2
    fi

}

# Adds all directories in $1 to the ALL_CONF_DIRS variable (if they are not
# already present) and sources the default.env file found at each directory.
# $1 should be a list of directory paths delimited by whitespace.
# $2 is a description of the config files being passed in $1 (used for error messaging only)
source_conf_files() {
  dirs=$1
  conf_locations=$2
  for adir in ${dirs}; do
      if echo "$ALL_CONF_DIRS" | grep -qE "^\s*$adir\s*$"; then
          # ignore directories that are already in ALL_CONF_DIRS
          continue
      fi
      if [ -e "$adir" ]; then
          ALL_CONF_DIRS="$ALL_CONF_DIRS
            $adir
          "
      else
          # Do not exit to not break unattended autodeploy since no human around to
          # fix immediately.
          # The new adir with typo will not be active but at least all the existing
          # will still work.
          echo "WARNING: '$adir' in $conf_locations does not exist" 1>&2
      fi
      COMPONENT_DEFAULT_ENV="$adir/default.env"
      if [ -f "$COMPONENT_DEFAULT_ENV" ]; then
          echo "reading '$COMPONENT_DEFAULT_ENV'"
          . "$COMPONENT_DEFAULT_ENV"
          source_conf_files "$COMPONENT_DEPENDENCIES" "a dependency of $adir"
      fi
  done
}

read_components_default_env() {
    # EXTRA_CONF_DIRS and DEFAULT_CONF_DIRS normally set by env.local so should read_env_local() first.

    # EXTRA_CONF_DIRS and DEFAULT_CONF_DIRS relative paths are relative to COMPOSE_DIR.
    if [ -d "$COMPOSE_DIR" ]; then
        cd "$COMPOSE_DIR"
    fi

    source_conf_files "$DEFAULT_CONF_DIRS" 'DEFAULT_CONF_DIRS'
    source_conf_files "$EXTRA_CONF_DIRS" 'EXTRA_CONF_DIRS'

    # Return to previous pwd.
    if [ -d "$COMPOSE_DIR" ]; then
        cd -
    fi
}


# All scripts sourcing default.env and env.local and needing to use any vars
# in DELAYED_EVAL list need to call this function to actually resolve the
# value of each var in DELAYED_EVAL list.
process_delayed_eval() {
    ALREADY_EVALED=''
    for i in ${DELAYED_EVAL}; do
        if echo "$ALREADY_EVALED" | grep -qE "^\s*$i\s*$"; then
          # only eval each variable once (in case it was added to the list multiple times)
          continue
        fi
        v="`eval "echo \\$${i}"`"
        eval 'export ${i}="`eval "echo ${v}"`"'
        echo "delayed eval '$(env |grep "${i}=")'"
        ALREADY_EVALED="
          $ALREADY_EVALED
          $i"
    done
}


# Main function to read all config files in appropriate order and call
# process_delayed_eval() at the appropriate moment.
read_configs() {
    discover_compose_dir
    read_default_env
    read_env_local  # for EXTRA_CONF_DIRS and DEFAULT_CONF_DIRS
    read_components_default_env  # uses EXTRA_CONF_DIRS and DEFAULT_CONF_DIRS, sets ALL_CONF_DIRS
    read_env_local  # again to override components default.env
    process_delayed_eval
}


# Alternative to main function read_configs() without reading the default.env
# of various components.  Use only when you know what you are doing.  Else use
# read_configs() to be safe.
read_basic_configs_only() {
    discover_compose_dir
    read_default_env
    read_env_local
    process_delayed_eval
}


# Generate COMPOSE_CONF_LIST from ALL_CONF_DIRS.
gen_compose_conf_list() {
    COMPOSE_CONF_LIST="-f docker-compose.yml"
    for adir in $ALL_CONF_DIRS; do
      if [ -f "$adir/docker-compose-extra.yml" ]; then
        COMPOSE_CONF_LIST="${COMPOSE_CONF_LIST} -f $adir/docker-compose-extra.yml"
      fi
    done
    CONFIGURED_COMPONENTS=''
    for adir in $ALL_CONF_DIRS; do
      CONFIGURED_COMPONENTS="
        $CONFIGURED_COMPONENTS
        $(basename $adir)"
    done

    for adir in $ALL_CONF_DIRS; do
      for conf_dir in "$adir"/config/*; do
        service_name=$(basename "$conf_dir")
        extra_compose="$conf_dir/docker-compose-extra.yml"
        if [ -f "$extra_compose" ]; then
          if echo "$CONFIGURED_COMPONENTS" | grep -q "$service_name"; then
            COMPOSE_CONF_LIST="${COMPOSE_CONF_LIST} -f $extra_compose"
          fi
        fi
      done
    done
}
