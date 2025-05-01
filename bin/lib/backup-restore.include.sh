# This file includes functions that are intended to be sourced by the do_backup_restore function (in bin/birdhouse)
# It assumes that various environment variables are set including:
#  - BIRDHOUSE_EXE
#  - BIRDHOUSE_BACKUP_VOLUME
#  - BIRDHOUSE_RESTORE_SNAPSHOT
#  - BIRDHOUSE_BACKUP_DRY_RUN

eval "$(${BIRDHOUSE_EXE} configs --print-log-command)"

do_backup() {
  description="$1"
  command="$2"
  stop_containers="$3"
  [ -z "${description}" ] && log WARN "No description provided for this backup job. A description is strongly recommended."
  [ -z "${command}" ] && log ERROR "No command provided for the backup job with description: '${description}'. A command is required. Skipping this backup." && return 1
  [ "${BIRDHOUSE_BACKUP_DRY_RUN}" = 'true' ] && echo "${description}" && return 0
  if [ -n "${stop_containers}" ]; then
    log INFO "Stopping containers: ${stop_containers}"
    ${BIRDHOUSE_EXE} --quiet compose stop ${stop_containers}
  fi
  log INFO "Backing up ${description} to the ${BIRDHOUSE_BACKUP_VOLUME} volume"
  ${command} && log INFO "Backup of ${description} complete" || log ERROR "Backup of ${description} failed"
  if [ -n "${stop_containers}" ]; then
    log INFO "Restarting containers: ${stop_containers}"
    ${BIRDHOUSE_EXE} --quiet compose start ${stop_containers}
  fi
}

do_restore() {
  description="$1"
  command="$2"
  volume_dest="$3"
  stop_containers="$4"
  [ -z "${description}" ] && log WARN "No description provided for this restore job. A description is strongly recommended."
  [ -z "${command}" ] && log ERROR "No command provided for the restore job with description: '${description}'. A command is required. Skipping this restore." && return 1
  [ -z "${volume_dest}" ] && log ERROR "No volume destination provided for the restore job with description: '${description}'. A volume destination is required. Skipping this restore." && return 1
  [ "${BIRDHOUSE_BACKUP_DRY_RUN}" = 'true' ] && echo "${description}" && return 0
  ${BIRDHOUSE_EXE} --quiet backup restic restore "${BIRDHOUSE_RESTORE_SNAPSHOT}:/backup/${volume_dest}" --delete --target "/backup/${volume_dest}" || return $?
  log INFO "${description} has been restored to the ${BIRDHOUSE_BACKUP_VOLUME} volume in the '${volume_dest}' folder."
  if [ "${BIRDHOUSE_BACKUP_RESTORE_NO_CLOBBER}" != 'true' ]; then
    if [ -n "${stop_containers}" ]; then
      log INFO "Stopping containers: ${stop_containers}"
      ${BIRDHOUSE_EXE} --quiet compose stop ${stop_containers}
    fi
    log INFO "Overwriting the current ${description} with the restored backup"
    ${command} && log INFO "Restore of ${description} complete" || log ERROR "Restore of ${description} failed"
    if [ -n "${stop_containers}" ]; then
      log INFO "Restarting containers: ${stop_containers}"
      ${BIRDHOUSE_EXE} --quiet compose start ${stop_containers}
    fi
  fi
}