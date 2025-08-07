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
#  # Set variable COMPOSE_DIR to the dir containing birdhouse-compose.sh and
#  # docker-compose.yml.
#
#  # Source the script providing function read_configs.
#  # read_configs uses COMPOSE_DIR to find default.env and env.local.
#  . ${COMPOSE_DIR}/read-configs.include.sh
#
#  # Call function read_configs to read the various config files in the
#  # appropriate order and process delayed eval vars properly.
#  read_configs


# Derive COMPOSE_DIR from the most probable locations.
# This is NOT meant to be exhaustive.
# Assume the checkout is named "birdhouse-deploy", which might NOT be true.
# Caller of this file can simply set COMPOSE_DIR itself, this is the safest way.
# WARNING: cannot use 'log' calls within this function until the following logging script gets resolved and sourced.
discover_compose_dir() {
    if [ -z "${COMPOSE_DIR}" ] || [ ! -e "${COMPOSE_DIR}" ]; then
        if [ -n "${BIRDHOUSE_COMPOSE}" ] && [ -f "${BIRDHOUSE_COMPOSE}" ]; then
            # Parent of the BIRDHOUSE_COMPOSE file is the COMPOSE_DIR
            COMPOSE_DIR=$(dirname "${COMPOSE_DIR}")
        elif [ -f "./birdhouse-compose.sh" ]; then
            # Current dir is COMPOSE_DIR
            COMPOSE_DIR="$(realpath .)"
        elif [ -f "../birdhouse-compose.sh" ]; then
            # Parent dir is COMPOSE_DIR
            # Case of all the scripts under deployment/ or scripts/
            COMPOSE_DIR="$(realpath ..)"
        elif [ -f "../birdhouse/birdhouse-compose.sh" ]; then
            # Sibling dir is COMPOSE_DIR
            # Case of all the tests under tests/
            COMPOSE_DIR="$(realpath ../birdhouse)"
        elif [ -f "./birdhouse/birdhouse-compose.sh" ]; then
            # Child dir is COMPOSE_DIR
            COMPOSE_DIR="$(realpath birdhouse)"
        # Below assume checkout is named birdhouse-deploy, which might not
        # always be true.
        elif [ -f "../birdhouse-deploy/birdhouse/birdhouse-compose.sh" ]; then
            # Case of sibling checkout at same level as birdhouse-deploy.
            COMPOSE_DIR="$(realpath "../birdhouse-deploy/birdhouse")"
        elif [ -f "../../birdhouse-deploy/birdhouse/birdhouse-compose.sh" ]; then
            # Case of subdir of sibling checkout at same level as birdhouse-deploy.
            COMPOSE_DIR="$(realpath "../../birdhouse-deploy/birdhouse")"
        elif [ -f "../../../birdhouse-deploy/birdhouse/birdhouse-compose.sh" ]; then
            # Case of sub-subdir of sibling checkout at same level as birdhouse-deploy.
            COMPOSE_DIR="$(realpath "../../../birdhouse-deploy/birdhouse")"
        fi
    fi
    # Perform last-chance validation in case 'COMPOSE_DIR' was incorrectly set explicitly
    # and that 'read-configs.include.sh' was sourced directly from an invalid location.
    if [ ! -f "${COMPOSE_DIR}/birdhouse-compose.sh" ]; then
        echo \
          "CRITICAL: [${COMPOSE_DIR}/birdhouse-compose.sh] not found," \
          "please set variable 'COMPOSE_DIR' to a valid location." \
          "Many features depend on this variable." 1>&2
        return 2
    fi
    export COMPOSE_DIR
}


# error out appropriately without closing shell according to 'sh <script>' or '. <script>' call
discover_compose_dir || return $? 2>/dev/null || exit $?
. "${COMPOSE_DIR}/scripts/error-handling.include.sh"
. "${COMPOSE_DIR}/scripts/logging.include.sh"
log INFO "Resolved docker-compose directory: [${COMPOSE_DIR}]"


