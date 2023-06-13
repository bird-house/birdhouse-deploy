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


discover_env_local() {
    if [ -z "$BIRDHOUSE_LOCAL_ENV" ]; then
        BIRDHOUSE_LOCAL_ENV="$COMPOSE_DIR/env.local"
    fi

    # env.local can be a symlink to the private config repo where the real
    # env.local file is source controlled.
    # Docker volume-mount will need the real dir of the file for symlink to
    # resolve inside the container.
    BIRDHOUSE_LOCAL_ENV_REAL_PATH="$(realpath "$BIRDHOUSE_LOCAL_ENV")"
    BIRDHOUSE_LOCAL_ENV_REAL_DIR="$(dirname "$BIRDHOUSE_LOCAL_ENV_REAL_PATH")"
}


read_default_env() {
    if [ -e "$COMPOSE_DIR/default.env" ]; then
        # Ensure DELAYED_EVAL is properly initialized before being appended to.
        DELAYED_EVAL=''

        . "$COMPOSE_DIR/default.env"
    else
        echo "WARNING: '$COMPOSE_DIR/default.env' not found" 1>&2
    fi
}


read_env_local() {
    # we don't use usual .env filename, because docker-compose uses it

    echo "Using local environment file at: ${BIRDHOUSE_LOCAL_ENV}"

    if [ -e "$BIRDHOUSE_LOCAL_ENV" ]; then
        saved_shell_options="$(set +o)"
        set +xv  # hide passwd in env.local in logs

        . "$BIRDHOUSE_LOCAL_ENV"

        # restore saved shell options
        eval "$saved_shell_options"

    else
        echo "WARNING: '$BIRDHOUSE_LOCAL_ENV' not found" 1>&2
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
      # push current adir onto the stack (this helps keep track of current adir when recursing)
      _adir_stack="$_adir_stack\n$adir"
      if [ ! -e "$adir" ]; then
          # Do not exit to not break unattended autodeploy since no human around to
          # fix immediately.
          # The new adir with typo will not be active but at least all the existing
          # will still work.
          echo "WARNING: '$adir' in $conf_locations does not exist" 1>&2
      fi
      if [ -f "$adir/default.env" ]; then
          # Source config settings of dependencies first if they haven't been sourced previously.
          # Note that this will also define the order that docker-compose-extra.yml files will be loaded.
          unset COMPONENT_DEPENDENCIES
          dependencies="$(. "$adir/default.env" && echo "$COMPONENT_DEPENDENCIES")"
          if [ -n "$dependencies" ]; then
            source_conf_files "$dependencies" "a dependency of $adir"
            # reset the adir variable in case it was changed in a recursive call
            adir="$(printf '%b' "$_adir_stack" | tail -1)"
          fi
          echo "reading '$adir/default.env'"
          . "$adir/default.env"
      fi
      if echo "$ALL_CONF_DIRS" | grep -qE "^\s*$adir\s*$"; then
          # check again in case a dependency has already added this to the ALL_CONF_DIRS variable
          continue
      fi
      ALL_CONF_DIRS="$ALL_CONF_DIRS
        $adir
      "
      # pop current adir from the stack once we're done with it
      _adir_stack="$(printf '%b' "$_adir_stack" | sed '$d')"
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


# Sets the COMPOSE_CONF_LIST variable to a string that contains all the docker-compose*.yml files that are
# required to pass to the docker compose command. This is determined by the contents of the ALL_CONF_DIRS
# variable (set using the read_components_default_env function).
# The file order is determined by the order of the config directories in ALL_CONF_DIRS.
# If a config directory also includes an override file for another component
# (eg: ./config/finch/config/proxy/docker-compose-extra.yml overrides ./config/proxy/docker-compose-extra.yml),
# the following additional order rules apply:
#
#  - if the component that is being overridden has already been added, the override file is added immediately
#  - otherwise, the override files will be added immediately after the component that is being overridden
#    has been added
create_compose_conf_list() {
  # ALL_CONF_DIRS relative paths are relative to COMPOSE_DIR.
  discover_compose_dir
  if [ -d "$COMPOSE_DIR" ]; then
      cd "$COMPOSE_DIR" || return
  fi

  COMPOSE_CONF_LIST="-f docker-compose.yml"
  COMPONENT_OVERRIDES=''
  LOADED_COMPONENTS=''
  for adir in $ALL_CONF_DIRS; do
    service_name=$(basename "$adir")
    LOADED_COMPONENTS="${LOADED_COMPONENTS}\n${service_name}"

    if [ -f "$adir/docker-compose-extra.yml" ]; then
      COMPOSE_CONF_LIST="${COMPOSE_CONF_LIST} -f $adir/docker-compose-extra.yml"
    fi

    # If previously loaded components specified overrides for the component that was just loaded, load those overrides now
    previous_overrides=$(printf '%b' "${COMPONENT_OVERRIDES}" | grep "^$service_name " | sed "s/^${service_name}//g" | tr '\n' ' ')
    COMPOSE_CONF_LIST="${COMPOSE_CONF_LIST} ${previous_overrides}"
    # Load overrides for other components unless the component to be overridden hasn't been loaded yet. If the component
    # hasn't been loaded yet, store a reference to it so that it can be added in as soon as the component is loaded.
    for conf_dir in "$adir"/config/*; do
      override_service_name=$(basename "$conf_dir")
      extra_compose="$conf_dir/docker-compose-extra.yml"
      if [ -f "$extra_compose" ]; then
        if printf '%b' "${LOADED_COMPONENTS}" | grep -q "^$override_service_name$"; then
          COMPOSE_CONF_LIST="${COMPOSE_CONF_LIST} -f $extra_compose"
        else
          COMPONENT_OVERRIDES="${COMPONENT_OVERRIDES}\n${override_service_name} -f ${extra_compose}"
        fi
      fi
    done
  done

    # Return to previous pwd.
  if [ -d "$COMPOSE_DIR" ]; then
      cd - || return
  fi
}


# Main function to read all config files in appropriate order and call
# process_delayed_eval() at the appropriate moment.
read_configs() {
    discover_compose_dir
    discover_env_local
    read_default_env
    read_env_local  # for EXTRA_CONF_DIRS and DEFAULT_CONF_DIRS, need discover_env_local
    read_components_default_env  # uses EXTRA_CONF_DIRS and DEFAULT_CONF_DIRS, sets ALL_CONF_DIRS
    read_env_local  # again to override components default.env, need discover_env_local
    process_delayed_eval
}


# Alternative to main function read_configs() without reading the default.env
# of various components.  Use only when you know what you are doing.  Else use
# read_configs() to be safe.
read_basic_configs_only() {
    discover_compose_dir
    discover_env_local
    read_default_env
    read_env_local  # need discover_env_local
    process_delayed_eval
}