discover_env_local() {
    if [ -z "${BIRDHOUSE_LOCAL_ENV}" ]; then
        BIRDHOUSE_LOCAL_ENV="${COMPOSE_DIR}/env.local"
    fi

    BIRDHOUSE_LOCAL_ENV=$(readlink -f "$BIRDHOUSE_LOCAL_ENV" || realpath "$BIRDHOUSE_LOCAL_ENV")
    export BIRDHOUSE_LOCAL_ENV

    # env.local can be a symlink to the private config repo where the real
    # env.local file is source controlled.
    # Docker volume-mount will need the real dir of the file for symlink to
    # resolve inside the container.
    BIRDHOUSE_LOCAL_ENV_REAL_PATH="$(realpath "${BIRDHOUSE_LOCAL_ENV}")"
    BIRDHOUSE_LOCAL_ENV_REAL_DIR="$(dirname "${BIRDHOUSE_LOCAL_ENV}_REAL_PATH")"
}


read_default_env() {
    if [ -e "${COMPOSE_DIR}/default.env" ]; then
        # Ensure DELAYED_EVAL is properly initialized before being appended to.
        DELAYED_EVAL=''

        . "${COMPOSE_DIR}/default.env"
    else
        log WARN "'${COMPOSE_DIR}/default.env' not found"
    fi
}


read_env_local() {
    # we don't use usual .env filename, because docker-compose uses it

    log INFO "Using local environment file at: ${BIRDHOUSE_LOCAL_ENV}"

    if [ -e "${BIRDHOUSE_LOCAL_ENV}" ]; then
        saved_shell_options="$(set +o)"
        set +xv  # hide passwd in env.local in logs

        . "${BIRDHOUSE_LOCAL_ENV}"

        # restore saved shell options
        eval "${saved_shell_options}"

    else
        log WARN "'${BIRDHOUSE_LOCAL_ENV}' not found"
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
      if echo "${ALL_CONF_DIRS}" | grep -qE "^\s*${adir}\s*$"; then
          # ignore directories that are already in ALL_CONF_DIRS
          continue
      fi
      # push current adir onto the stack (this helps keep track of current adir when recursing)
      _adir_stack="${_adir_stack}\n${adir}"
      if [ ! -e "${adir}" ]; then
          # Do not exit to not break unattended autodeploy since no human around to
          # fix immediately.
          # The new adir with typo will not be active but at least all the existing
          # will still work.
          #
          # Allowing not existing conf dir also helps for smooth
          # transition of component path when they are new/renamed/deleted.
          #
          # New component names can be added to BIRDHOUSE_EXTRA_CONF_DIRS before the
          # corresponding PR are merged and old component names can be removed
          # after the corresponding PR are merge without any impact on the
          # autodeploy process.
          log WARN "'${adir}' in ${conf_locations} does not exist"
      fi
      if [ -f "${adir}/default.env" ]; then
          # Source config settings of dependencies first if they haven't been sourced previously.
          # Note that this will also define the order that docker-compose-extra.yml files will be loaded.
          unset COMPONENT_DEPENDENCIES
          dependencies="$(. "${adir}/default.env" && echo "${COMPONENT_DEPENDENCIES}")"
          if [ -n "${dependencies}" ]; then
            old_conf_locations="${conf_locations}"
            source_conf_files "${dependencies}" "a dependency of ${adir}"
            conf_locations="${old_conf_locations}"
            # reset the adir variable in case it was changed in a recursive call
            adir="$(printf '%b' "${_adir_stack}" | tail -1)"
          fi
          log DEBUG "reading '${adir}/default.env'"
          . "${adir}/default.env"
      fi
      if echo "${ALL_CONF_DIRS}" | grep -qE "^\s*${adir}\s*$"; then
          # check again in case a dependency has already added this to the ALL_CONF_DIRS variable
          continue
      fi
      ALL_CONF_DIRS="${ALL_CONF_DIRS}
        ${adir}
      "
      # pop current adir from the stack once we're done with it
      _adir_stack="$(printf '%b' "${_adir_stack}" | sed '$d')"
  done
}

read_components_default_env() {
    # BIRDHOUSE_EXTRA_CONF_DIRS and BIRDHOUSE_DEFAULT_CONF_DIRS normally set by env.local so should read_env_local() first.

    # BIRDHOUSE_EXTRA_CONF_DIRS and BIRDHOUSE_DEFAULT_CONF_DIRS relative paths are relative to COMPOSE_DIR.
    if [ -d "${COMPOSE_DIR}" ]; then
        cd "${COMPOSE_DIR}" >/dev/null || true
    fi

    source_conf_files "${BIRDHOUSE_DEFAULT_CONF_DIRS}" 'BIRDHOUSE_DEFAULT_CONF_DIRS'
    source_conf_files "${BIRDHOUSE_EXTRA_CONF_DIRS}" 'BIRDHOUSE_EXTRA_CONF_DIRS'

    # Return to previous pwd.
    if [ -d "${COMPOSE_DIR}" ]; then
        cd - >/dev/null || true
    fi
}


# Check that all optional variables are defined with a different value than the default to emit a warning log message.
# Also check that required variables do not use generic defaults to indicate possible security issues.
check_default_vars() {
    # For required variables, do not check for omitted override,
    # since those will be flagged as error anyway (see 'check_required_vars').
    # Only indicate if there is a possible security concern.
    # Note that the defaults of required variables are not actually set in those variables, but
    # are listed in 'env.local.example', hence why they pose a possible security concern.
    # (ie: __DEFAULT__MAGPIE_ADMIN_PASSWORD exists, but MAGPIE_ADMIN_PASSWORD is not set, must have explicit override)
    for i in ${VARS}
    do
      n="${i#\$}"
      v=`eval echo "${i}" 2>/dev/null`
      default="\${__DEFAULT__${n}}"
      d=`eval echo "${default}" 2>/dev/null` || true  # eval may fail if no default variable exists
      if [ ! -z "${d}" ]; then
          if [ "${d}" = "${v}" ]; then
              log WARN \
                "Required variable [${n}] employs a default recommended for override." \
                "The security of your deployment may be compromised unless it is changed. Check env.local file."
          fi
      fi
    done

    # for optional variables, warn about possibility omitted override or when defaults are employed
    for i in ${OPTIONAL_VARS}
    do
        v="${i}"
        d=`eval echo "$v"`
        n="${i#\$}"
        default="\${__DEFAULT__${n}}"
        result=`echo "${d}" | grep -c "${default}"` || true  # grep may fail if no default variable exists
        if [ -z "`eval "echo ${v}"`" ]
        then
            log DEBUG "Optional variable [${n}] is not set. Check env.local file."
        fi
        if [ "${result}" -gt 0 ]
        then
            log WARN "Optional variable [${n}] employs a default recommended for override. Check env.local file."
        fi
    done
}


# If BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED is True then allow environment variables listed in
# BIRDHOUSE_BACKWARDS_COMPATIBLE_VARIABLES to override the equivalent deprecated variables as long as that
# equivalent deprecated variable is unset.
set_old_backwards_compatible_variables() {
    [ x"${BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED}" = x"True" ] || return 0
    BIRDHOUSE_OLD_VARS_OVERRIDDEN=""
    # Reverse the variable list so that old variables are overridden in the correct order.
    reverse_backwards_compatible_variables=""
    for back_compat_vars in ${BIRDHOUSE_BACKWARDS_COMPATIBLE_VARIABLES}
    do
        reverse_backwards_compatible_variables="${back_compat_vars} ${reverse_backwards_compatible_variables}"
    done
    for back_compat_vars in ${reverse_backwards_compatible_variables}
    do
        old_var="${back_compat_vars%%=*}"
        new_var="${back_compat_vars#*=}"
        old_var_set="`eval "echo \\${${old_var}+set}"`"  # will equal 'set' if the variable is set, null otherwise
        new_var_set="`eval "echo \\${${new_var}+set}"`"  # will equal 'set' if the variable is set, null otherwise
        if [ "${new_var_set}" = "set" ] && [ ! "${old_var_set}" = "set" ]; then
            new_value="`eval "echo \\$${new_var}"`"
            eval 'export ${old_var}="${new_value}"'
            BIRDHOUSE_OLD_VARS_OVERRIDDEN="${BIRDHOUSE_OLD_VARS_OVERRIDDEN} ${old_var} "  # space before and after old_var is for grep (below)
            log DEBUG "Variable [${new_var}] is being used to set the deprecated variable [${old_var}]."
        fi
    done
    for hardcoded_var in ${BIRDHOUSE_BACKWARDS_COMPATIBLE_HARDCODED_DEFAULTS}
    do
        new_var="${hardcoded_var%%=*}"
        hardcoded_old_value="${hardcoded_var#*=}"
        new_value="`eval "echo \\$${new_var}"`"
        if [ "${new_value}" = "\${__DEFAULT_${new_var}}" ]; then
            log WARN "Variable [${new_var}] is being set to the previously hardcoded default value [${hardcoded_old_value}]."
            eval 'export ${new_var}="${hardcoded_old_value}"'
        fi
    done
}

# If BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED is True then allow environment variables listed in
# BIRDHOUSE_BACKWARDS_COMPATIBLE_VARIABLES to override the equivalent non-deprecated variable.
# Otherwise, warn the user about deprecated variables that may still exist in the BIRDHOUSE_LOCAL_ENV
# file without overriding.
# If the first argument to this function is "pre-components", only the variables from
# BIRDHOUSE_BACKWARDS_COMPATIBLE_VARIABLES_PRE_COMPONENTS will be processed.
process_backwards_compatible_variables() {
    for back_compat_vars in ${BIRDHOUSE_BACKWARDS_COMPATIBLE_VARIABLES}
    do
      old_var="${back_compat_vars%%=*}"
      echo "${BIRDHOUSE_OLD_VARS_OVERRIDDEN}" | grep -q "[[:space:]]${old_var}[[:space:]]" && continue
      if [ "$1" = "pre-components" ] && \
        ! echo "${BIRDHOUSE_BACKWARDS_COMPATIBLE_VARIABLES_PRE_COMPONENTS}" | grep -q "^[[:space:]]*${old_var}[[:space:]]*$"; then
          continue
      fi

      new_var="${back_compat_vars#*=}"
      old_var_set="`eval "echo \\${${old_var}+set}"`"  # will equal 'set' if the variable is set, null otherwise
      if [ "${old_var_set}" = "set" ]; then
        old_value="`eval "echo \\$${old_var}"`"
        if [ x"${BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED}" = x"True" ]; then
          log WARN "Deprecated variable [${old_var}] is overriding [${new_var}]. Check env.local file."
          eval 'export ${new_var}="${old_value}"'
        else
          new_value="`eval "echo \\$${new_var}"`"
          if [ x"${old_value}" = x"${new_value}" ]; then
            log WARN "Deprecated variable [${old_var}] can be removed as it has been superseded by [${new_var}]. Check env.local file."
          else
            log WARN "Deprecated variable [${old_var}] is present but ignored in favour of [${new_var}]. Check env.local file."
          fi
        fi
      fi
    done
    if [ x"${BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED}" = x"True" ]; then
      BIRDHOUSE_EXTRA_CONF_DIRS="$BIRDHOUSE_EXTRA_CONF_DIRS ./optional-components/backwards-compatible-overrides"
    fi
    if [ ! "$1" = "pre-components" ]; then
      for default_old_var in ${BIRDHOUSE_BACKWARDS_COMPATIBLE_DEFAULTS}
      do
        old_var="${default_old_var%%=*}"
        default_old_value="${default_old_var#*=}"
        old_value="`eval "echo \\$${old_var}"`"
        if [ "${old_value}" = "${default_old_value}" ]; then
          log WARN "Variable [${old_var}] employs a deprecated default value recommended for override. Check env.local file."
        fi
      done
    fi
}


# Verify that all required variables are set, and error out otherwise with an error log message.
check_required_vars() {
    for i in ${VARS}
    do
        v="${i}"
        if [ -z "`eval "echo ${v}"`" ]
        then
            log ERROR "Required variable ${v#$} is not set. Check env.local file."
            return 1
        fi
    done
}


# All scripts sourcing default.env and env.local and needing to use any vars
# in DELAYED_EVAL list need to call this function to actually resolve the
# value of each var in DELAYED_EVAL list.
process_delayed_eval() {
    ALREADY_EVALED=''
    for i in ${DELAYED_EVAL}; do
        if echo "${ALREADY_EVALED}" | grep -qE "^\s*$i\s*$"; then
          # only eval each variable once (in case it was added to the list multiple times)
          continue
        fi
        v="`eval "echo \\$${i}"`"
        value=`eval "echo \"${v}\""`
        eval 'export ${i}="${value}"'
        log DEBUG "delayed eval '$(env | grep -e "^${i}=")'"
        ALREADY_EVALED="
          ${ALREADY_EVALED}
          $i"
    done
}


# Sets the COMPOSE_CONF_LIST variable to a string that contains all the docker-compose*.yml files that are
# required to pass to the docker compose command. This is determined by the contents of the ALL_CONF_DIRS
# variable (set using the read_components_default_env function).
# The file order is determined by the order of the config directories in ALL_CONF_DIRS.
# If a config directory also includes an override file for another component
# (eg: ./components/finch/config/proxy/docker-compose-extra.yml overrides ./components/proxy/docker-compose-extra.yml),
# the following additional order rules apply:
#
#  - if the component that is being overridden has already been added, the override file is added immediately
#  - otherwise, the override files will be added immediately after the component that is being overridden
#    has been added
create_compose_conf_list() {
  # ALL_CONF_DIRS relative paths are relative to COMPOSE_DIR.
  discover_compose_dir
  if [ -d "${COMPOSE_DIR}" ]; then
      log INFO "Found compose directory [${COMPOSE_DIR}]"
      cd "${COMPOSE_DIR}" || return
  fi

  COMPOSE_CONF_LIST="-f docker-compose.yml"
  COMPONENT_OVERRIDES=''
  LOADED_COMPONENTS=''
  for adir in ${ALL_CONF_DIRS}; do
    service_name=$(basename "${adir}")
    LOADED_COMPONENTS="${LOADED_COMPONENTS}\n${service_name}"

    if [ -f "${adir}/docker-compose-extra.yml" ]; then
      COMPOSE_CONF_LIST="${COMPOSE_CONF_LIST} -f ${adir}/docker-compose-extra.yml"
    fi

    # If previously loaded components specified overrides for the component that was just loaded, load those overrides now
    previous_overrides=$(printf '%b' "${COMPONENT_OVERRIDES}" | grep "^${service_name} " | sed "s/^${service_name}//g" | tr '\n' ' ')
    COMPOSE_CONF_LIST="${COMPOSE_CONF_LIST} ${previous_overrides}"
    # Load overrides for other components unless the component to be overridden hasn't been loaded yet. If the component
    # hasn't been loaded yet, store a reference to it so that it can be added in as soon as the component is loaded.
    for conf_dir in "${adir}"/config/*; do
      override_service_name=$(basename "${conf_dir}")
      extra_compose="${conf_dir}/docker-compose-extra.yml"
      if [ -f "${extra_compose}" ]; then
        if printf '%b' "${LOADED_COMPONENTS}" | grep -q "^${override_service_name}$"; then
          COMPOSE_CONF_LIST="${COMPOSE_CONF_LIST} -f ${extra_compose}"
        else
          COMPONENT_OVERRIDES="${COMPONENT_OVERRIDES}\n${override_service_name} -f ${extra_compose}"
        fi
      fi
    done
  done

    # Return to previous pwd.
  if [ -d "${COMPOSE_DIR}" ]; then
      log INFO "Moving to [${COMPOSE_DIR}]"
      cd - >/dev/null || return
  fi
}

# If unset, BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED is set to True to enable backwards compatible mode by default if this
# file is not being run through a supported interface.
set_backwards_compatible_as_default() {
  if [ ! "${__BIRDHOUSE_SUPPORTED_INTERFACE}" = 'True' ]; then
    log WARN "This file [$(readlink -f "$0" || realpath "$0")] is being executed through a non-supported interface for the Birdhouse software. This file may be moved or updated without warning."
    if [ ! "${BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED+set}" = 'set' ];then
      BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED=True
      log WARN "The BIRDHOUSE_BACKWARD_COMPATIBLE_ALLOWED variable is being set to 'True' by default. To avoid this behaviour set this variable or execute this file through a supported interface."
    fi
  fi
}

# Main function to read all config files in appropriate order and call
# process_delayed_eval() at the appropriate moment.
read_configs() {
    set_backwards_compatible_as_default
    discover_compose_dir
    discover_env_local
    read_default_env
    read_env_local  # for BIRDHOUSE_EXTRA_CONF_DIRS and BIRDHOUSE_DEFAULT_CONF_DIRS, need discover_env_local
    process_backwards_compatible_variables pre-components
    read_components_default_env  # uses BIRDHOUSE_EXTRA_CONF_DIRS and BIRDHOUSE_DEFAULT_CONF_DIRS, sets ALL_CONF_DIRS
    set_old_backwards_compatible_variables
    read_env_local  # again to override components default.env, need discover_env_local
    process_backwards_compatible_variables
    check_default_vars
    process_delayed_eval
}


# Alternative to main function read_configs() without reading the default.env
# of various components.  Use only when you know what you are doing.  Else use
# read_configs() to be safe.
read_basic_configs_only() {
    set_backwards_compatible_as_default
    discover_compose_dir
    discover_env_local
    read_default_env
    set_old_backwards_compatible_variables
    read_env_local  # need discover_env_local
    process_backwards_compatible_variables
    check_default_vars
    process_delayed_eval
}
