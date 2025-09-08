
# Changes

[//]: # (NOTES:)
[//]: # ( - comments are added here this way because comments in '.bumpversion.cfg' get wiped when it self-updates)
[//]: # ( - headers at level 2 must be with '---', not ##, to avoid comment-interpretation errors with bumpversion)
[//]: # (   see: https://github.com/c4urself/bump2version/issues/99)
[//]: # ( - bump2version will not tag automatically, so it must be done manually after PR is merged and approved)
[//]: # (   This is to ensure that new tags are applied directly on merge-commit, an not a commit within the PR)
[//]: # (   see decission: https://github.com/bird-house/birdhouse-deploy/pull/161#discussion_r661746230)

[//]: # (**DEFINE LATEST CHANGES UNDER BELOW 'Unreleased' SECTION - THEY WILL BE INTEGRATED IN NEXT RELEASE VERSION**)
[//]: # (  bump2version will take care to generate a new empty 'Unreleased' section after version bump)

[Unreleased](https://github.com/bird-house/birdhouse-deploy/tree/master) (latest)
------------------------------------------------------------------------------------------------------------------

## Changes

- DGGS: Add the new `components/dggs` providing an OGC API for Discrete Global Grid Systems.
  - DGGS API avaiable through `/dggs-api` path (default, configurable via `DGGS_API_PATH`).
  - Redirects available for `/ogcapi/dggs` and  `/ogcapi/collections/.../dggs`.
  - Sample configuration (minimum 1 resolvable data provider required) uses the new
    feature of `optional-components/secure-data-proxy` on CRIM's Hirondelle server.

- Data: Allow `optional-components/secure-data-proxy` to define generic and flexible locations.
  - `SECURE_DATA_PROXY_ROOT` can be defined as mount directory inside the `proxy` service.
  - `SECURE_DATA_PROXY_LOCATIONS` can be defined with any amount of custom locations.
  - All locations can be configured (as desired) under Magpie `secure-data-proxy` service for access control.
  - Other components (`wps_output-volume`, `stac-data-proxy`) that can optionally use this security middleware
    via `SECURE_DATA_PROXY_AUTH_INCLUDE` can still do so. Their mount points are handled separately.

[2.17.0](https://github.com/bird-house/birdhouse-deploy/tree/2.17.0) (2025-09-02)
------------------------------------------------------------------------------------------------------------------

## Changes

- STAC: Update STAC Browser to
  [`crim-ca/stac-browser:3.4.0-dev`](https://github.com/crim-ca/stac-browser/releases/tag/3.4.0-dev).

  - Dockers are now built directly with the GitHub CI releases
    (see https://github.com/crim-ca/stac-browser/pkgs/container/stac-browser).
  - Synchronize with latest changes (as of 2025-08-16).
    - Beside the necessary `prefixPath` override for Nginx Proxy redirect and a minor HTML file resolution fix,
      the image is entirely up-to-date with the official upstream code.
    - Supports STAC 1.1.0.
    - Supports language locales.
    - Greatly improves parsing of STAC metadata and their visual rendering.
    - Allows dynamic runtime [config.js](https://github.com/radiantearth/stac-browser/blob/main/config.js) overrides.
      For the time being, only the required `catalogUrl` is overridden, but further settings could be added later on.

- STAC: Update STAC API to `crim-ca/stac-app:2.0.1`.

  - Changes in [`crim-ca/stac-app:2.0.0`](https://github.com/crim-ca/stac-app/releases/tag/2.0.0) includes:
    - migration to `stac-fastapi==6.0.0` and corresponding fixes to support it
    - add `q` parameter free-text search on `/search`, `/collections` and `/collections/{collectionId}/items` endpoints
    - enforce JSON schema validation of all `stac_extensions` referenced by published STAC Items and Collections
    - multiple dependency updates
  - Minor package dependency fix in [`crim-ca/stac-app:2.0.1`](https://github.com/crim-ca/stac-app/releases/tag/2.0.1).

- STAC: Update `stac-db` and `stac-migration` to version `0.9.8`.

- STAC: Add `optional/stac-db-persist` and `STAC_DB_PERSIST_DIR` to allow custom STAC DB metadata storage location.

- Drop unsupported `pytest-lazy-fixture` python package for tests

  This package is no longer maintained and breaks for `pytest` versions 8+. We do not need it for our tests so
  it was dropped. In the future if we need to support lazy fixtures we should use the `pytest-lazy-fixtures`
  package instead (which is actively maintained).

- Dependabot automated updates for Python dependencies.

  The following Python dependencies were updated to their most recent compatible releases:
   - `jsonschema`: 4.17.1 -> 4.25.1
   - `prometheus-client`: 0.22.0 -> 0.22.1
   - `pytest`: 7.2.2 -> 8.4.1
   - `python-dotenv`: 1.0.1 -> 1.1.1
   - `requests`: 2.32.4 -> 2.32.5

## Fixes

- Backup: Fix STAC representative data restore operation (`birdhouse backup restore -r stac`).

  - Change the default `STAC_POPULATOR_BACKUP_VERSION=0.9.0` to employ
    the [Dockerfile of `stac-populator`](https://github.com/crim-ca/stac-populator/blob/master/docker/Dockerfile)
    fix with preconfigured `PYESSV_ARCHIVE_HOME` directory.
  - Add `stac-migration` along `stac-db` to the list of stopped/restored containers to ensure that the `stac-db`
    volume used by both does not yield a docker daemon error of "volume in use", and to apply any relevant
    migration scripts on the recreated `stac-db` volume.

[2.16.14](https://github.com/bird-house/birdhouse-deploy/tree/2.16.14) (2025-08-27)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Updated configuration of `.github/labeler.yml` to follow the new `actions/labeler` v5.0 conventions.

  In `Birdhouse-deploy` v2.16.11, the `actions/labeler` action was updated to v5.0 which introduced a new configuration
  format for the `.github/labeler.yml` file. This change updates the configuration to follow the new format. See: 
  [actions/labeler v5.0 release notes](https://github.com/actions/labeler/releases/tag/v5.0.0).

[2.16.13](https://github.com/bird-house/birdhouse-deploy/tree/2.16.13) (2025-08-27)
------------------------------------------------------------------------------------------------------------------

## Changes

- Updated the `finch` service to v0.12.1.

  This is a significant jump from the previous version (v0.9.2) and includes many bug fixes and dependency updates:

  - anyascii (replacement for unidecode)
  - xclim v0.43.0 (previously xclim v0.37)

[2.16.12](https://github.com/bird-house/birdhouse-deploy/tree/2.16.12) (2025-08-27)
------------------------------------------------------------------------------------------------------------------

## Fixes

- User kernels directory should always be writable

  The destination used to symlink user kernels (`/usr/local/share/jupyter`) is not always writable depending 
  on the jupyterlab docker image that is used to spawn the jupyterlab containers. To ensure that it is always 
  writable this places the link under `/var/tmp` which is guaranteed to be writable.

[2.16.11](https://github.com/bird-house/birdhouse-deploy/tree/2.16.11) (2025-08-22)
------------------------------------------------------------------------------------------------------------------

## Changes

- Added a Dependabot configuration for tracking version updates for `pip` and for GitHub Actions

  GitHub Actions have been updated to their most recent versions and their versions now point to commit hashes instead
  of version tags for security purposes. Dependabot has been configured to perform periodic updates on these actions.
  Python requirements (`requirements.txt`) now use commit hashes generated via the `pip-tools` library for security purposes
  as well. The list of Python library requirements has been moved to `requirements.in` and is also managed by Dependabot.

- Added `nodefaults` to the `environment-dev.yml` to ensure that the Anaconda "default" repository is never used for environment creation

- Replaced `bump2version` with a maintained fork (`bump-my-version`) in the development dependencies and the top-level Makefile
    
  Migrated the `.bumpversion.cfg` to use newer TOML format (`.bumpversion.toml`) and removed the logic in Makefile centred on
  tracking and updating the date of last version bump as this is now handled dynamically via `bump-my-version`


[2.16.10](https://github.com/bird-house/birdhouse-deploy/tree/2.16.10) (2025-08-16)
------------------------------------------------------------------------------------------------------------------

## Changes

- Proxy: allow to add parameters to Nginx listen directives via env.local

  One usage is to add the parameter "http2" to enable HTTP/2 protocol.

  Before
  ```sh
  $ curl --silent --include https://${BIRDHOUSE_FQDN_PUBLIC}/ | head -1
  HTTP/1.1 200 OK
  ```

  After `export PROXY_LISTEN_443_PARAMS="http2"` is set in `env.local` and
  `proxy` container restarted
  ```sh
  $ curl --silent --include https://${BIRDHOUSE_FQDN_PUBLIC}/ | head -1
  HTTP/2 200
  ```


[2.16.9](https://github.com/bird-house/birdhouse-deploy/tree/2.16.9) (2025-08-15)
------------------------------------------------------------------------------------------------------------------

## Changes

- Backup: Allow `BIRDHOUSE_BACKUP_VOLUME` to be employed directly as directory.

  This feature _**requires**_ using the `--no-restic` option to avoid it being involved by ``--snapshot`` override.
  Combining a directory path and omitting `--no-restic` can lead to undesired side effects.
  However, it allows using backup/restore operations for quick data manipulations on alternate locations than a
  volume to offer flexibility or to bypass `restic` operations.
  This can be employed for fixing problematic service data migrations or file system limitations with volumes.

  The directory structure must match exactly with `BIRDHOUSE_BACKUP_VOLUME` when used as volume
  (e.g.: `/tmp/backup/{component}-{backup_type}/...`).

  This feature also disables the automatic cleanup of the volume (since the directory is used directly).
  Therefore, users have to manage the contents of `BIRDHOUSE_BACKUP_VOLUME` on their own and consistently.

- Backup: Avoid `birdhouse backup restore` operation to complain about missing `-s|--snapshot` when not required.

  For example, `BIRDHOUSE_BACKUP_VOLUME=/tmp/backup birdhouse backup restore --no-restic -r stac` only operates on local
  data contents to be restored into the server instance. No remote `restic` snapshot is required to run the operation.

- Backup: Unification of script shebangs, variables names and function names with invoked operations.

  - Renames related to `backup [create|restore|restic]` when they apply to many operations simultaneously.
    This helps highlight that a variable with explicitly `CREATE`, `RESTORE` or `RESTIC` only applies to that
    specific operation, whereas others are shared.

    - `parse_backup_restore_common_args` => `parse_backup_common_args`
    - `BIRDHOUSE_BACKUP_RESTORE_NO_RESTIC` => `BIRDHOUSE_BACKUP_NO_RESTIC`
    - `BIRDHOUSE_BACKUP_RESTORE_COMMAND` => `BIRDHOUSE_BACKUP_COMMAND`

  - Renames to match the common `BIRDHOUSE_BACKUP_[...]` prefix employed by other "backup" variables:

    - `BIRDHOUSE_RESTORE_SNAPSHOT` => `BIRDHOUSE_BACKUP_RESTORE_SNAPSHOT`

- Backup: Add `stac-migration` image to the list of containers to stop on `birdhouse backup restore -r stac`.

  Because the service was not stopped, and that it links to `stac-db` and its corresponding volume, the
  following `docker volume rm stac-db` step would fail as the volume was still in use. This would lead to a restore
  operation dealing with dirty database contents and potentially conflicting restore data that would not be applied.
  Relates to added service `stac-migration` in [#534](https://github.com/bird-house/birdhouse-deploy/pull/534).

- Backup: Allow `BIRDHOUSE_LOG_LEVEL` to override the `stac-populator` log level involved with `-r stac`.

[2.16.8](https://github.com/bird-house/birdhouse-deploy/tree/2.16.8) (2025-08-13)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Allow user generated jupyterlab kernels to persist between sessions

  If a jupyterlab user wants to create a virtual environment to use as a kernel they can do so
  by creating a new virtual environment and installing it as a kernel with the `python -m ipykernel install`
  command.

  By default this command installs the kernel metadata in `/usr/local/share/jupyter/kernels` which is not
  persisted to a docker volume and so the kernel is no longer visible when the jupyterlab container restarts.
  Alternatively, the command can be run with the `--user` flag which installs the kernel metadata to the user's
  home directory (which is persisted to a docker volume) but the jupyterlab API does not recognize kernels
  installed in this way for some reason.

  To solve this issue, this creates a symlink from the kernels metadata folder in the user's home directory to
  a location outside of the user's home directory (`/usr/local/share/jupyter/user-kernels/kernels`) which can
  be detected by the juptyerlab API.

- Ensure jupyterlab container healthchecks don't fail by default

  The healthchecks assume that the jupyter data directory is in `/home/$NB_USER/.local` regardless of the value 
  of $HOME. This means that healthechecks for the jupyterlab containers were always failing even if the
  container was actually healthy.

  This fixes the issue by symlinking the relevant folder to `/home/$NB_USER/.local` within the container so that 
  the healthchecks can run as expected.

- Thanos-minio container should always restart on failure

  Since this container wasn't restarting automatically it could make the entire stack unavailable if it failed.
  The proxy container would refuse to start since it could not connect to the upstream thanos-minio server.

[2.16.7](https://github.com/bird-house/birdhouse-deploy/tree/2.16.7) (2025-08-05)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Fixed a malformed `rsync` command in `deploy-data-raven-testdata-to-thredds.yml` workflow.

  The `--exclude` option was not used properly which would cause the `rsync` command to fail. This is now fixed.

[2.16.6](https://github.com/bird-house/birdhouse-deploy/tree/2.16.6) (2025-08-01)
------------------------------------------------------------------------------------------------------------------

## Changes

- Jupyter env: Updated jupyter image (`py311-250423-update250730`) with new dependency `intake-esgf`, significantly
  changed `ravenpy` (v0.19.0), as well as marginal updates to Ouranos core libraries: `xclim` (v0.57.0),
  `xsdba` (v0.12.3), and `xscen` (v0.5.0).

  See [Ouranosinc/PAVICS-e2e-workflow-tests#150](https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/150)
  for more info.

- Updated `deploy-data-raven-testdata-to-thredds.yml` to reflect the new `raven-testdata` repository structure.

  The `deploy-data-raven-testdata-to-thredds.yml` workflow was updated to reflect the new structure of the `raven-testdata` repository. 
  The new structure includes a `data` directory that contains all the test data files and provides more granular
  control by setting tagged commits as targets for the test data required for a specific version of `raven` and `RavenPy`.
  This new layout emulates the same control functionality employed in `xclim`/`xclim-testdata`.

[2.16.5](https://github.com/bird-house/birdhouse-deploy/tree/2.16.5) (2025-07-18)
------------------------------------------------------------------------------------------------------------------

## Changes

- `canarieapi`: Update to default version [1.0.1](https://github.com/Ouranosinc/CanarieAPI/blob/master/CHANGES.rst#101-2025-07-17). 

  - Bug fix for configuration setting `PARSE_LOGS`.
  - Security updates.

- `cowbird`: Update to default version [2.5.2](https://github.com/Ouranosinc/cowbird/blob/master/CHANGES.rst#252-2025-07-17). 

  - Security updates.

- `magpie`: Update to default version [4.2.0](https://github.com/Ouranosinc/Magpie/blob/master/CHANGES.rst#420-2024-12-12).

  - Allow `ServiceTHREDDS` to use `/` in its metadata and data prefixes.
  - Security updates.

- `weaver`: Update to default version [6.6.2](https://github.com/crim-ca/weaver/blob/master/CHANGES.rst#662-2025-06-27).

  - Fixes for HTML page endpoints.
  - Various CLI fixes.
  - Security updates.

## Fixes 

- Fix empty newlines displayed on `COMPOSE_CONF_LIST` output.

[2.16.4](https://github.com/bird-house/birdhouse-deploy/tree/2.16.4) (2025-07-03)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Fix invalid `STAC_POPULATOR_BACKUP_IMAGE='${STAC_POPULATOR_BACKUP_DOCKER}:${STAC_POPULATOR_BACKUP_VERSION}'`.

  The `STAC_POPULATOR_BACKUP_IMAGE` variable was referring other variables missing their `_BACKUP` part.

[2.16.3](https://github.com/bird-house/birdhouse-deploy/tree/2.16.3) (2025-06-25)
------------------------------------------------------------------------------------------------------------------

## Fixes 

- Fix `thredds_transfer_size_kb_total` name in `optional-components/prometheus-longterm-rules`.

  Counter names have the suffix `_total`. Without this suffix, the counter value is not discovered
  properly in a rule and the prometheus rule will never return valid data.

- Fix bugs in prometheus-log-exporter.

- Avoid `tput: No value for $TERM and no -T specified` warnings if terminal is undefined.

[2.16.2](https://github.com/bird-house/birdhouse-deploy/tree/2.16.2) (2025-06-23)
------------------------------------------------------------------------------------------------------------------

## Changes

- Add option to backup "representative" application data

  Representative data is an application agnostic version of the stateful data used by components to store 
  the current state of the running service.

  This includes an option to backup and restore representative data for the `stac` component. Other components
  should be added in future updates.

- Add additional documentation for backups

  Also include a new script `birdhouse/scripts/create-restic-keypair.sh` to help users create and test SSH keypairs
  for use by restic when accessing restic repositories over SFTP.


[2.16.1](https://github.com/bird-house/birdhouse-deploy/tree/2.16.1) (2025-06-17)
------------------------------------------------------------------------------------------------------------------

## Changes

- Allow to set Prometheus log level for the monitoring and prometheus-longterm-metrics components

## Fixes

- Fix typo in prometheus-longterm-rules "thredds:kb_transfer_size_kb:increase_1h rule"

  Fix the follow error
  ```
  ts=2025-06-17T05:09:00.903Z caller=manager.go:201 level=error component="rule manager" msg="loading groups failed" err="/etc/prometheus/prometheus-longterm-metrics.rules: 41:17: group \"longterm-metrics-hourly\", rule 6, \"thredds:kb_transfer_size_kb:increase_1h\": could not parse expression: 1:40: parse error: unexpected right parenthesis ')'"
  ```

[2.16.0](https://github.com/bird-house/birdhouse-deploy/tree/2.16.0) (2025-06-16)
------------------------------------------------------------------------------------------------------------------

## Changes

- Add `backup` command in `bin/birdhouse` to backup and restore data to a restic repository

  This allows users to backup and restore:
    - application data, user data, and log data for all components
    - birdhouse logs
    - docker container logs
    - local environement file
  
  Restoring data either involves restoring it to a named volume (determined by `BIRDHOUSE_BACKUP_VOLUME`) or in the case
  of user data and application data, to overwrite the current data with the backup.

  For full details run the `bin/birdhouse backup --help` command.

  Backups are stored in a [restic](https://restic.readthedocs.io/en/stable/) repository which can be configured by creating 
  a file at `BIRDHOUSE_BACKUP_RESTIC_ENV_FILE` (default: `birdhouse/restic.env`)  which contains the 
  [environment variables](https://restic.readthedocs.io/en/stable/040_backup.html#environment-variables) 
  necessary for restic to create, and access a repository (see `birdhouse/restic.env.example` for details).

  The backup and restore commands can be further customized by setting any of the following variables:

  - `BIRDHOUSE_BACKUP_SSH_KEY_DIR`: 
    - The location of a directory that contains an SSH key used to access a remote machine where the restic repository 
      is hosted. Required if accessing a restic repository using the sftp protocol.
  - `BIRDHOUSE_BACKUP_RESTIC_BACKUP_ARGS`: 
    - Additional options to pass to the `restic backup` command when running the `birdhouse backup create` command.
       For example: `BIRDHOUSE_BACKUP_RESTIC_BACKUP_ARGS='--skip-if-unchanged --exclude-file "file-i-do-not-want-backedup.txt"`
  - `BIRDHOUSE_BACKUP_RESTIC_FORGET_ARGS`:
    - Additional options to pass to the `restic forget` command after running the backup job. This allows you to ensure 
      that restic deletes old backups according to your backup retention policy. If this is set, then restic will also 
      run the `restic prune` command after every backup to clean up old backup files.
      For example, to store backups daily for 1 week, weekly for 1 month, and monthly for a year:
      `BIRDHOUSE_BACKUP_RESTIC_FORGET_ARGS='--keep-daily=7 --keep-weekly=4 --keep-monthly=12'`
    
- Add scheduler job to automatically backup data

  Create a new scheduler job at `optional-components/scheduler-job-backup` which runs the `bin/birdhouse backup create` 
  command at regular intervals to ensure that the birdhouse stack's data is regularly backed up.

  To configure this job you must set the following variables:
    - `SCHEDULER_JOB_BACKUP_FREQUENCY`:
      - Cron schedule when to run this scheduler job (default is `'1 1 * * *'`, at 1:01 am daily)
    - `SCHEDULER_JOB_BACKUP_ARGS`:
      - Extra arguments to pass to the 'bin/birdhouse backup create' command when backing up data.
        For example, to back up everything set it to `'-a \* -u \* -l \* --birdhouse-logs --local-env-file'`

- Add `configs --print-log-command` option in `bin/birdhouse`

  This allows users to print a command that can be used to load the birdhouse logging functions in the current
  process. This is very similar to the `bin/birdhouse configs --print-config-command` except that it only loads
  the logging functions.

  Example usage:

  ```sh
  eval $(bin/birdhouse configs --print-log-command)
  log INFO 'here is an example log message'
  ```

  It is important to have a distinct option to just load the log commands because functions are not inherited
  by subprocesses which means that if you do something like:

  ```sh
  eval $(bin/birdhouse configs --print-config-command)
  log INFO 'this one works'
  sh -c 'log ERROR "this one does not"'
  ```

  the log command in the subprocess does not work. We would have to re-run the `eval` in the subprocess which would
  unnecessarily redefine all the existing configuration variables. Instead we can now do this:

  ```sh
  eval $(bin/birdhouse configs --print-log-command)
  log INFO 'this one works'
  sh -c 'eval $(bin/birdhouse configs --print-log-command); log INFO "this one does work now"'
  ```

  which is much quicker and does not require redefining all configuration variables.

  Note: this was introduced as a helper for the `bin/birdhouse backup` commands but was made part of the public
  interface because it is potentially very useful for other scripts that want to use the birdhouse logging mechanism. 
  For example, the `components/weaver/post-docker-compose-up` script defines its own logging functions which could
  now be easily replaced using this method.

- Add `BIRDHOUSE_COMPOSE_TEMPLATE_SKIP` environment variable to explicitly skip rebuilding template files if `true`

  This gives us the option to skip re-building template files even if the command to `bin/birdhouse compose` is `up`
  or `restart`. This is essentially the opposite of `BIRDHOUSE_COMPOSE_TEMPLATE_FORCE`.

  This option is necessary when running a command while the birdhouse stack is already running and we don't want to
  change the template files for the running stack.

- Add Prometheus rules defining long-term metrics (hourly and daily).

## Fixes

- Replace non-portable `sed -z` option

  The `birdhouse/scripts/get-services-json.include.sh` script includes the `sed` command using the `-z` flag. The
  `-z` flag is non-standard and is not supported by several well-used versions of `sed`.

  This became apparent when this script is run by the `optional-components/scheduler-job-backup` job which runs
  in an alpine based docker container.

- Fix bugs in Prometheus log parser meant to measure download volume. 

- Fix issue where the current environment is printed to stdout if no shell exec flags are set.

[2.15.1](https://github.com/bird-house/birdhouse-deploy/tree/2.15.1) (2025-06-04)
------------------------------------------------------------------------------------------------------------------

## Changes

- Stop build when a build step fails

  If a command exits with a non-zero exit code when deploying the stack (i.e. running `birdhouse-compose.sh`) the
  build process should stop and report that an unexpected error occurs.

  This is enforced by setting the `-e` flag when `birdhouse-compose.sh` is run by default. Several commands have been
  updated so that they are followed by `|| true` so that if they exit with a non-zero status it will not stop the
  script.

  Also a new environment variable `BIRDHOUSE_DEBUG_MODE` is introduced which can be set to `true` to set the `-x`
  flag which will write every command that is run by `birdhouse-compose.sh` to stderr. Previously, setting the
  `BIRDHOUSE_LOG_LEVEL` to `DEBUG` would set the `-x` flag whenever `pre-docker-compose-up` and `post-docker-compose-up`
  scripts are executed. Please use the `BIRDHOUSE_DEBUG_MODE` instead from now on. `BIRDHOUSE_LOG_LEVEL` should
  only be used to set the log level of the birdhouse logger.

[2.15.0](https://github.com/bird-house/birdhouse-deploy/tree/2.15.0) (2025-05-27)
------------------------------------------------------------------------------------------------------------------

## Changes

- Make scheduler jobs configurable

  The scheduler component automatically enables three jobs (autodeploy, logrotate, notebookdeploy). If someone wants
  to use the scheduler component but does not want these jobs, there is no obvious way to disable any one of these
  jobs.

  This change makes it possible to enable/disable jobs as required by the user and adds documentation to explain how 
  to do this.

  This change also converts existing jobs to be optional components. This makes the jobs more in-line with the way the
  stack is deployed (since version 1.24.0) and ensures that settings set as environment variables in the local environment
  file are not so sensitive to the order that they were declared in.

  **Breaking Change**:
  - the three jobs that were automatically enabled previously are now no longer enabled by default.
  - to re-enable these three jobs, source the relevant component in the `optional-components` subdirectory.

  **Deprecations**
  - setting additional scheduler jobs using the `BIRDHOUSE_AUTODEPLOY_EXTRA_SCHEDULER_JOBS` variable. Users should 
    create additional jobs by adding them as custom components instead.

  What about... ?
    - just schedule these jobs for a non-existant day like February 31st?
      - Answer: This would technically work but is not obvious to the user. It is better to make this explicit.
    - just set the schedule to the `'#'` string?
      - Answer: This is a hack that would work based on the specific way that the docker-crontab image sets schedules.
                However, this is not obvious to the user and is unreliable since it is not documented.

[2.14.0](https://github.com/bird-house/birdhouse-deploy/tree/2.14.0) (2025-05-12)
------------------------------------------------------------------------------------------------------------------

## Changes

- Weaver: update `weaver` component default version to [6.6.0](https://github.com/crim-ca/weaver/tree/6.6.0).

  Notable changes include:
  
  - Added HTML representation of job status.
  - Added alternate job `Profile` representations for interoperability with other clients like *WPS* and *openEO*.
  - Adjust job `status` value for `successful` instead of `succeeded` in accordance to latest OGC API standard edits.
    If clients were defined with explicit checks of the older value, they can request that job representation using
    query parameters `?profile=wps&f=json`. Otherwise, it is preferable that scripts are updated to allow either value
    to ensure the statuses are resolved correctly regardless of Weaver version employed by the server.
  - Docker build employs [Provenance](https://docs.docker.com/build/metadata/attestations/slsa-provenance)
    and [Software Bill of Materials (SBOM)](https://docs.docker.com/build/metadata/attestations/sbom) for
    traceable dependencies, validation of references, and trust for replicable execution pipelines.
  - Update Python 3.11 to Python 3.12 in the distributed Docker image.
  - Various bug fixes and security vulnerability fixes.

  For full changelog details, see [Weaver Changes](https://pavics-weaver.readthedocs.io/en/latest/changes.html).
  
- Cowbird: Update version [`2.5.1`](https://github.com/Ouranosinc/cowbird/blob/master/CHANGES.rst#251-2025-05-06) 
  for security fixes.

[2.13.5](https://github.com/bird-house/birdhouse-deploy/tree/2.13.5) (2025-05-08)
------------------------------------------------------------------------------------------------------------------

## Changes

- Script `extract-jupyter-users-from-magpie-db`: allow to customize the query

  An example query is provided if we want to list all users, except if they
  belong to some groups.


[2.13.4](https://github.com/bird-house/birdhouse-deploy/tree/2.13.4) (2025-05-05)
------------------------------------------------------------------------------------------------------------------

## Changes

- Update `stac` service to use `crim-ca/stac-app:1.1.0` image

  This updates the version of `stac-fastapi` to version 5 (currently the latest) and resolves and issue
  where paging links did not work properly.

  See more details [here](https://github.com/crim-ca/stac-app/pull/27).

## Fixes

- Forward correct headers through `twitcher` for the `stac` service

  The nginx configuration for `twitcher` was creating a `Forwarded` header to help `stac` construct a `base_url`
  behind the reverse proxy. However, with newer versions of `stac-fastapi` (the application running the `stac`
  service), the `Forwarded` header is being parsed incorrectly which means that the `base_url` was incorrectly
  formed.

  This change removes the problematic `Forwarded` header and instead send the information to the `stac` application
  using the `X-Forwarded-Port`, `X-Forwarded-Proto`, and `X-Forwarded-Host` headers. This technique allows `stac` 
  to generate the correct `base_url` for all versions (up to the current version 5). 

[2.13.3](https://github.com/bird-house/birdhouse-deploy/tree/2.13.3) (2025-05-03)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Makefile: Ensure the `bin/birdhouse` path employed by default resolves from anywhere.

  Previously, if `make -C path/to/birdhouse-deploy {target}` was invoked from anywhere else than within
  the `birdhouse-deploy` directory, the invoked script path would be invalid. Path resolution is improved
  to allow calls from anywhere, as well as, including the Makefile within an external one seamlessly.

[2.13.2](https://github.com/bird-house/birdhouse-deploy/tree/2.13.2) (2025-05-02)
------------------------------------------------------------------------------------------------------------------

## Changes

- Log multiple lines

  Allow the `log` command (defined in `scripts/logging.include.sh`) to log messages that span multiple lines.
  This also adds unit tests for the `scripts/logging.include.sh` file.

## Fixes

- Logging bug fixes:

  - Setting `NO_COLOR` or setting `BIRDHOUSE_COLOR` to a non-integer value raised an error since `BIRDHOUSE_COLOR`
    was tested with the numeric comparison `-eq`. This has now been fixed.

  - Providing an invalid log message level (e.g. `log BADLEVEL message`) would log a critical error message but not
    exit unless the `set -o pipefail` option was set. This has been updated so that the script will exit as intended
    even if the `pipefail` option is not set.

[2.13.1](https://github.com/bird-house/birdhouse-deploy/tree/2.13.1) (2025-04-28)
------------------------------------------------------------------------------------------------------------------

## Changes

- Jupyter env: new full build with significant changes to the Anaconda environment dependency composition.

  See [Ouranosinc/PAVICS-e2e-workflow-tests#147](https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/147)
  for more info.


[2.13.0](https://github.com/bird-house/birdhouse-deploy/tree/2.13.0) (2025-04-04)
------------------------------------------------------------------------------------------------------------------

## Changes

- Deprecate `portainer` component

  The portainer component is not currently being used and is not actually usable outside of a very specific
  host machine configuration. This change deprecates the component by moving it to the `deprecated-components`
  directory. It can still be enabled from that path if desired.

[2.12.0](https://github.com/bird-house/birdhouse-deploy/tree/2.12.0) (2025-04-03)
------------------------------------------------------------------------------------------------------------------

## Changes

- THREDDS: provide service information page details

  - Add multiple metadata variables
    (`THREDDS_ORGANIZATION_[...]`, `THREDDS_SUPPORT_[...]`, `THREDDS_ABSTRACT` and `THREDDS_KEYWORDS`)
    allowing customization of the THREDDS server information page.
  - Add a cross-reference to the `service-config.json` to the service information `/thredds/info/serverInfo.html` page.
  - Resolve the Magpie `ServiceTHREDDS` configuration disallowing access
    to `/twitcher/ows/proxy/thredds/info/serverInfo.html` by default.
    Every content under the THREDDS `/info/` prefix will be considered a Magpie `BROWSE` permission of "metadata".
    It is up to the organization to make this endpoint visible, either using `optional-components/all-public-access`
    or a similar custom Magpie permission definition.

[2.11.2](https://github.com/bird-house/birdhouse-deploy/tree/2.11.2) (2025-03-31)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Make sure that authentication routes use the correct scheme

  Two components that were added after the `BIRDHOUSE_PROXY_SCHEME` environment variable was introduced did not
  use it when checking whether a user was authenticated to view a resource using ``twitcher``'s verify route.
  This is now fixed so that the proper scheme is used.

- Fix bug where generated docker compose file is appended to not written

  Fixes a bug introduced when the version string was removed from the generated docker compose file. The previous
  line used `>` which truncated the file before writing. Now that the previous line is removed, the truncation 
  logic needed to be applied elsewhere. 

[2.11.1](https://github.com/bird-house/birdhouse-deploy/tree/2.11.1) (2025-03-27)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Remove deprecated version field from generated docker-compose files

  The `env-local` optional component generates a docker compose file that contained a version field which are
  deprecated. This fixes the issue by removing the code that generates the deprecated field.

  Also updates a declaration of an external volume in `prometheus-longterm-metrics` to use the compose v2 syntax.

- Fix bug where compose directory can't be found in `bin/birdhouse` script

    The `COMPOSE_DIR` variable cannnot be discovered properly if:
    
    - the `bin/birdhouse` script is called with the `configs --print-config-command` options.
    - the result of that call is `eval`ed in order to load the birdhouse configuration settings into 
      the calling process's environment.
    - this is done from a directory outside of the birdhouse-deploy source code directory.

    For example:

    ```sh
    cd /
    eval $(birdhouse configs --print-config-command)
    ```

    This is fixed by explicitly giving a value for the `COMPOSE_DIR` variable when using the `--print-config-command`
    option. The value is already correctly set in the `bin/birdhouse` script so it is easy to pass that 
    value on to the user. 

[2.11.0](https://github.com/bird-house/birdhouse-deploy/tree/2.11.0) (2025-03-24)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Wrong compose `up` extra arguments given to compose `restart`

  * For example, when setting `BIRDHOUSE_COMPOSE_UP_EXTRA_OPTS="--remove-orphans"` in
    `env.local`, that `--remove-orphans` flag is not supposed to be used with
    compose `restart`.  Fix regression from
    [PR #492](https://github.com/bird-house/birdhouse-deploy/pull/492).


## Changes

- Improve handling of `.template` files generation

  * Change the templating mechanism to run by default for the docker compose `restart` command instead of only `up`.
  * Add `BIRDHOUSE_COMPOSE_TEMPLATE_FORCE` variable that allows enforcing the generation of the `.template` files
    instead of only when compose `up` or `restart` command is passed by default.
  * Add automatic removal of empty directories conflicting with `.template` destinations. 
    This occurs only if a `docker compose` command ran early, and it generated volume mount directories to the
    yet non-existing files.
  * Add logs when template generation occurs, is skipped, or edge case directories are removed.

- Deprecate the `docker-compose` command as default

  Sets the default compose command to `docker compose` using the new `DOCKER_COMPOSE` environment variable.
  This uses compose v2 by default (instead of v1 which is very old and has been deprecated for a while).
  For backwards compatibility, you can set `DOCKER_COMPOSE=docker-compose` in the local environment file to 
  use the previous default.

- Remove deprecated catalog crawler code

  Code related to the solr catalog in the `birdhouse-compose.sh` file has been deprecated for a while and 
  is not currently usable with the current stack anyway so it is removed

  Also there is commented out old code that relates to the presence of an SSL certificate which is not use 
  and no longer relevant as of version 2.7.0.

- Update Docker Compose syntax to version 2 in all docker compose files

  **Breaking Change**: as of birdhouse-deploy version [2.7.3](https://github.com/bird-house/birdhouse-deploy/tree/2.7.3), 
  the stack could not be deployed with a docker compose version <`2.20.2`. However, that was not specified in the release 
  notes so we're stating it here.
  The incompatibility is due to the addition of various additional keys under 
  [healthcheck](https://docs.docker.com/reference/compose-file/services/#healthcheck) in the docker compose files
  including `interval`, `timeout`, `start_period`, and `start_interval`.

  The version 1 compose specification that docker uses is out of date and no longer maintained by docker.
  We currently have a mix of version 1 syntax and version 2 (specifically `2.20.2`+) syntax in our docker compose
  files.

  This means that the stack will not properly run with a docker compose version <`2.20.2`. For any version >`2.20.2` 
  the stack runs properly but displays lots of deprecation warnings about deprecated 
  [version strings](https://docs.docker.com/reference/compose-file/version-and-name/), [external
  volumes](https://docs.docker.com/reference/compose-file/volumes/#external) and [external 
  network](https://docs.docker.com/reference/compose-file/networks/#external) definitions.

  This PR updates all version 1 syntax so that these deprecation warnings are not displayed. Documentation has 
  been updated to make this dependency on a modern version of docker explicit.

  **Migration Steps**: 
    - if you are using a version of docker compose <`2.20.2` update your docker compose version
    - if you deploy any external components that use any of the old docker compose syntax you may want to update
      those docker compose files as well so that you aren't bombarded by deprecation warnings whenever you start
      the birdhouse stack.  

[2.10.1](https://github.com/bird-house/birdhouse-deploy/tree/2.10.1) (2025-03-10)
------------------------------------------------------------------------------------------------------------------

## Changes

- Update STAC app version to 1.0.1

  This update includes a bug fix which treats date-time values as ranges instead of strings when building 
  JSON schemas for use in queryables or collection summaries.
  See https://github.com/crim-ca/stac-app/pull/24 for more details.

[2.10.0](https://github.com/bird-house/birdhouse-deploy/tree/2.10.0) (2025-02-24)
------------------------------------------------------------------------------------------------------------------

## Changes

- Add the `prometheus-longterm-metrics` and `thanos` optional components

  The `prometheus-longterm-metrics` component collects longterm monitoring metrics from the original prometheus instance
  (the one created by the ``components/monitoring`` component).

  Longterm metrics are any prometheus rule that have the label ``group: longterm-metrics`` or in other words are
  selectable using prometheus's ``'{group="longterm-metrics"}'`` query filter. To see which longterm metric rules are
  added by default see the 
  ``optional-components/prometheus-longterm-metrics/config/monitoring/prometheus.rules.template`` file.

  To configure this component:

  * update the ``PROMETHEUS_LONGTERM_RETENTION_TIME`` variable to set how long the data will be kept by prometheus

  Enabling the `prometheus-longterm-metrics` component creates the additional endpoint ``/prometheus-longterm-metrics``.

  The `thanos` component enables better storage of longterm metrics collected by the 
  ``optional-components/prometheus-longterm-metrics`` component. Data will be collected from the
  ``prometheus-longterm-metrics`` and stored in an S3 object store indefinitely.
  
  When enabling this component, please change the default values for the ``THANOS_MINIO_ROOT_USER`` and ``THANOS_MINIO_ROOT_PASSWORD``
  by updating the ``env.local`` file. These set the login credentials for the root user that runs the 
  [minio](https://min.io/) object store.
  
- Enabling the `thanos` component creates the additional endpoints:

  * ``/thanos-query``: a prometheus-like query interface to inspect the data stored by thanos
  * ``/thanos-minio``: a minio web console to inspect the data stored by minio.

[2.9.1](https://github.com/bird-house/birdhouse-deploy/tree/2.9.1) (2025-02-10)
------------------------------------------------------------------------------------------------------------------

## Changes

- STAC: update `stac` component to version [1.0.0](https://github.com/crim-ca/stac-app/releases/tag/1.0.0)

  This update makes the `/queryables` endpoint run much more quickly by stashing the queryables data in the
  database instead of building it from scratch every time the `/queryables` endpoint was accessed.

  It also adds two new endpoints `PATCH /queryables` and `PATCH /summaries` which automatically update the
  queryables and collection summaries based on the data that is currently present in the database. See the
  [documentation](https://github.com/crim-ca/stac-app/blob/040d350ade758871b6e95db9c86c04202433ef0e/README.md)
  for more details.

[2.9.0](https://github.com/bird-house/birdhouse-deploy/tree/2.9.0) (2025-02-03)
------------------------------------------------------------------------------------------------------------------

## Changes

- JupyterHub: update `jupyterhub` component default version to [5.2.1](https://github.com/Ouranosinc/jupyterhub/releases/tag/5.2.1-20241114)

  This implements all changes between JupyterHub version 
  [4.1.6 and 5.2.1](https://jupyterhub.readthedocs.io/en/stable/reference/changelog.html).

  **Breaking backward incompatible change**: This update requires the following manual upgrade steps:

  - If your local environment file sets the `c.DockerSpawner.image_whitelist` config option in the 
    `JUPYTERHUB_ENABLE_MULTI_NOTEBOOKS` environnment variable. Change `c.DockerSpawner.image_whitelist` 
    to `c.DockerSpawner.allowed_images`.

  If you have changed any of the default `jupyterhub` settings you may need to consult the [JupyterHub upgrade
  guide](https://jupyterhub.readthedocs.io/en/latest/howto/upgrading-v5.html) to see if any of those settings
  have been changed.

[2.8.2](https://github.com/bird-house/birdhouse-deploy/tree/2.8.2) (2025-01-30)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Generic_bird broken because a DELAYED_EVAL is missing

  * Generic_bird consumes `FINCH_IMAGE` which is a delayed eval variable so
    generic_bird variable should also be a delayed eval variable.


## Changes

- Allow to override certbot image in `env.local` to easily test newer version
  and update to latest version.


[2.8.1](https://github.com/bird-house/birdhouse-deploy/tree/2.8.1) (2025-01-20)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Weaver: adjust missing `WEAVER_MANAGER_NAME` in healthchecks expecting matching `SCRIPT_NAME` configuration

  * Weaver's own `healthcheck` definition did not resolve to the expected endpoint.
  * Canarie-API `monitoring` endpoint for Weaver did not resolve to the expected endpoint.

[2.8.0](https://github.com/bird-house/birdhouse-deploy/tree/2.8.0) (2025-01-17)
------------------------------------------------------------------------------------------------------------------

## Changes

- Weaver: update `weaver` component default version to [6.1.1](https://github.com/crim-ca/weaver/tree/6.1.1).

  ### Relevant changes
  * Add support of *OGC API - Processes - Part 3: Workflows and Chaining* with *Nested Process* ad-hoc workflow.
  * Add support of *OGC API - Processes - Part 3: Workflows and Chaining* with *Remote Collection* (STAC and OGC).
  * Add support of *OGC API - Processes - Part 4: Job Management* endpoints for job "pending" creation and execution.
  * Add support of *OGC API - Processes - Part 4: Job Management* endpoints for job provenance as *W3C PROV* metadata.
  * Multiple alignment and fixes related to latest *OGC API - Processes - Part 1: Core* definitions regarding handling
    of input parameters and headers when submitting jobs to obtain alternate result representations and behavior.
  * Add HTML responses by default via web browsers or as requested by `Accept` headers or `f` query parameter.
  * Add improved CWL schema validation with `Weaver`-specific definitions where applicable
    (see https://github.com/crim-ca/weaver/tree/master/weaver/schemas/cwl).

- Weaver: modifications to `proxy` configurations for `weaver`

  * Add `WEAVER_ALT_PREFIX` optional variable that auto-configures `WEAVER_ALT_PREFIX_PROXY_LOCATION`,
    which allows setting an alternate endpoint to redirect requests to `weaver`.
    It uses `/ogcapi` by default which is a very common expectation from servers supporting OGC standards.
  * Use the `TWITCHER_VERIFY_PATH` approach to accelerate access of `weaver` resources authorization.
  * Modify proxy pass definitions and URL prefixes to resolve correctly with HTML resources.

[2.7.3](https://github.com/bird-house/birdhouse-deploy/tree/2.7.3) (2025-01-17)
------------------------------------------------------------------------------------------------------------------

## Changes

- Add integration test framework

  This update adds a framework for testing the deployed stack using pytest. This will allow developers to check
  that their changes are consistent with the existing stack and to add additionally tests when new functionality
  is introduced. 

  Changes to implement this include:

  - existing unit tests are moved to the `tests/unit/` directory
  - new integration tests are written in the `tests/integration/` directory. More tests will be added in the
    future!
  - `conftest.py` scripts updated to bring the stack up/down in a consistent way for the integration tests.
  - unit tests updated to accomodate new testing infrastructure as needed.
  - unit tests updated to test logging outputs better
  - `birdhouse` interface script updated to support testing infrastructure (this should not change anything for
    other end-users).
  - additional documentation added to `birdhouse` interface to improve user experience.
  - docker healthchecks added to more components so that the readiness of the stack can be determined with or
    without the use of the `canarie-api` component.
  - deprecates the `optional-components/wps-healthchecks` component since the healthchecks are now added by default
    to all WPS components.

  Next steps:

  - add more integration tests as needed
  - add a framework for testing migrating the stack from one version to another

[2.7.2](https://github.com/bird-house/birdhouse-deploy/tree/2.7.2) (2025-01-16)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Jupyterhub: allow users created before Cowbird was enabled to spawn jupyterlab

  Users created before Cowbird was enabled will not have a "workspace directory" created. A workspace directory
  is a symlink to the directory that contains their Jupyterhub data.
  
  When Cowbird is enabled, Jupyterhub checks if the workspace directory exists and raises an error if it doesn't.
  
  This change allows Jupyterhub to create the symlink if it doesn't exist instead of raising an error. 
  This means that users without a "workspace directory" will be able to continue using Jupyterhub as they did 
  before without the need for manual intervention by a system administrator who would otherwise need to manually
  create the symlink for them.

- Add resolver for http nginx configuration

  Nginx requires a resolver to be explicity defined when using `proxy_pass` with a variable in the argument passed
  to `proxy_pass`. This resolver is defined explicitly for the https server block but not for the http server block.

  This adds the explicit resolver for the http server block as well so that `proxy_pass` works when called using using
  http URLs as well.
  

[2.7.1](https://github.com/bird-house/birdhouse-deploy/tree/2.7.1) (2024-12-20)
------------------------------------------------------------------------------------------------------------------

## Changes

- Updated Cowbird to version 2.5.0

  This update fixes an issue where Magpie reports a webhook failure on almost every action.
  See a full description of the issue in https://github.com/Ouranosinc/cowbird/pull/78.

[2.7.0](https://github.com/bird-house/birdhouse-deploy/tree/2.7.0) (2024-12-19)
------------------------------------------------------------------------------------------------------------------

## Changes

- Enable local deployment to improve development and testing

  The Birdhouse stack can now be deployed locally and accessed on a browser on the host machine without the need 
  for an SSL certificate. This is useful for local development and for running tests against the full stack while developing and in CI environments.

  To enable this, add the new `optional-components/local-dev-test` component to `BIRDHOUSE_EXTRA_CONF_DIRS` and
  set the following environment variables in the local environment file:

  * `export BIRDHOUSE_FQDN=host.docker.internal`
  * `export BIRDHOUSE_HTTP_ONLY=True`

  You should also add ``host.docker.internal`` to your ``/etc/hosts`` file pointing to the loopback address so 
  that URLs generated by Birdhouse that refer to ``host.docker.internal`` will resolve properly in a browser:

  ```
  echo '127.0.0.1    host.docker.internal' | sudo tee -a /etc/hosts
  ```

  After deploying the stack, you can now interact with the Birdhouse software at ``http://host.docker.internal`` 
  from the machine that is the docker host.

  In order to implement the changes above, the following non-breaking changes have been made to the deployment code:

  - added a configuration variable `BIRDHOUSE_HTTP_ONLY` which is not set by default. If set to `True` the `proxy` component will only serve content over `http` (not `https`).
  - added the following configuration variables. These should not be set directly unless you really know what you're doing:
    - `BIRDHOUSE_PROXY_SCHEME`: default remains `https`. If `BIRDHOUSE_HTTP_ONLY` is `True` then the default becomes `http`
    - `PROXY_INCLUDE_HTTPS`: default remains `include /etc/nginx/conf.d/https.include;`. If `BIRDHOUSE_HTTP_ONLY` is `True`, the default is that the variable is unset. 
  - changed the default values for the following configuration variables:
    - `BIRDHOUSE_ALLOW_UNSECURE_HTTP`: default remains `""`. If `BIRDHOUSE_HTTP_ONLY` is `True` then the default becomes `True`.
  - logs are written to stderr by default. Previously they were written to stdout.
    - this allows us to call scripts and programmatically use their outputs. Previously log entries would need to be 
      manually filtered out before program outputs could be used.
    - added the `--log-stdout` and `--log-file` flags to the `bin/birdhouse` interface to allow redirecting logs to 
      stdout or to a specific file instead.
    - log redirection can also now be set using environment variables:
      - `BIRDHOUSE_LOG_FD` can be used to redirect logs to a file descriptor (ex: `BIRDHOUSE_LOG_FD=3`)
      - `BIRDHOUSE_LOG_FILE` can be used to redirect logs to file (ex: `BIRDHOUSE_LOG_FILE=/some/file/on/disk.log`)
      - Note that the variables here should not be set in the local environment file since that file is sourced **after**
        some logs are written. Instead, set these by exporting them in the parent process that calls `bin/birdhouse`.
    - for backwards compatibility, if scripts are not called through the `bin/birdhouse` interface, logs will still be 
      written to stdout.

[2.6.5](https://github.com/bird-house/birdhouse-deploy/tree/2.6.5) (2024-12-18)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Fix incorrect Geoserver URL in Cowbird configuration

  The Geoserver URL in the Cowbird configuration was incorrect as it used a non-standard port.
  This changes the URL to the one used by docker compose internally. This allows Cowbird to execute
  webhooks that target Geoserver.

[2.6.4](https://github.com/bird-house/birdhouse-deploy/tree/2.6.4) (2024-12-09)
------------------------------------------------------------------------------------------------------------------

## Fixes

- canarie-api: fix new Thredds v5 monitoring URL

  Fix the error below at the URL https://HOST/canarie/node/service/stats:
  Bad return code from http://thredds:8080//twitcher/ows/proxy/thredds/catalog.html (Expecting 200, Got 404

  Old URL: http://thredds:8080//twitcher/ows/proxy/thredds/catalog.html
  New URL: http://thredds:8080/twitcher/ows/proxy/thredds/catalog/catalog.html

  An oversight from the previous PR
  https://github.com/bird-house/birdhouse-deploy/pull/413


[2.6.3](https://github.com/bird-house/birdhouse-deploy/tree/2.6.3) (2024-12-05)
------------------------------------------------------------------------------------------------------------------

## Changes

- Update Thredds to supported version

  Unidata has dropped support for TDS versions < 5.x. This updates Thredds to version 5.5.

  This Thredds v5 actually have 2 minors issues
  * Magpie Allow or Deny exception under top-level Allow or Deny do not work on NCSS only,
    see [Ouranosinc/Magpie#633](https://github.com/Ouranosinc/Magpie/issues/633).
  * Performance problem with WMS only, see [Unidata/tds#406](https://github.com/Unidata/tds/issues/406).

  They are considered minor and not blocking the release because
  * Magpie top-level Allow or Deny still work across the board,
    exception under top-level also works across the board,
    except for NCSS only and NCSS is not widely used.
  * WMS is not widely used, similar to NCSS.

  Other features from this newer Thredds
  * Security fixes (newer Tomcat) and if there is a critical vulnerability,
    we won't be able to stay on v4 series because it is not even available on
    DockerHub anymore as Unidata has dropped support.
  * New experimental Zarr support.


[2.6.2](https://github.com/bird-house/birdhouse-deploy/tree/2.6.2) (2024-12-03)
------------------------------------------------------------------------------------------------------------------

## Changes

- Fix help string description for `bin/birdhouse configs` command

  Update description of the `configs` subcommand to better describe it.
  The description when calling `bin/birdhouse -h` now matches the description when calling `bin/birdhouse configs -h`
  
- Jupyterhub: Update recommended paths for public share folders

  The recommended public share folders in the `env.local.example` file create a conflict with the default
  `PUBLIC_WORKSPACE_WPS_OUTPUTS_SUBDIR` path when both are enabled and mounted on a Jupyterlab container.
  This change updates the recommended paths for the public share folders to avoid this conflict and adds a
  warning helping users to avoid this conflict.

  Note: the conflict arises when `PUBLIC_WORKSPACE_WPS_OUTPUTS_SUBDIR` is mounted to a container as read-only
  volume and then Jupyterhub tries to mount the public share folder within that volume. Since the parent volume
  is read-only, the second volume mount fails.


## Fixes

- Correct docker image for `stac-populator` optional component

  This sets the docker image for the `stac-populator` component to a version that actually contains the code
  that is executed when `stac-populator` is called. The previous image no longer contained the relevant code.

[2.6.1](https://github.com/bird-house/birdhouse-deploy/tree/2.6.1) (2024-11-22)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Fix regressions introduced by PR #359 "Flexible locations for data served by thredds"

  In [PR #359](https://github.com/bird-house/birdhouse-deploy/pull/359/):

  `secure-thredds/config/magpie/permissions.cfg` started to use variable but was never renamed to `.template`
  so those variable never get template expanded
  (commit [317d96c3](https://github.com/bird-house/birdhouse-deploy/commit/317d96c39db7a6d79d1568a7094441ccdedc55ae)).

  `bootstrap-testdata` default value was removed but did not source `read-configs.include.sh` so the variable
   stayed blank (commit [4ab0fc74](https://github.com/bird-house/birdhouse-deploy/commit/4ab0fc74cb8fa601d75ecfc2a94749b23f60109c)).
   The default value was there initially so the script can be used in standalone situation (not inside a checkout).


[2.6.0](https://github.com/bird-house/birdhouse-deploy/tree/2.6.0) (2024-11-19)
------------------------------------------------------------------------------------------------------------------

## Changes

- Add the `prometheus-log-parser` optional component

  This component parses log files from other components and converts their logs to prometheus
  metrics that are then ingested by the monitoring Prometheus instance (the one created by the
  `components/monitoring` component).

  For more information on how this component reads log files and converts them to prometheus components see
  the [log-parser](https://github.com/DACCS-Climate/log-parser/) documentation.

  To configure this component:

  * set the `PROMETHEUS_LOG_PARSER_POLL_DELAY` variable to a number of seconds to set how often the log parser
    checks if new lines have been added to log files (default: 1)
  * set the `PROMETHEUS_LOG_PARSER_TAIL` variable to `"true"` to only parse new lines in log files. If unset,
    this will parse all existing lines in the log file as well (default: `"true"`)

  To view all metrics exported by the log parser:

  * Navigate to the `https://<BIRDHOUSE_FQDN>/prometheus/graph` search page
  * Put `{job="log_parser"}` in the search bar and click the "Execute" button

- Update the prometheus version to the current latest `v2.53.3`. This is required to support   
  loading multiple prometheus scrape configuration files with the `scrape_config_files`
  configuration option.

[2.5.5](https://github.com/bird-house/birdhouse-deploy/tree/2.5.5) (2024-11-14)
------------------------------------------------------------------------------------------------------------------

## Changes
- Jupyter env: new full build with latest of everything

  See [Ouranosinc/PAVICS-e2e-workflow-tests#137](https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/137)
  for more info.


[2.5.4](https://github.com/bird-house/birdhouse-deploy/tree/2.5.4) (2024-10-31)
------------------------------------------------------------------------------------------------------------------

## Changes

- THREDDS: add more options to configure `catalog.xml`
  - The default THREDDS configuration creates two default datasets, the *Service Data* dataset and the 
    *Main* dataset. The *Service Data* dataset is used internally and hosts WPS outputs. The *Main* dataset is the
    place where users can access data served by THREDDS. Both of these are configured to serve files with the following 
    extensions: .nc .ncml .txt .md .rst .csv

  - In order to allow the THREDDS server to serve files with additional extensions, this introduces two new
    variables:
    - `THREDDS_SERVICE_DATA_EXTRA_FILE_FILTERS`: this allows users to specify additional [filter 
        elements](https://docs.unidata.ucar.edu/tds/current/userguide/tds_dataset_scan_ref.html#including-only-desired-files) to the *Service Data* dataset. This is especially useful if a WPS 
        outputs files with an extension other than the default (eg: .h5) to the `wps_outputs/` directory.
    - `THREDDS_DATASET_DATASETSCAN_BODY`: this allows users to specify the whole body of the *Main* dataset's 
       [`<datasetScan>`](https://docs.unidata.ucar.edu/tds/current/userguide/tds_dataset_scan_ref.html) element.
       This allows users to fully customize how this dataset serves files.

  - We limit the configuration options for the *Service Data* dataset more than the *Main* dataset because the *Service
    Data* dataset requires a basic configuration in order to properly serve WPS outputs. Making significant changes
    to this configuration could have unexpected negative impacts on WPS usage.

  - In order to allow customization of the Magpie THREDDS configuration in case new file extensions are added we introduce
    two additional variables:
    - `THREDDS_MAGPIE_EXTRA_METADATA_PREFIXES`: additional file prefixes (ie. regular expression match patterns) that Magpie
      should treat as metadata (accessible with "browse" permissions).
    - `THREDDS_MAGPIE_EXTRA_DATA_PREFIXES`: additional file prefixes (ie. regular expression match patterns) that Magpie
      should treat as data (accessible with "read" permissions).

  - The defaults for these new variables are fully backwards compatible. Without changing these variables, the THREDDS
    server should behave exactly the same as before except that .md files and .rst files are now considered metadata
    files according to the Magpie configuration, meaning that they can now be viewed with "browse" permissions.

[2.5.3](https://github.com/bird-house/birdhouse-deploy/tree/2.5.3) (2024-09-11)
------------------------------------------------------------------------------------------------------------------

## Changes

- Magpie/Twitcher: update Python packages and base Docker image to address security vulnerabilities 

  - [Magpie 4.1.1](https://github.com/Ouranosinc/Magpie/blob/master/CHANGES.rst#411-2024-07-23)
    (relates to [Ouranosinc/Magpie#622](https://github.com/Ouranosinc/Magpie/pull/622)).
  - [Twitcher 0.10.0](https://github.com/bird-house/twitcher/blob/master/CHANGES.rst#0100-2024-07-22)
    (relates to [bird-house/twitcher#136](https://github.com/bird-house/twitcher/pull/136)).

- xclim-testdata: adapt repository cloning script to the new data structure

  The `xclim-testdata` repo has been restructured to include the data in a `data` subdirectory.
  This change updates the cloning script to account for this new structure and to ensure that the
  user experience is consistent with the previous version.

  See:
  * [xclim-testdata PR/29](https://github.com/Ouranosinc/xclim-testdata/pull/29)
  * [xclim PR/1889](https://github.com/Ouranosinc/xclim/pull/1889)

[2.5.2](https://github.com/bird-house/birdhouse-deploy/tree/2.5.2) (2024-07-19)
------------------------------------------------------------------------------------------------------------------

## Changes

- GeoServer: upgrade to 2.25.2 to fix vulnerabilities

  See:
  * https://nsfocusglobal.com/remote-code-execution-vulnerability-between-geoserver-and-geotools-cve-2024-36401-cve-2024-36404-notification/
  * https://github.com/geoserver/geoserver/security/advisories/GHSA-6jj6-gm7p-fcvv
  * https://github.com/geotools/geotools/security/advisories/GHSA-w3pj-wh35-fq8w

  This change will upgrade to GeoServer 2.25.2 and GeoTools 31.2 (the version of `gt-complex.jar`).

  ```shell
  $ docker exec -u 0 geoserver find / -iname '**gt-complex**'
  /usr/local/tomcat/webapps/geoserver/WEB-INF/lib/gt-complex-31.2.jar
  ```

  The previous version was GeoServer 2.22.2 and GeoTools 28.2.

  ```shell
  $ docker exec -u 0 geoserver find / -iname '**gt-complex**'
  /usr/local/tomcat/webapps/geoserver/WEB-INF/lib/gt-complex-28.2.jar
  ```

  Also enable
  * OGC-API plugins https://docs.geoserver.org/stable/en/user/community/ogc-api/features/index.html
    so we can slowly transition from the WPS plugin.
  * STAC Datastore plugin https://docs.geoserver.org/latest/en/user/community/stac-datastore/index.html
    so we can test integration with our STAC component.


[2.5.1](https://github.com/bird-house/birdhouse-deploy/tree/2.5.1) (2024-07-10)
------------------------------------------------------------------------------------------------------------------

- Cowbird: bump version to [2.4.0](https://github.com/Ouranosinc/cowbird/blob/master/CHANGES.rst#240-2024-07-09).

  - Includes multiple dependency updates for latest security and performance improvements.

[2.5.0](https://github.com/bird-house/birdhouse-deploy/tree/2.5.0) (2024-06-20)
------------------------------------------------------------------------------------------------------------------

## Changes

- Weaver: bump version to [5.6.1](https://github.com/crim-ca/weaver/tree/5.6.1).

  - See full changes details in 
    [Weaver changes](https://pavics-weaver.readthedocs.io/en/latest/changes.html#changes-5-6-1)
  - In summary:
    - multiple control setting options to customize some behaviors
    - improved *OGC API - Processes* standard conformance
    - improved support of *Common Workflow Language (CWL)* features (secrets, sub-workflow, auth-propagation, etc.)

- Weaver: WPS retry logic on post-compose step.
  - Apply `--network birdhouse_default` to the Docker `curl` image to allow HTTP requests to properly resolve
    against the running services (WPS bird providers, Weave and Magpie). In some cases, this network would not
    be automatically resolved.
  - Fix the index used during HTTP request retry to avoid going one step over the intended retry attempts.

[2.4.2](https://github.com/bird-house/birdhouse-deploy/tree/2.4.2) (2024-06-12)
------------------------------------------------------------------------------------------------------------------

## Changes
- deploy-data: allow more flexibility to deploy files from other checkout in same config file

  Given the config file can specify multiple checkouts, this flexibility to
  have `SRC_DIR` be an absolute path will allow one checkout to take files from
  other checkouts, using absolute path to the other checkouts.  `SRC_DIR` can
  still be a relative path of the current checkout, as before, to preserve
  backward-compatibility.

  Possible use-case: re-organize the layout of various files from the various
  checkouts in an intermediate location before rsyncing this intermediate
  location to the final destination.


[2.4.1](https://github.com/bird-house/birdhouse-deploy/tree/2.4.1) (2024-06-05)
------------------------------------------------------------------------------------------------------------------

## Fixes
- Weaver: Adjust invalid `data_sources.yml` definitions.

  - Add the missing `data_sources.yml` volume mount for  `weaver-worker`.
  - When `weaver-worker` runs a `Workflow`, the nested `step` process locations need to be resolved according to the
    current `"localhost"` instance. However, the Web API running in `weaver` service is not visible from the worker.
    Since the configuration is shared between `weaver` and `weaver-worker`, use the public endpoint of `weaver` to
    make process URL resolution consistent, and also provide more useful references in job logs when resolution fails.

[2.4.0](https://github.com/bird-house/birdhouse-deploy/tree/2.4.0) (2024-06-04)
------------------------------------------------------------------------------------------------------------------

## Changes
- Rename variables, constants and files from PAVICS to Birdhouse

  For historical reasons the name PAVICS was used in variable names, constants and filenames in this repo to refer
  to the software stack in general. This was because, for a long time, the PAVICS deployment of this stack was the
  only one that was being used in production. However, now that multiple deployments of this software exist in
  production (that are not named PAVICS), we remove unnecessary references to PAVICS in order to reduce confusion
  for maintainers and developers who may not be aware of the historical reasons for the PAVICS name.

  This update makes the following changes:

  * The string ``PAVICS`` in environment variables, constant values, and file names have been changed to 
    ``BIRDHOUSE`` (case has been preserved where possible).
    * For example:
      * ``PAVICS_FQDN`` -> ``BIRDHOUSE_FQDN``
      * ``pavics_compose.sh`` -> ``birdhouse_compose.sh``
      * ``THREDDS_DATASET_LOCATION_ON_CONTAINER='/pavics-ncml'`` -> ``THREDDS_DATASET_LOCATION_ON_CONTAINER='/birdhouse-ncml'``
  * Comment strings and documentation that refers to the software stack as ``PAVICS`` have been changed to use
    ``Birdhouse``.
  * Recreated the ``pavics-compose.sh`` script that runs ``birdhouse-compose.sh`` in backwards compatible mode.
    * Backwards compatible mode means that variables in ``env.local`` that contain the string ``PAVICS`` will be used
      to set the equivalent variable that contains ``BIRDHOUSE``. For example, the ``PAVICS_FQDN`` variable set in
      the ``env.local`` file will be used to set the value of ``BIRDHOUSE_FQDN``.
  * Removed unused variables:
    * `CMIP5_THREDDS_ROOT`

- Create a new CLI entrypoint in ``bin/birdhouse`` that can be used to invoke ``pavics-compose.sh`` or 
  ``birdhouse-compose.sh`` from one convenient location. This script also includes some useful options and provides
  a generic entrypoint to the stack that can be extended in the future. In the future, users should treat this
  entrypoint as the only stable CLI for interacting with the Birdhouse software.

### Migration Guide

  - Update ``env.local`` file to replace all variables that contain ``PAVICS`` with ``BIRDHOUSE``.
    Variable names have also been updated to ensure that they start with the prefix ``BIRDHOUSE_``.
    * see [`env.local.example`](./birdhouse/env.local.example) to see new variable names
    * see the ``BIRDHOUSE_BACKWARDS_COMPATIBLE_VARIABLES`` variable (defined in [`default.env`](./birdhouse/default.env)) for a 
      full list of changed environment variable names.
  - Update any external scripts that access the old variable names directly to use the updated variable names.
  - Update any external scripts that access any of the following files to use the new file name:

    | old file name           | new file name              |
    |-------------------------|----------------------------|
    | pavics-compose.sh       | birdhouse-compose.sh       |
    | PAVICS-deploy.logrotate | birdhouse-deploy.logrotate |
    | configure-pavics.sh     | configure-birdhouse.sh     |
    | trigger-pavicscrawler   | trigger-birdhousecrawler   |

  - Update any external scripts that called ``pavics-compose.sh`` or ``read-configs.include.sh`` to use the CLI 
    entrypoint in ``bin/birdhouse`` instead.
  - The following default values have changed. If your deployment was using the old default value, update your 
    ``env.local`` file to explicitly set the old default values.

    | old variable name                          | new variable name                    | old default value       | new default value          |
    |--------------------------------------------|--------------------------------------|-------------------------|:---------------------------|
    | POSTGRES_PAVICS_USERNAME                   | BIRDHOUSE_POSTGRES_USERNAME          | postgres-pavics         | postgres-birdhouse         |
    | THREDDS_DATASET_LOCATION_ON_CONTAINER      | (no change)                          | /pavics-ncml            | /birdhouse-ncml            |
    | THREDDS_SERVICE_DATA_LOCATION_ON_CONTAINER | (no change)                          | /pavics-data            | /birdhouse-data            |
    | (hardcoded)                                | BIRDHOUSE_POSTGRES_DB                | pavics                  | birdhouse                  |
    | PAVICS_LOG_DIR                             | BIRDHOUSE_LOG_DIR                    | /var/log/PAVICS         | /var/log/birdhouse         |
    | (hardcoded)                                | GRAFANA_DEFAULT_PROVIDER_FOLDER      | Local-PAVICS            | Local-Birdhouse            |
    | (hardcoded)                                | GRAFANA_DEFAULT_PROVIDER_FOLDER_UUID | local-pavics            | local-birdhouse            |
    | (hardcoded)                                | GRAFANA_PROMETHEUS_DATASOURCE_UUID   | local_pavics_prometheus | local_birdhouse_prometheus |

    Note that the `PAVICS_LOG_DIR` variable was actually hardcoded as `/var/log/PAVICS` in some scripts. If 
    `PAVICS_LOG_DIR` was set to anything other than `/var/log/PAVICS` you'll end up with inconsistent log outputs as 
    previously some logs would have been sent to `PAVICS_LOG_DIR` and others to `/var/log/PAVICS`. We recommend merging
    these two log files. Going forward, all logs will be sent to `BIRDHOUSE_LOG_DIR`. 

  - Update any jupyter notebooks that make use of the `PAVICS_HOST_URL` environment variable to use the new
    `BIRDHOUSE_HOST_URL` instead.
  - Set the ``BIRDHOUSE_POSTGRES_DB`` variable to ``pavics`` in the ``env.local`` file. This value was previously
    hardcoded to the string ``pavics`` so to maintain backwards compatibility with any existing databases this should be
    kept the same. If you do want to update to the new database name, you will need to rename the existing database.
    For example, the following will update the existing database named ``pavics`` to ``birdhouse`` (assuming the old
    default values for the postgres username):

    ```shell
    docker exec -it postgres psql -U postgres-pavics -d postgres -c 'ALTER DATABASE pavics RENAME TO birdhouse'
    ```

    You can then update the ``env.local`` file to the new variable name and restart the stack
  - Set the ``BIRDHOUSE_POSTGRES_USER`` variable to ``postgres-pavics`` in the ``env.local`` file if you would like to 
    preserve the old default value. If you would like to change the value of ``BIRDHOUSE_POSTGRES_USER`` then also 
    update the name for any running postgres instances. For example, the following will update the user named 
    ``postgres-pavics`` to ``postgres-birdhouse``:

    ```shell
    docker exec -it postgres psql -U postgres-pavics -d postgres -c 'CREATE USER "tmpsuperuser" WITH SUPERUSER'
    docker exec -it postgres psql -U tmpsuperuser -d postgres -c 'ALTER ROLE "postgres-pavics" RENAME TO "postgres-birdhouse"'
    docker exec -it postgres psql -U tmpsuperuser -d postgres -c 'ALTER ROLE "postgres-birdhouse" WITH PASSWORD '\''postgres-qwerty'\'
    docker exec -it postgres psql -U postgres-birdhouse -d postgres -c 'DROP ROLE "tmpsuperuser"'
    ```

    Note that the ``postgres-qwerty`` value is meant just for illustration, you should replace this with the value of 
    the ``BIRDHOUSE_POSTGRES_PASSWORD`` variable.
    Note that you'll need to do the same for the ``stac-db`` service as well (assuming that you weren't previously
    overriding the ``STAC_POSTGRES_USER`` with a custom value).

[2.3.3](https://github.com/bird-house/birdhouse-deploy/tree/2.3.3) (2024-05-29)
------------------------------------------------------------------------------------------------------------------

## Changes

- Bump cadvisor version to the latest version: v0.49.1
  - See the cadvisor repo for all changes: https://github.com/google/cadvisor/compare/v0.36.0...v0.49.1
  - This updated was prompted by the fact that the previously installed version of cadvisor (v0.36.0) did not support
    newer versions of docker. When deploying this repo with recent docker version, cadvisor was unable to discover or 
    monitor running containers.

[2.3.2](https://github.com/bird-house/birdhouse-deploy/tree/2.3.2) (2024-05-27)
------------------------------------------------------------------------------------------------------------------

## Changes

- Make the monitoring component docker images configurable
  - The following variables have been added to the `components/monitoring/default.env` file and can be overridden in 
    `env.local` to change the docker image for one of the services enabled by the monitoring component:
    - `GRAFANA_VERSION`
    - `GRAFANA_DOCKER`
    - `CADVISOR_VERSION`
    - `CADVISOR_DOCKER`
    - `PROMETHEUS_VERSION`
    - `PROMETHEUS_DOCKER`
    - `NODE_EXPORTER_VERSION`
    - `NODE_EXPORTER_DOCKER`
    - `ALERTMANAGER_VERSION`
    - `ALERTMANAGER_DOCKER`
  - Note that the defaults are the same as the previous hardcoded versions so this change is fully backwards compatible.

[2.3.1](https://github.com/bird-house/birdhouse-deploy/tree/2.3.1) (2024-05-21)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Scripts that read configuration settings and that exit early on error fail unexpectedly

  - Scripts that call `set -e` before reading configuration settings were failing early because some lines are
    intentionally returning a non-zero value when setting variable defaults. This change modifies lines that may return 
    a non-zero status but should not cause the script to exit early.
  - Scripts that were exiting early prior to this change include:
    - birdhouse/deployment/fix-geoserver-data-dir-perm
    - birdhouse/deployment/fix-write-perm
    - birdhouse/deployment/trigger-deploy-notebook

[2.3.0](https://github.com/bird-house/birdhouse-deploy/tree/2.3.0) (2024-05-14)
------------------------------------------------------------------------------------------------------------------

## Changes

- bump canarie-api version to [1.0.0](https://github.com/Ouranosinc/CanarieAPI/releases/tag/1.0.0)

  - This version of canarie-api permits running the proxy (nginx) container independently of the canarie-api
    application. This makes it easier to monitor the logs of canarie-api and proxy containers simultaneously and
    allows for the configuration files for canarie-api to be mapped to the canarie-api containers where appropriate.

[2.2.2](https://github.com/bird-house/birdhouse-deploy/tree/2.2.2) (2024-05-11)
------------------------------------------------------------------------------------------------------------------

## Changes
- Jupyter env: new full build with latest of almost everything

  See [Ouranosinc/PAVICS-e2e-workflow-tests#121](https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/121)
  for more info.


[2.2.1](https://github.com/bird-house/birdhouse-deploy/tree/2.2.1) (2024-05-01)
------------------------------------------------------------------------------------------------------------------

## Changes

- bump jupyterhub version to 4.1.5-20240426
  
  - This is the latest bugfix update to jupyterhub after the release of version 4.1.0. There haven't been any additional
    updates for a few weeks now, so we can assume that this version is relatively stable now. See the [jupyterhub 
    changelog](https://jupyterhub.readthedocs.io/en/stable/reference/changelog.html) for details.

## Fixes

- docs: Fix version of `sphinx-mdinclude` to address incompatible `docutils` operation under ReadTheDocs Sphinx build.

  - See [docutils 0.21 changes](https://docutils.sourceforge.io/RELEASE-NOTES.html#release-0-21-2024-04-09).
  - See issue [sphinx-mdinclude#47](https://github.com/omnilib/sphinx-mdinclude/issues/47)
    and PR [sphinx-mdinclude#55](https://github.com/omnilib/sphinx-mdinclude/pull/55).

[2.2.0](https://github.com/bird-house/birdhouse-deploy/tree/2.2.0) (2024-04-18)
------------------------------------------------------------------------------------------------------------------

## Changes

- Node Services: Add definitions and variables for every service represented by
  the [DACCS-Climate/Marble-node-registry](https://github.com/DACCS-Climate/Marble-node-registry).

  - Add `version` field using the corresponding `<SERVICE>_VERSION` variables.
  - Add `types` field restricted by specific values instead of previous `keywords` expected to be extendable.
  - Add `<SERVICE>_IMAGE_URI` variables to provide `rel: service-meta` link for every service.
  - Update all `$schema` references of service node registry
    to [1.2.0](https://github.com/DACCS-Climate/Marble-node-registry/releases/tag/1.2.0) instead of `main`.
    During unit tests, specific `$schema` reference in the respective service configuration will be used for validation.
  
  See [bird-house/birdhouse-deploy#441](https://github.com/bird-house/birdhouse-deploy/issues/441) for more details.

[2.1.3](https://github.com/bird-house/birdhouse-deploy/tree/2.1.3) (2024-04-09)
------------------------------------------------------------------------------------------------------------------

## Fixes
- GeoServer: fix invalid media-type specified for the service's endpoint in `service-config.json.template`
- Jupyterhub: fix authentication bug when changing settings
  
  If the `JUPYTERHUB_AUTHENTICATOR_AUTHORIZATION_URL` variable or `JUPYTERHUB_CRYPT_KEY` is unset without clearing the 
  jupyterhub database, users could no longer spawn jupyterlab servers. 

[2.1.2](https://github.com/bird-house/birdhouse-deploy/tree/2.1.2) (2024-03-25)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Weaver: celery-healthcheck: update regular expression

  The `celery-healthcheck` file which checks if celery node is online when weaver starts up was using an outdated
  regular expression to check if a node was online or not. This has been fixed so that this script can now reliably
  check whether the node is available or not.

[2.1.1](https://github.com/bird-house/birdhouse-deploy/tree/2.1.1) (2024-03-06)
------------------------------------------------------------------------------------------------------------------

## Changes

- logging: decrease logging level for empty optional vars from WARN to DEBUG

  To avoid drowning real WARN messages.  Many optional vars can be valid if empty.

- config: add sample config to configure docker-compose to remove orphans

  To remove orphans containers when components are disabled.  Also link to full
  documentations if other env var can be used.

- compose script: allow to pass extra options to `up` operation

  The previous docker-compose built-in env var was not working so had to add
  this homegrown solution.

  When disabling components, their existing containers will not be removed
  unless option `--remove-orphans` is given together with  `./pavics-compose.sh up -d`.

  This change allow any additional options, not just `--remove-orphans`.

- compose script: exit early when any errors occurred during invocation

  Before, all the `post-docker-compose-up` would still execute after
  `docker-compose` has an error.


[2.1.0](https://github.com/bird-house/birdhouse-deploy/tree/2.1.0) (2024-02-23)
------------------------------------------------------------------------------------------------------------------

## Changes
- Compose script utilities:
  * Add `BIRDHOUSE_COLOR` option and various logging/messaging definitions in `birdhouse/scripts/logging.include.sh`.
  * Replace all explicit color "logging" related `echo` in scripts by a utility `log {LEVEL} {message}` function
    that employs variables `LOG_DEBUG`, `LOG_INFO`, `LOG_WARN`, `LOG_ERROR` and `LOG_CRITICAL` as applicable per
    respective messages to report logging messages in a standard approach.
    Colors can be disabled with `BIRDHOUSE_COLOR=0` and logging level can be set with `BIRDHOUSE_LOG_LEVEL={LEVEL}`
    where all levels above or equal to the configured one will be displayed (default logging level is `INFO`).
  * Unify all `birdhouse/scripts` utilities to employ the same `COMPOSE_DIR` variable (auto-resolved or explicitly set)
    in order to include or source any relevant dependencies they might have within the `birdhouse-deploy` repository.
  * Add `info` option (ie: `pavics-compose.sh info`) that will stop processing just before `docker-compose` call.
    This can be used to perform a "dry-run" of the command and validate that was is loaded is as expected, by inspecting
    provided log messages.
  * Replace older backtick (``` ` ```) executions by `$(...)` representation except for `eval` calls that require
    them for backward compatibility of `sh` on some server instances.
  * Modify the `sh -x` calls to scripts listed in `COMPONENT_PRE_COMPOSE_UP` and `COMPONENT_POST_COMPOSE_UP` to employ
    the `-x` flag (showing commands) only when `BIRDHOUSE_LOG_LEVEL=DEBUG`.

- Defaults:
  * Add multiple `SERVER_[...]` variables with defaults using previously hard coded values referring to PAVICS.
    These variables use a special combination of `DELAYED_EVAL` and `OPTIONAL_VARS` definitions that can make use
    of a variable formatted as `<ANY_NAME>='${__DEFAULT__<ANY_NAME>}'` that will print a warning messages indicating
    that the default is employed, although *STRONGLY* recommended to be overridden. This allows a middle ground between
    backward-compatible `env.local` while flagging potentially misused configurations.

## Fixes
- Canarie-API: updated references
  * Use the new `SERVER_[...]` variables.
  * Replace the LICENSE URL of the server node pointing
    at [Ouranosinc/pavics-sdi](https://github.com/Ouranosinc/pavics-sdi) instead
    of intended [bird-house/birdhouse-deploy](https://github.com/bird-house/birdhouse-deploy).
- Magpie: ensure that the `MAGPIE_ADMIN_USERNAME` variable is respected
  * When determining the `JUPYTERHUB_ADMIN_USERS` variable
  * Double check that it is being respected everywhere else
- env.local.example: fix `JUPYTERHUB_CONFIG_OVERRIDE` comment section

  `JUPYTERHUB_CONFIG_OVERRIDE` was disconnected from its sample code.

[2.0.6](https://github.com/bird-house/birdhouse-deploy/tree/2.0.6) (2024-02-15)
------------------------------------------------------------------------------------------------------------------

## Changes

- Weaver: add option to automatically unregister old providers

  Introduces the `WEAVER_UNREGISTER_DROPPED_PROVIDERS` variable. If set to "True", Weaver providers that are no longer 
  working (not responding when deployed) and are not named in `WEAVER_WPS_PROVIDERS` will be unregistered. This is  
  useful when deploying Weaver with fewer providers than a previous deployment.

  For example, if the stack is deployed with the Weaver, Finch, and Raven components. Then later deployed with just
  Weaver and Raven, the Finch provider will be unregistered from weaver.

  Previously, the Finch provider would have remained as a Weaver provider despite the fact that it has been removed from
  the stack.

[2.0.5](https://github.com/bird-house/birdhouse-deploy/tree/2.0.5) (2024-01-22)
------------------------------------------------------------------------------------------------------------------

## Changes
- Jupyter env: new incremental build for compatibility with upcoming Thredds v5

  See https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/134 for more info.


[2.0.4](https://github.com/bird-house/birdhouse-deploy/tree/2.0.4) (2024-01-18)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Allow users to log in to Jupyterhub with their email address

  Previously, JupyterHub's `MagpieAuthenticator` class treated the email address entered into the username field as
  the username itself. This led to a mismatch between the username in JupyterHub and the username in Magpie.
  To resolve this, we update the JupyterHub docker image to a version where this bug is fixed. 

  See https://github.com/Ouranosinc/jupyterhub/pull/26 and https://github.com/Ouranosinc/Magpie/issues/598 for 
  reference.

[2.0.3](https://github.com/bird-house/birdhouse-deploy/tree/2.0.3) (2024-01-16)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Autodeploy broken due to instanciated left-over files in ./config/ dir

  The `.gitignore` syntax was wrong.  Regression from v2.0.0.


[2.0.2](https://github.com/bird-house/birdhouse-deploy/tree/2.0.2) (2023-12-15)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Cowbird README file disappears now that cowbird is a default component

  The settings to enable the Cowbird README file (added in version 1.41.0) assumed that the cowbird component would
  be loaded after the juptyerhub component. Now that the cowbird component is part of the `DEFAULT_CONF_DIRS` and
  therefore will always be loaded first, this updates the settings so that the README file will be enabled given the new
  component load order.

[2.0.1](https://github.com/bird-house/birdhouse-deploy/tree/2.0.1) (2023-12-11)
------------------------------------------------------------------------------------------------------------------

## Changes
- Code documentation: provide an additional reason to not exit early if a directory listed in the `EXTRA_CONF_DIRS` variable does not exist.

## Fixes
- Twitcher: unable to change log level because of typo in qualname config


[2.0.0](https://github.com/bird-house/birdhouse-deploy/tree/2.0.0) (2023-12-11)
------------------------------------------------------------------------------------------------------------------

## Changes

- Update `DEFAULT_CONF_DIRS` to the minimal components required to deploy the stack

  Changes `DEFAULT_CONF_DIRS` to refer exclusively to the proxy, magpie, twitcher, stac, and cowbird components.
  Also moves all components that were previously under the `birdhouse/config` directory to the `birdhouse/components`
  directory. This removes the arbitrary distinction between these groups of components that didn't have any functional
  or logical reason.

  Because this change updates the default components, this is not backwards compatible unless the following changes are
  made to the local environment file (`birdhouse/env.local` by default):

  - add any components no longer in the `DEFAULT_CONF_DIRS` list to the `EXTRA_CONF_DIRS` list.
    For example, to keep the jupyterhub component enabled, add `./components/jupyterhub` to the `EXTRA_CONF_DIRS` list.

  - update the `PROXY_ROOT_LOCATION` to redirect the root path `/` to an enabled component. By default, this will
    redirect to Magpie's landing page, unless jupyterhub is enabled, in which case it will redirect to jupyterhub's
    landing page.
    If any other behaviour is desired, `PROXY_ROOT_LOCATION` should be updated in the `env.local` file.

[1.42.2](https://github.com/bird-house/birdhouse-deploy/tree/1.42.2) (2023-12-08)
------------------------------------------------------------------------------------------------------------------

## Changes
- Jupyter: new incremental build to include `SAlib` for sensitivity analysis
  and `fstd2nc` to convert RPN files (from Environment Canada) to netCDF files

  Also make `/notebook_dir/` read-only to avoid users putting their files there
  and losing them since only `/notebook_dir/writable-workspace` is persisted on
  disk.

  See https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/128 for more
  details about `SAlib` and
  https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/132 for more
  details about `fstd2nc`.


[1.42.1](https://github.com/bird-house/birdhouse-deploy/tree/1.42.1) (2023-12-07)
------------------------------------------------------------------------------------------------------------------

## Changes

- Allow user to access their Magpie cookie programmatically

  When the user logs in to jupyterhub, their Magpie cookie is stored in the jupyterhub database. This allows the user
  to access this variable to programmatically access resources protected by magpie without having to copy/paste these 
  cookies from their browser session or add a username and password in plaintext to the file. 

  For example, to access a dataset behind a secured URL with `xarray.open_dataset` using a username and password.
  (this is *not recommended* as it makes it much easier to accidentally leak user credentials):

  ```python
  import requests
  from request_magpie import MagpieAuth
  import xarray
  
  with requests.session() as session:
       session.auth = MagpieAuth("https://mynode/magpie", "myusername", "myverysecretpassword")
       store = xarray.backends.PydapDataStore.open("https://mynode/thredds/some/secure/dataset.nc", session=session)
       dataset = xarray.open_dataset(store)
  ```

  And to do the same thing using the current magpie cookie already used to log in the current user (no need to include 
  username and password, this is *strongly recommended* over the technique above):
  
  ```python
  import os
  import requests
  import xarray
  
  with requests.session() as session:
      r = requests.get(f"{os.getenv('JUPYTERHUB_API_URL')}/users/{os.getenv('JUPYTERHUB_USER')}", 
                       headers={"Authorization": f"token {os.getenv('JUPYTERHUB_API_TOKEN')}"})
      for name, value in r.json().get("auth_state", {}).get("magpie_cookies", {}).items():
          session.cookies.set(name, value)
      store = xarray.backends.PydapDataStore.open("https://mynode/thredds/some/secure/dataset.nc", session=session)
      dataset = xarray.open_dataset(store)        
  ```

  Note that users who are already logged in to jupyterhub will need to log out and log in for these changes to take
  effect.

[1.42.0](https://github.com/bird-house/birdhouse-deploy/tree/1.42.0) (2023-11-30)
------------------------------------------------------------------------------------------------------------------

## Changes

- Update `cowbird` service from [2.2.0](https://github.com/Ouranosinc/cowbird/tree/2.2.0)
  to [2.3.0](https://github.com/Ouranosinc/cowbird/tree/2.3.0).

[1.41.0](https://github.com/bird-house/birdhouse-deploy/tree/1.41.0) (2023-11-30)
------------------------------------------------------------------------------------------------------------------

## Changes
- New optional-component `optional-components/test-cowbird-jupyter-access` that executes a script to set up a test user  
  along with different test files. This component is used for the related 
  [e2e test](https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/blob/master/notebooks-auth/test_cowbird_jupyter.ipynb)
  from the [PAVICS-e2e-workflow-tests](https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests) repo.
- Update `cowbird` service from [2.1.0](https://github.com/Ouranosinc/cowbird/tree/2.1.0)
  to [2.2.0](https://github.com/Ouranosinc/cowbird/tree/2.2.0).
- Add new `README` file to be used on `jupyterhub` when `cowbird` is activated. The file describes to the user the 
  different directories and permissions found in its workspace.

## Fixes
- Updates incorrect WPS outputs resource name in the cowbird config.

[1.40.0](https://github.com/bird-house/birdhouse-deploy/tree/1.40.0) (2023-11-30)
------------------------------------------------------------------------------------------------------------------

- `optional-components/stac-data-proxy`: add a new feature to allow hosting of local STAC assets.

  The new component defines variables `STAC_DATA_PROXY_DIR_PATH` (default `${DATA_PERSIST_ROOT}/stac-data`) and
  `STAC_DATA_PROXY_URL_PATH` (default `/data/stac`) that are aliased (mapped) under `nginx` to provide a URL
  where locally hosted STAC assets can be downloaded from. This allows a server node to be a proper data provider,
  where its STAC-API can return Catalog, Collection and Item definitions that points at these local assets available
  through the `STAC_DATA_PROXY_URL_PATH` endpoint.

  When enabled, this component can be combined with `optional-components/secure-data-proxy` to allow per-resource
  access control of the contents under `STAC_DATA_PROXY_DIR_PATH` by setting relevant Magpie permissions under service
  `secure-data-proxy` for children resources that correspond to `STAC_DATA_PROXY_URL_PATH`. Otherwise, the path and
  all of its contents are publicly available, in the same fashion that WPS outputs are managed without
  `optional-components/secure-data-proxy`. More details are provided under the component's
  [README](./birdhouse/optional-components/README.rst#provide-a-proxy-for-local-stac-asset-hosting).

- `optional-components/stac-public-access`: add public write permission for `POST /stac/search` request.

  Since [`pystac_client`](https://github.com/stac-utils/pystac-client), a common interface to interact with STAC API,
  employs `POST` method by default to perform search, the missing permission caused an unexpected error for users that
  are not aware of the specific permission control of Magpie. Since nothing is created by that endpoint, but rather,
  the POST'ed body employs the convenient JSON format to provide search criteria, it is safe to set this permission
  when the STAC service was configured to be publicly searchable.

[1.39.2](https://github.com/bird-house/birdhouse-deploy/tree/1.39.2) (2023-11-30)
------------------------------------------------------------------------------------------------------------------

## Changes

- Jupyterhub: periodically check whether the logged-in user still have permission to access

  By setting the `JUPYTERHUB_CRYPT_KEY` environment variable in the `env.local` file, jupyterhub will store user's
  authentication information (session cookie) in the database. This allows jupyterhub to periodically check whether the
  user still has permission to access jupyterhub (the session cookie is not expired and the permission have not 
  changed).
  
  The minimum duration between checks can be set with the `JUPYTERHUB_AUTHENTICATOR_REFRESH_AGE` variable which is an 
  integer (in seconds).

  Note that users who are already logged in to jupyterhub will need to log out and log in for these changes to take
  effect.

  To forcibly log out all users currently logged in to jupyterhub you can run the following command to force the
  recreation of the cookie secret:

  ```shell
  docker exec jupyterhub rm /persist/jupyterhub_cookie_secret && docker restart jupyterhub
  ```

[1.39.1](https://github.com/bird-house/birdhouse-deploy/tree/1.39.1) (2023-11-29)
------------------------------------------------------------------------------------------------------------------

## Changes

- Limit usernames in Magpie to match restrictions by Jupyterhub's Dockerspawner

  When Jupyterhub spawns a new jupyterlab container, it escapes any non-ascii, non-digit character in the username. 
  This results in a username that may not match the expected username (as defined by Magpie). This mismatch results in 
  the container failing to spawn since expected volumes cannot be mounted to the jupyterlab container.

  This fixes the issue by ensuring that juptyerhub does not convert the username that is receives from Magpie.

  Note that this updates the Magpie version.

[1.39.0](https://github.com/bird-house/birdhouse-deploy/tree/1.39.0) (2023-11-27)
------------------------------------------------------------------------------------------------------------------

## Changes

- Add a Magpie Webhook to create the Magpie resources corresponding to the STAC-API path elements when a `STAC-API`
  `POST /collections/{collection_id}` or `POST /collections/{collection_id}/items/{item_id}` request is accomplished.
  - When creating the STAC `Item`, the `source` entry in `links` corresponding to a `THREDDS` file on the same instance
    is used to define the Magpie `resource_display_name` corresponding to a file to be mapped later on
    (eg: a NetCDF `birdhouse/test-data/tc_Anon[...].nc`).
  - Checking same instance `source` path is necessary because `STAC` could refer to external assets, and we do not want
    to inject Magpie resource that are not part of the active instance where the hook is running.

[1.38.0](https://github.com/bird-house/birdhouse-deploy/tree/1.38.0) (2023-11-21)
------------------------------------------------------------------------------------------------------------------

## Changes
Flexible locations for data served by THREDDS. This PR adds two capabilities:

- Makes it possible to configure all aspects of the two default top-level THREDDS catalogs that has been available on Birdhouse (conventionally referred to as `Birdhouse` and `Datasets` on PAIVCS). This is done by defining the following two sets of new environment variables. The `THREDDS_DATASET_` set of variables are meant to control properties of the `Datasets` catalog:

    * THREDDS_DATASET_LOCATION_ON_CONTAINER
    * THREDDS_DATASET_LOCATION_ON_HOST
    * THREDDS_DATASET_LOCATION_NAME
    * THREDDS_DATASET_URL_PATH

    The `THREDDS_SERVICE_DATA_` set of variables control properties of the `Birdhouse` catalog.

    * THREDDS_SERVICE_DATA_LOCATION_ON_CONTAINER
    * THREDDS_SERVICE_DATA_LOCATION_ON_HOST
    * THREDDS_SERVICE_DATA_LOCATION_NAME
    * THREDDS_SERVICE_DATA_URL_PATH

    These new variables are defined in [`thredds/default.env`](./birdhouse/config/thredds/default.env) and included in [`env.local.example`](./birdhouse/env.local.example). Their default values have been chosen to ensure the behaviours of the two catalogs remain unchanged (for reasons of backward compatibility).

- Adds the ability to define additional top-level THREDDS catalogs. This is achieved by introducing the `THREDDS_ADDITIONAL_CATALOG` variable in [`thredds/default.env`](./birdhouse/config/thredds/default.env) that can be used to inject custom XML configuration for a new catalog. This information is picked up by the THREDDS server. An example is provided in [`env.local.example`](./birdhouse/env.local.example).

[1.37.2](https://github.com/bird-house/birdhouse-deploy/tree/1.37.2) (2023-11-10)
------------------------------------------------------------------------------------------------------------------

- Fix `weaver` and `cowbird` inconsistencies for `public` WPS outputs directory handling.

  Because `cowbird` needs to mount multiple directories within the user-workspace for `jupyterhub`, it needs to define
  a dedicated `public/wps_outputs` sub-directory to distinguish it from other `public` files not part of WPS outputs.
  However, for WPS birds, other files than WPS outputs are irrelevant, and are therefore mounted directly in their
  container. The variable `PUBLIC_WORKSPACE_WPS_OUTPUTS_SUBDIR` was being misused in the context of `weaver`,
  causing WPS output URLs for `public` context to be nested as `/wpsoutputs/weaver/public/wps_outputs/{jobID}`
  instead of the intended location `/wpsoutputs/weaver/public/{jobID}`, in contrast to user-context WPS outputs
  located under `/wpsoutputs/weaver/users/{userID}/{jobID}`.

  Relates to [Ouranosinc/pavics-sdi#314](https://github.com/Ouranosinc/pavics-sdi/pull/314).

[1.37.1](https://github.com/bird-house/birdhouse-deploy/tree/1.37.1) (2023-11-03)
------------------------------------------------------------------------------------------------------------------

## Fixes
- `optional-components/all-public-access`: remove erroneous Magpie route permission properties for GeoServer.

[1.37.0](https://github.com/bird-house/birdhouse-deploy/tree/1.37.0) (2023-11-01)
------------------------------------------------------------------------------------------------------------------

## Changes
- Geoserver: protect web interface and ows routes behind magpie/twitcher
 
  Updates Magpie version to [3.35.0](https://github.com/Ouranosinc/Magpie/tree/3.35.0) in order to take advantage of 
  updated Geoserver Service.

  The `geoserverwms` Magpie service is now deprecated. If a deployment is currently using this service, it is highly
  recommended that the permissions are transferred from the deprecated `geoserverwms` service to the `geoserver` 
  service.

  The `/geoserver` endpoint is now protected by default. If a deployment currently assumes open access to Geoserver and 
  would like to keep the same permissions after upgrading to this version, please update the permissions for the 
  `geoserver` service in Magpie to allow the `anonymous` group access.

  A `Magpie` service named `geoserver` with type `wfs` exists already and must be manually deleted before the new
  `Magpie` service created here can take effect.

  The `optional-components/all-public-access` component provides full access to the `geoserver` service for the 
  `anonymous` group in Magpie. Please note that this includes some permissions that will allow anonymous users to 
  perform destructive operations. Because of this, please remember that enabling the 
  `optional-components/all-public-access` component is not recommended in a production environment.

  Introduces the `GEOSERVER_SKIP_AUTH` environment variable. If set to `True`, then requests to the geoserver endpoint 
  will not be authorized through twitcher/magpie at all. This is not recommended at all. However, it will slightly 
  improve performance when accessing geoserver endpoints.

  See https://github.com/bird-house/birdhouse-deploy/issues/333 for details.

[1.36.0](https://github.com/bird-house/birdhouse-deploy/tree/1.36.0) (2023-10-31)
------------------------------------------------------------------------------------------------------------------

## Changes

- Protect jupyterhub behind twitcher authentication

  - Sets magpie cookies whenever a user logs in or out through jupyterhub so that they are automatically logged in 
    or out through magpie as well.
  - Ensures that the user has permission to access jupyterhub according to magpie when logging in.

[1.35.2](https://github.com/bird-house/birdhouse-deploy/tree/1.35.2) (2023-10-24)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Fix warning from JupyterHub regarding DockerSpawner method never awaited.
  - [`DockerSpawner.start`](
    https://github.com/jupyterhub/dockerspawner/blob/a6bf72e7/dockerspawner/dockerspawner.py#L1246) is defined
    as `async`. Therefore, `async def` and `await super().start()` where not properly invoked by `CustomDockerSpawner`
    in [`jupyterhub_config.py.template`](./birdhouse/config/jupyterhub/jupyterhub_config.py.template).

[1.35.1](https://github.com/bird-house/birdhouse-deploy/tree/1.35.1) (2023-10-18)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Jupyterhub cull interval setting must be an integer:
  - Previously, the default `jupyter_idle_kernel_cull_interval` setting is calculated by dividing the 
    `jupyter_idle_kernel_cull_timeout` setting by 2 using float division. This meant that the result was a float 
    instead of the expected integer value. This caused and error when the jupyterlab server spawned.
    In order to fix this, the value is cast to an integer after division.

[1.35.0](https://github.com/bird-house/birdhouse-deploy/tree/1.35.0) (2023-10-16)
------------------------------------------------------------------------------------------------------------------

## Changes
- Jupyterhub configurable idle server culling.
  - Add optional variables `JUPYTER_IDLE_SERVER_CULL_TIMEOUT`, `JUPYTER_IDLE_KERNEL_CULL_TIMEOUT` and
    `JUPYTER_IDLE_KERNEL_CULL_INTERVAL` that allows fined-grained configuration of user-kernel and server-wide
    docker image culling when their activity status reached a certain idle timeout threshold.
  - Enable idle kernel culling by default with a timeout of 1 day, and user server culling with timeout of 3 days.
  - Avoids the need for custom `JUPYTERHUB_CONFIG_OVERRIDE` specifically for idle server culling.
    If similar argument parameters should be defined using an older `JUPYTERHUB_CONFIG_OVERRIDE` definition,
    the new configuration strategy can be skipped by setting `JUPYTER_IDLE_KERNEL_CULL_TIMEOUT=0`.

[1.34.0](https://github.com/bird-house/birdhouse-deploy/tree/1.34.0) (2023-10-10)
------------------------------------------------------------------------------------------------------------------

## Changes
- Allow users to submit a Weaver job requesting to store outputs to the public location instead of their user-workspace.
- Update default Weaver version from [4.22.0](https://github.com/crim-ca/weaver/tree/4.22.0)
  to [4.32.0](https://github.com/crim-ca/weaver/tree/4.32.0).
- Add `COWBIRD_LOG_LEVEL` environment variable to allow control over logging level of Cowbird services.

[1.33.5](https://github.com/bird-house/birdhouse-deploy/tree/1.33.5) (2023-10-02)
------------------------------------------------------------------------------------------------------------------

## Changes

- Adding a description for the STAC service that will be served at the `/services` endpoint

[1.33.4](https://github.com/bird-house/birdhouse-deploy/tree/1.33.4) (2023-10-02)
------------------------------------------------------------------------------------------------------------------

## Fixes
- Clean up: Make bind-mount locations more flexible

  Clean up unused variables and correct file paths from the changes made in 1.33.2

[1.33.3](https://github.com/bird-house/birdhouse-deploy/tree/1.33.3) (2023-09-29)
------------------------------------------------------------------------------------------------------------------

## Changes

- Add test data and volume for `test-geoserver-secured-access`

[1.33.2](https://github.com/bird-house/birdhouse-deploy/tree/1.33.2) (2023-09-27)
------------------------------------------------------------------------------------------------------------------

## Changes
- Make bind-mount locations more flexible

  Previously, most bind mount locations on the host machine were subdirectories of the folder specified by the 
  `DATA_PERSIST_ROOT` environment variable (`/data` by default). This change allows the user to set custom locations
  for the following additional variables, so that they don't need to be all under the same common directory.

  - `LOGROTATE_DATA_DIR` (default: `${DATA_PERSIST_ROOT}/logrotate`)
  - `MONGODB_DATA_DIR` (default: `${DATA_PERSIST_ROOT}/mongodb_persist`)
  - `COWBIRD_MONGODB_DATA_DIR` (default: `${DATA_PERSIST_ROOT}/mongodb_cowbird_persist`)
  - `POSTGRES_DATA_DIR` (default `${DATA_PERSIST_ROOT}/frontend_persist`)
  - `WEAVER_MONGODB_DATA_DIR` (default `${DATA_PERSIST_ROOT}/mongodb_weaver_persist`)

  The following variable is also added which is another location on disk where files that may contain links
  are placed. Because the links need to be mounted together in order to resolve properly, the subdirectories
  of this directory are not configurable:

  - `DATA_PERSIST_SHARED_ROOT` (default: same as `DATA_PERSIST_ROOT`)

  The following variables now create subdirectories under `DATA_PERSIST_SHARED_ROOT` (previously they were
  created under `DATA_PERSIST_ROOT` by default):

  - `USER_WORKSPACES` (default `user_workspaces`)
  - `WEAVER_WPS_OUTPUTS_DIR` (default `wps_outputs/weaver`)


[1.33.1](https://github.com/bird-house/birdhouse-deploy/tree/1.33.1) (2023-09-25)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Docker compose version missing in ``stac/config/magpie/`` compose file
  - The ``version:`` key was not set in the ``stac/config/magpie/docker-compose-extra.yml`` file which caused
    ``docker-compose`` to report a version mismatch and fail to start.

[1.33.0](https://github.com/bird-house/birdhouse-deploy/tree/1.33.0) (2023-09-25)
------------------------------------------------------------------------------------------------------------------

## Changes
- Add public WPS outputs directory to Cowbird and add corresponding volume mount to JupyterHub.
- Update `cowbird` service from [1.2.0](https://github.com/Ouranosinc/cowbird/tree/1.2.0)
  to [2.1.0](https://github.com/Ouranosinc/cowbird/tree/2.1.0).
- Require `MongoDB==5.0` Docker image for Cowbird's database.
- Add `WPS_OUTPUTS_DIR` env variable to manage the location of the WPS outputs data.

## Important
Because of the new `MongoDB==5.0` database requirement for Cowbird that uses (potentially) distinct version from other 
birds, a separate Docker image is employed only for Cowbird. If some processes, jobs, or other Cowbird-related data 
was already defined on one of your server instances, manual transfer between the generic 
`${DATA_PERSIST_ROOT}/mongodb_persist` to new  `${DATA_PERSIST_ROOT}/mongodb_cowbird_persist` directory must be 
accomplished. The data in the new directory should then be migrated to the new version following the same procedure as
described for Weaver in 
[Database Migration](https://pavics-weaver.readthedocs.io/en/latest/installation.html?#database-migration).

[1.32.0](https://github.com/bird-house/birdhouse-deploy/tree/1.32.0) (2023-09-22)
------------------------------------------------------------------------------------------------------------------

## Changes

- Changes `JUPYTERHUB_VERSION` from `1.4.0-20210506` to `4.0.2-20230816`.
  - This upgrade is needed to resolve a compatibility issue when using `Spawner.disable_user_config = True` in Jupyterhub 
    config and the new image which run `jupyter-server 2.7.3`.

- Add an image to the list of images that can be launched from JupyterHub which will be used to start an instance of MLflow.
  - Note that the jupyter lab google drive extension is not supported with this image.

[1.31.3](https://github.com/bird-house/birdhouse-deploy/tree/1.31.3) (2023-09-21)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Move initial ``stac`` service Magpie definition under its component configuration.
  - Before this change, ``optional-components/stac-public-access`` was mandatory since the ``stac`` service under
    Magpie was not created otherwise, leading to "*service not found*" error when requesting the ``/stac`` endpoint.
  - Ensure that the first ``stac`` resource under ``stac`` service in Magpie is created by default.
    Without this resource being defined initially, it is very easy to forget creating it, which would not take into
    account the required ``/stac/stac`` request path to properly resolve the real endpoints where STAC API is served.

- Remove `optional-components/stac-public-access` dependency under `optional-components/all-public-access`
  to avoid indirectly enforcing `components/stac` when `optional-components/all-public-access` is enabled.
  Users that desire using `optional-components/stac-public-access` will have to add it explicitly to the list
  of `EXTRA_CONF_DIRS`.

- Rename `optional-components/stac-public-access/config/magpie/config.yml.template` to
  `optional-components/stac-public-access/config/magpie/permissions.cfg` in order to align
  with permissions-specific contents as accomplished with other components.

- Fix invalid endpoint redirect for `STAC` when using Twitcher/Magpie.

- Apply Magpie permission on `/stac/stac` since the second `/stac` is needed to secure access properly.

[1.31.2](https://github.com/bird-house/birdhouse-deploy/tree/1.31.2) (2023-09-13)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Fix invalid templated configurations of `flyingpigeon` that could remain in the old 
  location (`birdhouse/config/flyingpigeon`) when updating an existing instance to `1.31.0`.

[1.31.1](https://github.com/bird-house/birdhouse-deploy/tree/1.31.1) (2023-09-13)
------------------------------------------------------------------------------------------------------------------

## Changes

- Small change to the location of schema defining services
  - Changed https://github.com/DACCS-Climate/DACCS-node-registry to https://github.com/DACCS-Climate/Marble-node-registry
    in all service-config.json.template files.

[1.31.0](https://github.com/bird-house/birdhouse-deploy/tree/1.31.0) (2023-09-13)
------------------------------------------------------------------------------------------------------------------

## Changes:

- Deprecate the `flyingpigeon` web processing service.
  The service can be enabled using [`deprecated-components/flyingpigeon`](birdhouse/deprecated-components/flyingpigeon) in `EXTRA_CONF_DIRS`.

[1.30.1](https://github.com/bird-house/birdhouse-deploy/tree/1.30.1) (2023-09-11)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Fix incorrect tag ``X-Robots-Tags`` header to appropriate ``X-Robots-Tag`` (no final ``s``) name.
  Optional component name ``optional-components/x-robots-tag-header`` and variable ``X_ROBOTS_TAG_HEADER``
  have also been adjusted accordingly.

[1.30.0](https://github.com/bird-house/birdhouse-deploy/tree/1.30.0) (2023-09-06)
------------------------------------------------------------------------------------------------------------------

## Changes

- Add ``optional-components/x-robots-tags-header`` and ``X_ROBOTS_TAGS_HEADER`` variable to allow setting the desired
  header value server-wide.

- Delete unused Dockerfiles, fixes
  [#349](https://github.com/bird-house/birdhouse-deploy/issues/349) and
  [#352](https://github.com/bird-house/birdhouse-deploy/pull/352)

  * birdhouse/docker/geoserver: not used since 3-4 years, replaced by https://github.com/kartoza/docker-geoserver

  * birdhouse/config/geoserver/Dockerfile: was introduced in commit [f3b9896e6b771e0aff62c6851c2376d730ddadaf](https://github.com/bird-house/birdhouse-deploy/commit/f3b9896e6b771e0aff62c6851c2376d730ddadaf)
    (PR [#233](https://github.com/bird-house/birdhouse-deploy/pull/233), commit
    [d1ecc63284ec9d2940bfa2b1b4baca3fbe1308b3](https://github.com/bird-house/birdhouse-deploy/commit/d1ecc63284ec9d2940bfa2b1b4baca3fbe1308b3)) as a temporary
    solution only, not needed with newer kartoza docker images.

- Move birdhouse/docker/solr to birdhouse/deprecated-components/solr/docker
  to group related files together.  Solr has been deprecated since PR
  [#311](https://github.com/bird-house/birdhouse-deploy/pull/311)
  (commit
  [a8d3612fdb7fd7758b24e75b0ef697fd3d8ace51](https://github.com/bird-house/birdhouse-deploy/commit/a8d3612fdb7fd7758b24e75b0ef697fd3d8ace51)).


[1.29.2](https://github.com/bird-house/birdhouse-deploy/tree/1.29.2) (2023-08-24)
------------------------------------------------------------------------------------------------------------------

## Changes

- Monitoring: allow access to magpie members of group `monitoring`

  To allow accessing the various monitoring WebUI without having full blown
  magpie admin priviledge to add and remove users.

  Add existing users to this new `monitoring` group to allow them access to the
  various monitoring WebUI.  This way, we do not need to share the `admin` user
  account and do not have to add them to the `administrators` group.


[1.29.1](https://github.com/bird-house/birdhouse-deploy/tree/1.29.1) (2023-08-15)
------------------------------------------------------------------------------------------------------------------

## Changes

- Small STAC changes
  - This PR includes some changes that were suggested in a review for #297. But because the PR was already merged,
    further updates are included here:
    - removes extra block to include in docker compose files (no longer needed)
    - moves docker compose file in `stac-public-access` component to the correct location
    - uses `PAVICS_FQDN_PUBLIC` for public facing URLs in all places

[1.29.0](https://github.com/bird-house/birdhouse-deploy/tree/1.29.0) (2023-08-10)
------------------------------------------------------------------------------------------------------------------

## Changes
- Do not expose additional ports:
  - Docker compose no longer exposes any container ports outside the default network except for ports 80 and 443 from 
    the proxy container. This ensures that ports that are not intended for external access are not exposed to the wider 
    internet even if firewall rules are not set correctly.
  - Note that if the `monitoring` component is used then port 9100 will be exposed from the `node-exporter` container.
    This is because this container must be run on the host machine's network and unfortunately there is no known
    workaround that would not require this port to be exposed on the host machine.
  - Fixes https://github.com/bird-house/birdhouse-deploy/issues/222


[1.28.0](https://github.com/bird-house/birdhouse-deploy/tree/1.28.0) (2023-08-10)
------------------------------------------------------------------------------------------------------------------

## Changes
- Adds [STAC](https://github.com/crim-ca/stac-app) to the stack (optional) when ``./components/stac`` 
  is added to ``EXTRA_CONF_DIRS``. For more details, refer to 
  [STAC Component](https://github.com/bird-house/birdhouse-deploy/blob/master/birdhouse/components/README.rst#STAC)
  Following happens when enabled:
    
  * Service ``stac`` (API) gets added with endpoints ``/twitcher/ows/proxy/stac`` and ``/stac``.
    
  * STAC catalog can be explored via the ``stac-browser`` component, available under ``/stac-browser``.
      
  * Image [crim-ca/stac-app](https://github.com/crim-ca/stac-app) is a STAC implementation based on 
  [stac-utils/stac-fastapi](https://github.com/stac-utils/stac-fastapi).

  * Image [crim-ca/stac-browser](https://github.com/crim-ca/stac-browser) is a fork of 
  [radiantearth/stac-browser](https://github.com/radiantearth/stac-browser) in order to have the capacity to build 
  the Docker container. The image reference will change when the 
  [stac-browser PR related to Dockerfile](https://github.com/bird-house/birdhouse-deploy/issues/346) will have been 
  merged.
      
  * Adds `Magpie` permissions and service for `stac` endpoints.
  
- Adds [stac-populator](https://github.com/crim-ca/stac-populator) to populate STAC catalog with sample collection 
  items via [CEDA STAC Generator](https://github.com/cedadev/stac-generator), employed in sample 
  [CMIP Dataset Ingestion Workflows](https://github.com/cedadev/stac-generator-example/tree/master/conf).

- Adds ``optional-components/stac-public-access`` to give public access to the STAC catalog.

[1.27.1](https://github.com/bird-house/birdhouse-deploy/tree/1.27.1) (2023-07-10)
------------------------------------------------------------------------------------------------------------------

## Changes
- Add Magpie webhook definitions for permission creation and deletion cases to be processed by Cowbird.
- Add `USER_WORKSPACE_UID` and `USER_WORKSPACE_GID` env variables to manage ownership of the user workspaces used by
  Cowbird, JupyterHub and others.
- Update `magpie` service from [3.31.0](https://github.com/Ouranosinc/Magpie/tree/3.31.0)
  to [3.34.0](https://github.com/Ouranosinc/Magpie/tree/3.34.0)
- Update `cowbird` service from [1.1.1](https://github.com/Ouranosinc/cowbird/tree/1.1.1)
  to [1.2.0](https://github.com/Ouranosinc/cowbird/tree/1.2.0)

[1.27.0](https://github.com/bird-house/birdhouse-deploy/tree/1.27.0) (2023-07-06)
------------------------------------------------------------------------------------------------------------------

- Deprecate unused/unmaintained components

  Move unused and unmaintained components to a separate [`deprecated-components/`](birdhouse/deprecated-components)
  subdirectory and remove them from the `DEFAULT_CONF_DIRS` list if required.

[1.26.11](https://github.com/bird-house/birdhouse-deploy/tree/1.26.11) (2023-07-04)
------------------------------------------------------------------------------------------------------------------

## Fixes
- Components endpoint now returns valid json

  The JSON string reported by the `/components/` path was not valid JSON due to a misconfigured regular expression
  used to generate the content. The issue was that integers were not being properly parsed by the regular expression
  meaning that paths that contained integers other than 0 were not recognized as valid paths.

  This fixes https://github.com/bird-house/birdhouse-deploy/issues/339

[1.26.10](https://github.com/bird-house/birdhouse-deploy/tree/1.26.10) (2023-07-04)
------------------------------------------------------------------------------------------------------------------

## Changes

- Move canarie-api configuration for cowbird from proxy to canarie-api config directory
  - The canarie-api configuration for cowbird was being loaded whenever the proxy component was enabled instead
    of when the canarie-api component was enabled. Since these components can now be enabled separately, the
    configuration has to be moved to ensure that canarie-api configuration files aren't unintentionally mounted
    to a container that is just running an nginx proxy.

[1.26.9](https://github.com/bird-house/birdhouse-deploy/tree/1.26.9) (2023-07-04)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Fix Cowbird's `sync_permissions` config which used invalid Magpie service types.

[1.26.8](https://github.com/bird-house/birdhouse-deploy/tree/1.26.8) (2023-06-22)
------------------------------------------------------------------------------------------------------------------

## Fixes
- Tests: some tests fail to run when `CWD` is not `COMPOSE_DIR`

  The root cause is the automatic `COMPOSE_DIR` detection in
  `read-configs.include.sh` missed one case and the detection ordering was wrong
  for one other case as well.

  This was not found before because the checkout was properly named
  "birdhouse-deploy".  When the checkout is named something else, then we hit
  this error.

  Fixes the error found here
  https://github.com/bird-house/birdhouse-deploy/pull/329#pullrequestreview-1480211502

## Changes
- Autodeploy: document test procedure

- Dev environment: add Conda `environment-dev.yml` to easily install all the dev tools required

- Tests: make test runs more robust, able to run from any `CWD`

  Before, test runs can only be started from inside the checkout, at some
  "popular" locations inside the checkout.  Now it can be started from
  litterally anywhere.


[1.26.7](https://github.com/bird-house/birdhouse-deploy/tree/1.26.7) (2023-06-19)
------------------------------------------------------------------------------------------------------------------

## Changes

- A new endpoint `/services` is added that provides a JSON string describing each of the user facing services currently 
  enabled on the stack. This is a static string and serves a different purpose than the endpoints served by canarie-api
  (monitoring status). This endpoint is meant to be polled by the node registry scripts 
  (https://github.com/DACCS-Climate/DACCS-node-registry) to provide information about what services are meant to be 
  available without having to poll other endpoints directly.

- A new endpoint `/version` is added that provides a string containing the current version number of the stack 
  (e.g. "1.26.0"). This endpoint is meant to be polled by the node registry scripts 
  (https://github.com/DACCS-Climate/DACCS-node-registry).


[1.26.6](https://github.com/bird-house/birdhouse-deploy/tree/1.26.6) (2023-06-16)
------------------------------------------------------------------------------------------------------------------

## Fixes
- `components/` endpoint displays intended information after auto-deploy

  Previously, the script that generates the content for the `components/` endpoint
  was using a feature of `grep` that is not supported by all versions of `grep`.
  This meant that this script running in the auto-deployment docker container was
  not able to properly parse the running components using `grep`. 
  This fixes the issue by making the script compliant with all versions of `grep`.

  Resolves https://github.com/bird-house/birdhouse-deploy/issues/342

[1.26.5](https://github.com/bird-house/birdhouse-deploy/tree/1.26.5) (2023-06-16)
------------------------------------------------------------------------------------------------------------------

## Fixes
- Autodeploy: optionally fix file permissions

  The autodeploy mechanism creates new files owned by root. If this is not desired then users have to manually
  update the file ownership after each autodeployment. This adds an option to change the ownership of all files
  to a specific user after each autodeployment. 

  For example, if the code in this repo is currently owned by a user named `birduser` with uid 1002, then by
  setting `export AUTODEPLOY_CODE_OWNERSHIP="1002:1002"` in `env.local`, all files and folders in this repo will 
  continue to be owned by `birduser` after each autodeployment. 

[1.26.4](https://github.com/bird-house/birdhouse-deploy/tree/1.26.4) (2023-06-06)
------------------------------------------------------------------------------------------------------------------

## Changes
- Jupyter env: new version with latest RavenPy

  See https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/119 for more
  details.


[1.26.3](https://github.com/bird-house/birdhouse-deploy/tree/1.26.3) (2023-06-01)
------------------------------------------------------------------------------------------------------------------

## Changes
- Jupyter env: new version with latest Xclim and RavenPy

  See https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/115 for more
  details.

- Raven WPS: new version to match with new RavenPy inside the Jupyter env

  See https://github.com/Ouranosinc/raven/compare/v0.14.2...v0.18.1 for more
  details.

## Fixes
- Notebook autodeploy: unable to read the `env.local`

  When `env.local` is a symlink we need to volume-mount the destination of the
  symlink so it resolves inside the notebook autodeploy container.

  This will allow notebook autodeploy config variable to be set in `env.local`.

  Also had someone changed the value of `JUPYTERHUB_USER_DATA_DIR` in `env.local`,
  it would not have worked without this fix.

  This is a non-breaking fix.


[1.26.2](https://github.com/bird-house/birdhouse-deploy/tree/1.26.2) (2023-05-25)
------------------------------------------------------------------------------------------------------------------

## Changes

- Update Zenodo config
  *  Add Misha to creators
  *  Add birdhouse community

- Licence: update copyright line with year and ownership

[1.26.1](https://github.com/bird-house/birdhouse-deploy/tree/1.26.1) (2023-04-26)
------------------------------------------------------------------------------------------------------------------

## Changes

- Zenodo: A configuration file for [Zenodo](https://zenodo.org/) was added to the source code, listing all contributing authors on the *birdhouse-deploy* repository.


[1.26.0](https://github.com/bird-house/birdhouse-deploy/tree/1.26.0) (2023-04-20)
------------------------------------------------------------------------------------------------------------------


## Breaking changes

- CanarieAPI: update to `0.7.1`.

  - The Docker running `CanarieAPI` is now using Python 3 (since `0.4.x` tags).
    Configurations need to be updated if any specific Python 2 definitions were used.
    See [2to3](https://docs.python.org/3/library/2to3.html) to help migrate configurations automatically if necessary.
  - Update the [CanarieAPI configuration](birdhouse/config/canarie-api/docker_configuration.py.template) to use
    Python 3.x executable code.

## Changes

- CanarieAPI: update to `0.7.1`.

  - The server node now provides a generic ``server`` configuration for the current ``platform`` definition.
  - Added multiple missing docuementation references for all the services included within `CanarieAPI` configurations.
  - With new `CanarieAPI` version, a slightly improved UI with more service details are provided for the active server:

![image](https://user-images.githubusercontent.com/19194484/232822454-e39c0111-54dc-4f9b-adf6-5ea6e59d67e3.png)

- Add optional variables witht defaults to define reference Docker image version tags.

  Following optional variables are defined by default. These are used as reference in the respective Docker compose
  service definition of these components, as well as in their `CanarieAPI` configuration to retrieve the release time
  of the tag, and refer to relevant URL references as needed.

  - `CATALOG_VERSION`
  - `FINCH_VERSION`
  - `FLYINGPIGEON_VERSION`
  - `GEOSERVER_VERSION`
  - `HUMMINGBIRD_VERSION`
  - `MALLEEFOWL_VERSION`
  - `RAVEN_VERSION`

## Fixes:

- CanarieAPI: update to `0.7.1`.

  - Fixes an `AttributeError` raised due to misconfiguration of the Web Application with Flask 2.x definitions
    (relates to [Ouranosinc/CanarieAPI#10](https://github.com/Ouranosinc/CanarieAPI/pull/10)).
  - Skip over `0.4.x`, `0.5.x`, `0.6.x`  versions to avoid issue related to `cron` job monitoring and log parser
    command failures in order to collect configured service statistics and statuses
    (see also [Ouranosinc/CanarieAPI#14](https://github.com/Ouranosinc/CanarieAPI/pull/14)).

- Weaver: update CanarieAPI monitoring definitions
  - Move monitoring of public endpoint under [optional-components/canarie-api-full-monitoring][canarie-monitor].
  - Add monitoring of private endpoint by default when using Weaver component.

- Cowbird: update CanarieAPI monitoring definitions
  - Add monitoring of public endpoint under [optional-components/canarie-api-full-monitoring][canarie-monitor].
  - Add public Magpie permission on Cowbird entrypoint only to allow its monitoring.

[canarie-monitor]: birdhouse/optional-components/canarie-api-full-monitoring

[1.25.7](https://github.com/bird-house/birdhouse-deploy/tree/1.25.7) (2023-04-20)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Fix flaky WPS provider responses (i.e.: other WPS birds) causing failure during their registration in `weaver`.

  In some cases, the WPS birds would not respond properly when starting the stack, either because they are still
  initiating or due to other temporary failures such as services being restarted until healthy. This fix introduces 
  a retry mechanism to attempt WPS registration in `weaver` up to `WEAVER_WPS_PROVIDERS_RETRY_COUNT=5` times 
  (1 initial attempt + 5 retries), and with `WEAVER_WPS_PROVIDERS_RETRY_AFTER=5` second intervals between each retry.
  If the maximum number of retries for any WPS provider or the `WEAVER_WPS_PROVIDERS_MAX_TIME` across all registrations
  are reached, the operation is aborted.

[1.25.6](https://github.com/bird-house/birdhouse-deploy/tree/1.25.6) (2023-04-20)
------------------------------------------------------------------------------------------------------------------

## Fixes
- Config var `PAVICS_FQDN_PUBLIC` not usable in component `default.env` and external scripts

  Currently, `PAVICS_FQDN_PUBLIC` is only usable in `.template` files, in
  `docker-compose-extra.yml` files and in component pre/post compose scripts
  because they are handled by `pavics-compose.sh`.

  It was good enough but now with delayed eval feature, we can do better.
  `PAVICS_FQDN_PUBLIC` can be as accessible as the other `PAVICS_FQDN` var.

  Both vars allow a host to have a different public and internal hostname.
  Some scripts, `certbotwrapper` for example, prefer the public hostname than
  the internal hostname when they are different because Let's Encrypt only
  knows about the public hostname.

  With the pluggable nature of this stack, we can have many external scripts
  from many external repos reading the config vars and they can have the need
  to specifically access the public hostname.

  Bonus, we now have a sample use of `DELAYED_EVAL` list, right in the main `default.env`.

## Changes

- `pavics-compose` output rendering

  Prints the activated compose file list line-by-line such that it can be more easily readable. 

  Before the change, the output was as follows:
  ![image](https://user-images.githubusercontent.com/19194484/233111255-ef31b36f-7bb9-4856-80b7-9aa5b17ae167.png)

  After the change, the output is more easily readable:
  ![image](https://user-images.githubusercontent.com/19194484/233113601-8955a9cb-3da1-4f5a-9a36-4c8653b5606a.png)

- Various documentation updates

  * Update list of OS tested
  * Framework tests code block not rendering properly
  * [Add a few sentences on the required hardware to run the platform](https://github.com/bird-house/birdhouse-deploy/issues/312)
  * [Add license](https://github.com/bird-house/birdhouse-deploy/issues/309)
  * [Document how to change MAGPIE_ADMIN_PASSWORD](https://github.com/bird-house/birdhouse-deploy/issues/57)
  * [Document assumption EXTRA_CONF_DIRS assume relative path to docker-compose.yml](https://github.com/bird-house/birdhouse-deploy/issues/53)
  * [Document how to get LetsEncrypt SSL cert if not using Vagrant that automate the whole thing](https://github.com/bird-house/birdhouse-deploy/issues/55)
  * [Document config for self-signed SSL](https://github.com/bird-house/birdhouse-deploy/issues/52)
  * Update the "Release Instructions" in the README to use `make bump <major|minor|patch>` command instead of directly calling `bump2version` to harmonize with the section "Tagging policy" right above.

[1.25.5](https://github.com/bird-house/birdhouse-deploy/tree/1.25.5) (2023-04-12)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Fix disapearing Thredds docker image

  The current docker image version for thredds (4.6.18) is no longer hosted in the
  [Unidata docker repository](https://hub.docker.com/r/unidata/thredds-docker/tags).

  Pushed the same image from Ouranos production to PAVICS DockerHub, restoring
  the missing Thredds image.

  Discovered that Unidata is also not keeping their tag immutable, like Kartoza Geoserver image.

  So Ouranos tag has the approximate month of Unidata re-release of 4.6.18.

  On our production server:
  ```
  $ docker images |grep thredds|grep 4.6.18
  unidata/thredds-docker              4.6.18              25997a1b2893   15 months ago   5.63GB
  ```

  On our staging server:
  ```
  $ docker images |grep thredds | grep 4.6.18
  unidata/thredds-docker              4.6.18              09103737360a   16 months ago   5.62GB
  ```


[1.25.4](https://github.com/bird-house/birdhouse-deploy/tree/1.25.4) (2023-04-12)
------------------------------------------------------------------------------------------------------------------

## Fixes
- Enforce the load order of components defined in env.local
  
  Extra components defined in the `EXTRA_CONF_DIRS` variables were being loaded before the dependant components
  defined in the `COMPONENT_DEPENDENCIES` variables in each default.env file. This meant that if an extra component
  was meant to override some setting defined in a dependant component, the setting would not be overridden by the
  extra component. 

  This change enforces the following load order rules:

  - components defined in `DEFAULT_CONF_DIRS` are loaded before those in `EXTRA_CONF_DIRS`
  - components are loaded in the order they appear in either `DEFAULT_CONF_DIRS` or `EXTRA_CONF_DIRS`
  - components that appear in `COMPONENT_DEPENDENCIES` variable are immediately loaded unless they have already been
    loaded

  For example, with the following files in place:

  ```shell
  # env.local
  DEFAULT_CONF_DIRS="
    ./config/twitcher
    ./config/project-api
    ./config/magpie
  "
  EXTRA_CONF_DIRS="
    ./optional-components/generic_bird
    ./components/cowbird
  "
  
  # config/twitcher/default.env
  COMPONENT_DEPENDENCIES="
    ./config/magpie
  "
  # optional-components/generic_bird/default.env
  COMPONENT_DEPENDENCIES="
    ./config/wps_outputs-volume
  "
  ```
  
  the load order is:

  - ./config/magpie (loaded as a dependency of twitcher, not loaded a second time after project-api)
  - ./config/twitcher
  - ./config/project-api
  - ./config/wps_outputs-volume (loaded as a dependency of generic_bird)
  - ./optional-components/generic_bird
  - ./components/cowbird

  This load order also applies to the order that docker-compose-extra.yml files are specified. If a component also
  includes an override file for another component (eg: ./config/finch/config/proxy/docker-compose-extra.yml overrides 
  ./config/proxy/docker-compose-extra.yml), the following additional load order rules apply:

  - if the component that is being overridden has already been loaded, the override file is loaded immediately
  - otherwise, the override files will be loaded immediately after the component that is being overridden has been loaded

  For example, with the following files in place:

    ```shell
  # env.local
  DEFAULT_CONF_DIRS="
    ./config/finch
    ./config/proxy
  "
  ```
  ```yaml
  # config/proxy/docker-compose-extra.yml
    ...
  # config/finch/docker-compose-extra.yml
    ...
  # config/finch/config/proxy/docker-compose-extra.yml
    ...
  ```

  the docker compose files will be loaded in the following order: 

  - config/finch/docker-compose-extra.yml
  - config/proxy/docker-compose-extra.yml
  - config/finch/config/proxy/docker-compose-extra.yml

- Add tests to ensure override capabilities are preserved which allows all default
  behaviors of the platform can be customized.

  See [birdhouse/README.rst](birdhouse/README.rst) for instruction to run the
  tests.

[1.25.3](https://github.com/bird-house/birdhouse-deploy/tree/1.25.3) (2023-04-12)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Canarie-api: add old config file into historical gitignore

  In order to maintain backwards compatibility, old files that are no longer present in the code should be 
  kept in the gitignore files. This adds back one file to the relevant .gitignore file that no longer exists under 
  `conf.extra-service.d/canarie-api.conf`.

[1.25.2](https://github.com/bird-house/birdhouse-deploy/tree/1.25.2) (2023-04-12)
------------------------------------------------------------------------------------------------------------------

## Changes
- Jupyter: new image to add esgf-pyclient and xncml to fix Jenkins failure

  See PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/118 for more details.

  - Adds `esgf-pyclient` for esgf-dap.ipynb (https://github.com/Ouranosinc/pavics-sdi/pull/269)
  - Adds `xncml` for gen_catalog refactoring (https://github.com/Ouranosinc/pavics-vdb/pull/46)
  - Fixes annoying harmless error `ERROR 1: PROJ: proj_create_from_database: Open of /opt/conda/envs/birdy/share/proj failed`
  - Relevant changes (alphabetical order):
  ```diff
  >   - esgf-pyclient=0.3.1=pyh1a96a4e_2

  <   - gdal=3.5.3=py38h1f15b03_4
  >   - gdal=3.6.0=py38h58634bd_13

  >     - xncml==0.2
  ```


[1.25.1](https://github.com/bird-house/birdhouse-deploy/tree/1.25.1) (2023-04-11)
------------------------------------------------------------------------------------------------------------------

## Changes

- Canarie-api should not be a mandatory component.

  Canarie-api is currently deployed in the same container as the nginx reverse proxy
  service meaning that it is not possible to deploy nginx without including canarie-api.

  This means that it is currently not possible to run this deployment without canarie-api
  or use a different monitoring application. This change fully separates the configuration
  for canarie-api and nginx so that a user can choose to run nginx with or without canarie-api.

  Canarie-api has been kept on the DEFAULT_CONF_DIRS list so that canarie-api is included by
  default, for backwards-compatibility. In order to run nginx without canarie-api, remove the
  `./conf/canarie-api` line from the DEFAULT_CONF_DIRS environment variable. 
  
  A user can also choose a specific version of the nginx docker image to use by specifying 
  the PROXY_IMAGE environment variable (default is "nginx"). Note that if canarie-api is used
  (by including the `./conf/canarie-api` line in DEFAULT_CONF_DIRS), then the PROXY_IMAGE 
  variable will be ignored.

[1.25.0](https://github.com/bird-house/birdhouse-deploy/tree/1.25.0) (2023-04-01)
------------------------------------------------------------------------------------------------------------------

## Fixes
- Geoserver: update to latest version 2.22.2 to get vulnerability fix

  For vulnerability in `jt-jiffle` < 1.1.22, see
  https://nvd.nist.gov/vuln/detail/CVE-2022-24816, and
  https://github.com/geosolutions-it/jai-ext/security/advisories/GHSA-v92f-jx6p-73rx.

  Changed to use the CORS (Cross-Origin Resource Sharing) default config from
  the image instead of our own.  Both are quite similar so if we can use the
  default config, future upgrade will be simpler.

  New Geoserver version will have `jt-jiffle` 1.1.24.  The old one had version 1.1.20.
  ```
  $ docker run -it --rm --entrypoint bash pavics/geoserver:2.22.2-kartoza-build20230226-r5-allow-change-context-root-and-fix-missing-stable-plugins

  | |/ /__ _ _ __| |_ ___ ______ _  |  _ \  ___   ___| | _____ _ __   / ___| ___  ___/ ___|  ___ _ ____   _____ _ __
  | ' // _` | '__| __/ _ \_  / _` | | | | |/ _ \ / __| |/ / _ \ '__| | |  _ / _ \/ _ \___ \ / _ \ '__\ \ / / _ \ '__|
  | . \ (_| | |  | || (_) / / (_| | | |_| | (_) | (__|   <  __/ |    | |_| |  __/ (_) |__) |  __/ |   \ V /  __/ |
  |_|\_\__,_|_|   \__\___/___\__,_| |____/ \___/ \___|_|\_\___|_|     \____|\___|\___/____/ \___|_|    \_/ \___|_|

  root@c3787dccea2d:/geoserver# find / -iname '**jt-jiffle**'
  /usr/local/tomcat/webapps/geoserver/WEB-INF/lib/jt-jiffle-language-1.1.24.jar
  /usr/local/tomcat/webapps/geoserver/WEB-INF/lib/jt-jiffle-op-1.1.24.jar
  root@c3787dccea2d:/geoserver#
  ```

  Used our own custom build image because the original kartoza image is missing 2 plugins that we use, see https://github.com/kartoza/docker-geoserver/issues/508 and to avoid excessively slow startup due to https://github.com/kartoza/docker-geoserver/issues/515.

  CORS config difference:
  ```diff
  --- web.xml.old 2023-03-22 16:10:20.000000000 -0400
  +++ web.xml.new 2023-03-22 16:10:06.000000000 -0400

       <filter>
           <filter-name>CorsFilter</filter-name>
           <filter-class>org.apache.catalina.filters.CorsFilter</filter-class>
           <init-param>
  -            <param-name>cors.allowed.methods</param-name>
  -            <param-value>GET,POST,HEAD,OPTIONS,PUT</param-value>
  -        </init-param>
  -        <init-param>
               <param-name>cors.allowed.origins</param-name>
               <param-value>*</param-value>
           </init-param>
           <init-param>
               <param-name>cors.allowed.headers</param-name>
  -            <param-value>Content-Type,X-Requested-With,accept,Origin,Access-Control-Request-Method,Access-Control-Request-Headers,Authorization,Authentication</param-value>
  +            <param-value>Content-Type,X-Requested-With,accept,Access-Control-Request-Method,Access-Control-Request-Headers,If-Modified-Since,Range,Origin,Authorization</param-value>
  +        </init-param>
  +        <init-param>
  +            <param-name>cors.exposed.headers</param-name>
  +            <param-value>Access-Control-Allow-Origin,Access-Control-Allow-Credentials</param-value>
           </init-param>
       </filter>
  ```
  Missing `cors.allowed.methods`, new `cors.exposed.headers`.

  For `cors.allowed.headers`, missing `Authentication`, new `If-Modified-Since,Range`.

  Hopefully everything still works with the new CORS config and future upgrade will be simpler.

  Tested with the following notebooks, hopefully CORS changes are effectively tested there:
  * https://github.com/Ouranosinc/pavics-sdi/blob/f4aecf64889f0c8503ea67b59b6558ae18407cf6/docs/source/notebooks/WFS_example.ipynb
  * https://github.com/Ouranosinc/pavics-sdi/blob/f4aecf64889f0c8503ea67b59b6558ae18407cf6/docs/source/notebooks/regridding.ipynb
  * https://github.com/bird-house/finch/blob/877312d325d4de5c3efcb4f1f75fbe5cd22660d6/docs/source/notebooks/subset.ipynb
  * https://github.com/Ouranosinc/raven/blob/0be6d77d71bcaf4546de97b13bafc6724068a73d/docs/source/notebooks/01_Getting_watershed_boundaries.ipynb
    with `RAVEN_GEO_URL` pointing to another Geoserver (also from this PR) to
    test CORS (Cross-Origin Resource Sharing)

## Changes
- Raven: allow to customize the Geoserver it will use

  Useful to test the local Geoserver or to have your own Geoserver with your
  own data.  Default to PAVICS Geoserver.

  Set `RAVEN_GEO_URL` in `env.local` to something like `https://host/geoserver/`.

- env.local.example: change default Geoserver admin user from 'admin' to 'admingeo'

  This only impacts new deployment when `env.local.example` is instanciated
  to `env.local`.

  This is to avoid confusion with the admin user of Magpie, which is also 'admin'.


[1.24.1](https://github.com/bird-house/birdhouse-deploy/tree/1.24.1) (2023-03-27)
------------------------------------------------------------------------------------------------------------------

## Fixes
- Cowbird: Resolve `celery` tasks not properly registered for dispatching from the API to the worker service.

  When calling the `https://${PAVICS_FDQN_PUBLIC}/cowbird/version` endpoint, a task is submitted to `cowbird-worker`
  to validate that it is responsive and in sync with `cowbird`. The instance was reporting an error indicating that
  `celery` tasks were not properly detected.

  To facilitate detection of this kind of problem, better error log reporting was added to the `/version` endpoint
  under [`cowbird==1.1.1`](https://github.com/Ouranosinc/cowbird/tree/1.1.0).

[1.24.0](https://github.com/bird-house/birdhouse-deploy/tree/1.24.0) (2023-03-22)
------------------------------------------------------------------------------------------------------------------
## Fixes
- Make all components pluggable

  The default stack was not configurable. This meant that if someone wanted to deploy a
  subset of the default stack there was no good way of configuring birdhouse-deploy to run
  this subset only. 

  Previously, additional components could be added to the stack (ex: weaver, cowbird, etc.)
  by adding them to the `EXTRA_CONF_DIRS` variable. This change extends this functionality
  to all components. 

  For backwards compatibility, all components that were in the original default stack are now
  listed in the `DEFAULT_CONF_DIRS` variable (in `birdhouse/default.env`). To run a subset of the
  original stack, update `DEFAULT_CONF_DIRS` to only include the configuration directories for
  the desired components.

  The components that will be added to the stack are only those whose configuration directory
  is listed in either `DEFAULT_CONF_DIRS` or `EXTRA_CONF_DIRS`. Note that some components are
  dependent on others to run and will automatically add the other components to the stack as 
  a dependency. For example, twitcher requires magpie so if you only specify twitcher, magpie
  will be added to the stack as well. To inspect component dependencies, look at the 
  `COMPONENT_DEPENDENCIES` environment variable that is extended in some `default.env` files.
  For example, `birdhouse/config/twitcher/default.env` contains:

  ```shell
  COMPONENT_DEPENDENCIES="
    $COMPONENT_DEPENDENCIES
    ./config/magpie
  ```

  Components can also have optional dependencies. These are additional configuration options to
  run if both components are deployed in the stack at the same time. These are defined in the
  `config/*/docker-compose-extra.yml` files where the `*` refers to another component that _could be_
  deployed. For example, `birdhouse/config/raven/config/magpie/docker-compose-extra.yml` contains
  additional configuration settings for the raven docker service that only apply if magpie is
  also deployed. This relaxes some dependencies between components and allows more flexibility
  when choosing what parts of the stack to deploy.

## Changes:

- Cowbird: Updated Cowbird config for user workspaces and for working callbacks to Magpie.

  When enabling Cowbird, the config will now mount a different working directory with JupyterHub, which 
  corresponds to the user workspaces created with Cowbird. These workspaces will use symlinks to the Jupyterhub 
  data directories.

  For example, we have the original directory, which is still mounted by default by JupyterHub, which contains 
  the user's notebooks :
![image](https://user-images.githubusercontent.com/36516122/223465560-ea4a7d6f-807d-49ae-8500-49a6e6ed677a.png)

  If Cowbird is enabled, JupyterHub mounts Cowbird's workspace instead, which has a symlink to the other dir :
![image](https://user-images.githubusercontent.com/36516122/223465960-ce81e829-b703-4374-b059-685b0e684a57.png)

  Cowbird's workspace can also contain other files related to other services.
  Cowbird's workspace directory is defined by the added environment variable `USER_WORKSPACES`.

- JupyterHub: Updated config to support Cowbird, which uses a different working directory.

  JupyterHub now mounts the variable `WORKSPACE_DIR` when starting a JupyterLab instance. It will refer to the 
  original JupyterHub data directory by default, and if Cowbird is activated, it will be overridden to refer 
  to Cowbird's workspace instead.

  In JupyterHub with Cowbird enabled, the `writable-workspace` is the Cowbird user's workspace :
![image](https://user-images.githubusercontent.com/36516122/223800065-0e0ab578-4e67-4d21-8d7c-552c87ceea41.png)

  When we open the notebooks dir, it displays the files found at the symlink's source :
![image](https://user-images.githubusercontent.com/36516122/223800540-769d50a2-4ce8-480f-b75d-c6d4e29dead1.png)

- Updated eo and nlp images to latest version in the `env.local.example` config.

[1.23.3](https://github.com/bird-house/birdhouse-deploy/tree/1.23.3) (2023-02-17)
------------------------------------------------------------------------------------------------------------------

## Fixes
- Vagrant: fix mismatch docker-compose version with autodeploy resulting in containers being recreated

  Normally a `./pavics-compose.sh up -d` after an autodeploy has run, should
  only create any new containers, not recreating all the existing containers.

  This is because docker-compose v2 seems to be incompatible with old v1.  This
  is the last v1 version still compatible with the docker-compose in the
  autodeploy.

  This old docker-compose v1 seems to work just fine with latest docker cli.

  This is the quickest way to get Vagrant boxes up and running without causing
  backward incompatible changes to existing production deployment.

  If we update the docker-compose inside autodeploy to v2, this will force all
  existing deployment to also update their installed docker-compose.

  A more long term solution would be to always run `./pavics-compose.sh` using
  the docker-compose image from autodeploy so the version will always match and
  any docker-compose version update will be transparent.

- Vagrant: ubuntu version after bionic is missing net-tools package pre-installed

  net-tools package is required to have the route command to set the default
  gateway.  Without the default gateway set, the VM will not be visible outside
  of its own subnet.


[1.23.2](https://github.com/bird-house/birdhouse-deploy/tree/1.23.2) (2023-02-17)
------------------------------------------------------------------------------------------------------------------

## Fixes
- Fix birds not creating their wps output under each bird name

  Before this fix, finch, raven, flyingpigeon were dumping their output directly
  under `https://PAVICS_HOST/wpsoutputs/`.

  With this fix, it will be under each bird name, ex:
  `https://PAVICS_HOST/wpsoutputs/finch/` which is cleaner and follows what
  malleefowl and hummingbird already does.

  Fixes https://github.com/bird-house/birdhouse-deploy/issues/11.
  Fixes https://crim-ca.atlassian.net/browse/DAC-398

  Requires PR https://github.com/Ouranosinc/pavics-sdi/pull/280,
  https://github.com/bird-house/finch/pull/273 and
  https://github.com/Ouranosinc/raven/pull/459.

  If `optional-components/secure-data-proxy` is enabled, might need some
  additional permissions for each bird in
  https://github.com/bird-house/birdhouse-deploy/blob/master/birdhouse/optional-components/secure-data-proxy/config/magpie/config.yml.template.

[1.23.1](https://github.com/bird-house/birdhouse-deploy/tree/1.23.1) (2023-02-13)
------------------------------------------------------------------------------------------------------------------

[//]: # (list changes here, using '-' for each new entry, remove this when items are added)

## Fixes
- Vars in `DELAYED_EVAL` list are not expanded properly outside of `pavics-compose.sh`

  There are other scripts sourcing `default.env` and `env.local` and all those
  scripts have to expand the vars in `DELAYED_EVAL` list to have their actual
  values.

  Only scripts using the 3 variables in `DELAYED_EVAL` list are broken.

  `DELAYED_EVAL` was previously introduced in PR https://github.com/bird-house/birdhouse-deploy/pull/272.

  **Sample errors**

  `fix-geoserver-data-dir-perm` (called at the end of `pavics-compose.sh`):
  ```
  fix GeoServer data dir permission on first run only, when data dir do not exist yet.
  + DATA_DIR='${DATA_PERSIST_ROOT}/geoserver'
  + '[' -n  ]
  + docker run --rm --name fix-geoserver-data-dir-perm --volume '${DATA_PERSIST_ROOT}/geoserver:/datadir' --env FIRST_RUN_ONLY bash:5.1.4 bash -xc 'if [ -z "$FIRST_RUN_ONLY" -o ! -f /datadir/global.xml ]; \
      then chown -R 1000:10001 /datadir; else echo "No execute."; fi'
  docker: Error response from daemon: create ${DATA_PERSIST_ROOT}/geoserver: "${DATA_PERSIST_ROOT}/geoserver" includes invalid characters for a local volume name, only "[a-zA-Z0-9][a-zA-Z0-9_.-]" are allowed. If you intended to pass a host directory, use absolute path.
  ```

  `trigger-deploy-notebook` (broke notebook deploy job):
  ```
  + TMP_SCRIPT=/tmp/notebookdeploy/notebookdeploy.XXXXXXIfafFK/deploy-notebook
  + cat
  + chmod a+x /tmp/notebookdeploy/notebookdeploy.XXXXXXIfafFK/deploy-notebook
  + docker run --rm --name deploy_tutorial_notebooks -u root -v /tmp/notebookdeploy/notebookdeploy.XXXXXXIfafFK/deploy-notebook:/deploy-notebook:ro -v /tmp/notebookdeploy/notebookdeploy.XXXXXXIfafFK/tutorial-notebooks:/tutorial-notebooks:ro -v '${DATA_PERSIST_ROOT}/jupyterhub_user_data:/notebook_dir:rw' --entrypoint /deploy-notebook bash:5.1.4
  docker: Error response from daemon: create ${DATA_PERSIST_ROOT}/jupyterhub_user_data: "${DATA_PERSIST_ROOT}/jupyterhub_user_data" includes invalid characters for a local volume name, only "[a-zA-Z0-9][a-zA-Z0-9_.-]" are allowed. If you intended to pass a host directory, use absolute path.
  ```

  **Explanation of the fix**

  All scripts have to remember to call function `process_delayed_eval` in order
  to obtain the real value of each vars in `DELAYED_EVAL` list.

  Centralized all logic about reading configs (config files reading order,
  remember to call `process_delayed_eval`) to avoid mistake and to ease updating
  logic in the future.  Too many scripts were reading the configs  themselves and
  some are not doing it properly, ex: forgot to hide password when reading
  `env.local`.

  **All scripts should do this going forward**

  ```sh
  # Set variable COMPOSE_DIR to the dir containing pavics-compose.sh and docker-compose.yml.

  # Source the script providing function read_configs.
  # read_configs uses COMPOSE_DIR to find default.env and env.local.
  . $COMPOSE_DIR/read-configs.include.sh

  # Call function read_configs to read the various config files in the appropriate order and process delayed eval vars properly.
  read_configs
  ```

[1.23.0](https://github.com/bird-house/birdhouse-deploy/tree/1.23.0) (2023-02-10)
------------------------------------------------------------------------------------------------------------------

## Changes:

- secure-data-proxy: add new [`secure-data-proxy`][secure-data-proxy] optional component.

  When enabled, this component will enforce authentication and authorization to be resolved against the `/wpsoutputs`
  endpoint prior to accessing the results produced by WPS executions. A Magpie service named `secure-data-proxy` is
  created to define the resource and permission hierarchy of directories and files the users and groups can access.
  When disabled, the original behavior to provide open access to `/wpsoutputs` is employed.

  A variable named `SECURE_DATA_PROXY_AUTH_INCLUDE` is dynamically assigned based on the activation or not of this
  component. Corresponding validation of optional/mandatory/delayed-eval variables used by this component are also
  applied dynamically, as well as mounting the necessary `nginx` and `docker-compose` extended configurations.

- Weaver: adjust user-context output directory hooks and permissions for [`secure-data-proxy`][secure-data-proxy].

  When a process defined in Weaver (either a WPS provider or a local definition) is executed by a user that was granted
  authorization to run a job, the corresponding user-context directory under `/wpsoutputs/users/{user-id}` will be used
  for storing the execution outputs and will have the appropriate permissions set for that user to grant them access to
  those outputs.

## Fixes:

- Magpie/Twitcher: update minimum version `magpie>=3.31.0` to employ `twitcher>=0.8.0` in `MapgieAdatepr`.

  - Resolve an issue where `response.request` references were not set in OWS proxy responses when handled by Twitcher.
    This caused `MapgieAdatepr` response hooks to fail, which in turn caused failing requests for any non-WPS
    service that defined any proxy request hook, such as in the case of [`weaver`][weaver-component] component.

  - Adds the Twitcher ``/ows/verify/{service_name}[/{extra_path}`` endpoint employed for validating authorized access
    to Magpie service/resources, in the same fashion as the protected proxy endpoint, but without performing the proxied
    request toward the target service. This is mandatory for using the new [`secure-data-proxy`][secure-data-proxy] 
    optional component, otherwise the proxy endpoint triggers data download twice, once for authorization and another
    for actually accessing the data.

  See also [Ouranosinc/Magpie#571](https://github.com/Ouranosinc/Magpie/pull/571)
  and [bird-house/twitcher#118](https://github.com/bird-house/twitcher/pull/118).

[secure-data-proxy]: birdhouse/optional-components/secure-data-proxy
[weaver-component]: birdhouse/components/weaver

[1.22.11](https://github.com/bird-house/birdhouse-deploy/tree/1.22.11) (2023-02-03)
------------------------------------------------------------------------------------------------------------------

## Changes:
- Proxy: add `/components` endpoint that provides a JSON list of loaded components by the platform.

  Prior to this functionality, it was impossible to know which potential capabilities, services or behaviors were to be
  expected by a given DACCS/PAVICS/birdhouse instance. Using this endpoint, nodes can obtain minimal machine-readable
  details about their supported capabilities, allowing better interoperability.
  
  Furthermore, developers maintaining distinct stacks and integrating different features can have a better
  understanding of behaviors by the various web services when performing requests against a given node.

[1.22.10](https://github.com/bird-house/birdhouse-deploy/tree/1.22.10) (2023-01-31)
------------------------------------------------------------------------------------------------------------------

## Fixes:
- Weaver: fixes for running `post-docker-compose-up` operation.

  - When the target `curl` image was not already available on the machine (each time for ephemeral test instances), the 
    docker pull outputs on the first call would mangle the monitoring messages. An initial pull is done to avoid it.

  - When running on `sh` (as expected by the script's shebang), the utility variable `$RANDOM` is missing.
    A POSIX portable equivalent is used if `$RANDOM` could not be resolved.

[1.22.9](https://github.com/bird-house/birdhouse-deploy/tree/1.22.9) (2023-01-25)
------------------------------------------------------------------------------------------------------------------

## Changes:
- Jupyter: allow recursive directory deletion

  This was not possible before since non-empty dir deletion was not possible.

- Jupyter: re-enable terminal for all users

  It was disabled to avoid malicious usage but with the monitoring in
  place and the demo account restricted to limited resources, it's
  probably safe to try enabling this again.

  For legitimate users, not having the terminal is pretty annoying.
  Should not penalize legit users for some rogue users.


[1.22.8](https://github.com/bird-house/birdhouse-deploy/tree/1.22.8) (2023-01-24)
------------------------------------------------------------------------------------------------------------------

## Fixes:

- Weaver: fix post script to be compatible with autodeploy

  Autodeploy runs inside its own docker container and `curl` is not available.
  Therefore Weaver post script should be using `curl` from a docker image
  instead of locally installed flavor.

- Jupyter: fix the Docker Spawner `start` function to support JupyterHub image selection names 
  that use the `<name>:<version>` format.


[1.22.7](https://github.com/bird-house/birdhouse-deploy/tree/1.22.7) (2022-12-23)
------------------------------------------------------------------------------------------------------------------

## Fixes:

- Overriding `DATA_PERSIST_ROOT` in `env.local` do not take effect for
  `JUPYTERHUB_USER_DATA_DIR`, `MAGPIE_PERSIST_DIR`, and `GEOSERVER_DATA_DIR`.

  These 3 vars will have to be delayed evaluated for override in `env.local` to
  take effect.

  For a variable to be delayed evaluated, it has to be defined using
  single-quote and be added to the list of `DELAYED_EVAL` in `default.env`.

  If those steps are forgotten in `env.local`, it will still work since
  `env.local` is the last file to be read.  However those steps should not be
  forgotten in any `default.env` for all components.

  So the impact or burden is on the developpers to write their `default.env`
  file properly, not on the users that only modify the `env.local` file.

  All `default.env` files header have been updated with notice about this new
  delayed evaluation feature.

  Fixes https://github.com/bird-house/birdhouse-deploy/issues/270.

## Changes:

- Warn when a dir in `EXTRA_CONF_DIRS` does not exist.

  Most likely a typo in a new dir.  Just warn and not exit directly to avoid
  leaving the entire platform down during an unattended autodeploy since no
  one is around to take immediate action.

  Fixes https://github.com/bird-house/birdhouse-deploy/issues/266.


[1.22.6](https://github.com/bird-house/birdhouse-deploy/tree/1.22.6) (2022-12-19)
------------------------------------------------------------------------------------------------------------------

## Changes:

- new Jupyter env for `urlpath`

  See PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/112

  - Adds `urlpath` for https://github.com/Ouranosinc/pavics-sdi/pull/268, fixes https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/issues/110
  - Relevant changes (alphabetical order):
  ```diff
  <   - climpred=2.2.0=pyhd8ed1ab_0
  >   - climpred=2.3.0=pyhd8ed1ab_0

  <   - dask=2022.11.0=pyhd8ed1ab_0
  >   - dask=2022.11.1=pyhd8ed1ab_0

  <   - flox=0.6.3=pyhd8ed1ab_0
  >   - flox=0.6.4=pyhd8ed1ab_0

  <   - h5netcdf=1.0.2=pyhd8ed1ab_0
  >   - h5netcdf=1.1.0=pyhd8ed1ab_0

  <   - numpy=1.23.4=py38h7042d01_1
  >   - numpy=1.23.5=py38h7042d01_0

  >   - urlpath=1.2.0=pyhd8ed1ab_0
  ```


[1.22.5](https://github.com/bird-house/birdhouse-deploy/tree/1.22.5) (2022-12-02)
------------------------------------------------------------------------------------------------------------------

## Changes:

- new Jupyter env with latest of everything

  PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/106

  - Unpin Shapely (fixes https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/issues/99)
  - Unpin Dask (fixes https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/issues/100)
  - Pin `intake-esm` since newer version activated validation of optional fields and broke our notebooks (https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/issues/109)
  - Mamba is fully usable alongside Conda.  Previously the installation used Mamba but then Mamba is uninstalled because it breaks the jupyter conda plugin
  - New packages:
    - performance optimization: flox, pyston
    - new feature: geopy, streamlit, python-pptx
    - jupyter plugin: jupyterlab-tabular-data-editor to easily edit `.csv` files
   - Removed package:
     - jupyter-panel-proxy, interfere with `panel serve` commands
  - Relevant changes (alphabetical order):
  ```diff
  <   - bokeh=2.4.2=py38h578d9bd_1
  >   - bokeh=2.4.3=pyhd8ed1ab_3
  
  <   - cartopy=0.20.1=py38hf9a4893_1
  >   - cartopy=0.21.0=py38hf6c3373_3
  
  <   - cf_xarray=0.7.2=pyhd8ed1ab_0
  >   - cf_xarray=0.7.5=pyhd8ed1ab_0
  
  <   - cftime=1.6.0=py38h71d37f0_1
  >   - cftime=1.6.2=py38h26c90d9_1
  
  <   - clisops=0.9.0=pyh6c4a22f_0
  >   - clisops=0.9.3=pyh1a96a4e_0
  
  # unpin
  <   - dask=2022.1.0=pyhd8ed1ab_0
  >   - dask=2022.11.0=pyhd8ed1ab_0
  
  # new
  >   - flox=0.6.3=pyhd8ed1ab_0
  
  <   - fiona=1.8.20=py38hbb147eb_2
  >   - fiona=1.8.22=py38hc72d8cd_2
  
  <   - gdal=3.3.3=py38hcf2042a_0
  >   - gdal=3.5.3=py38h1f15b03_3
  
  <   - geopandas=0.10.2=pyhd8ed1ab_1
  >   - geopandas=0.12.1=pyhd8ed1ab_1
  
  # new
  >   - geopy=2.3.0=pyhd8ed1ab_0
  >   - pyston_lite=2.3.4=py38h0a891b7_1
  >   - python-pptx=0.6.21=pyhd8ed1ab_0
  
  <   - ravenpy=0.7.8=pyh8a188c0_0
  >   - ravenpy=0.9.0=pyha21a80b_0
  
  # pip to conda
  <     - requests-magpie==0.1.1
  >   - requests-magpie=0.2.0=pyhd8ed1ab_0
  
  <   - rioxarray=0.11.1=pyhd8ed1ab_0
  >   - rioxarray=0.13.1=pyhd8ed1ab_0
  
  <   - roocs-utils=0.6.1=pyh6c4a22f_0
  >   - roocs-utils=0.6.3=pyh1a96a4e_0
  
  # unpin
  <   - shapely=1.7.1=py38hb7fe4a8_5
  >   - shapely=1.8.5=py38hafd38ec_2
  
  # new
  >   - streamlit=1.15.0=pyhd8ed1ab_0
  
  <   - xarray=2022.3.0=pyhd8ed1ab_0
  >   - xarray=2022.10.0=pyhd8ed1ab_0
  
  <   - xclim=0.36.0=pyhd8ed1ab_0
  >   - xclim=0.39.0=pyhd8ed1ab_0
  
  <   - xesmf=0.6.2=pyhd8ed1ab_0
  >   - xesmf=0.6.3=pyhd8ed1ab_1
  
  # new
  >     - jupyterlab-tabular-data-editor==1.0.0
  ```

- documentation:
  - Add `Weaver` component diagram to better illustrate its interactions with other *birdhouse* services.
  - Move `monitoring` component images under its respective component directory.

[1.22.4](https://github.com/bird-house/birdhouse-deploy/tree/1.22.4) (2022-11-08)
------------------------------------------------------------------------------------------------------------------

## Changes:

- autodeploy: allow repos to optionally decide if a deploy is required

  Useful when only a subset of file changes in a repo will actually impact deployment.

  Without this mechanism any file changes in a repo will trigger a deployment, which
  would cost a full platform restart for no reason.

  Var `GIT_CHANGED_FILES` is given to optional script `<repo_root>/autodeploy/conditional-trigger`
  and only an exit code 0 will trigger deploy.

- fix-geoserver-data-dir-perm: allow overriding data dir to use on another instance of Geoserver


[1.22.3](https://github.com/bird-house/birdhouse-deploy/tree/1.22.3) (2022-10-25)
------------------------------------------------------------------------------------------------------------------

## Fixes:

- jupyter env: reap defunct processes with proper pid 1 init process

    Before, process hierarchy:

    ```sh
    $ docker exec jupyter-lvu ps -efH
    UID          PID    PPID  C STIME TTY          TIME CMD
    jenkins       88       0  0 21:01 ?        00:00:00 ps -efH
    jenkins        1       0  0 18:57 ?        00:00:00 /opt/conda/bin/python /opt/conda/bin/conda run -n birdy /usr/local/bin/start-notebook.sh --ip=0.0.0.0 --port=8888 --notebook-dir=/notebook_dir --SingleUserNotebookApp.default_url=/lab --debug --disable-user-config --NotebookApp.terminals_enabled=False --NotebookApp.shutdown_no_activity_timeout=345600 --MappingKernelManager.cull_idle_timeout=86400 --MappingKernelManager.cull_connected=True
    jenkins        7       1  0 18:57 ?        00:00:00   /bin/bash /tmp/tmpmx46emji
    jenkins       21       7  0 18:57 ?        00:00:27     /opt/conda/envs/birdy/bin/python3.8 /opt/conda/envs/birdy/bin/jupyterhub-singleuser --ip=0.0.0.0 --port=8888 --notebook-dir=/notebook_dir --SingleUserNotebookApp.default_url=/lab --debug --disable-user-config --NotebookApp.terminals_enabled=False --NotebookApp.shutdown_no_activity_timeout=345600 --MappingKernelManager.cull_idle_timeout=86400 --MappingKernelManager.cull_connected=True
    ```

    Before, reproducible defunct firefox-esr processes:
    ```sh
    True
    [{'pid': 302, 'create_time': 1666550504.76, 'name': 'firefox-esr'}, {'pid': 303, 'create_time': 1666550504.8, 'name': 'firefox-esr'}]

    True
    [{'pid': 302, 'create_time': 1666550504.76, 'name': 'firefox-esr'}, {'pid': 303, 'create_time': 1666550504.8, 'name': 'firefox-esr'}, {'pid': 692, 'create_time': 1666550867.43, 'name': 'firefox-esr'}, {'pid': 693, 'create_time': 1666550867.45, 'name': 'firefox-esr'}]

    $ docker exec jupyter-lvu ps
        PID TTY          TIME CMD
          1 ?        00:00:00 conda
          7 ?        00:00:00 bash
         21 ?        00:00:20 jupyterhub-sing
        296 ?        00:00:00 geckodriver <defunct>
        302 ?        00:00:00 firefox-esr <defunct>
        303 ?        00:00:45 firefox-esr <defunct>
        379 ?        00:00:00 Web Content <defunct>
        407 ?        00:00:04 WebExtensions <defunct>
        486 ?        00:00:00 Web Content <defunct>
        507 ?        00:00:38 file:// Content <defunct>
        581 ?        00:00:15 python
        686 ?        00:00:00 geckodriver
        692 ?        00:00:00 firefox-esr <defunct>
        693 ?        00:00:34 firefox-esr
        768 ?        00:00:00 Web Content
        796 ?        00:00:04 WebExtensions
        874 ?        00:00:13 file:// Content
        902 ?        00:00:00 Web Content
        961 ?        00:00:00 ps
    ```

    After, process hierarchy:

    ```sh
    $ docker exec jupyter-lvu2 ps -efH
    UID          PID    PPID  C STIME TTY          TIME CMD
    jenkins       49       0  0 21:01 ?        00:00:00 ps -efH
    jenkins        1       0  0 21:00 ?        00:00:00 /sbin/docker-init -- conda run -n birdy /usr/local/bin/start-notebook.sh --ip=0.0.0.0 --port=8888 --notebook-dir=/notebook_dir --SingleUserNotebookApp.default_url=/lab --debug --disable-user-config --NotebookApp.terminals_enabled=False --NotebookApp.shutdown_no_activity_timeout=345600 --MappingKernelManager.cull_idle_timeout=86400 --MappingKernelManager.cull_connected=True
    jenkins        7       1  0 21:00 ?        00:00:00   /opt/conda/bin/python /opt/conda/bin/conda run -n birdy /usr/local/bin/start-notebook.sh --ip=0.0.0.0 --port=8888 --notebook-dir=/notebook_dir --SingleUserNotebookApp.default_url=/lab --debug --disable-user-config --NotebookApp.terminals_enabled=False --NotebookApp.shutdown_no_activity_timeout=345600 --MappingKernelManager.cull_idle_timeout=86400 --MappingKernelManager.cull_connected=True
    jenkins        8       7  0 21:00 ?        00:00:00     /bin/bash /tmp/tmp6chrvz_j
    jenkins       22       8  9 21:00 ?        00:00:06       /opt/conda/envs/birdy/bin/python3.8 /opt/conda/envs/birdy/bin/jupyterhub-singleuser --ip=0.0.0.0 --port=8888 --notebook-dir=/notebook_dir --SingleUserNotebookApp.default_url=/lab --debug --disable-user-config --NotebookApp.terminals_enabled=False --NotebookApp.shutdown_no_activity_timeout=345600 --MappingKernelManager.cull_idle_timeout=86400 --MappingKernelManager.cull_connected=True
    ```

    After, unable to reproduce defunct firefox-esr processes:
    ```sh
    False
    []

    True
    [{'create_time': 1666550929.17, 'pid': 962, 'name': 'firefox-esr'}]

    $ docker exec jupyter-lvu2 ps
        PID TTY          TIME CMD
          1 ?        00:00:00 docker-init
          6 ?        00:00:00 conda
          7 ?        00:00:00 bash
         21 ?        00:00:20 jupyterhub-sing
        928 ?        00:00:11 python
        955 ?        00:00:00 geckodriver
        962 ?        00:00:46 firefox-esr
       1035 ?        00:00:00 Web Content
       1061 ?        00:00:03 WebExtensions
       1176 ?        00:00:00 Web Content
       1223 ?        00:00:21 file:// Content
       1327 ?        00:00:00 ps
    ```

    How to reproduce defunct firefox-esr processes (run twice to create defunct processes from first run):
    ```python
    import psutil
    import panel as pn
    import numpy as np
    import xarray as xr

    pn.extension()

    def checkIfProcessRunning(processName):
        '''
        Check if there is any running process that contains the given name processName.
        '''
        #Iterate over the all the running process
        for proc in psutil.process_iter():

            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True

        return False;

    def findProcessIdByName(processName):
        '''
        Get a list of all the PIDs of a all the running process whose name contains
        the given string processName
        '''
        listOfProcessObjects = []
        #Iterate over the all the running process
        for proc in psutil.process_iter():

           pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
           # Check if process name contains the given name string.
           if processName.lower() in pinfo['name'].lower() :
               listOfProcessObjects.append(pinfo)

        return listOfProcessObjects;

    print(checkIfProcessRunning('firefox-esr'))
    print(findProcessIdByName('firefox-esr'))

    import hvplot.xarray
    panel = pn.Column()
    data = xr.DataArray(np.random.rand(200,400), name='data')
    app = pn.Column(data.hvplot.quadmesh())
    app.save('test.html')
    for ii in range(0,10):
        data = xr.DataArray(np.random.rand(200,400), name='data')
        app = pn.Column(data.hvplot.quadmesh())
        app.save(f"test{ii}.png")
    print(checkIfProcessRunning('firefox-esr'))
    print(findProcessIdByName('firefox-esr'))
    ```


[1.22.2](https://github.com/bird-house/birdhouse-deploy/tree/1.22.2) (2022-09-19)
------------------------------------------------------------------------------------------------------------------

## Changes:

- `deploy-data`: allow `post_actions` to vary depending on files changed on subsequent run

  Useful for `post_actions` to know the git version change between the current
  and the previous run and which files are impacted.

  Actions can perform extra git commands if needed or simply used the
  provide git diff output and/or rsync output to decide what to do next.

  **Non-breaking changes**
  - `deploy-data` script: add new vars `GIT_PREVIOUS_COMMIT_HASH`, `GIT_NEW_COMMIT_HASH`, `GIT_CHANGED_FILES`,
    `RSYNC_OUTPUT`, accessible to `post_actions` scripts.


[1.22.1](https://github.com/bird-house/birdhouse-deploy/tree/1.22.1) (2022-09-01)
------------------------------------------------------------------------------------------------------------------

## Changes:

- birdhouse-deploy: fix bump versioning methodology to auto-update `releaseTime` accordingly.
  
  ### Relevant changes
  * Adds `Makefile` to run basic DevOps maintenance commands on the repository.
  * Adds `RELEASE.txt` with the active release tag and datetime.
  * Replace `now:` directives by `utcnow:` to report time properly according to employed ISO format.
  * Update contribution guidelines regarding methodology to create a new revision.

[1.22.0](https://github.com/bird-house/birdhouse-deploy/tree/1.22.0) (2022-08-24)
------------------------------------------------------------------------------------------------------------------

## Changes:
- Geoserver: Adds `./optional-components/test-geoserver-secured-access`, to test Twitcher-protected access to Geoserver
  
  Relevant changes:
  - New Provider (Magpie) : geoserver-secured
  - New Location (Proxy) : /geoserver-secured
  - Copied current WFS GetCapabilities and DescribeFeatureType permissions to new Provider

[1.21.1](https://github.com/bird-house/birdhouse-deploy/tree/1.21.1) (2022-08-24)
------------------------------------------------------------------------------------------------------------------

## Changes

- birdhouse-deploy: fix invalid `canarie-api-full-monitoring` endpoints adding double `/` when substituting variables.
- birdhouse-deploy: add optional variables `MAGPIE_LOG_LEVEL` and `TWITCHER_LOG_LEVEL` (both `INFO` by default) to 
  allow instead to customize reported details by instances for debugging purposes. Note that setting `DEBUG` will leak
  sensible details in their logs and should be reserved only for testing environments.

[1.21.0](https://github.com/bird-house/birdhouse-deploy/tree/1.21.0) (2022-08-19)
------------------------------------------------------------------------------------------------------------------

## Changes

- Cowbird: add new service [Ouranosinc/cowbird](https://github.com/Ouranosinc/cowbird/) to the stack.

  ### Relevant changes
  * Cowbird can be integrated to the instance using [components/cowbird](./birdhouse/components/cowbird) 
    when added to in ``EXTRA_CONF_DIRS`` in the ``env.local`` variable definitions.
  * Offers syncing operations between various other *birds* in order to apply user/group permissions between
    corresponding files, granting access to them seamlessly through distinct services.
  * Allows event and callback triggers to sync permissions and volume paths between API endpoints and local storages.

- Nginx: add missing `X-Forwarded-Host` header to allow `Twitcher` to report the proper server host location when the
  service to be accessed uses an internal Docker network reference through the service private URL defined in `Magpie`.

- birdhouse-deploy: fix missing `GEOSERVER_ADMIN_USER` variable templating 
  from [pavics-compose.sh](./birdhouse/pavics-compose.sh).

[1.20.4](https://github.com/bird-house/birdhouse-deploy/tree/1.20.4) (2022-08-19)
------------------------------------------------------------------------------------------------------------------

## Changes:

- Weaver: update `weaver` component default version to [4.22.0](https://github.com/crim-ca/weaver/tree/4.22.0).

  ### Relevant changes
  * Minor improvements to facilitate retrieval of XML and JSON Process definition and their seamless execution with 
    XML or JSON request contents using either WPS or *OGC API - Processes* REST endpoints interchangeably.
  * Fixes to WPS remote provider parsing registered in Weaver to successfully perform the relevant process executions.
  * Add WPS remote provider retry conditions to handle known problematic cases during process execution (on remote)
    that can lead to sporadic failures of the monitored job. When possible, retried submission leading to successful
    execution will result in the monitored job to complete successfully and transparently to the user. Relevant errors
    and retry attempts are provided in the job logs.
  * Add WPS remote provider status exception response as XML message from the failed remote execution within the
    monitored local job logs to help users understand how to resolve any encountered issue on the remote service.
  * Bump version ``OWSLib==0.26.0`` to fix ``processVersion`` attribute resolution from WPS remote provider definition
    to populate ``Process.version`` property employed in converted `Process` description to `OGC API - Process` schema
    (relates to `geopython/OWSLib#794 <https://github.com/geopython/OWSLib/pull/794>`_).

[1.20.3](https://github.com/bird-house/birdhouse-deploy/tree/1.20.3) (2022-08-18)
------------------------------------------------------------------------------------------------------------------

## Fixes:
- Canarie-api: fix unable to verify LetsEncrypt SSL certs

  LetsEncrypt older root certificate "DST Root CA X3" expired on September 30,
  2021, see https://letsencrypt.org/docs/dst-root-ca-x3-expiration-september-2021/

  All the major browsers and OS platform has previously added the new root
  certificate "ISRG Root X1" ahead of time so the transition to the new
  root certificate is seemless for all clients.

  Python `requests` package bundle their own copy of known root
  certificates and is late to add this new root cert "ISRG Root X1".  Had
  it automatically fallback to the OS copy of the root cert bundle, this
  would have been seemless.

  The fix is to force `requests` to use the OS copy of the root cert bundle.

  Fix for this error:
  ```
  $ docker exec proxy python -c "import requests; requests.request('GET', 'https://lvupavicsmaster.ouranos.ca/geoserver')"
  Traceback (most recent call last):
    File "<string>", line 1, in <module>
    File "/usr/local/lib/python2.7/dist-packages/requests/api.py", line 50, in request
      response = session.request(method=method, url=url, **kwargs)
    File "/usr/local/lib/python2.7/dist-packages/requests/sessions.py", line 468, in request
      resp = self.send(prep, **send_kwargs)
    File "/usr/local/lib/python2.7/dist-packages/requests/sessions.py", line 576, in send
      r = adapter.send(request, **kwargs)
    File "/usr/local/lib/python2.7/dist-packages/requests/adapters.py", line 433, in send
      raise SSLError(e, request=request)
  requests.exceptions.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:661)
  ```

  Default SSL root cert bundle of `requests`:
  ```
  $ docker exec proxy python -c "import requests; print requests.certs.where()"
  /usr/local/lib/python2.7/dist-packages/requests/cacert.pem
  ```

  Confirm the fix works:
  ```
  $ docker exec -it proxy bash
  root@37ed3a2a03ae:/opt/local/src/CanarieAPI/canarieapi# REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt python -c "import requests; requests.request('GET', 'https://lvupavicsmaster.ouranos.ca/geoserver')"
  root@37ed3a2a03ae:/opt/local/src/CanarieAPI/canarieapi#

  $ docker exec proxy env |grep REQ
  REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
  ```

  Fixes https://github.com/bird-house/birdhouse-deploy/issues/198


[1.20.2](https://github.com/bird-house/birdhouse-deploy/tree/1.20.2) (2022-08-17)
------------------------------------------------------------------------------------------------------------------

## Changes:
- birdhouse-deploy: fix missing bump of server version reported in ``canarie`` service configuration

[1.20.1](https://github.com/bird-house/birdhouse-deploy/tree/1.20.1) (2022-08-11)
------------------------------------------------------------------------------------------------------------------

## Changes:
- GeoServer: enable metadata-plugin for modifying layer metadata, including bulk modifications

  See plugin documentation at https://docs.geoserver.org/2.19.x/en/user/community/metadata/index.html

  Related to issue https://github.com/Ouranosinc/pavics-sdi/issues/234

  Add new "Metadata" tab in Layer Edit page:
  ![Screenshot 2022-01-25 at 00-25-45 GeoServer Edit Layer](https://user-images.githubusercontent.com/11966697/150916419-fce99147-2903-414b-8b83-551709ef87d6.png)


[1.20.0](https://github.com/bird-house/birdhouse-deploy/tree/1.20.0) (2022-08-10)
------------------------------------------------------------------------------------------------------------------

## Changes

- Weaver: update `weaver` component default version from [4.12.0](https://github.com/crim-ca/weaver/tree/4.12.0)
  to [4.20.0](https://github.com/crim-ca/weaver/tree/4.20.0).
  See [full CHANGELOG](https://github.com/crim-ca/weaver/blob/4.20.0/CHANGES.rst) for details.

  ### Breaking changes
  * Docker commands that target `weaver-worker` to start or use `celery` must be adjusted according to how its new CLI
    resolves certain global parameters. Since the [celery-healthcheck](./birdhouse/components/weaver/celery-healthcheck)
    script uses this CLI, `celery` commands were adjusted to consider those changes. If custom scripts or command
    overrides are used to call `celery`, similar changes will need to be applied according to employed Weaver version.
    See details in [Weaver 4.15.0 changes](https://github.com/crim-ca/weaver/blob/master/CHANGES.rst#4150-2022-04-20).

  ### Relevant changes
  * Support OpenAPI-based `schema` field for Process I/O definitions to align with latest *OGC API - Processes* changes.
  * Support `Prefer` header to define execution mode of jobs according to latest *OGC API - Processes* recommendations.
  * Support `transmissionMode` to return file-based outputs by HTTP `Link` header references as desired.
  * Support deployment of new processes using YAML and CWL based request contents directly to remove the need to
    convert and indirectly embed their definitions in specific JSON schema structures.
  * Support process revisions allowing users to iteratively update process metadata and their definitions without full
    un/re-deployment of the complete process for each change. This also allows multiple process revisions to live
    simultaneously on the instance, which can be described or launched for job executions with specific tagged versions.
  * Add control query parameters to retrieve outputs in different JSON schema variations according to desired structure.
  * Add statistics collection following job execution to obtain machine resource usage by the executed process.
  * Improve handling of Content-Type definitions for reporting inputs, outputs and logs retrieval from job executions.
  * Fixes related to reporting of job results with different formats and URL references based on requested execution
    methods and control parameters.
  * Fixes to resolve pending vulnerabilities or feature integrations by package dependencies (`celery`, `pywps`, etc.).
  * Fixes related to parsing of WPS-1/2 remote providers URL from a CWL definition using `GetCapabilities` endpoint.
  * Fixes and addition of multiple Weaver CLI capabilities to employ new features.


[1.19.2](https://github.com/bird-house/birdhouse-deploy/tree/1.19.2) (2022-07-20)
------------------------------------------------------------------------------------------------------------------

## Changes

- Finch: new release for new Xclim

  Finch release notes:

  0.9.2 (2022-07-19)
  ------------------
  * Fix Finch unable to startup in the Docker image.

  0.9.1 (2022-07-07)
  ------------------
  * Avoid using a broken version of ``libarchive`` in the Docker image.

  0.9.0 (2022-07-06)
  ------------------
  * Fix use of ``output_name``, add ``output_format`` to xclim indicators.
  * Change all outputs to use ``output`` as the main output field name (instead of ``output_netcdf``).
  * Updated to xclim 0.37:

      - Percentile inputs of xclim indicators have been renamed with generic names, excluding an explicit mention to the target percentile.
      - In ensemble processes, these percentiles can now be chosen through ``perc_[var]`` inputs. The default values are inherited from earlier versions of xclim.
  * Average shape process downgraded to be single-threaded, as ESMF seems to have issues with multithreading.
  * Removed deprecated processes ``subset_ensemble_bbox_BCCAQv2``, ``subset_ensemble_BCCAQv2`` and ``BCCAQv2_heat_wave_frequency_gridpoint``.
  * Added ``csv_precision`` to all processes allowing CSV output. When given, it controls the number of decimal places in the output.


[1.19.1](https://github.com/bird-house/birdhouse-deploy/tree/1.19.1) (2022-07-19)
------------------------------------------------------------------------------------------------------------------

## Changes

- Various changes to get the new production host up and running

    **Non-breaking changes**
    - Bootstrap testsuite: only crawl the subset enough to pass canarie-api monitoring: faster when system under test has too much other stuff.
    - New script: `check-autodeploy-repos`: to ensure autodeploy will trigger normally.
    - New script: `sync-data`: to pull data from existing production host to a new production host or to a staging host to emulate the production host.
    - thredds, geoserver, generic_bird: set more appropriate production values, taken from https://github.com/Ouranosinc/birdhouse-deploy/commit/316439e310e915e0a4ef35d25744cab76722fa99
    - monitoring: fix redundant `network_mode: host` and `ports` binding since host network_mode will already automatically perform port bindings

    **Breaking changes**
    - None

## Related Issue / Discussion

- https://github.com/bird-house/birdhouse-deploy-ouranos/pull/16
- https://github.com/Ouranosinc/pavics-vdb/pull/48
- https://github.com/Ouranosinc/ouranos-ansible/pull/2


[1.19.0](https://github.com/bird-house/birdhouse-deploy/tree/1.19.0) (2022-06-08)
------------------------------------------------------------------------------------------------------------------

## Changes:

- Magpie/Twitcher: update `magpie` service
  from [3.21.0](https://github.com/Ouranosinc/Magpie/tree/3.21.0)
  to [3.26.0](https://github.com/Ouranosinc/Magpie/tree/3.26.0) and
  bundled `twitcher` from [0.6.2](https://github.com/bird-house/twitcher/tree/v0.6.2)
  to [0.7.0](https://github.com/bird-house/twitcher/tree/v0.7.0).
  
  - Adds [Service Hooks](https://pavics-magpie.readthedocs.io/en/latest/configuration.html#service-hooks) allowing 
    Twitcher to apply HTTP pre-request/post-response modifications to requested services and resources in accordance
    to `MagpieAdapter` implementation and using plugin Python scripts when matched against specific request parameters.

  - Using *Service Hooks*, inject ``X-WPS-Output-Context`` header in Weaver job submission requests through the proxied
    request by Twitcher and `MagpieAdapter`. This header contains the user ID that indicates to Weaver were to store 
    job output results, allowing to save them in the corresponding user's workspace directory under `wpsoutputs` path.
    More details found in PR https://github.com/bird-house/birdhouse-deploy/pull/244.

  - Using *Service Hooks*, filter processes returned by Weaver in JSON response from ``/processes`` endpoint using
    respective permissions applied onto each ``/processes/{processID}`` for the requesting user. Users will only be able
    to see processes for which they have read access to retrieve the process description.
    More details found in PR https://github.com/bird-house/birdhouse-deploy/pull/245.

  - Using *Service Hooks*, automatically apply permissions for the user that successfully deployed a Weaver process 
    using ``POST /processes`` request, granting it direct access to this process during process listing, process 
    description request and for submitting job execution of this process.
    Only this user deploying the process will have access to it until further permissions are added in Magpie to share
    or publish it with other users, groups and/or publicly. The user must have the necessary permission to deploy a new
    process in the first place. More details found in PR https://github.com/bird-house/birdhouse-deploy/pull/247.

[1.18.13](https://github.com/bird-house/birdhouse-deploy/tree/1.18.13) (2022-06-07)
------------------------------------------------------------------------------------------------------------------

## Changes:

- deploy-data: new env var DEPLOY_DATA_RSYNC_USER_GRP to avoid running cronjobs as root

  When `deploy-data` is used by the `scheduler` component, it is run as
  `root`.  This new env var will force the rsync process to run as a regular user to
  follow security best practice to avoid running as root when not needed.

  Note that the `git checkout` step done by `deploy-data` is still run as root.
  This is because `deploy-data` is currently still run as root so it can
  execute `docker` commands (ex: spawning the `rsync` command above in its own
  docker container).

  To fix this limitation, the regular user inside the `deploy-data` container
  need to have docker access inside the container and outside on the host at
  the same time.  If we make that regular user configurable so the script
  `deploy-data` is generic and can work for any organisations, this is tricky
  for the moment so will have to be handle in another PR.

  So for the moment we have not achieved full non-root user in cronjobs
  launched by the `scheduler` compoment but the most important part, the part
  that perform the actual job (rsync or execute custom command using an
  external docker container) is running as non-root.

  See PR https://github.com/bird-house/birdhouse-deploy-ouranos/pull/18 that
  make use of this new env var.

  When `deploy-data` is invoking an external script that itself spawn a new
  `docker run`, then it is up to this external script to ensure the proper
  non-root user is used by `docker run`.
  See PR https://github.com/Ouranosinc/pavics-vdb/pull/50 that handle that
  case.


[1.18.12](https://github.com/bird-house/birdhouse-deploy/tree/1.18.12) (2022-05-05)
------------------------------------------------------------------------------------------------------------------

## Changes:

- Jupyter env: new build for new XClim and to get Dask dashboard and Panel server app to work

  Deploy new Jupyter env from PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/105 on PAVICS.

  Detailed changes can be found at https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/105.

  Dask dashboard no manual URL mangling required:

  ![Screenshot from 2022-04-13 22-37-49](https://user-images.githubusercontent.com/11966697/163303916-f781ac23-d10a-4cd6-807c-b10c8703afc3.png)

  "Render with Panel" button works:
  ![Screenshot from 2022-05-04 15-18-03](https://user-images.githubusercontent.com/11966697/166810160-f6989da4-6e8f-4407-8fd5-4ef71770e1f2.png)


  Relevant changes:

  ```diff
  # new
  >   - dask-labextension=5.2.0=pyhd8ed1ab_0
  >   - jupyter-panel-proxy=0.2.0a2=py_0
  >   - jupyter-server-proxy=3.2.1=pyhd8ed1ab_0
  
  # removed, interfere with panel
  <     - handcalcs==1.4.1
  
  <   - xclim=0.34.0=pyhd8ed1ab_0
  >   - xclim=0.36.0=pyhd8ed1ab_0
  
  <   - cf_xarray=0.6.3=pyhd8ed1ab_0
  >   - cf_xarray=0.7.2=pyhd8ed1ab_0
  
  <   - clisops=0.8.0=pyh6c4a22f_0
  >   - clisops=0.9.0=pyh6c4a22f_0
  
  # downgrade by clisops
  <   - pandas=1.4.1=py38h43a58ef_0
  >   - pandas=1.3.5=py38h43a58ef_0
  
  <   - rioxarray=0.10.3=pyhd8ed1ab_0
  >   - rioxarray=0.11.1=pyhd8ed1ab_0
  
  <   - nc-time-axis=1.4.0=pyhd8ed1ab_0
  >   - nc-time-axis=1.4.1=pyhd8ed1ab_0
  
  <   - roocs-utils=0.5.0=pyh6c4a22f_0
  >   - roocs-utils=0.6.1=pyh6c4a22f_0
  
  <   - panel=0.12.7=pyhd8ed1ab_0
  >   - panel=0.13.1a2=py_0
  
  <   - plotly=5.6.0=pyhd8ed1ab_0
  >   - plotly=5.7.0=pyhd8ed1ab_0
  ```


[1.18.11](https://github.com/bird-house/birdhouse-deploy/tree/1.18.11) (2022-04-21)
------------------------------------------------------------------------------------------------------------------

## Changes:

- Finch: new release for dask performance problem

  PR to deploy new Finch releases in https://github.com/bird-house/finch/pull/233 on PAVICS.

  See the Finch PR for more info.

  Finch release notes:

  0.8.3 (2022-04-21)
  ------------------
  * Preserve RCP dimension in ensemble processes, even when only RCP is selected.
  * Pin ``dask`` and ``distributed`` at ``2022.1.0``, see https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/issues/100


[1.18.10](https://github.com/bird-house/birdhouse-deploy/tree/1.18.10) (2022-04-07)
------------------------------------------------------------------------------------------------------------------

## Changes:

- Jupyter env: new xlrd, pre-commit, pin dask, distributed, cf_xarray, latest of everything else

  Deploy new Jupyter env from PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/101 on PAVICS.

  Detailed changes can be found at https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/101.

  Relevant changes:
  ```diff
  >   - pre-commit=2.17.0=py38h578d9bd_0
  >   - xlrd=2.0.1=pyhd8ed1ab_3
  
  <   - xclim=0.32.1=pyhd8ed1ab_0
  >   - xclim=0.34.0=pyhd8ed1ab_0
  
  <   - cfgrib=0.9.9.1=pyhd8ed1ab_1
  >   - cfgrib=0.9.10.1=pyhd8ed1ab_0
  
  <   - cftime=1.5.1.1=py38h6c62de6_1
  >   - cftime=1.6.0=py38h3ec907f_0
  
  <   - intake-xarray=0.5.0=pyhd8ed1ab_0
  >   - intake-xarray=0.6.0=pyhd8ed1ab_0
  
  <   - pandas=1.3.5=py38h43a58ef_0
  >   - pandas=1.4.1=py38h43a58ef_0
  
  <   - regionmask=0.8.0=pyhd8ed1ab_1
  >   - regionmask=0.9.0=pyhd8ed1ab_0
  
  <   - rioxarray=0.9.1=pyhd8ed1ab_0
  >   - rioxarray=0.10.3=pyhd8ed1ab_0
  
  <   - xarray=0.20.2=pyhd8ed1ab_0
  >   - xarray=2022.3.0=pyhd8ed1ab_0
  
  <   - zarr=2.10.3=pyhd8ed1ab_0
  >   - zarr=2.11.1=pyhd8ed1ab_0
  ```


[1.18.9](https://github.com/bird-house/birdhouse-deploy/tree/1.18.9) (2022-03-16)
------------------------------------------------------------------------------------------------------------------

## Changes:

- Finch: update `finch` component 
  from [0.7.7](https://github.com/bird-house/finch/releases/tag/v0.7.7)
  to [0.8.2](https://github.com/bird-house/finch/releases/tag/v0.8.2)

  Relevant Changes:
  - v0.8.0
    - Add hourly_to_daily process
    - Avoid annoying warnings by updating birdy (environment-docs)
    - Upgrade to clisops 0.8.0 to accelerate spatial averages over regions. 
    - Upgrade to xesmf 0.6.2 to fix spatial averaging bug not weighing correctly cells with varying areas. 
    - Update to PyWPS 4.5.1 to allow the creation of recursive directories for outputs.
  - v0.8.2
    - Add ``geoseries_to_netcdf`` process, converting a geojson (like a OGC-API request) to a CF-compliant netCDF. 
    - Add ``output_name`` argument to most processes (excepted subsetting and averaging processes), to control 
      the name (or prefix) of the output file. 
    - New dependency ``python-slugify`` to ensure filenames are safe and valid. 
    - Pinning dask to ``<=2022.1.0`` to avoid a performance issue with ``2022.1.1``.

[1.18.8](https://github.com/bird-house/birdhouse-deploy/tree/1.18.8) (2022-03-09)
------------------------------------------------------------------------------------------------------------------

## Changes:

- Weaver: fix tests
  
  Relevant changes:
  - Increase default timeout (`60s -> 120s`) for
    [components/weaver/post-docker-compose-up](./birdhouse/components/weaver/post-docker-compose-up) script to allow it
    to complete with many WPS bird taking a long time to boot. Before this fix, test instances only managed to register 
    `catalog`, `finch`, and `flyingpigeon` providers, but timed out for `hummingbird` and following WPS birds.

    This resolves the first few cell tests by having birds ready for use:

    ```text
    [2022-03-09T02:13:34.966Z] pavics-sdi-master/docs/source/notebook-components/weaver_example.ipynb . [ 57%]
    [2022-03-09T02:13:46.069Z] .......FF.                                                               [ 61%]
    ```

  - Add override ``request_options.yml`` in
    [birdhouse/optional-components/test-weaver](./birdhouse/optional-components/test-weaver)
    that disables SSL verification specifically for the remaining 2 `F` cell above. Error is related to the job 
    execution itself on the test instance, which fails when Weaver sends requests to `hummingbird`'s `ncdump` process. 
    An SSL verification error happens, because the test instance uses a self-signed SSL certificate.

[1.18.7](https://github.com/bird-house/birdhouse-deploy/tree/1.18.7) (2022-03-08)
------------------------------------------------------------------------------------------------------------------

## Changes:
- Weaver: update `weaver` component
  from [4.5.0](https://github.com/crim-ca/weaver/tree/4.5.0)
  to [4.12.0](https://github.com/crim-ca/weaver/tree/4.12.0).

  Relevant changes:
  - Adds `WeaverClient` and *Weaver CLI*. Although not strictly employed by the platform itself to offer *Weaver* as a
    service, these can be employed to interact with *Weaver* using Python or shell commands, providing access to all
    WPS *birds* offered by the platform using the common [OGC API - Processes][ogcapi-proc] interface through
    [Weaver Providers](https://pavics-weaver.readthedocs.io/en/latest/processes.html#remote-provider).
  - Adds [Vault](https://pavics-weaver.readthedocs.io/en/latest/processes.html#vault) functionality allowing temporary
    and secure storage to upload files for single-use process execution.
  - Various bugfixes and conformance resolution related to [OGC API - Processes][ogcapi-proc].
  - Fix `weaver-mongodb` link references for `weaver-worker`. New default variables `WEAVER_MONGODB_[HOST|PORT|URL]`
    are defined to construct different INI configuration formats employed by `weaver` and `weaver-worker` images.
  - Fix missing `EXTRA_VARS` variables in [Weaver's default.env](./birdhouse/components/weaver/default.env).
  - Fix [celery-healthcheck](./birdhouse/components/weaver/celery-healthcheck) of `weaver-worker` to consider
    multiple tasks.

[ogcapi-proc]: https://github.com/opengeospatial/ogcapi-processes

[1.18.6](https://github.com/bird-house/birdhouse-deploy/tree/1.18.6) (2022-03-08)
------------------------------------------------------------------------------------------------------------------

- Magpie: update `magpie` service
  from [3.19.1](https://github.com/Ouranosinc/Magpie/tree/3.19.1)
  to [3.21.0](https://github.com/Ouranosinc/Magpie/tree/3.21.0).

  Relevant changes:
  - Update *WFS*, *WMS* and *WPS* related services to properly implement the relevant *Permissions* and *Resources*
    according to their specific implementation details. For example, *GeoServer*-based *WMS* implementation supports
    *Workspaces* and additional operations that are not offered by standard *OGC*-based *WMS*. Some of these
    implementation specific operations can be taken advantage of with improved *Permissions* and *Resources* resolution.
  - Add multi-*Resource* effective access resolution for *Services* that support it.
    For example, accessing multiple *Layers* under a permission-restricted *WFS* with parameters that allow multiple
    values within a single request is now possible, if the user is granted to all specified *Resources*.
    Previously, users would require to access each *Layer Resource* individually with distinct requests.
  - Magpie's API and UI are more verbose about supported hierarchical *Resource* structure under a given *Service* type.
    When creating *Resources*, specific structures have to be respected, and only valid cases are proposed in the UI.
  - Minor UI fixes.

[1.18.5](https://github.com/bird-house/birdhouse-deploy/tree/1.18.5) (2022-01-27)
------------------------------------------------------------------------------------------------------------------

## Changes:
- Jupyter: update Jupyter env for latest XClim, RavenPy and all packages

  Deploy new Jupyter env from PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/95 on PAVICS.

  Detailed changes can be found at https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/95.

  Relevant changes:
  ```diff
  <   - xclim=0.31.0=pyhd8ed1ab_0
  >   - xclim=0.32.1=pyhd8ed1ab_0
  
  <   - ravenpy=0.7.5=pyhff6ddc9_0
  >   - ravenpy=0.7.8=pyh8a188c0_0
  
  <   - python=3.7.12=hb7a2778_100_cpython
  >   - python=3.8.12=hb7a2778_2_cpython
  
  # removed
  <   - vcs=8.2.1=pyh9f0ad1d_0
  
  <   - numpy=1.21.4=py37h31617e3_0
  >   - numpy=1.21.5=py38h87f13fb_0
  
  <   - xarray=0.20.1=pyhd8ed1ab_0
  >   - xarray=0.20.2=pyhd8ed1ab_0
  
  <   - rioxarray=0.8.0=pyhd8ed1ab_0
  >   - rioxarray=0.9.1=pyhd8ed1ab_0
  
  <   - cf_xarray=0.6.1=pyh6c4a22f_0
  >   - cf_xarray=0.6.3=pyhd8ed1ab_0
  
  <   - gdal=3.3.2=py37hd5a0ba4_2
  >   - gdal=3.3.3=py38hcf2042a_0
  
  <   - rasterio=1.2.6=py37hc20819c_2
  >   - rasterio=1.2.10=py38hfd64e68_0
  
  <   - climpred=2.1.6=pyhd8ed1ab_1
  >   - climpred=2.2.0=pyhd8ed1ab_0
  
  <   - clisops=0.7.0=pyh6c4a22f_0
  >   - clisops=0.8.0=pyh6c4a22f_0
  
  <   - xesmf=0.6.0=pyhd8ed1ab_0
  >   - xesmf=0.6.2=pyhd8ed1ab_0
  
  <   - birdy=v0.8.0=pyh6c4a22f_1
  >   - birdy=0.8.1=pyh6c4a22f_1
  
  <   - cartopy=0.20.0=py37hbe109c4_0
  >   - cartopy=0.20.1=py38hf9a4893_1
  
  <   - dask=2021.11.2=pyhd8ed1ab_0
  >   - dask=2022.1.0=pyhd8ed1ab_0
  
  <   - numba=0.53.1=py37hb11d6e1_1
  >   - numba=0.55.0=py38h4bf6c61_0
  
  <   - pandas=1.3.4=py37he8f5f7f_1
  >   - pandas=1.3.5=py38h43a58ef_0
  ```


[1.18.4](https://github.com/bird-house/birdhouse-deploy/tree/1.18.4) (2022-01-25)
------------------------------------------------------------------------------------------------------------------

## Changes:
- vagrant: support RockyLinux

  RockyLinux 8 is the successor to Centos 7.

  Centos 8 has become like a "RHEL 8 beta" than the equivalent of RHEL 8.

  RockyLinux 8 is the new equivalent of RHEL 8, following the original spirit
  of the Centos project.

  More info at https://rockylinux.org/about.


[1.18.3](https://github.com/bird-house/birdhouse-deploy/tree/1.18.3) (2021-12-17)
------------------------------------------------------------------------------------------------------------------

## Changes:
- Jupyter: new build with latest changes

  See PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/94 for
  more info.

  Change summary:

  ```diff
  <   - xclim=0.28.1=pyhd8ed1ab_0
  >   - xclim=0.31.0=pyhd8ed1ab_0
  
  <   - ravenpy=0.7.4=pyh7f9bfb9_0
  >   - ravenpy=0.7.5=pyhff6ddc9_0
  
  <   - xarray=0.19.0=pyhd8ed1ab_1
  >   - xarray=0.20.1=pyhd8ed1ab_0
  
  <   - rasterio=1.2.1=py37ha549118_0
  >   - rasterio=1.2.6=py37hc20819c_2
  
  <   - bokeh=2.3.3=py37h89c1867_0
  >   - bokeh=2.4.2=py37h89c1867_0
  
  <   - cartopy=0.19.0.post1=py37h0c48da3_1
  >   - cartopy=0.20.0=py37hbe109c4_0
  
  <   - cffi=1.14.6=py37hc58025e_0
  >   - cffi=1.15.0=py37h036bc23_0
  
  <   - climpred=2.1.5.post1=pyhd8ed1ab_0
  >   - climpred=2.1.6=pyhd8ed1ab_1
  
  <   - clisops=0.6.5=pyh6c4a22f_0
  >   - clisops=0.7.0=pyh6c4a22f_0
  
  <   - dask=2021.9.0=pyhd8ed1ab_0
  >   - dask=2021.11.2=pyhd8ed1ab_0
  
  <   - gdal=3.1.4=py37h2ec2946_8
  >   - gdal=3.3.2=py37hd5a0ba4_2
  
  <   - geopandas=0.9.0=pyhd8ed1ab_1
  >   - geopandas=0.10.2=pyhd8ed1ab_0
  
  <   - nc-time-axis=1.3.1=pyhd8ed1ab_2
  >   - nc-time-axis=1.4.0=pyhd8ed1ab_0
  
  <   - pandas=1.2.5=py37h219a48f_0
  >   - pandas=1.3.4=py37he8f5f7f_
  
  <   - poppler=0.89.0=h2de54a5_5
  >   - poppler=21.09.0=ha39eefc_3
  
  <   - rioxarray=0.7.0=pyhd8ed1ab_0
  >   - rioxarray=0.8.0=pyhd8ed1ab_0
  
  <   - roocs-utils=0.4.2=pyh6c4a22f_0
  >   - roocs-utils=0.5.0=pyh6c4a22f_0
  ```

[1.18.2](https://github.com/bird-house/birdhouse-deploy/tree/1.18.2) (2021-12-13)
------------------------------------------------------------------------------------------------------------------

## Fixes
- Thredds: update for Log4j Vulnerability CVE-2021-44228

  Quebec gouvernment has shutdown its website due to this vulnerability so it's pretty serious
  (https://montrealgazette.com/news/quebec/quebec-government-shutting-down-websites-report).

  Thredds release notes: https://github.com/Unidata/thredds/releases
  
  https://www.oracle.com/security-alerts/alert-cve-2021-44228.html
  
  **Oracle Security Alert Advisory - CVE-2021-44228 Description**
  
  This Security Alert addresses CVE-2021-44228, a remote code execution
  vulnerability in Apache Log4j. It is remotely exploitable without
  authentication, i.e., may be exploited over a network without the need for a
  username and password.
  
  Due to the severity of this vulnerability and the publication of exploit code
  on various sites, Oracle strongly recommends that customers apply the updates
  provided by this Security Alert as soon as possible.
  
  **Affected Products and Versions**
  Apache Log4j, versions 2.0-2.14.1
  
  We have 4 Java component but only 1 is vulnerable: Thredds:
  
  **After fix**:
  ```
  $ docker run -it --rm unidata/thredds-docker:4.6.18 bash
  root@f65aadd2955c:/usr/local/tomcat# find -iname '**log4j**'
  ./webapps/thredds/WEB-INF/classes/log4j2.xml
  ./webapps/thredds/WEB-INF/lib/log4j-api-2.15.0.jar
  ./webapps/thredds/WEB-INF/lib/log4j-core-2.15.0.jar
  ./webapps/thredds/WEB-INF/lib/log4j-slf4j-impl-2.15.0.jar
  ./webapps/thredds/WEB-INF/lib/log4j-web-2.15.0.jar
  ```
  
  **Before fix (unidata/thredds-docker:4.6.15)**:
  ```
  $ docker exec -it thredds find / -iname '**log4j**'
  find: ‘/proc/1/map_files’: Operation not permitted
  find: ‘/proc/12/map_files’: Operation not permitted
  find: ‘/proc/20543/map_files’: Operation not permitted
  /usr/local/tomcat/webapps/twitcher#ows#proxy#thredds/WEB-INF/classes/log4j2.xml
  /usr/local/tomcat/webapps/twitcher#ows#proxy#thredds/WEB-INF/lib/log4j-api-2.13.3.jar
  /usr/local/tomcat/webapps/twitcher#ows#proxy#thredds/WEB-INF/lib/log4j-core-2.13.3.jar
  /usr/local/tomcat/webapps/twitcher#ows#proxy#thredds/WEB-INF/lib/log4j-slf4j-impl-2.13.3.jar
  /usr/local/tomcat/webapps/twitcher#ows#proxy#thredds/WEB-INF/lib/log4j-web-2.13.3.jar
  ```
  
  **Other components (ncwms2, geoserver, solr) have log4j older than version 2.0
  so supposedly not affected**:
  
  ```
  $ docker exec -it ncwms2 find / -iname '**log4j**'
  /opt/conda/envs/birdhouse/opt/apache-tomcat/webapps/ncWMS2/WEB-INF/classes/log4j.properties
  /opt/conda/envs/birdhouse/opt/apache-tomcat/webapps/ncWMS2/WEB-INF/lib/log4j-1.2.17.jar
  /opt/conda/envs/birdhouse/opt/apache-tomcat/webapps/ncWMS2/WEB-INF/lib/slf4j-log4j12-1.7.2.jar
  
  $ docker exec -it geoserver find / -iname '**log4j**'
  /build_data/log4j.properties
  find: ‘/etc/ssl/private’: Permission denied
  find: ‘/proc/tty/driver’: Permission denied
  find: ‘/proc/1/map_files’: Operation not permitted
  find: ‘/proc/15/task/47547’: No such file or directory
  find: ‘/proc/15/map_files’: Operation not permitted
  find: ‘/proc/47492/map_files’: Operation not permitted
  find: ‘/root’: Permission denied
  /usr/local/tomcat/log4j.properties
  /usr/local/tomcat/webapps/geoserver/WEB-INF/lib/log4j-1.2.17.jar
  /usr/local/tomcat/webapps/geoserver/WEB-INF/lib/metrics-log4j-3.0.2.jar
  /usr/local/tomcat/webapps/geoserver/WEB-INF/lib/slf4j-log4j12-1.6.4.jar
  find: ‘/var/cache/apt/archives/partial’: Permission denied
  find: ‘/var/cache/ldconfig’: Permission denied
  
  $ docker exec -it solr find / -iname '**log4j**'
  /data/solr/log4j.properties
  /opt/birdhouse/eggs/birdhousebuilder.recipe.solr-0.1.5-py2.7.egg/birdhousebuilder/recipe/solr/templates/log4j.properties
  /opt/conda/envs/birdhouse/opt/solr/docs/solr-core/org/apache/solr/logging/log4j
  /opt/conda/envs/birdhouse/opt/solr/docs/solr-core/org/apache/solr/logging/log4j/Log4jInfo.html
  /opt/conda/envs/birdhouse/opt/solr/docs/solr-core/org/apache/solr/logging/log4j/Log4jWatcher.html
  /opt/conda/envs/birdhouse/opt/solr/docs/solr-core/org/apache/solr/logging/log4j/class-use/Log4jInfo.html
  /opt/conda/envs/birdhouse/opt/solr/docs/solr-core/org/apache/solr/logging/log4j/class-use/Log4jWatcher.html
  /opt/conda/envs/birdhouse/opt/solr/example/resources/log4j.properties
  /opt/conda/envs/birdhouse/opt/solr/licenses/log4j-1.2.17.jar.sha1
  /opt/conda/envs/birdhouse/opt/solr/licenses/log4j-LICENSE-ASL.txt
  /opt/conda/envs/birdhouse/opt/solr/licenses/log4j-NOTICE.txt
  /opt/conda/envs/birdhouse/opt/solr/licenses/slf4j-log4j12-1.7.7.jar.sha1
  /opt/conda/envs/birdhouse/opt/solr/server/lib/ext/log4j-1.2.17.jar
  /opt/conda/envs/birdhouse/opt/solr/server/lib/ext/slf4j-log4j12-1.7.7.jar
  /opt/conda/envs/birdhouse/opt/solr/server/resources/log4j.properties
  /opt/conda/envs/birdhouse/opt/solr/server/scripts/cloud-scripts/log4j.properties
  /opt/conda/pkgs/solr-5.2.1-1/opt/solr/docs/solr-core/org/apache/solr/logging/log4j
  /opt/conda/pkgs/solr-5.2.1-1/opt/solr/docs/solr-core/org/apache/solr/logging/log4j/Log4jInfo.html
  /opt/conda/pkgs/solr-5.2.1-1/opt/solr/docs/solr-core/org/apache/solr/logging/log4j/Log4jWatcher.html
  /opt/conda/pkgs/solr-5.2.1-1/opt/solr/docs/solr-core/org/apache/solr/logging/log4j/class-use/Log4jInfo.html
  /opt/conda/pkgs/solr-5.2.1-1/opt/solr/docs/solr-core/org/apache/solr/logging/log4j/class-use/Log4jWatcher.html
  /opt/conda/pkgs/solr-5.2.1-1/opt/solr/example/resources/log4j.properties
  /opt/conda/pkgs/solr-5.2.1-1/opt/solr/licenses/log4j-1.2.17.jar.sha1
  /opt/conda/pkgs/solr-5.2.1-1/opt/solr/licenses/log4j-LICENSE-ASL.txt
  /opt/conda/pkgs/solr-5.2.1-1/opt/solr/licenses/log4j-NOTICE.txt
  /opt/conda/pkgs/solr-5.2.1-1/opt/solr/licenses/slf4j-log4j12-1.7.7.jar.sha1
  /opt/conda/pkgs/solr-5.2.1-1/opt/solr/server/lib/ext/log4j-1.2.17.jar
  /opt/conda/pkgs/solr-5.2.1-1/opt/solr/server/lib/ext/slf4j-log4j12-1.7.7.jar
  /opt/conda/pkgs/solr-5.2.1-1/opt/solr/server/resources/log4j.properties
  /opt/conda/pkgs/solr-5.2.1-1/opt/solr/server/scripts/cloud-scripts/log4j.properties
  ```

[1.18.1](https://github.com/bird-house/birdhouse-deploy/tree/1.18.1) (2021-12-08)
------------------------------------------------------------------------------------------------------------------

## Fixes
- Update `Mapgie` version [3.19.0](https://github.com/Ouranosinc/Magpie/blob/master/CHANGES.rst#3190-2021-12-02)  
  to [3.19.1](https://github.com/Ouranosinc/Magpie/blob/master/CHANGES.rst#3191-2021-12-08) with fix of unhandled
  request concurrent cleanup with adapter caching, as observed in [bird-house/birdhouse-deploy#224 (comment)](
  https://github.com/bird-house/birdhouse-deploy/pull/224#issuecomment-985668339).

[1.18.0](https://github.com/bird-house/birdhouse-deploy/tree/1.18.0) (2021-12-08)
------------------------------------------------------------------------------------------------------------------

## Changes
- Upgrade default `Weaver` version to [4.5.0](https://github.com/crim-ca/weaver/blob/master/CHANGES.rst#450-2021-11-25) 
  (from [4.2.1](https://github.com/crim-ca/weaver/blob/master/CHANGES.rst#421-2021-10-20)) for new features and fixes.
  Most notable changes are: 
  - Adds support of `X-WPS-Output-Context` header to define the WPS output nested directory (for user context).
  - Adds support of `X-Auth-Docker` header to define a private Docker registry authentication token when the 
    referenced Docker image in the deployed Application Package requires it to fetch it for Process execution. 
  - Require `MongoDB==5.0` Docker image for Weaver's database.
  - Fixes related to handling `dismiss` operation of job executions and retrieval of their results.
  - Fixes related to fetching remote files and propagation of intermediate results between Workflow steps.

## Important
Because of the new `MongoDB==5.0` database requirement for Weaver that uses (potentially) distinct version from other 
birds (notably `phoenix` with `MongoDB==3.4`), a separate Docker image is employed only for Weaver. If some processes, 
jobs, or other Weaver-related data was already defined on one of your server instances, manual transfer between the 
generic `${DATA_PERSIST_ROOT}/mongodb_persist` to new  `${DATA_PERSIST_ROOT}/mongodb_weaver_persist` directory must 
be accomplished. The data in the new directory should then be migrated to the new version following the procedure 
described in [Database Migration](https://pavics-weaver.readthedocs.io/en/latest/installation.html?#database-migration).

## Legal Notice
While migrating from ``MongoDB==3.4`` to ``MongoDB==5.0``, its license changes from AGPL to SSPL
(reference: [mongodb/mongo@6ea81c8/README#L89-L95](https://github.com/mongodb/mongo/blob/6ea81c88/README#L89-L95)).
This should not impact users using the platform for public and Open Source uses, but should be considered otherwise.

[1.17.6](https://github.com/bird-house/birdhouse-deploy/tree/1.17.6) (2021-12-03)
------------------------------------------------------------------------------------------------------------------

## Changes
- Upgrade Magpie/Twitcher to 3.19.0, and add new related environment variables.
  * Adjust Twitcher runner to employ `gunicorn` instead of `waitress`.
  * Add new environment variables to handle email usage, used for features such as 
    user registration/approval and user assignment to groups with terms and conditions.
  * Add expiration variable for temporary tokens.

[1.17.5](https://github.com/bird-house/birdhouse-deploy/tree/1.17.5) (2021-11-16)
------------------------------------------------------------------------------------------------------------------

## Changes
- Upgrade Finch to 0.7.7
  [Release notes for 0.7.7](https://github.com/bird-house/finch/releases/tag/v0.7.7)
- [Release notes for 0.7.6](https://github.com/bird-house/finch/releases/tag/v0.7.6)
  
[1.17.4](https://github.com/bird-house/birdhouse-deploy/tree/1.17.4) (2021-11-03)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Add missing ``config/canarie-api/weaver_config.py`` entry to ``.gitignore`` of ``./components/weaver``
  that is generated from the corresponding template file.

  If upgrading from previous `1.17.x` version, autodeploy will not resume automatically even with this fix because of 
  the *dirty* state of the repository. A manual `git pull` will be required to fix subsequent autodeploy triggers.

[1.17.3](https://github.com/bird-house/birdhouse-deploy/tree/1.17.3) (2021-11-03)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Minor fix to `install-docker.sh` and comment update for other scripts due to Magpie upgrade

  `install-docker.sh`: fix to work with users with sudo privilege.  Before it needed user `root`.

  Other comments in scripts are due to new Magpie in PR https://github.com/bird-house/birdhouse-deploy/pull/107.


[1.17.2](https://github.com/bird-house/birdhouse-deploy/tree/1.17.2) (2021-11-03)
------------------------------------------------------------------------------------------------------------------

## Changes

- scripts: add `extract-jupyter-users-from-magpie-db`

  Extract Jupyter users from Magpie DB so we can send announcements to all Jupyter users.

  Sample output:

  ```
  $ ./scripts/extract-jupyter-users-from-magpie-db  > /tmp/out
  + echo SELECT email,user_name FROM users ORDER BY email
  + docker exec -i postgres-magpie psql -U postgres-magpie magpiedb

  $ cat /tmp/out
           email          |   user_name
  ------------------------+---------------
   admin-catalog@mail.com | admin-catalog
   admin@mail.com         | admin
   anonymous@mail.com     | anonymous
   authtest@example.com   | authtest
  (4 rows)
  ```


[1.17.1](https://github.com/bird-house/birdhouse-deploy/tree/1.17.1) (2021-11-02)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Apply ``mongodb`` network to ``mongodb`` image in order to allow ``phoenix`` to properly reference it.
- Remove ``mongodb`` definition from ``./components/weaver`` since the extended ``mongodb`` network is already provided.

[1.17.0](https://github.com/bird-house/birdhouse-deploy/tree/1.17.0) (2021-11-01)
------------------------------------------------------------------------------------------------------------------

## Changes

- Adds [Weaver](https://github.com/crim-ca/weaver) to the stack (optional) when ``./components/weaver`` 
  is added to ``EXTRA_CONF_DIRS``. For more details, refer to 
  [Weaver Component](https://github.com/bird-house/birdhouse-deploy/blob/master/birdhouse/components/README.rst#Weaver)
  Following happens when enabled:
    
  * Service ``weaver`` (API) gets added with endpoints ``/twitcher/ows/proxy/weaver`` and ``/weaver``.
      
  * All *birds* offering a WPS 1.x/2.x endpoint are automatically added as providers known by `Weaver`
    (birds: ``catalog``, ``finch``, ``flyingpigeon``, ``hummingbird``, ``malleefowl`` and ``raven``).
    This offers an automatic mapping of WPS 1.x/2.x requests of process descriptions and execution nested under
    the *birds* to corresponding [OGC-API - Processes](https://github.com/opengeospatial/ogcapi-processes/) 
    RESTful interface (and added functionalities). 
    
  * New processes can be deployed and executed using 
    Dockerized [Application Packages](https://pavics-weaver.readthedocs.io/en/latest/package.html).
    Additionally, all existing processes (across *bird* providers and Dockerized Application Packages) 
    can be chained into [Workflows](https://pavics-weaver.readthedocs.io/en/latest/processes.html#workflow)
      
  * Images ``weaver-worker`` (`Weaver`'s job executor) and ``docker-proxy`` (sibling Docker container dispatcher)
    are added to the stack to support above functionalities.
      
  * Adds `Magpie` permissions and service for `Weaver` endpoints.
  
  * Adds ``./optional-components/test-weaver`` for even more `Magpie` extended permissions for `Weaver` 
    for getting access to resources for functionalities required by [Weaver Testing notebook][weaver-test-notebook].

[weaver-test-notebook]: https://github.com/Ouranosinc/pavics-sdi/blob/master/docs/source/notebook-components/weaver_example.ipynb


[1.16.2](https://github.com/bird-house/birdhouse-deploy/tree/1.16.2) (2021-10-27)
------------------------------------------------------------------------------------------------------------------

## Changes

- geoserver: enable geopkg plugin

  https://docs.geoserver.org/latest/en/user/community/geopkg/

  ==========

  This plugin brings in the ability to write GeoPackage files in GeoServer.
  Reading GeoPackage files is part of the core functionality of GeoServer, and
  does not require this extension.

  GeoPackage is an SQLite based standard format that is able to hold multiple
  vector and raster data layers in a single file.

  GeoPackage can be used as an output format for WFS GetFeature (creating one
  vector data layer) as well as WMS GetMap (creating one raster data layer). The
  GeoServer GeoPackage extension also allows to create a completely custom made
  GeoPackage with multiple layers, using the GeoPackage process.

  ==========

  Concretely this plugin adds a new GeoPackage download format, see screenshot below:
  ![Screenshot from 2021-10-27 17-09-05](https://user-images.githubusercontent.com/11966697/139147774-ffd320e4-0d70-4246-a532-f66e065fcd4c.png)


[1.16.1](https://github.com/bird-house/birdhouse-deploy/tree/1.16.1) (2021-10-25)
------------------------------------------------------------------------------------------------------------------

## Changes

- Thredds: Enable Netcdf Subset Service (NCSS)

  "The Netcdf Subset Service (NCSS) is one of the ways that the TDS can serve data. It is an experimental REST protocol for returning subsets of CDM datasets." https://www.unidata.ucar.edu/software/tds/current/reference/NetcdfSubsetServiceConfigure.html
  
  More NCSS docs: https://www.unidata.ucar.edu/software/tds/current/reference/NetcdfSubsetServiceReference.html

  Briefly, the advantage to enable NCSS is to be able to perform subsetting directly in the browser (manipulating URL parameters), avoiding the overhead for using OpenDAP (needs another client than the existing browser).  This even works for `.ncml` files.

  Recall previously using "HTTPServer" link type, we were able to download directly the `.nc` files but for `.ncml` we got the xml content instead. With this new "NetcdfSubset" link type, we can actually download the NetCDF content of a `.ncml` file directly from the browser.
  
  Sample screenshots:
  
  ![Screenshot 2021-10-21 at 21-32-14 Catalog Services](https://user-images.githubusercontent.com/11966697/138379386-c658cf05-09a2-44dd-ae6e-9337800212d0.png)
  
  ![Screenshot 2021-10-21 at 21-31-13 NetCDF Subset Service for Grids](https://user-images.githubusercontent.com/11966697/138379396-de6cdedf-6bc7-44b8-9da8-42d496abbdf2.png)
  
  dataset.xml:
  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <gridDataset location="/twitcher/ows/proxy/thredds/ncss/birdhouse/testdata/flyingpigeon/cmip3/tasmin.sresa2.miub_echo_g.run1.atm.da.nc" path="path">
    <axis name="lat" shape="6" type="double" axisType="Lat">
      <attribute name="units" value="degrees_north"/>
      <attribute name="long_name" value="latitude"/>
      <attribute name="standard_name" value="latitude"/>
      <attribute name="bounds" value="lat_bnds"/>
      <attribute name="axis" value="Y"/>
      <attribute name="_ChunkSizes" type="int" value="6"/>
      <attribute name="_CoordinateAxisType" value="Lat"/>
      <values>42.67760468 46.38855743 50.09945297 53.81027222 57.52099228 61.2315712</values>
    </axis>
    <axis name="lon" shape="7" type="double" axisType="Lon">
      <attribute name="units" value="degrees_east"/>
      <attribute name="long_name" value="longitude"/>
      <attribute name="standard_name" value="longitude"/>
      <attribute name="bounds" value="lon_bnds"/>
      <attribute name="axis" value="X"/>
      <attribute name="_ChunkSizes" type="int" value="7"/>
      <attribute name="_CoordinateAxisType" value="Lon"/>
      <values start="281.25" increment="3.75" npts="7"/>
    </axis>
    <axis name="time" shape="7200" type="double" axisType="Time">
      <attribute name="units" value="days since 1860-1-1"/>
      <attribute name="calendar" value="360_day"/>
      <attribute name="bounds" value="time_bnds"/>
      <attribute name="_ChunkSizes" type="int" value="7200"/>
      <attribute name="_CoordinateAxisType" value="Time"/>
      <values start="66960.5" increment="1.0" npts="7200"/>
    </axis>
    <gridSet name="time lat lon">
      <projectionBox>
        <minx>279.375</minx>
        <maxx>305.625</maxx>
        <miny>40.82210731506348</miny>
        <maxy>63.08675956726074</maxy>
      </projectionBox>
      <axisRef name="time"/>
      <axisRef name="lat"/>
      <axisRef name="lon"/>
      <grid name="tasmin" desc="Minimum Daily Surface Air Temperature" shape="time lat lon" type="float">
        <attribute name="original_name" value="T2MIN"/>
        <attribute name="coordinates" value="height"/>
        <attribute name="long_name" value="Minimum Daily Surface Air Temperature"/>
        <attribute name="standard_name" value="air_temperature"/>
        <attribute name="cell_methods" value="time: minimum (interval: 30 minutes)"/>
        <attribute name="units" value="K"/>
        <attribute name="missing_value" type="float" value="1.0E20"/>
        <attribute name="history" value="tas=max(195,tas) applied to raw data; min of 194.73 detected;"/>
        <attribute name="_ChunkSizes" type="int" value="7200 6 7"/>
      </grid>
    </gridSet>
    <LatLonBox>
      <west>-78.7500</west>
      <east>-56.2500</east>
      <south>42.6776</south>
      <north>61.2315</north>
    </LatLonBox>
    <TimeSpan>
      <begin>2046-01-01T12:00:00Z</begin>
      <end>2065-12-30T12:00:00Z</end>
    </TimeSpan>
    <AcceptList>
      <GridAsPoint>
        <accept displayName="xml">xml</accept>
        <accept displayName="xml (file)">xml_file</accept>
        <accept displayName="csv">csv</accept>
        <accept displayName="csv (file)">csv_file</accept>
        <accept displayName="geocsv">geocsv</accept>
        <accept displayName="geocsv (file)">geocsv_file</accept>
        <accept displayName="netcdf">netcdf</accept>
        <accept displayName="netcdf4">netcdf4</accept>
      </GridAsPoint>
      <Grid>
        <accept displayName="netcdf">netcdf</accept>
        <accept displayName="netcdf4">netcdf4</accept>
      </Grid>
    </AcceptList>
  </gridDataset>
  ```


[1.16.0](https://github.com/bird-house/birdhouse-deploy/tree/1.16.0) (2021-10-20)
------------------------------------------------------------------------------------------------------------------

## Changes

- Upgrade geoserver to latest upstream kartoza/geoserver:2.19.0

  Completely removed our geoserver custom Docker build.  Upgrade will be much easier next time.  Fixes https://github.com/Ouranosinc/pavics-sdi/issues/197

  **Backward-incompatible** change:
  * new mandatory var `GEOSERVER_ADMIN_PASSWORD` needed in `env.local`
  * manual deployment upgrade procedure required for existing Geoserver datadir (`/data/geoserver/`) to match user inside the Geoserver docker image (`1000:10001`)
  ```
  # destroy geoserver container so we can work on its datadir /data/geoserver/
  ./pavics-compose.sh stop geoserver && ./pavics-compose.sh rm -vf geoserver

  # checkout this new code to have fix-geoserver-data-dir-perm
  git checkout 1.16.0  # tag containing this PR

  # chown -R 1000:10001 /data/geoserver/
  # this can take a while depending how big /data/geoserver/ is and how fast is your disk
  ./deployment/fix-geoserver-data-dir-perm

  # bring up the new geoserver version
  ./pavics-compose.sh up -d
  ```

  What is cool with this new upstream version, from deployment perspective:

  * many plugins are pre-downloaded, we just have to enable them, see https://github.com/kartoza/docker-geoserver/blob/553ed2982685f366ddcbac3d3e1626cb493cf84b/scripts/setup.sh#L13-L41, no need for our custom build to add plugins anymore !!!
    * full plugin list we can enable https://github.com/kartoza/docker-geoserver/blob/553ed2982685f366ddcbac3d3e1626cb493cf84b/build_data/stable_plugins.txt and https://github.com/kartoza/docker-geoserver/blob/553ed2982685f366ddcbac3d3e1626cb493cf84b/build_data/community_plugins.txt

  * admin password can be set via config, no need for manual step post deployment anymore, sweet !!!

  What might be different from the previous version:

  * Jai and Jai_ImageIO might be different from previous version.  The previous version (https://github.com/bird-house/birdhouse-deploy/tree/c0ffb413a3dff70bbe2c98c38690d6e919f11386/birdhouse/docker/geoserver/resources) we added them manually and there is a "native" component.
    * The new GeoServer seems to have switched to "JAI-EXT, a set of replacement operations with bug fixes and NODATA support, for all image processing. In case there is no interest in NODATA support, one can disable JAI-EXT and install the native JAI extensions to improve raster processing performance." excerpt from https://github.com/geoserver/geoserver/blob/770dc6f7023bc2ab32597cfc7a3a9cc35ff3b608/doc/en/user/source/production/java.rst#outdated-install-native-jai-and-imageio-extensions.
    * Also see https://docs.geoserver.org/stable/en/user/configuration/image_processing/index.html.
    * I have no idea what is the actual performance impact of this change.
  * No more manual install of various NetCDF system libraries (zlib, hdf5, archive), see our previous custom build https://github.com/bird-house/birdhouse-deploy/blob/c0ffb413a3dff70bbe2c98c38690d6e919f11386/birdhouse/docker/geoserver/Dockerfile#L26-L35
    * Since we can enable `netcdf-plugin` on the fly so I am guessing those system libraries are not needed anymore but I do not know the actual real impact of this change.

  Blocking issues and PRs:
  * https://github.com/Ouranosinc/pavics-sdi/issues/220
  * https://github.com/Ouranosinc/raven/pull/397
  * https://github.com/CSHS-CWRA/RavenPy/pull/118

  Related issues:
  * https://github.com/kartoza/docker-geoserver/issues/232
  * https://github.com/kartoza/docker-geoserver/issues/233
  * https://github.com/kartoza/docker-geoserver/issues/250


[1.15.2](https://github.com/bird-house/birdhouse-deploy/tree/1.15.2) (2021-09-22)
------------------------------------------------------------------------------------------------------------------

  ## Changes
  
  - Finch: update to version 0.7.5

    Changelog https://github.com/bird-house/finch/blob/master/CHANGES.rst#075-2021-09-07

    ### 0.7.5 (2021-09-07)
    * Update to xclim 0.27
    * Added ``empirical_quantile_mapping`` process calling ``xclim.sdba.EmpiricalQuantileMapping``.
    * Update to PyWPS 4.4.5


[1.15.1](https://github.com/bird-house/birdhouse-deploy/tree/1.15.1) (2021-09-21)
------------------------------------------------------------------------------------------------------------------
  ## Changes
  
  - Finch: Increase ``maxrequestsize`` from 100mb to 400mb to enable ERA5 data subset. Should be possible to bring this back down with smarter averaging processes. 

[1.15.0](https://github.com/bird-house/birdhouse-deploy/tree/1.15.0) (2021-09-20)
------------------------------------------------------------------------------------------------------------------

## Changes

*  **Backward-incompatible change**: do not, by default, volume-mount the Jupyter env README file since that file has been deleted in this repo.  That file is fairly specific to Ouranos while we want this repo to be generic.  PR https://github.com/Ouranosinc/PAVICS-landing/pull/31 restored that file in PAVICS-landing repo that is Ouranos specific.
    * Previous default added as a comment in `env.local` for existing deployment to restore the previous behavior.  Although the README file has been deleted in this PR, it has already been previously deployed so existing system can restore the previous behavior of having the existing README file.  This file will simply be not updated anymore.

* Delete the deployment of that README file as well since that README file is deleted. PR https://github.com/bird-house/birdhouse-deploy-ouranos/pull/15 restore the deployment for Ouranos.

* Each Org will be responsible for the deployment of their own README file.  PR https://github.com/bird-house/birdhouse-deploy-ouranos/pull/15 can be used as a working example from Ouranos.

* Add sample code for simple and naive notebook sharing between Jupyter users.

### Notebook sharing details

Shared notebooks will be visible to all users logged in, even the public demo user so do not share any notebooks containing sensitive private info.

Can not share to a specific user.

Anyone will see the login id of everyone else so if the login id needs to be kept private, change this sample code.

Inside Jupyter, user will have the following additional folders:

```
.
├── mypublic/  # writable by current user
│   ├── current-user-public-share-file.ipynb
│   ├── (...)
├── public/  # read-only for everyone
│   ├── loginid-1-public/
│   │   └── loginid-1-shared-file.ipynb
│   │   └── (...)
│   ├── loginid-2-public/
│   │   └── loginid-2-shared-file.ipynb
│   │   └── (...)
│   ├── (...)-public/
│   │   └── (...)
```

User can drop their files to be shared under folder `mypublic` and see other users share under `public/{other-loginid}-public`.

Matching PR https://github.com/Ouranosinc/PAVICS-landing/pull/31 updating README inside the Jupyter env to explain this new sharing mechanism.

Deployed to https://medus.ouranos.ca/jupyter/ for acceptance testing.


[1.14.4](https://github.com/bird-house/birdhouse-deploy/tree/1.14.4) (2021-09-10)
------------------------------------------------------------------------------------------------------------------

  ## Changes

  - Jupyter: update for new RavenPy and other new packages

    Bokeh png export now also works.

    Other noticeable changes:
    ```diff
    <   - ravenpy=0.7.0=pyh1bb2064_0
    >   - ravenpy=0.7.4=pyh7f9bfb9_0

    <   - xclim=0.28.0=pyhd8ed1ab_0
    >   - xclim=0.28.1=pyhd8ed1ab_0

    >   - geckodriver=0.29.1=h3146498_0
    >   - selenium=3.141.0=py37h5e8e339_1002
    >   - nested_dict=1.61=pyhd3deb0d_0
    >   - paramiko=2.7.2=pyh9f0ad1d_0
    >   - scp=0.14.0=pyhd8ed1ab_0
    >   - s3fs=2021.8.1=pyhd8ed1ab_0

    # Downgrade !
    <   - pandas=1.3.1=py37h219a48f_0
    >   - pandas=1.2.5=py37h219a48f_0

    <   - owslib=0.24.1=pyhd8ed1ab_0
    >   - owslib=0.25.0=pyhd8ed1ab_0

    <   - cf_xarray=0.6.0=pyh6c4a22f_0
    >   - cf_xarray=0.6.1=pyh6c4a22f_0

    <   - rioxarray=0.5.0=pyhd8ed1ab_0
    >   - rioxarray=0.7.0=pyhd8ed1ab_0

    <   - climpred=2.1.4=pyhd8ed1ab_0
    >   - climpred=2.1.5.post1=pyhd8ed1ab_0

    <   - dask=2021.7.1=pyhd8ed1ab_0
    >   - dask=2021.9.0=pyhd8ed1ab_0
    ```

    See PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/89 for more info.
  
[1.14.3](https://github.com/bird-house/birdhouse-deploy/tree/1.14.3) (2021-09-08)
------------------------------------------------------------------------------------------------------------------

  ## Changes

  - Raven: update to version 0.14.2

    Changelog https://github.com/Ouranosinc/raven/blob/master/CHANGES.rst#0142

    0.14.2
    ------
    * Update to RavenPy 0.7.4 (pin climpred below version 2.1.6)
    * Fixed a process-breaking bug in `wps_hydrobasins_shape_selection`

    0.14.1
    ------
    * Update to RavenPy 0.7.3 (pin xclim version 0.28.1)

    0.14
    ----

    * Update to RavenPy 0.7.2
    * Use new OWSlib WFS topological filters
    * More informative install documentation
    * Upgrade to PyWPS 4.4.5

    Jenkins build only known error (`Full_process_example_1.ipynb`):
    http://jenkins.ouranos.ca/job/ouranos-staging/job/lvupavicsmaster.ouranos.ca/59/console


[1.14.2](https://github.com/bird-house/birdhouse-deploy/tree/1.14.2) (2021-09-01)
------------------------------------------------------------------------------------------------------------------

  ## Changes

  - Re-enables the caching feature of `Twitcher` that was disabled temporarily in 
    [#182](https://github.com/bird-house/birdhouse-deploy/pull/182). 
    Handles issue [Ouranosinc/Magpie#433](https://github.com/Ouranosinc/Magpie/issues/433).

[1.14.1](https://github.com/bird-house/birdhouse-deploy/tree/1.14.1) (2021-08-31)
------------------------------------------------------------------------------------------------------------------

- monitoring: make some prometheus alert threshold configurable via env.local

  Default values are previous hardcoded values so this is fully backward compatible.

  Different organizations with different policies and hardware can now
  adapt the alert threshold to their specific needs, decreasing false
  positive alerts.

  Too much false positive alerts will decrease the importance and
  usefulness of each alert. Alerts should not feel like spams.

  Not all alert thresholds are changed to make configurable.  Only thresholds
  that are most likely to need customization or that logically should be
  configurable are made configurable.

  Fixes https://github.com/bird-house/birdhouse-deploy/issues/66.


[1.14.0](https://github.com/bird-house/birdhouse-deploy/tree/1.14.0) (2021-08-02)
------------------------------------------------------------------------------------------------------------------

  ### Changes

  - Add request caching settings in `TWitcher` INI configuration to work with `Magpie` to help reduce permission and
    access control computation time.
    
  - Add `magpie` logger under `Twitcher` INI configuration to provide relevant logging details provided 
    by `MagpieAdapter` it employs for service and resource access resolution.

  - Change logging level of `sqlalchemy.engine` under `Magpie` INI configuration to `WARN` in order to avoid by default
    over verbose database queries.

  - Update `Magpie` version to 3.14.0 with corresponding `Twitcher` using `MagpieAdapter` to obtain fixes about
    request caching and logging improvements during `Twitcher` security check failure following raised exception.
    
    Please note that because the previous default version was 3.12.0, a security fix introduced in 3.13.0 is included.
    (see details here: [3.13.0 (2021-06-29)](https://github.com/Ouranosinc/Magpie/blob/master/CHANGES.rst#3130-2021-06-29))
    
    This security fix explicitly disallows duplicate emails for different user accounts, which might require manual 
    database updates if such users exist on your server instance. To look for possible duplicates, the following command
    can be used. Duplicate entries must be updated or removed such that only unique emails are present.
    
    ```shell
    echo "select email,user_name from users" | \
    docker exec -i postgres-magpie psql -U $POSTGRES_MAGPIE_USERNAME magpiedb | \
    sort > /tmp/magpie_users.txt
    ```

  ### Fixes

  - Adjust incorrect `magpie.url` value in `Magpie` INI configuration.


[1.13.14](https://github.com/bird-house/birdhouse-deploy/tree/1.13.14) (2021-07-29)
------------------------------------------------------------------------------------------------------------------

- jupyter: update for JupyterLab v3, fix memory monitor display and RavenPy-0.7.0

  See PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/85 for more info.

  Relevant changes:
  ```diff
  <   - jupyterlab=2.2.9=pyhd8ed1ab_0
  >   - jupyterlab=3.1.0=pyhd8ed1ab_0

  <   - jupyterlab_server=1.2.0=py_0
  >   - jupyterlab_server=2.6.1=pyhd8ed1ab_0

  <   - jupyter-archive=2.2.0=pyhd8ed1ab_0
  >   - jupyter-archive=3.0.1=pyhd8ed1ab_0

  <   - jupyter_bokeh=2.0.4=pyhd8ed1ab_0
  >   - jupyter_bokeh=3.0.2=pyhd8ed1ab_0

  <   - jupyterlab-git=0.24.0=pyhd8ed1ab_0
  >   - jupyterlab-git=0.31.0=pyhd8ed1ab_0

  <   - nbdime=2.1.0=py_0
  >   - nbdime=3.1.0=pyhd8ed1ab_0

  # Pip to Conda package
  <     - nbresuse==0.4.0
  >   - nbresuse=0.4.0=pyhd8ed1ab_0

  >   - nbclassic=0.3.1=pyhd8ed1ab_1

  >   - jupyterlab-system-monitor=0.8.0=pyhd8ed1ab_1
  >   - jupyter-resource-usage=0.5.1=pyhd8ed1ab_0
  >   - jupyterlab-topbar=0.6.1=pyhd8ed1ab_2
  >     - jupyterlab-logout=0.5.0

  <   - jupyter_conda=5.1.1=hd8ed1ab_0

  <   - ravenpy=0.6.0=pyh1bb2064_2
  >   - ravenpy=0.7.0=pyh1bb2064_0

  <   - pandas=1.2.5=py37h219a48f_0
  >   - pandas=1.3.1=py37h219a48f_0

  <   - xarray=0.18.2=pyhd8ed1ab_0
  >   - xarray=0.19.0=pyhd8ed1ab_1

  <   - dask=2021.7.0=pyhd8ed1ab_0
  >   - dask=2021.7.1=pyhd8ed1ab_0

  <   - regionmask=0.6.2=pyhd8ed1ab_0
  >   - regionmask=0.7.0=pyhd8ed1ab_0
  ```

[1.13.13](https://github.com/bird-house/birdhouse-deploy/tree/1.13.13) (2021-07-26)
------------------------------------------------------------------------------------------------------------------

  ###  Changes

  - jupyter: update for RavenPy-0.6.0, Xclim-0.28.0 and latest of everything else

    See PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/84 for more info.

    Relevant changes:
    ```diff
    <   - ravenpy=0.5.2=pyh7f9bfb9_0
    >   - ravenpy=0.6.0=pyh1bb2064_2
    
    <   - xclim=0.27.0=pyhd8ed1ab_0
    >   - xclim=0.28.0=pyhd8ed1ab_0
    
    # birdy rebuild
    <   - birdy=v0.8.0=pyh6c4a22f_0
    >   - birdy=v0.8.0=pyh6c4a22f_1
    
    <   - cf_xarray=0.5.2=pyh6c4a22f_0
    >   - cf_xarray=0.6.0=pyh6c4a22f_0
    
    <   - cftime=1.4.1=py37h902c9e0_0
    >   - cftime=1.5.0=py37h6f94858_0
    
    <   - dask=2021.6.0=pyhd8ed1ab_0
    >   - dask=2021.7.0=pyhd8ed1ab_0
    
    <   - nc-time-axis=1.2.0=py_1
    >   - nc-time-axis=1.3.1=pyhd8ed1ab_2
    
    <   - rioxarray=0.4.1.post0=pyhd8ed1ab_0
    >   - rioxarray=0.5.0=pyhd8ed1ab_0
    
    <   - numpy=1.20.3=py37h038b26d_1
    >   - numpy=1.21.1=py37h038b26d_0
    
    <   - pandas=1.2.4=py37h219a48f_0
    >   - pandas=1.2.5=py37h219a48f_0
    
    <   - plotly=4.14.3=pyh44b312d_0
    >   - plotly=5.1.0=pyhd8ed1ab_1
    
    <     - nbconvert==5.6.1
    >   - nbconvert=6.1.0=py37h89c1867_0
    ```

[1.13.12](https://github.com/bird-house/birdhouse-deploy/tree/1.13.12) (2021-07-13)
------------------------------------------------------------------------------------------------------------------

  ###  Changes

  - Add `csv` files to Thredds filter

[1.13.11](https://github.com/bird-house/birdhouse-deploy/tree/1.13.11) (2021-07-06)
------------------------------------------------------------------------------------------------------------------

  ### Changes

  - Notebook deployment: allow to specify required branch for any tutorial
    notebook repos in `env.local`.

    Example: set `WORKFLOW_TESTS_BRANCH` and any other
    notebook deploy config like `PAVICS_LANDING_BRANCH` in `env.local`.

    To support testing of this PR
    https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/79.

  - jupyter: minor update to add `unzip` package

    `unzip` needed to test PAVICS-landing notebooks under Jenkins.  No other
    package updates.

    See PR
    https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/79
    for more details.

[1.13.10](https://github.com/bird-house/birdhouse-deploy/tree/1.13.10) (2021-06-30)
------------------------------------------------------------------------------------------------------------------

  ### Changes
  
  - Add `bump2version` configuration to allow self-update of files that refer to new version releases 
    and apply update of features listed in this changelog.
  - Add this `CHANGES.md` file with all previous version details extracted for PR merge commit messages.
  - Add listing of change history to generated documentation on
    [bird-house/birdhouse-deploy ReadTheDocs](https://birdhouse-deploy.readthedocs.io/en/latest/).
  - Update ``CONTRIBUTING.rst`` file to include note about updating this changelog for future PR.
  
  ### Fixes
  
  - Resolves [#157](https://github.com/bird-house/birdhouse-deploy/issues/157)

[1.13.9](https://github.com/bird-house/birdhouse-deploy/tree/1.13.9) (2021-06-18)
------------------------------------------------------------------------------------------------------------------

- `jupyter`: update for raven notebooks

  To deploy the new Jupyter env to PAVICS.

  Given it's an incremental build, these are the only differences:

  ```diff
  >   - intake-geopandas=0.2.4=pyhd8ed1ab_0
  >   - intake-thredds=2021.6.16=pyhd8ed1ab_0
  >   - intake-xarray=0.5.0=pyhd8ed1ab_0
  ```

  See PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/76.

[1.13.8](https://github.com/bird-house/birdhouse-deploy/tree/1.13.8) (2021-06-15)
------------------------------------------------------------------------------------------------------------------

- `jupyter`: new version for updated `ravenpy`, `birdy` and `xclim`

  PR to deploy the new Jupyter env to PAVICS.

  See PR [Ouranosinc/PAVICS-e2e-workflow-tests#75](https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/75)
  for more details.

  ### Changes

  ```diff
  <   - ravenpy=0.4.2=py37_1
  >   - ravenpy=0.5.2=pyh7f9bfb9_0

  # Renamed.
  <   - raven=3.0.4.318=hc9bffa2_2
  >   - raven-hydro=3.0.4.322=h516393e_0

  <   - ostrich=21.03.16=h2bc3f7f_0
  >   - ostrich=21.03.16=h4bd325d_1

  <   - xclim=0.25.0=pyhd8ed1ab_0
  >   - xclim=0.27.0=pyhd8ed1ab_0

  # Old version was from pip.
  <     - birdhouse-birdy==0.7.0
  >   - birdy=v0.8.0=pyh6c4a22f_0

  # Was previously included in another package, now it is standalone.
  >   - pydantic=1.8.2=py37h5e8e339_0

  # New libs for upcoming Raven notebooks
  >   - gcsfs=2021.6.0=pyhd8ed1ab_0
  >   - intake=0.6.2=pyhd8ed1ab_0
  >   - intake-esm=2021.1.15=pyhd8ed1ab_0
  >   - zarr=2.8.3=pyhd8ed1ab_0

  <   - xarray=0.17.0=pyhd8ed1ab_0
  >   - xarray=0.18.2=pyhd8ed1ab_0

  <   - owslib=0.23.0=pyhd8ed1ab_0
  >   - owslib=0.24.1=pyhd8ed1ab_0

  <   - cf_xarray=0.5.1=pyh44b312d_0
  >   - cf_xarray=0.5.2=pyh6c4a22f_0

  <   - clisops=0.6.3=pyh44b312d_0
  >   - clisops=0.6.5=pyh6c4a22f_0

  <   - dask=2021.2.0=pyhd8ed1ab_0
  >   - dask=2021.6.0=pyhd8ed1ab_0

  # Downgrade !
  <   - gdal=3.2.1=py37hc5bc4e4_7
  >   - gdal=3.1.4=py37h2ec2946_8

  # Downgrade !
  <   - rasterio=1.2.2=py37hd5c4cce_0
  >   - rasterio=1.2.1=py37ha549118_0

  <   - hvplot=0.7.1=pyh44b312d_0
  >   - hvplot=0.7.2=pyh6c4a22f_0

  <   - rioxarray=0.3.1=pyhd8ed1ab_0
  >   - rioxarray=0.4.1.post0=pyhd8ed1ab_0

  # Downgrade !
  <   - xskillscore=0.0.19=pyhd8ed1ab_0
  >   - xskillscore=0.0.18=py_1
  ```

  Full diff of `conda env export`:
  [210415-210527.1-update210615-conda-env-export.diff.txt](https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/files/6658638/210415-210527.1-update210615-conda-env-export.diff.txt)

  Full new `conda env export`:
  [210527.1-update210615-conda-env-export.yml.txt](https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/files/6658646/210527.1-update210615-conda-env-export.yml.txt)

[1.13.7](https://github.com/bird-house/birdhouse-deploy/tree/1.13.7) (2021-06-10)
------------------------------------------------------------------------------------------------------------------

- `jupyterhub`: allow config override via env.local

  ### Overview

  This is basically the same as `ENABLE_JUPYTERHUB_MULTI_NOTEBOOKS` but at the bottom of the file so it can 
  override everything.

  `ENABLE_JUPYTERHUB_MULTI_NOTEBOOKS` is kept for backward-compat.

  First useful application is to enable server culling for auto shutdown of idle kernels and idle jupyter single server,
  hopefully fixes [#67](https://github.com/bird-house/birdhouse-deploy/issues/67).

  The culling settings will only take effect the next time user restart their personal Jupyter server because it seems 
  that the Jupyter server is the one culling itself.  JupyterHub do not perform the culling, it simply forwards the 
  culling settings to the Jupyter server.

  ```sh
  $ docker inspect jupyter-lvu --format '{{ .Args }}'
  [run -n birdy /usr/local/bin/start-notebook.sh --ip=0.0.0.0 --port=8888 --notebook-dir=/notebook_dir --SingleUserNotebookApp.default_url=/lab --debug --disable-user-config --NotebookApp.terminals_enabled=False --NotebookApp.shutdown_no_activity_timeout=180 --MappingKernelManager.cull_idle_timeout=180 --MappingKernelManager.cull_connected=True]
  ```

  ### Changes

  **Non-breaking changes**
  - `jupyterhub`: allow config override via env.local

  ### Tests

  Deployed to https://lvupavicsdev.ouranos.ca/jupyter (timeout set to 5 mins)

[1.13.6](https://github.com/bird-house/birdhouse-deploy/tree/1.13.6) (2021-06-02)
------------------------------------------------------------------------------------------------------------------

- Bugfix for autodeploy job

  The new code added with 
  [this merge](https://github.com/bird-house/birdhouse-deploy/commit/d90765acabe248e65c4899929fbe37a9e8661643) 
  created a new bug for the autodeploy job.

  From the autodeploy job's log :
  ```
  triggerdeploy START_TIME=2021-05-13T14:00:03+0000
  Error: DEPLOY_DATA_JOB_SCHEDULE not set
  ```
  If the `AUTODEPLOY_NOTEBOOK_FREQUENCY` variable is not set in the `env.local` file, it would create the error above.
  The variable is set in the `default.env` file, in case it is not defined in the `env.local`, and is then used for the 
  new env file from `pavics-jupyter-base` 
  [here](https://github.com/bird-house/pavics-jupyter-base/blob/1f81480fe90e0a110f0320c6d6cb17f73b657733/scheduler-jobs/deploy_data_pavics_jupyter.env#L15).
  The error happens because the `default.env` was not called in the `triggerdeploy.sh` script, and the variable was not 
  set when running the `env.local`.

  Solution was tested in a test environment and the cronjob seems to be fixed now.

  Tests were executed to see if the same situation could be found anywhere else. 
  From what was observed, `default.env` seems to be called consistently before the `env.local`.
  Only [here](https://github.com/bird-house/birdhouse-deploy/blob/7e2b8cb428be29d52d27b4b1faa73be7017712ea/birdhouse/deployment/deploy.sh#L109), 
  `default.env` doesn't seem to be called. A `default.env` call has also been added in that file.

[1.13.5](https://github.com/bird-house/birdhouse-deploy/tree/1.13.5) (2021-05-19)
------------------------------------------------------------------------------------------------------------------

- magpie 3.x + gunicorn bind

[1.13.4](https://github.com/bird-house/birdhouse-deploy/tree/1.13.4) (2021-05-18)
------------------------------------------------------------------------------------------------------------------

- Update to raven 0.13.0

[1.13.3](https://github.com/bird-house/birdhouse-deploy/tree/1.13.3) (2021-05-11)
------------------------------------------------------------------------------------------------------------------

- - Add new docker-compose optional components
    * `optional-components/database-external-ports`
    * `optional-components/wps-healthchecks`

  Following is the output result when using `optional-components/wps-healthcheck`
  ```
  ubuntu@daccs-instance-26730-daccsci:~$ pavics-compose ps
  reading './components/monitoring/default.env'
  reading './optional-components/testthredds/default.env'
  COMPOSE_CONF_LIST=-f docker-compose.yml -f ./components/monitoring/docker-compose-extra.yml -f ./optional-components/canarie-api-full-monitoring/docker-compose-extra.yml -f ./optional-components/all-public-access/docker-compose-extra.yml -f ./optional-components/testthredds/docker-compose-extra.yml -f ./optional-components/secure-thredds/docker-compose-extra.yml -f ./optional-components/wps-healthchecks/docker-compose-extra.yml -f ./optional-components/database-external-ports/docker-compose-extra.yml
       Name                    Command                  State                                                                                Ports
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  alertmanager      /bin/alertmanager --config ...   Up             0.0.0.0:9093->9093/tcp
  cadvisor          /usr/bin/cadvisor -logtostderr   Up (healthy)   0.0.0.0:9999->8080/tcp
  catalog           /bin/sh -c python /home/do ...   Up (healthy)   0.0.0.0:8086->80/tcp
  finch             gunicorn --bind=0.0.0.0:50 ...   Up (healthy)   0.0.0.0:8095->5000/tcp
  flyingpigeon      /bin/bash -c source activa ...   Up (healthy)   0.0.0.0:8093->8093/tcp
  frontend          /bin/sh -c /bin/bash ./bin ...   Up             0.0.0.0:3000->3000/tcp
  geoserver         /entrypointwrapper               Up             0.0.0.0:8087->8080/tcp
  grafana           /run.sh                          Up             0.0.0.0:3001->3000/tcp
  hummingbird       /usr/bin/tini -- make upda ...   Up (healthy)   0.0.0.0:28097->28097/tcp, 0.0.0.0:38097->38097/tcp, 8000/tcp, 8080/tcp, 0.0.0.0:8097->8097/tcp, 8443/tcp, 0.0.0.0:48097->9001/tcp
  jupyterhub        jupyterhub                       Up             0.0.0.0:8800->8000/tcp
  magpie            /bin/sh -c crond -c $CRON_ ...   Up             0.0.0.0:2001->2001/tcp
  malleefowl        /usr/bin/tini -- make upda ...   Up (healthy)   0.0.0.0:28091->28091/tcp, 0.0.0.0:38091->38091/tcp, 8000/tcp, 8080/tcp, 0.0.0.0:8091->8091/tcp, 8443/tcp, 0.0.0.0:48091->9001/tcp
  mongodb           /entrypoint.sh bash -c cho ...   Up             0.0.0.0:27017->27017/tcp
  ncwms2            /usr/bin/tini -- make upda ...   Up             0.0.0.0:8080->8080/tcp, 0.0.0.0:48080->9001/tcp
  node-exporter     /bin/node_exporter --path. ...   Up
  phoenix           /usr/bin/tini -- make upda ...   Up             0.0.0.0:38443->38443/tcp, 8000/tcp, 8080/tcp, 0.0.0.0:8081->8081/tcp, 0.0.0.0:8443->8443/tcp, 0.0.0.0:9001->9001/tcp
  portainer         /portainer                       Up             0.0.0.0:9000->9000/tcp
  postgis           /bin/sh -c /start-postgis.sh     Up             5432/tcp
  postgres          docker-entrypoint.sh postgres    Up             0.0.0.0:5432->5432/tcp
  postgres-magpie   docker-entrypoint.sh postgres    Up             0.0.0.0:5433->5432/tcp
  project-api       /bin/sh -c npm run bootstr ...   Up             0.0.0.0:3005->3005/tcp
  prometheus        /bin/prometheus --config.f ...   Up             0.0.0.0:9090->9090/tcp
  proxy             /entrypoint                      Up             0.0.0.0:443->443/tcp, 0.0.0.0:80->80/tcp, 0.0.0.0:58079->8079/tcp, 0.0.0.0:58086->8086/tcp, 0.0.0.0:58091->8091/tcp, 0.0.0.0:58093->8093/tcp,
                                                                    0.0.0.0:58094->8094/tcp
  raven             /bin/bash -c source activa ...   Up (healthy)   0.0.0.0:8096->9099/tcp
  solr              /usr/bin/tini -- /bin/sh - ...   Up             0.0.0.0:8983->8983/tcp, 0.0.0.0:48983->9001/tcp
  testthredds       /entrypointwrapper               Up (healthy)   0.0.0.0:8084->8080/tcp, 8443/tcp
  thredds           /entrypointwrapper               Up (healthy)   0.0.0.0:8083->8080/tcp, 8443/tcp
  twitcher          pserve /opt/birdhouse/src/ ...   Up             0.0.0.0:8000->8000/tcp, 8080/tcp, 8443/tcp, 9001/tcp
  ```

[1.13.2](https://github.com/bird-house/birdhouse-deploy/tree/1.13.2) (2021-05-11)
------------------------------------------------------------------------------------------------------------------

- Custom notebooks

[1.13.1](https://github.com/bird-house/birdhouse-deploy/tree/1.13.1) (2021-05-10)
------------------------------------------------------------------------------------------------------------------

- `jupyterhub`: update to ver 1.4.0-20210506

  ### Changes

  **Non-breaking changes**

  - `jupyterhub`: update to ver 1.4.0-20210506

  ### Tests

  - Deployed to https://lvupavics.ouranos.ca/jupyter
  - Able to login
  - Able to start personal Jupyter server

  ## Additional Information

  - Jupyter hub release note: https://github.com/jupyterhub/jupyterhub/blob/1.4.0/docs/source/changelog.md

[1.13.0](https://github.com/bird-house/birdhouse-deploy/tree/1.13.0) (2021-05-06)
------------------------------------------------------------------------------------------------------------------

- bump default log retention to `500m` instead of `2m`, more suitable for prod

  ### Overview

  Bump default log retention to `500m` instead of `2m`, more suitable for prod

  Forgot to push during PR [#152](https://github.com/bird-house/birdhouse-deploy/pull/152).

  ### Changes

  **Non-breaking changes**
  - Bump default log retention to `500m` instead of `2m`, more suitable for prod

[1.12.4](https://github.com/bird-house/birdhouse-deploy/tree/1.12.4) (2021-05-06)
------------------------------------------------------------------------------------------------------------------

- Update to new finch [0.7.4](https://github.com/bird-house/finch/tree/v0.7.4).

  ### Overview

  Updates finch's image to just released [0.7.4](https://github.com/bird-house/finch/tree/v0.7.4).

  ### Changes

  **Non-breaking changes**
  - Updates finch's xclim to 0.26.
  - Finch now has improved metadata handling : output's attributes are read from config and ensemble 
    processes' datasets are included in the attributes of the output.
  - Ensemble processes now compute meaningful statistics for indicators using day-of-year "units".

  ### Tests

  * https://daccs-jenkins.crim.ca/job/PAVICS-e2e-workflow-tests/job/master/392/parameters/ against 
    Ouranos' prod `pavics.ouranos.ca` to baseline the state of things

  * https://daccs-jenkins.crim.ca/job/PAVICS-e2e-workflow-tests/job/master/393/parameters/ against 
    `lvupavicsdev.ouranos.ca` that has this PR deployed.

  Both all passes.

[1.12.3](https://github.com/bird-house/birdhouse-deploy/tree/1.12.3) (2021-05-04)
------------------------------------------------------------------------------------------------------------------

- Change overview:
  * allow customization of `/data` persistence root on disk, retaining current default for existing deployment
  * add data persistence for `mongodb` container

[1.12.2](https://github.com/bird-house/birdhouse-deploy/tree/1.12.2) (2021-04-28)
------------------------------------------------------------------------------------------------------------------

- Add contributions guideline and policy

[1.12.1](https://github.com/bird-house/birdhouse-deploy/tree/1.12.1) (2021-04-28)
------------------------------------------------------------------------------------------------------------------

- `proxy`: allow homepage (location /) to be configurable

[1.12.0](https://github.com/bird-house/birdhouse-deploy/tree/1.12.0) (2021-04-19)
------------------------------------------------------------------------------------------------------------------

- Magpie upgrade strike II

  Strike II of this original PR https://github.com/bird-house/birdhouse-deploy/pull/107.

  Matching notebook fix https://github.com/Ouranosinc/pavics-sdi/pull/218

  Performed test upgrade on staging (Medus) using prod (Boreas) Magpie DB, everything went well and Jenkins passed (http://jenkins.ouranos.ca/job/ouranos-staging/job/medus.ouranos.ca/80/parameters/).  This Jenkins build uses the corresponding branch in https://github.com/Ouranosinc/pavics-sdi/pull/218 and with `TEST_MAGPIE_AUTH` enabled.

  Manual upgrade migration procedure:
  1. Save `/data/magpie_persist` folder from prod `pavics.ouranos.ca`: `cd /data; tar czf magpie_persist.prod.tgz magpie_persist`
  2. scp `magpie_persist.prod.tgz` to `medus`
  3. login to `medus`
  4. `cd /path/to/birdhouse-deploy/birdhouse`
  5. `./pavics-compose.sh down`
  6. `git checkout master`
  7. `cd /data`
  8. `rm -rf magpie_persist`
  9. `tar xzf magpie_persist.prod.tgz`  # restore Magpie DB with prod version
  10. `cd /path/to/birdhouse-deploy/birdhouse`
  11. `./pavics-compose.sh up -d`
  12. Update `env.local` `MAGPIE_ADMIN_PASSWORD` with prod passwd for Twitcher to be able to access Magpie since we juste restore the Magpie DB from prod
  13. `./pavics-compose.sh restart twitcher`  # for Twitcher to get new Magpie admin passwd
  14. Baseline working state: trigger Jenkins test suite, ensure all pass except `pavics_thredds.ipynb` that requires new Magpie
  15. Baseline working state: view existing services permissions on group Anonymous (https://medus.ouranos.ca/magpie/ui/groups/anonymous/default)
  16. `git checkout restore-previous-broken-magpie-upgrade-so-we-can-work-on-a-fix`  # This current branch
  17. `./pavics-compose.sh up -d`  # upgrade to new Magpie
  18. `docker logs magpie`: check no DB migration error
  19. Trigger Jenkins test suite again

[1.11.29](https://github.com/bird-house/birdhouse-deploy/tree/1.11.29) (2021-04-16)
------------------------------------------------------------------------------------------------------------------

- Update Raven and Jupyter env for Raven demo

  Raven release notes in 
  PR [Ouranosinc/raven#374](https://github.com/Ouranosinc/raven/pull/374])
  and [Ouranosinc/raven#382](https://github.com/Ouranosinc/raven/pull/382)

  Jupyter env update in 
  PR [Ouranosinc/PAVICS-e2e-workflow-tests#71](https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/71)

  Other fixes:
  * Fix intermittent Jupyter spawning error by doubling various timeouts config 
    (it's intermittent so hard to test so we are not sure which ones of timeout fixed it)
  * Fix Finch and Raven "Broken pipe" error when the request size is larger than default 3mb (bumped to 100mb) 
    (fixes [Ouranosinc/raven#361](https://github.com/Ouranosinc/raven/issues/361) 
    and Finch related [comment](https://github.com/bird-house/finch/issues/98#issuecomment-811230388))
  * Lower chance to have "Max connection" error for Finch and Raven (bump parallelprocesses from 2 to 10). 
    In prod, the server has the CPU needed to run 10 concurrent requests if needed so this prevent users having to
    "wait" after each other.

[1.11.28](https://github.com/bird-house/birdhouse-deploy/tree/1.11.28) (2021-04-09)
------------------------------------------------------------------------------------------------------------------

- `jupyter`: update for new `clisops`, `xclim`, `ravenpy`

  Matching PR to deploy the new Jupyter env to PAVICS.

  See PR [Ouranosinc/PAVICS-e2e-workflow-tests#68](https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/68)
  for more info.

  Relevant changes:
  ```diff
  <   - clisops=0.5.1=pyhd3deb0d_0
  >   - clisops=0.6.3=pyh44b312d_0

  <   - xclim=0.23.0=pyhd8ed1ab_0
  >   - xclim=0.25.0=pyhd8ed1ab_0

  >   - ostrich=0.1.2=h2bc3f7f_0
  >   - raven=0.1.1=h2bc3f7f_0

  <     - ravenpy==0.2.3  # from pip
  >   - ravenpy=0.3.1=py37_0  # from conda

  >   - aiohttp=3.7.4=py37h5e8e339_0

  <   - roocs-utils=0.1.5=pyhd3deb0d_1
  >   - roocs-utils=0.3.0=pyh6c4a22f_0

  <   - cf_xarray=0.4.0=pyh44b312d_0
  >   - cf_xarray=0.5.1=pyh44b312d_0

  <   - rioxarray=0.2.0=pyhd8ed1ab_0
  >   - rioxarray=0.3.1=pyhd8ed1ab_0

  <   - xarray=0.16.2=pyhd8ed1ab_0
  >   - xarray=0.17.0=pyhd8ed1ab_0

  <   - geopandas=0.8.2=pyhd8ed1ab_0
  >   - geopandas=0.9.0=pyhd8ed1ab_0

  <   - gdal=3.1.4=py37h2ec2946_5
  >   - gdal=3.2.1=py37hc5bc4e4_7

  <   - jupyter_conda=4.1.0=hd8ed1ab_1
  >   - jupyter_conda=5.0.0=hd8ed1ab_0

  <   - python=3.7.9=hffdb5ce_100_cpython
  >   - python=3.7.10=hffdb5ce_100_cpython
  ```

[1.11.27](https://github.com/bird-house/birdhouse-deploy/tree/1.11.27) (2021-04-01)
------------------------------------------------------------------------------------------------------------------

- reverted name of monitoring routes to original

  The Canarie API complains that `stats` are up but don't return the correct response.
  It is assumed that it was because the monitoring key was changed to reflect the actual content.

  Validation service: https://science.canarie.ca/researchsoftware/services/validator/service.html
  Use Managed
  Enter URL: http://pavics.ouranos.ca/canarie/renderer
  Submit

  Deployed on my dev VM, fix worked, thanks !

  ![Screenshot_2021-04-01 CANARIE Research Software Logiciels de recherche de CANARIE](https://user-images.githubusercontent.com/11966697/113295664-7c359b80-92c6-11eb-8c50-5e77f498d84f.png)

[1.11.26](https://github.com/bird-house/birdhouse-deploy/tree/1.11.26) (2021-03-31)
------------------------------------------------------------------------------------------------------------------

- Update canarieAPI doc links

  - Updated components' version number.
  - Replaced links to githubio docs to readthedocs.
  - renderer is provided by THREDDS-WMS.
  - slicer is provided by finch.

[1.11.25](https://github.com/bird-house/birdhouse-deploy/tree/1.11.25) (2021-03-26)
------------------------------------------------------------------------------------------------------------------

- finch: update to version 0.7.1

  See Finch release PR https://github.com/bird-house/finch/pull/164 for more release info.

  This update will fix the following Jenkins error introduced by https://github.com/bird-house/finch/pull/161#discussion_r601975311:

  ```
  12:37:00  _________ finch-master/docs/source/notebooks/finch-usage.ipynb::Cell 1 _________
  12:37:00  Notebook cell execution failed
  12:37:00  Cell 1: Cell outputs differ
  12:37:00
  12:37:00  Input:
  12:37:00  help(wps.frost_days)
  12:37:00
  12:37:00  Traceback:
  12:37:00   mismatch 'stdout'
  12:37:00
  12:37:00   assert reference_output == test_output failed:
  12:37:00
  12:37:00    'Help on meth...ut files.\n\n' == 'Help on meth...ut files.\n\n'
  12:37:00    Skipping 70 identical leading characters in diff, use -v to show
  12:37:00    - min=None, missing_options=None, check_missing='any', thresh='0 degC', freq='YS', variable=None, output_formats=None) method of birdy.client.base.WPSClient instance
  12:37:00    + min=None, check_missing='any', cf_compliance='warn', data_validation='raise', thresh='0 degC', freq='YS', missing_options=None, variable=None, output_formats=None) method of birdy.client.base.WPSClient instance
  12:37:00          Number of days where daily minimum temperatures are below 0.
  12:37:00
  12:37:00          Parameters
  12:37:00          ----------
  12:37:00          tasmin : ComplexData:mimetype:`application/x-netcdf`, :mimetype:`application/x-ogc-dods`
  12:37:00              NetCDF Files or archive (tar/zip) containing netCDF files.
  12:37:00          thresh : string
  12:37:00              Freezing temperature.
  12:37:00          freq : {'YS', 'MS', 'QS-DEC', 'AS-JUL'}string
  12:37:00              Resampling frequency.
  12:37:00          check_missing : {'any', 'wmo', 'pct', 'at_least_n', 'skip', 'from_context'}string
  12:37:00              Method used to determine which aggregations should be considered missing.
  12:37:00          missing_options : ComplexData:mimetype:`application/json`
  12:37:00              JSON representation of dictionary of missing method parameters.
  12:37:00    +     cf_compliance : {'log', 'warn', 'raise'}string
  12:37:00    +         Whether to log, warn or raise when inputs have non-CF-compliant attributes.
  12:37:00    +     data_validation : {'log', 'warn', 'raise'}string
  12:37:00    +         Whether to log, warn or raise when inputs fail data validation checks.
  12:37:00          variable : string
  12:37:00              Name of the variable in the NetCDF file.
  12:37:00
  12:37:00          Returns
  12:37:00          -------
  12:37:00          output_netcdf : ComplexData:mimetype:`application/x-netcdf`
  12:37:00              The indicator values computed on the original input grid.
  12:37:00          output_log : ComplexData:mimetype:`text/plain`
  12:37:00              Collected logs during process run.
  12:37:00          ref : ComplexData:mimetype:`application/metalink+xml; version=4.0`
  12:37:00              Metalink file storing all references to output files.
  ```

  Jenkins build with Finch notebooks passing against newer Finch: http://jenkins.ouranos.ca/job/ouranos-staging/job/lvupavics.ouranos.ca/45/console

[1.11.24](https://github.com/bird-house/birdhouse-deploy/tree/1.11.24) (2021-03-19)
------------------------------------------------------------------------------------------------------------------

- Avoid docker pull since pull rate limit on dockerhub

  Pin bash tag so it is reproducible (previously it was more or less reproducible since we always ensure "latest" tag).

  Avoid the following error:

  ```
  + docker pull bash
  Using default tag: latest
  Error response from daemon: toomanyrequests: You have reached your pull rate limit. You may increase the limit by authenticating and upgrading: https://www.docker.com/increase-rate-limit
  ```

[1.11.23](https://github.com/bird-house/birdhouse-deploy/tree/1.11.23) (2021-03-17)
------------------------------------------------------------------------------------------------------------------

- Custom Jupyter user images

  Adds CRIM's nlp and eo images to the available list of images in JupyterHub

  The base image (pavics-jupyter-base) wasn't added to the list, because it is assumed the users will always be 
  using the other more specialized images.

  We were already able to add/override Jupyter images but this PR makes it more integrated: those image will 
  also be pulled in advanced so startup is much faster for big images since these images will already be cached.

  Backward incompatible changes:
  DOCKER_NOTEBOOK_IMAGE renamed to DOCKER_NOTEBOOK_IMAGES and is now a space separated list of images. 
  Any existing override in env.local using the old name will have to switch to the new name.

[1.11.22](https://github.com/bird-house/birdhouse-deploy/tree/1.11.22) (2021-03-16)
------------------------------------------------------------------------------------------------------------------

- finch: update to 0.7.0

  Require PR https://github.com/bird-house/birdhouse-deploy/pull/131 for extra testdata for the new regridding notebook.

  Regridding notebook will also need to be adjusted for some output to pass Jenkins test suite, 
  PR https://github.com/Ouranosinc/pavics-sdi/pull/206.

  Nbval escape regex also needed for the regridding notebook, 
  PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/63

  See Finch changelog in PR https://github.com/bird-house/finch/pull/158

  Passing Jenkins build 
  http://jenkins.ouranos.ca/job/PAVICS-e2e-workflow-tests/job/update-nbval-sanitize-config-for-pavics-sdi-regridding-notebook/10/console

[1.11.21](https://github.com/bird-house/birdhouse-deploy/tree/1.11.21) (2021-02-19)
------------------------------------------------------------------------------------------------------------------

- Configurable Jupyterhub README

  While 
  the [`README.ipynb`](https://github.com/bird-house/birdhouse-deploy/blob/master/docs/source/notebooks/README.ipynb) 
  provided by `birdhouse-deploy` is good, it does not quite fit our needs at PCIC. This PR allows users to configure 
  their own `README` for Jupyterhub.

  ### Changes
  - Adds `JUPYERHUB_README` as configuration option in the appropriate spots

[1.11.20](https://github.com/bird-house/birdhouse-deploy/tree/1.11.20) (2021-02-19)
------------------------------------------------------------------------------------------------------------------

- `jupyter`: update to version 210216 for xESMF

  Matching PR to deploy https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/61 to PAVICS.

  For regridding notebook, see https://github.com/Ouranosinc/pavics-sdi/pull/201#issuecomment-778329309.

  Noticeable changes:

  ```diff
  >   - xesmf=0.5.2=pyhd8ed1ab_0

  <   - owslib=0.21.0=pyhd8ed1ab_0
  >   - owslib=0.23.0=pyhd8ed1ab_0

  <   - cftime=1.3.1=py37h6323ea4_0
  >   - cftime=1.4.1=py37h902c9e0_0

  <   - dask=2021.1.1=pyhd8ed1ab_0
  >   - dask=2021.2.0=pyhd8ed1ab_0

  <   - rioxarray=0.1.1=pyhd8ed1ab_0
  >   - rioxarray=0.2.0=pyhd8ed1ab_0
  ```

[1.11.19](https://github.com/bird-house/birdhouse-deploy/tree/1.11.19) (2021-02-10)
------------------------------------------------------------------------------------------------------------------

- `proxy`: proxy_read_timeout config should be configurable

  We have a performance problem with the production deployment at Ouranos so we need a longer timeout. 
  Being an Ouranos specific need, it should not be hardcoded as in previous PR https://github.com/bird-house/birdhouse-deploy/pull/122.

  The previous increase was sometime not enough !

  The value is now configurable via `env.local` as most other customizations.  Documentation updated.

  Timeout in Prod:
  ```
  WPS_URL=https://pavics.ouranos.ca/twitcher/ows/proxy/raven/wps FINCH_WPS_URL=https://pavics.ouranos.ca/twitcher/ows/proxy/finch/wps FLYINGPIGEON_WPS
  _URL=https://pavics.ouranos.ca/twitcher/ows/proxy/flyingpigeon/wps pytest --nbval-lax --verbose docs/source/notebooks/Running_HMETS_with_CANOPEX_datas
  et.ipynb --sanitize-with docs/source/output-sanitize.cfg --ignore docs/source/notebooks/.ipynb_checkpoints

  HTTPError: 504 Server Error: Gateway Time-out for url: https://pavics.ouranos.ca/twitcher/ows/proxy/raven/wps

  ===================================================== 11 failed, 4 passed, 1 warning in 249.80s (0:04:09) ===========================================
  ```

  Pass easily on my test VM with very modest hardware (10G ram, 2 cpu):
  ```
  WPS_URL=https://lvupavicsmaster.ouranos.ca/twitcher/ows/proxy/raven/wps FINCH_WPS_URL=https://lvupavicsmaster.ouranos.ca/twitcher/ows/proxy/finch/wp
  s FLYINGPIGEON_WPS_URL=https://lvupavicsmaster.ouranos.ca/twitcher/ows/proxy/flyingpigeon/wps pytest --nbval-lax --verbose docs/source/notebooks/Runni
  ng_HMETS_with_CANOPEX_dataset.ipynb --sanitize-with docs/source/output-sanitize.cfg --ignore docs/source/notebooks/.ipynb_checkpoints

  =========================================================== 15 passed, 1 warning in 33.84s ===========================================================
  ```

  Pass against Medus:
  ```
  WPS_URL=https://medus.ouranos.ca/twitcher/ows/proxy/raven/wps FINCH_WPS_URL=https://medus.ouranos.ca/twitcher/ows/proxy/finch/wps FLYINGPIGEON_WPS_URL=https://medus.ouranos.ca/twitcher/ows/proxy/flyingpigeon/wps pytest --nbval-lax --verbose docs/source/notebooks/Running_HMETS_with_CANOPEX_dataset.ipynb --sanitize-with docs/source/output-sanitize.cfg --ignore docs/source/notebooks/.ipynb_checkpoints

  ============================================== 15 passed, 1 warning in 42.44s =======================================================
  ```

  Pass against `hirondelle.crim.ca`:
  ```
  WPS_URL=https://hirondelle.crim.ca/twitcher/ows/proxy/raven/wps FINCH_WPS_URL=https://hirondelle.crim.ca/twitcher/ows/proxy/finch/wps FLYINGPIGEON_WPS_URL=https://hirondelle.crim.ca/twitcher/ows/proxy/flyingpigeon/wps pytest --nbval-lax --verbose docs/source/notebooks/Running_HMETS_with_CANOPEX_dataset.ipynb --sanitize-with docs/source/output-sanitize.cfg --ignore docs/source/notebooks/.ipynb_checkpoints

  =============================================== 15 passed, 1 warning in 35.61s ===============================================
  ```

  For comparison, a run on Prod without Twitcher (PR https://github.com/bird-house/birdhouse-deploy-ouranos/pull/5):
  ```
  WPS_URL=https://pavics.ouranos.ca/raven/wps FINCH_WPS_URL=https://pavics.ouranos.ca/twitcher/ows/proxy/finch/wps FLYINGPIGEON_WPS_URL=https://pavics
  .ouranos.ca/twitcher/ows/proxy/flyingpigeon/wps pytest --nbval-lax --verbose docs/source/notebooks/Running_HMETS_with_CANOPEX_dataset.ipynb --sanitize
  -with docs/source/output-sanitize.cfg --ignore docs/source/notebooks/.ipynb_checkpoints

  HTTPError: 504 Server Error: Gateway Time-out for url: https://pavics.ouranos.ca/raven/wps

  ================================================ 11 failed, 4 passed, 1 warning in 248.99s (0:04:08) =================================================
  ```

  A run on Prod without Twitcher and Nginx (direct hit Raven):
  ```
  WPS_URL=http://pavics.ouranos.ca:8096/ FINCH_WPS_URL=https://pavics.ouranos.ca/twitcher/ows/proxy/finch/wps FLYINGPIGEON_WPS_URL=https://pavics.oura
  nos.ca/twitcher/ows/proxy/flyingpigeon/wps pytest --nbval-lax --verbose docs/source/notebooks/Running_HMETS_with_CANOPEX_dataset.ipynb --sanitize-with
   docs/source/output-sanitize.cfg --ignore docs/source/notebooks/.ipynb_checkpoints

  ===================================================== 15 passed, 1 warning in 218.46s (0:03:38) ======================================================

[1.11.18](https://github.com/bird-house/birdhouse-deploy/tree/1.11.18) (2021-02-02)
------------------------------------------------------------------------------------------------------------------

- update Raven and Jupyter env

  See https://github.com/Ouranosinc/raven/compare/v0.10.0...v0.11.1 for change details.

  Jupyter env change details: https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/60

  Jenkins run 
  (this Jupyter env `pavics/workflow-tests:210201.2` against a devel version of Raven `0.11.1` + `--nbval-lax`) 
  http://jenkins.ouranos.ca/job/PAVICS-e2e-workflow-tests/job/test-nbval-lax-DO_NOT_MERGE/4/console

  Only known error:
  ```
  20:25:45  =========================== short test summary info ============================
  20:25:45  FAILED pavics-sdi-master/docs/source/notebooks/WMS_example.ipynb::Cell 1
  20:25:45  FAILED pavics-sdi-master/docs/source/notebooks/WMS_example.ipynb::Cell 2
  20:25:45  FAILED pavics-sdi-master/docs/source/notebooks/WMS_example.ipynb::Cell 3
  20:25:45  FAILED pavics-sdi-master/docs/source/notebooks/WMS_example.ipynb::Cell 4
  20:25:45  FAILED pavics-sdi-master/docs/source/notebooks/WMS_example.ipynb::Cell 5
  20:25:45  FAILED pavics-sdi-master/docs/source/notebooks/WMS_example.ipynb::Cell 6
  20:25:45  FAILED pavics-sdi-master/docs/source/notebooks/WMS_example.ipynb::Cell 7
  20:25:45  FAILED raven-master/docs/source/notebooks/Bias_correcting_climate_data.ipynb::Cell 8
  20:25:45  FAILED raven-master/docs/source/notebooks/Bias_correcting_climate_data.ipynb::Cell 9
  20:25:45  FAILED raven-master/docs/source/notebooks/Bias_correcting_climate_data.ipynb::Cell 10
  20:25:45  FAILED raven-master/docs/source/notebooks/Bias_correcting_climate_data.ipynb::Cell 11
  20:25:45  FAILED raven-master/docs/source/notebooks/Full_process_example_1.ipynb::Cell 13
  20:25:45  FAILED raven-master/docs/source/notebooks/Full_process_example_1.ipynb::Cell 17
  20:25:45  FAILED raven-master/docs/source/notebooks/Full_process_example_1.ipynb::Cell 18
  20:25:45  FAILED raven-master/docs/source/notebooks/Full_process_example_1.ipynb::Cell 19
  20:25:45  FAILED raven-master/docs/source/notebooks/Full_process_example_1.ipynb::Cell 20
  20:25:45  FAILED raven-master/docs/source/notebooks/Full_process_example_1.ipynb::Cell 21
  20:25:45  FAILED raven-master/docs/source/notebooks/Multiple_watersheds_simulation.ipynb::Cell 1
  20:25:45  FAILED raven-master/docs/source/notebooks/Multiple_watersheds_simulation.ipynb::Cell 3
  20:25:45  FAILED raven-master/docs/source/notebooks/Multiple_watersheds_simulation.ipynb::Cell 4
  20:25:45  FAILED raven-master/docs/source/notebooks/Multiple_watersheds_simulation.ipynb::Cell 5
  20:25:45  FAILED raven-master/docs/source/notebooks/Region_selection.ipynb::Cell 7
  20:25:45  FAILED raven-master/docs/source/notebooks/Region_selection.ipynb::Cell 8
  20:25:45  FAILED raven-master/docs/source/notebooks/Subset_climate_data_over_watershed.ipynb::Cell 5
  20:25:45  ============ 24 failed, 226 passed, 2 skipped in 2528.69s (0:42:08) ============
  ```

[1.11.17](https://github.com/bird-house/birdhouse-deploy/tree/1.11.17) (2021-01-28)
------------------------------------------------------------------------------------------------------------------

- finch: update to version 0.6.1

  See Finch PR https://github.com/bird-house/finch/pull/147 for release notes.

  Deployed on my dev server, Jenkins run no new errors: http://jenkins.ouranos.ca/job/PAVICS-e2e-workflow-tests/job/master/900/console

[1.11.16](https://github.com/bird-house/birdhouse-deploy/tree/1.11.16) (2021-01-14)
------------------------------------------------------------------------------------------------------------------

- finch: upgrade to version 0.6.0

  See Finch PR for release notes https://github.com/bird-house/finch/pull/138.

  Should fix https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/issues/58.

[1.11.15](https://github.com/bird-house/birdhouse-deploy/tree/1.11.15) (2021-01-14)
------------------------------------------------------------------------------------------------------------------

- `jupyter`: update to version 201214

  Matching PR to deploy the new Jupyter env in PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/56 to PAVICS.

  Relevant changes:

  ```diff
  >   - cfgrib=0.9.8.5=pyhd8ed1ab_0

  <   - clisops=0.3.1=pyh32f6830_1
  >   - clisops=0.4.0=pyhd3deb0d_0

  <   - dask=2.30.0=py_0
  >   - dask=2020.12.0=pyhd8ed1ab_0

  <   - owslib=0.20.0=py_0
  >   - owslib=0.21.0=pyhd8ed1ab_0

  <   - xarray=0.16.1=py_0
  >   - xarray=0.16.2=pyhd8ed1ab_0

  <   - xclim=0.21.0=py_0
  >   - xclim=0.22.0=pyhd8ed1ab_0

  <   - jupyter_conda=3.4.1=pyh9f0ad1d_0
  >   - jupyter_conda=4.1.0=hd8ed1ab_1
  ```

[1.11.14](https://github.com/bird-house/birdhouse-deploy/tree/1.11.14) (2020-12-17)
------------------------------------------------------------------------------------------------------------------
- Add ability to execute post actions for deploy-data script.

  Script `deploy-data` was previously introduced in PR [#72](https://github.com/bird-house/birdhouse-deploy/pull/72) to 
  deploy any files from any git repos to the local host it runs.

  Now it grows the ability to run commands from the git repo it just pulls.

  Being able to run commands open new possibilities:
  * post-processing after files from git repo are deployed (ex: advanced file re-mapping)
  * execute up-to-date scripts from git repos (PR https://github.com/bird-house/birdhouse-deploy-ouranos/pull/2)

  Combining this `deploy-data` with the `scheduler` component means we have a way for cronjobs to 
  automatically always execute the most up-to-date version of any scripts from any git repos.

[1.11.13](https://github.com/bird-house/birdhouse-deploy/tree/1.11.13) (2020-12-14)
------------------------------------------------------------------------------------------------------------------
- `jupyterhub`: update to version 1.3.0 to include login terms patch

  This version of jupyterhub includes the login terms patch originally
  introduced in commit 
  [8be8eeac211d3f5c2de620781db8832fdb8f9093](https://github.com/bird-house/birdhouse-deploy/commit/8be8eeac211d3f5c2de620781db8832fdb8f9093)
  of PR [#104](https://github.com/bird-house/birdhouse-deploy/pull/104).

  This official login terms feature has a few enhancements (see https://github.com/jupyterhub/jupyterhub/pull/3264#discussion_r530466178):

  * no javascript dependency
  * pop-up reminder for user to check the checkbox

  Behavior change is the "Sign in" button is not longer disabled if
  unchecked.  It simply does not work and reminds the user to check the
  checkbox if unchecked.

  Before:

  ![recorded](https://user-images.githubusercontent.com/11966697/99327962-1aa9ee80-2849-11eb-9ce8-3be6a1484e94.gif)

  After:
  ![recorded](https://user-images.githubusercontent.com/11966697/100246404-18115e00-2f07-11eb-9061-d35434ace3aa.gif)

[1.11.12](https://github.com/bird-house/birdhouse-deploy/tree/1.11.12) (2020-11-25)
------------------------------------------------------------------------------------------------------------------
- Fix geoserver not configured properly behind proxy.

  Hitting https://pavics.ouranos.ca/geoserver/wfs?request=GetCapabilities&version=1.1.0

  Before fix (wrong scheme and wrong port):
  ```
  <ows:Operation name="GetCapabilities">
  <ows:DCP>
  <ows:HTTP>
  <ows:Get xlink:href="http://pavics.ouranos.ca:80/geoserver/wfs"/>
  <ows:Post xlink:href="http://pavics.ouranos.ca:80/geoserver/wfs"/>
  </ows:HTTP>
  </ows:DCP>
  ```

  After fix:
  ```
  <ows:Operation name="GetCapabilities">
  <ows:DCP>
  <ows:HTTP>
  <ows:Get xlink:href="https://pavics.ouranos.ca:443/geoserver/wfs"/>
  <ows:Post xlink:href="https://pavics.ouranos.ca:443/geoserver/wfs"/>
  </ows:HTTP>
  </ows:DCP>
  ```

  This config automate manual step to set proxy base url in Geoserver UI 
  https://docs.geoserver.org/2.9.3/user/configuration/globalsettings.html#proxy-base-url

  I had to override the docker image entrypoint to edit the `server.xml` on the fly before starting Geoserver (Tomcat) 
  since setting Java proxy config did not seem to work (see first commit).

  Related to https://github.com/Ouranosinc/raven/issues/297.

[1.11.11](https://github.com/bird-house/birdhouse-deploy/tree/1.11.11) (2020-11-20)
------------------------------------------------------------------------------------------------------------------
- Various small fixes.

  `monitoring`: prevent losing stats when VM auto start from a power failure

  `check-instance-ready`: new script to smoke test instance 
  (use in `bootstrap-instance-for-testsuite` for our automation pipeline).

  jupyter: add CATALOG_USERNAME and anonymous to blocked_users list for security
  See comment https://github.com/bird-house/birdhouse-deploy/pull/102#issuecomment-730109547
  and comment https://github.com/bird-house/birdhouse-deploy/pull/102#issuecomment-730407914

      They are not real Jupyter users and their password is known.

      See config/magpie/permissions.cfg.template that created those users.

      Tested:
      ```
      [W 2020-11-20 13:25:18.924 JupyterHub auth:487] User 'admin-catalog' blocked. Stop authentication
      [W 2020-11-20 13:25:18.924 JupyterHub base:752] Failed login for admin-catalog

      [W 2020-11-20 13:49:18.069 JupyterHub auth:487] User 'anonymous' blocked. Stop authentication
      [W 2020-11-20 13:49:18.070 JupyterHub base:752] Failed login for anonymous
      ```

[1.11.10](https://github.com/bird-house/birdhouse-deploy/tree/1.11.10) (2020-11-18)
------------------------------------------------------------------------------------------------------------------
- Add terms conditions to JupyterHub login page and update to latest JupyterHub version.

  User have to check the checkbox agreeing to the terms and conditions in order to login 
  (fixes [Ouranosinc/pavics-sdi#188](https://github.com/Ouranosinc/pavics-sdi/issues/188)).

  User will have to accept the terms and conditions (the checkbox) each time he needs to login. 
  However, if user do not logout or wipe his browser cookies, the next time he navigate to the login page, 
  he'll just log right in, no password is asked so no terms and conditions to accept either.

  This behavior is optional and only enabled if `JUPYTER_LOGIN_TERMS_URL` in `env.local` is set.

  Had to patch the `login.html` template from jupyterhub docker image for this feature 
  (PR [jupyterhub/jupyterhub#3264](https://github.com/jupyterhub/jupyterhub/pull/3264)).

  Also update jupyterhub docker image to latest version.

  Deployed to my test server https://lvupavics.ouranos.ca/jupyter/hub/login 
  (pointing to a bogus terms and conditions link for now).

  Tested on Firefox and Google Chrome.

  Tested that upgrade from jupyterhub `1.0.0` to `1.2.1` is completely transparent to already logged in jupyter users.
  ```
  [D 2020-11-18 19:53:52.517 JupyterHub app:2055] Verifying that lvu is running at http://172.18.0.3:8888/jupyter/user/lvu/
  [D 2020-11-18 19:53:52.523 JupyterHub utils:220] Server at http://172.18.0.3:8888/jupyter/user/lvu/ responded with 302
  [D 2020-11-18 19:53:52.523 JupyterHub _version:76] jupyterhub and jupyterhub-singleuser both on version 1.2.1
  [I 2020-11-18 19:53:52.524 JupyterHub app:2069] lvu still running
  ```

  ![recorded](https://user-images.githubusercontent.com/11966697/99327962-1aa9ee80-2849-11eb-9ce8-3be6a1484e94.gif)

[1.11.9](https://github.com/bird-house/birdhouse-deploy/tree/1.11.9) (2020-11-13)
------------------------------------------------------------------------------------------------------------------
- `jupyter`: new image with 4 new extensions

  The google drive extension for JupyterLab requires a settings file containing the clientid of the project created 
  in developers.google.com, which give authorization to use google drive.

  This PR's role is to include this file in the birdhouse configs.

  Matching PR [Ouranosinc/PAVICS-e2e-workflow-tests#54](https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/54)
  (commit [5d5a9aa2251386378406efb5b414b3aa6db0b37e](https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/commit/5d5a9aa2251386378406efb5b414b3aa6db0b37e)) 
  for the new image with 4 new extensions: `jupytext`, `jupyterlab-google-drive`, `jupyter_conda` and `jupyterlab-git`

  Matching PR https://github.com/Ouranosinc/pavics-sdi/pull/185 for documentation about the new extensions.

[1.11.8](https://github.com/bird-house/birdhouse-deploy/tree/1.11.8) (2020-11-06)
------------------------------------------------------------------------------------------------------------------
- bump `finch` to version-0.5.3

[1.11.7](https://github.com/bird-house/birdhouse-deploy/tree/1.11.7) (2020-11-06)
------------------------------------------------------------------------------------------------------------------
- bump `thredds-docker` to 4.6.15

[1.11.6](https://github.com/bird-house/birdhouse-deploy/tree/1.11.6) (2020-11-06)
------------------------------------------------------------------------------------------------------------------
- Prepare fresh deployment for automated tests.

  @MatProv is building an automated pipeline that will provision and deploy a full PAVICS stack and run our Jenkins test suite for each PR here.

  So each time his new fresh instance comes up, there are a few steps to perform for the Jenkins test suite to pass.  Those steps are captured in `scripts/bootstrap-instance-for-testsuite`.  @MatProv please call this script, do not perform each steps yourself so any future changes to those steps will be transparent to your pipeline.  A new optional components was also required, done in PR https://github.com/bird-house/birdhouse-deploy/pull/92.

  For security reasons, Jupyterhub will block the test user to login since its password is known publicly.

  Each step are also in their own script so can be assembled differently to prepare the fresh instance if desired.

  Solr query in the canarie monitoring also updated to target the minimal dataset from `bootstrap-testdata` so the canarie monitoring page works on all PAVICS deployment (fixes https://github.com/bird-house/birdhouse-deploy/issues/6).  @MatProv you can use this canarie monitoring page (ex: https://pavics.ouranos.ca/canarie/node/service/status) to confirm the fresh instance is ready to run the Jenkins test suite.

[1.11.5](https://github.com/bird-house/birdhouse-deploy/tree/1.11.5) (2020-10-27)
------------------------------------------------------------------------------------------------------------------
- `jupyter`: new image for python 3.8, new xclim and memory_profiler

  Matching PR to deploy the new Jupyter image to PAVICS.

  Deployed to https://medus.ouranos.ca/jupyter/ for testing.  This one has python 3.8, might worth some manual testing.

  Relevant changes:
  ```diff
  <   - python=3.7.8=h6f2ec95_1_cpython
  >   - python=3.8.6=h852b56e_0_cpython

  <   - xclim=0.20.0=py_0
  >   - xclim=0.21.0=py_0

  <   - dask=2.27.0=py_0
  >   - dask=2.30.0=py_0

  <   - rioxarray=0.0.31=py_0
  >   - rioxarray=0.1.0=py_0

  >   - memory_profiler=0.58.0=py_0
  ```

  More info, see PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/53 (commit https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/commit/f07f1657ed13a0ed92854c5d01f9d3ed785e870d)

[1.11.4](https://github.com/bird-house/birdhouse-deploy/tree/1.11.4) (2020-10-15)
------------------------------------------------------------------------------------------------------------------
- Sync Raven testdata to Thredds for Raven tutorial notebooks.

  Leveraging the cron daemon of the scheduler component, sync Raven testdata to Thredds for Raven tutorial notebooks.

  Activation of the pre-configured cronjob is via `env.local` as usual for infra-as-code.

  New generic `deploy-data` script can clone any number of git repos, sync any number of folders in the git repo to any number of local folders, with ability to cherry-pick just the few files needed (Raven testdata has many types of files, we only need to sync `.nc` files to Thredds, to avoid polluting Thredds storage `/data/datasets/testdata/raven`).

  Limitation of the first version of this `deploy-data` script:
  * Do not handle re-organizing file layout, this is a pure sync only with very limited rsync filtering for now (tutorial notebooks deploy from multiple repos, need re-organizing the file layout)

  So the script has room to grow.  I see it as a generic solution to the repeated problem "take files from various git repos and deploy them somewhere automatically".  If we need to deploy another repo, juste write a new config file, stop writing boilerplate code again.

  Minor unrelated change in this PR:
  * README update to reference the new birdhouse-deploy-ouranos.
  * Make sourcing the various pre-configured cronjob backward-compat with older version of the repo where those cronjob did not exist yet.

[1.11.3](https://github.com/bird-house/birdhouse-deploy/tree/1.11.3) (2020-09-28)
------------------------------------------------------------------------------------------------------------------
- `jupyter`: new build for new xclim with fix for missing clisops dependency

  Matching PR to deploy new Jupyter env from PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/52 (commit https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/commit/18c8397ff30c9ba4b9f56896df4c898c7e9a356e).

  Deployed to https://medus.ouranos.ca/jupyter/ for testing.

  Relevant changes:
  ```diff
  >   - clisops=0.3.1=pyh32f6830_1

  <     - xclim==0.19.0
  >   - xclim=0.20.0=py_0

  <   - xarray=0.16.0py_0
  >   - xarray=0.16.1=py_0

  <   - dask=2.26.0=py_0
  >   - dask=2.27.0=py_0

  <   - fiona=1.8.13=py37h0492a4a_1
  >   - fiona=1.8.17=py37ha3d844c_0

  <   - gdal=3.0.4=py37h4b180d9_10
  >   - gdal=3.1.2=py37h518339e_2

  <   - jupyter_server=0.1.1=py37_0
  >   - jupyter_server=1.0.1=py37hc8dfbb8_0

  >     - jupyternotify==0.1.15

  >     - pytest-tornasync==0.6.0.post2
  ```

  See PR above for full changes.

[1.11.2](https://github.com/bird-house/birdhouse-deploy/tree/1.11.2) (2020-09-15)
------------------------------------------------------------------------------------------------------------------
- Auto-renew LetsEncrypt SSL certificate.

  Auto-renew LetsEncrypt SSL certificate leveraging the cron jobs of the "scheduler" component.  Meaning this feature is self-contained in the PAVICS stack, no dependency on the host's cron jobs.

  Default behavior is to attempt renewal everyday.  `certbot` client in `renew` mode will not hit LetsEncrypt server if renewal is not allowed (not within 1 month of expiry) so this should not put too much stress on LetsEncrypt server.  However, this gives us 30 retry opportunities (1 month) if something is wrong on the first try.

  All configs are centralized in `env.local`, easing reproducibility on multiple deployments of PAVICS and following infra-as-code.

  User can still perform the renewal manually by calling `certbotwrapper` directly. User is not forced to enable the "scheduler" component but will miss out on the automatic renewal.

  Documentation for activating this automatic renewal is in `env.local.example`.

  See `vagrant-utils/configure-pavics.sh` for how it's being used for real in a Vagrant box.

  Logs (`/var/log/PAVICS/renew_letsencrypt_ssl.log`) when no renewal is necessary, proxy down time less than 1 minute:
  [certbot-renew-no-ops.txt](https://github.com/bird-house/birdhouse-deploy/files/5209376/certbot-renew-no-ops.txt)
  ```
  ==========
  certbotwrapper START_TIME=2020-09-11T01:20:02+0000
  + realpath /vagrant/birdhouse/deployment/certbotwrapper
  + THIS_FILE=/vagrant/birdhouse/deployment/certbotwrapper
  + dirname /vagrant/birdhouse/deployment/certbotwrapper
  + THIS_DIR=/vagrant/birdhouse/deployment
  + pwd
  + SAVED_PWD=/
  + . /vagrant/birdhouse/deployment/../default.env
  + export 'DOCKER_NOTEBOOK_IMAGE=pavics/workflow-tests:200803'
  + export 'FINCH_IMAGE=birdhouse/finch:version-0.5.2'
  + export 'THREDDS_IMAGE=unidata/thredds-docker:4.6.14'
  + export 'JUPYTERHUB_USER_DATA_DIR=/data/jupyterhub_user_data'
  + export 'JUPYTER_DEMO_USER=demo'
  + export 'JUPYTER_DEMO_USER_MEM_LIMIT=2G'
  + export 'JUPYTER_DEMO_USER_CPU_LIMIT=0.5'
  + export 'JUPYTER_LOGIN_BANNER_TOP_SECTION='
  + export 'JUPYTER_LOGIN_BANNER_BOTTOM_SECTION='
  + export 'CANARIE_MONITORING_EXTRA_CONF_DIR=/conf.d'
  + export 'THREDDS_ORGANIZATION=Birdhouse'
  + export 'MAGPIE_DB_NAME=magpiedb'
  + export 'VERIFY_SSL=true'
  + export 'AUTODEPLOY_DEPLOY_KEY_ROOT_DIR=/root/.ssh'
  + export 'AUTODEPLOY_PLATFORM_FREQUENCY=7 5 * * *'
  + export 'AUTODEPLOY_NOTEBOOK_FREQUENCY=@hourly'
  + ENV_LOCAL_FILE=/vagrant/birdhouse/deployment/../env.local
  + set +x
  + CERT_DOMAIN=
  + '[' -z  ]
  + CERT_DOMAIN=lvupavicsmaster.ouranos.ca
  + '[' '!' -z 1 ]
  + cd /vagrant/birdhouse/deployment/..
  + docker stop proxy
  proxy
  + cd /
  + CERTBOT_OPTS=
  + '[' '!' -z 1 ]
  + CERTBOT_OPTS=renew
  + docker run --rm --name certbot -v /etc/letsencrypt:/etc/letsencrypt -v /var/lib/letsencrypt:/var/lib/letsencrypt -v /var/log/letsencrypt:/var/log/letsencrypt -p 443:443 -p 80:80 certbot/certbot:v1.3.0 renew
  Saving debug log to /var/log/letsencrypt/letsencrypt.log

  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  Processing /etc/letsencrypt/renewal/lvupavicsmaster.ouranos.ca.conf
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  Cert not yet due for renewal

  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  The following certs are not due for renewal yet:
    /etc/letsencrypt/live/lvupavicsmaster.ouranos.ca/fullchain.pem expires on 2020-11-02 (skipped)
  No renewals were attempted.
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  + RC=0
  + '[' '!' -z 1 ]
  + TMP_SSL_CERT=/tmp/tmp_certbotwrapper_ssl_cert.pem
  + CERTPATH=/etc/letsencrypt/live/lvupavicsmaster.ouranos.ca
  + cd /vagrant/birdhouse/deployment/..
  + docker run --rm --name copy_cert -v /etc/letsencrypt:/etc/letsencrypt bash cat /etc/letsencrypt/live/lvupavicsmaster.ouranos.ca/fullchain.pem /etc/letsencrypt/live/lvupavicsmaster.ouranos.ca/privkey.pem
  + diff /home/vagrant/certkey.pem /tmp/tmp_certbotwrapper_ssl_cert.pem
  + rm -v /tmp/tmp_certbotwrapper_ssl_cert.pem
  removed '/tmp/tmp_certbotwrapper_ssl_cert.pem'
  + '[' -z  ]
  + docker start proxy
  proxy
  + cd /
  + set +x

  certbotwrapper finished START_TIME=2020-09-11T01:20:02+0000
  certbotwrapper finished   END_TIME=2020-09-11T01:20:21+0000
  ```

  Logs when renewal is needed but failed due to firewall, `certbot` adds a random delay so proxy could be down up to 10 mins:
  [certbot-renew-error.txt](https://github.com/bird-house/birdhouse-deploy/files/5209403/certbot-renew-error.txt)

  ```
  ==========
  certbotwrapper START_TIME=2020-09-11T13:00:04+0000
  + realpath /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/certbotwrapper
  + THIS_FILE=/home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/certbotwrapper
  + dirname /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/certbotwrapper
  + THIS_DIR=/home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment
  + pwd
  + SAVED_PWD=/
  + . /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/../default.env
  + export 'DOCKER_NOTEBOOK_IMAGE=pavics/workflow-tests:200803'
  + export 'FINCH_IMAGE=birdhouse/finch:version-0.5.2'
  + export 'THREDDS_IMAGE=unidata/thredds-docker:4.6.14'
  + export 'JUPYTERHUB_USER_DATA_DIR=/data/jupyterhub_user_data'
  + export 'JUPYTER_DEMO_USER=demo'
  + export 'JUPYTER_DEMO_USER_MEM_LIMIT=2G'
  + export 'JUPYTER_DEMO_USER_CPU_LIMIT=0.5'
  + export 'JUPYTER_LOGIN_BANNER_TOP_SECTION='
  + export 'JUPYTER_LOGIN_BANNER_BOTTOM_SECTION='
  + export 'CANARIE_MONITORING_EXTRA_CONF_DIR=/conf.d'
  + export 'THREDDS_ORGANIZATION=Birdhouse'
  + export 'MAGPIE_DB_NAME=magpiedb'
  + export 'VERIFY_SSL=true'
  + export 'AUTODEPLOY_DEPLOY_KEY_ROOT_DIR=/root/.ssh'
  + export 'AUTODEPLOY_PLATFORM_FREQUENCY=7 5 * * *'
  + export 'AUTODEPLOY_NOTEBOOK_FREQUENCY=@hourly'
  + ENV_LOCAL_FILE=/home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/../env.local
  + set +x
  + CERT_DOMAIN=
  + '[' -z  ]
  + CERT_DOMAIN=medus.ouranos.ca
  + '[' '!' -z 1 ]
  + cd /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/..
  + docker stop proxy
  proxy
  + cd /
  + CERTBOT_OPTS=
  + '[' '!' -z 1 ]
  + CERTBOT_OPTS=renew
  + docker run --rm --name certbot -v /etc/letsencrypt:/etc/letsencrypt -v /var/lib/letsencrypt:/var/lib/letsencrypt -v /var/log/letsencrypt:/var/log/letsencrypt -p 443:443 -p 80:80 certbot/certbot:v1.3.0 renew
  Saving debug log to /var/log/letsencrypt/letsencrypt.log

  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  Processing /etc/letsencrypt/renewal/medus.ouranos.ca.conf
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  Cert is due for renewal, auto-renewing...
  Non-interactive renewal: random delay of 10.77459918236335 seconds
  Plugins selected: Authenticator standalone, Installer None
  Renewing an existing certificate
  Performing the following challenges:
  http-01 challenge for medus.ouranos.ca
  Waiting for verification...
  Challenge failed for domain medus.ouranos.ca
  http-01 challenge for medus.ouranos.ca
  Cleaning up challenges
  Attempting to renew cert (medus.ouranos.ca) from /etc/letsencrypt/renewal/medus.ouranos.ca.conf produced an unexpected error: Some challenges have failed.. Skipping.
  All renewal attempts failed. The following certs could not be renewed:
    /etc/letsencrypt/live/medus.ouranos.ca/fullchain.pem (failure)

  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  All renewal attempts failed. The following certs could not be renewed:
    /etc/letsencrypt/live/medus.ouranos.ca/fullchain.pem (failure)
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  1 renew failure(s), 0 parse failure(s)
  IMPORTANT NOTES:
   - The following errors were reported by the server:

     Domain: medus.ouranos.ca
     Type:   connection
     Detail: Fetching
     http://medus.ouranos.ca/.well-known/acme-challenge/F-_TzoOMcgoo5WC9FQvi_QdKuoqdsrQFa7MR2bEdnJE:
     Timeout during connect (likely firewall problem)

     To fix these errors, please make sure that your domain name was
     entered correctly and the DNS A/AAAA record(s) for that domain
     contain(s) the right IP address. Additionally, please check that
     your computer has a publicly routable IP address and that no
     firewalls are preventing the server from communicating with the
     client. If you're using the webroot plugin, you should also verify
     that you are serving files from the webroot path you provided.
  + RC=1
  + '[' '!' -z 1 ]
  + TMP_SSL_CERT=/tmp/tmp_certbotwrapper_ssl_cert.pem
  + CERTPATH=/etc/letsencrypt/live/medus.ouranos.ca
  + cd /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/..
  + docker run --rm --name copy_cert -v /etc/letsencrypt:/etc/letsencrypt bash cat /etc/letsencrypt/live/medus.ouranos.ca/fullchain.pem /etc/letsencrypt/live/medus.ouranos.ca/privkey.pem
  + diff /etc/letsencrypt/live/medus.ouranos.ca/certkey.pem /tmp/tmp_certbotwrapper_ssl_cert.pem
  + rm -v /tmp/tmp_certbotwrapper_ssl_cert.pem
  removed '/tmp/tmp_certbotwrapper_ssl_cert.pem'
  + '[' -z  ]
  + docker start proxy
  proxy
  + cd /
  + set +x

  certbotwrapper finished START_TIME=2020-09-11T13:00:04+0000
  certbotwrapper finished   END_TIME=2020-09-11T13:00:49+0000
  ```

  Logs when renewal is successful, again proxy could be down up to 10 mins due to random delay by `certbot` client:
  [certbot-renew-success-in-2-run-after-file-copy-fix.txt](https://github.com/bird-house/birdhouse-deploy/files/5209924/certbot-renew-success-in-2-run-after-file-copy-fix.txt)

  ```
  ==========
  certbotwrapper START_TIME=2020-09-11T13:10:04+0000
  + realpath /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/certbotwrapper
  + THIS_FILE=/home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/certbotwrapper
  + dirname /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/certbotwrapper
  + THIS_DIR=/home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment
  + pwd
  + SAVED_PWD=/
  + . /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/../default.env
  + export 'DOCKER_NOTEBOOK_IMAGE=pavics/workflow-tests:200803'
  + export 'FINCH_IMAGE=birdhouse/finch:version-0.5.2'
  + export 'THREDDS_IMAGE=unidata/thredds-docker:4.6.14'
  + export 'JUPYTERHUB_USER_DATA_DIR=/data/jupyterhub_user_data'
  + export 'JUPYTER_DEMO_USER=demo'
  + export 'JUPYTER_DEMO_USER_MEM_LIMIT=2G'
  + export 'JUPYTER_DEMO_USER_CPU_LIMIT=0.5'
  + export 'JUPYTER_LOGIN_BANNER_TOP_SECTION='
  + export 'JUPYTER_LOGIN_BANNER_BOTTOM_SECTION='
  + export 'CANARIE_MONITORING_EXTRA_CONF_DIR=/conf.d'
  + export 'THREDDS_ORGANIZATION=Birdhouse'
  + export 'MAGPIE_DB_NAME=magpiedb'
  + export 'VERIFY_SSL=true'
  + export 'AUTODEPLOY_DEPLOY_KEY_ROOT_DIR=/root/.ssh'
  + export 'AUTODEPLOY_PLATFORM_FREQUENCY=7 5 * * *'
  + export 'AUTODEPLOY_NOTEBOOK_FREQUENCY=@hourly'
  + ENV_LOCAL_FILE=/home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/../env.local
  + set +x
  + CERT_DOMAIN=
  + '[' -z  ]
  + CERT_DOMAIN=medus.ouranos.ca
  + '[' '!' -z 1 ]
  + cd /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/..
  + docker stop proxy
  proxy
  + cd /
  + CERTBOT_OPTS=
  + '[' '!' -z 1 ]
  + CERTBOT_OPTS=renew
  + docker run --rm --name certbot -v /etc/letsencrypt:/etc/letsencrypt -v /var/lib/letsencrypt:/var/lib/letsencrypt -v /var/log/letsencrypt:/var/log/letsencrypt -p 443:443 -p 80:80 certbot/certbot:v1.3.0 renew
  Saving debug log to /var/log/letsencrypt/letsencrypt.log

  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  Processing /etc/letsencrypt/renewal/medus.ouranos.ca.conf
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  Cert is due for renewal, auto-renewing...
  Non-interactive renewal: random delay of 459.45712705256506 seconds
  Plugins selected: Authenticator standalone, Installer None
  Renewing an existing certificate
  Performing the following challenges:
  http-01 challenge for medus.ouranos.ca
  Waiting for verification...
  Cleaning up challenges

  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  new certificate deployed without reload, fullchain is
  /etc/letsencrypt/live/medus.ouranos.ca/fullchain.pem
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  Congratulations, all renewals succeeded. The following certs have been renewed:
    /etc/letsencrypt/live/medus.ouranos.ca/fullchain.pem (success)
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  + RC=0
  + '[' '!' -z 1 ]
  + TMP_SSL_CERT=/tmp/tmp_certbotwrapper_ssl_cert.pem
  + CERTPATH=/etc/letsencrypt/live/medus.ouranos.ca
  + cd /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/..
  + docker run --rm --name copy_cert -v /etc/letsencrypt:/etc/letsencrypt bash cat /etc/letsencrypt/live/medus.ouranos.ca/fullchain.pem /etc/letsencrypt/live/medus.ouranos.ca/privkey.pem
  + diff /etc/letsencrypt/live/medus.ouranos.ca/certkey.pem /tmp/tmp_certbotwrapper_ssl_cert.pem
  --- /etc/letsencrypt/live/medus.ouranos.ca/certkey.pem
  +++ /tmp/tmp_certbotwrapper_ssl_cert.pem
  @@ -1,33 +1,33 @@
   -----BEGIN CERTIFICATE-----

  REMOVED for Privacy.

   -----END PRIVATE KEY-----
  + '[' 0 -eq 0 ]
  + cp -v /tmp/tmp_certbotwrapper_ssl_cert.pem /etc/letsencrypt/live/medus.ouranos.ca/certkey.pem
  cp: can't create '/etc/letsencrypt/live/medus.ouranos.ca/certkey.pem': File exists
  + rm -v /tmp/tmp_certbotwrapper_ssl_cert.pem
  removed '/tmp/tmp_certbotwrapper_ssl_cert.pem'
  + '[' -z  ]
  + docker start proxy
  proxy
  + cd /
  + set +x

  certbotwrapper finished START_TIME=2020-09-11T13:10:04+0000
  certbotwrapper finished   END_TIME=2020-09-11T13:18:10+0000
  ==========
  certbotwrapper START_TIME=2020-09-11T15:00:06+0000
  + realpath /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/certbotwrapper
  + THIS_FILE=/home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/certbotwrapper
  + dirname /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/certbotwrapper
  + THIS_DIR=/home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment
  + pwd
  + SAVED_PWD=/
  + . /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/../default.env
  + export 'DOCKER_NOTEBOOK_IMAGE=pavics/workflow-tests:200803'
  + export 'FINCH_IMAGE=birdhouse/finch:version-0.5.2'
  + export 'THREDDS_IMAGE=unidata/thredds-docker:4.6.14'
  + export 'JUPYTERHUB_USER_DATA_DIR=/data/jupyterhub_user_data'
  + export 'JUPYTER_DEMO_USER=demo'
  + export 'JUPYTER_DEMO_USER_MEM_LIMIT=2G'
  + export 'JUPYTER_DEMO_USER_CPU_LIMIT=0.5'
  + export 'JUPYTER_LOGIN_BANNER_TOP_SECTION='
  + export 'JUPYTER_LOGIN_BANNER_BOTTOM_SECTION='
  + export 'CANARIE_MONITORING_EXTRA_CONF_DIR=/conf.d'
  + export 'THREDDS_ORGANIZATION=Birdhouse'
  + export 'MAGPIE_DB_NAME=magpiedb'
  + export 'VERIFY_SSL=true'
  + export 'AUTODEPLOY_DEPLOY_KEY_ROOT_DIR=/root/.ssh'
  + export 'AUTODEPLOY_PLATFORM_FREQUENCY=7 5 * * *'
  + export 'AUTODEPLOY_NOTEBOOK_FREQUENCY=@hourly'
  + ENV_LOCAL_FILE=/home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/../env.local
  + set +x
  + CERT_DOMAIN=
  + '[' -z  ]
  + CERT_DOMAIN=medus.ouranos.ca
  + '[' '!' -z 1 ]
  + cd /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/..
  + docker stop proxy
  proxy
  + cd /
  + CERTBOT_OPTS=
  + '[' '!' -z 1 ]
  + CERTBOT_OPTS=renew
  + docker run --rm --name certbot -v /etc/letsencrypt:/etc/letsencrypt -v /var/lib/letsencrypt:/var/lib/letsencrypt -v /var/log/letsencrypt:/var/log/letsencrypt -p 443:443 -p 80:80 certbot/certbot:v1.3.0 renew
  Saving debug log to /var/log/letsencrypt/letsencrypt.log

  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  Processing /etc/letsencrypt/renewal/medus.ouranos.ca.conf
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  Cert not yet due for renewal

  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  The following certs are not due for renewal yet:
    /etc/letsencrypt/live/medus.ouranos.ca/fullchain.pem expires on 2020-12-10 (skipped)
  No renewals were attempted.
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  + RC=0
  + '[' '!' -z 1 ]
  + TMP_SSL_CERT=/tmp/tmp_certbotwrapper_ssl_cert.pem
  + CERTPATH=/etc/letsencrypt/live/medus.ouranos.ca
  + cd /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/..
  + docker run --rm --name copy_cert -v /etc/letsencrypt:/etc/letsencrypt bash cat /etc/letsencrypt/live/medus.ouranos.ca/fullchain.pem /etc/letsencrypt/live/medus.ouranos.ca/privkey.pem
  + diff /etc/letsencrypt/live/medus.ouranos.ca/certkey.pem /tmp/tmp_certbotwrapper_ssl_cert.pem
  --- /etc/letsencrypt/live/medus.ouranos.ca/certkey.pem
  +++ /tmp/tmp_certbotwrapper_ssl_cert.pem
  @@ -1,33 +1,33 @@
   -----BEGIN CERTIFICATE-----

  REMOVED for Privacy.

   -----END PRIVATE KEY-----
  + '[' 0 -eq 0 ]
  + cp -v /tmp/tmp_certbotwrapper_ssl_cert.pem /etc/letsencrypt/live/medus.ouranos.ca/certkey.pem
  '/tmp/tmp_certbotwrapper_ssl_cert.pem' -> '/etc/letsencrypt/live/medus.ouranos.ca/certkey.pem'
  + rm -v /tmp/tmp_certbotwrapper_ssl_cert.pem
  removed '/tmp/tmp_certbotwrapper_ssl_cert.pem'
  + '[' -z  ]
  + docker start proxy
  proxy
  + cd /
  + set +x

  certbotwrapper finished START_TIME=2020-09-11T15:00:06+0000
  certbotwrapper finished   END_TIME=2020-09-11T15:00:31+0000
  ```

[1.11.1](https://github.com/bird-house/birdhouse-deploy/tree/1.11.1) (2020-09-15)
------------------------------------------------------------------------------------------------------------------
- `jupyter`: new updated image with new handcalcs package

  Matching PR to deploy the new jupyter image to PAVICS.

  See PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/50
  (commit https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/commit/02333bfa11931f4a0b7c9607b88904bd063bed70)
  that built the new image with the detailed change vs the previous image.

  Add handcalcs https://github.com/connorferster/handcalcs/ and unpin hvplot
  since pinning did not solve violin plot issue, see this comment
  https://github.com/bird-house/birdhouse-deploy/pull/63#issuecomment-668270608

  Successful Jenkins build
  http://jenkins.ouranos.ca/job/PAVICS-e2e-workflow-tests/job/periodic-rebuild-and-add-handcalcs/1/console

  Noticeable changes:
  ```diff
  >     - handcalcs==0.8.1

  <     - xclim==0.18.0
  >     - xclim==0.19.0

  <   - hvplot=0.5.2=py_0
  >   - hvplot=0.6.0=pyh9f0ad1d_0

  <   - dask=2.22.0=py_0
  >   - dask=2.26.0=py_0

  <   - bokeh=2.1.1=py37hc8dfbb8_0
  >   - bokeh=2.2.1=py37hc8dfbb8_0

  <   - numba=0.50.1=py37h0da4684_1
  >   - numba=0.51.2=py37h9fdb41a_0
  ```

[1.11.0](https://github.com/bird-house/birdhouse-deploy/tree/1.11.0) (2020-08-25)
------------------------------------------------------------------------------------------------------------------
- Improved plugable component architecture.

  Before this PR, components needing default values, needing template variable substitution, needing to execute commands pre and post `docker-compose up` are hardcoding their needs directly to the "core" system, basically "leaking" their requirements out even when they are not activated (fixes https://github.com/bird-house/birdhouse-deploy/issues/62).

  This PR provides true plugable architecture for the components so they can provide all their needs without having to modify the code of the "core" system.

  All the components (monitoring, generic_bird, emu, testthredds) are modified to leverage the new plugable architecture, with additional customizations given it is cleaner/easier to have default configuration values.

  Given this PR both changes the architecture and modify many components at the same time, it is best to read each commit separately to easier understand which code change belongs to which "goal".

  Deployed here https://lvupavicsmaster.ouranos.ca with all the impacted components activated to test the change:
  * Canarie: https://lvupavicsmaster.ouranos.ca/canarie/node/service/status
  * Generic bird (using Finch): https://lvupavicsmaster.ouranos.ca/twitcher/ows/proxy/generic_bird?service=WPS&version=1.0.0&request=GetCapabilities
  * Emu: https://lvupavicsmaster.ouranos.ca/twitcher/ows/proxy/emu?service=WPS&version=1.0.0&request=GetCapabilities
  * Test Thredds: https://lvupavicsmaster.ouranos.ca/testthredds/catalog.html
  * Prometheus: http://lvupavicsmaster.ouranos.ca:9090/alerts
  * AlertManager: http://lvupavicsmaster.ouranos.ca:9093/
  * Grafana dashboard: http://lvupavicsmaster.ouranos.ca:3001/d/pf6xQMWGz/docker-and-system-monitoring?orgId=1&refresh=5m

[1.10.4](https://github.com/bird-house/birdhouse-deploy/tree/1.10.4) (2020-08-05)
------------------------------------------------------------------------------------------------------------------
- `jupyter`: new update image with hvplot pinned to older version for violin plot

  See PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/48 (commit https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/commit/4ad6ba6fa2a4ecf6d5d78e0602b39202307bcb76) for more detailed info.

  Deployed to Medus for testing (as regular PAVICS image, not the devel image).  @aulemahal reported back that violin plot still do not work even with the old hvplot pinned in this image.

  I'll release this image as-is since violin plot is also not working in the previous image that had hvplot 0.6.0 so no new regression there.  Will unpin hvplot on next image build because pinning it did not fix violin plot (probably interference from other newer packages in this build).

  Noticeable changes:
  ```diff
  <   - hvplot=0.6.0=pyh9f0ad1d_0
  >   - hvplot=0.5.2=py_0

  <   - dask=2.20.0=py_0
  >   - dask=2.22.0=py_0

  <   - geopandas=0.8.0=py_1
  >   - geopandas=0.8.1=py_0

  <   - pandas=1.0.5=py37h0da4684_0
  >   - pandas=1.1.0=py37h3340039_0

  <   - matplotlib=3.2.2=1
  >   - matplotlib=3.3.0=1

  <   - numpy=1.18.5=py37h8960a57_0
  >   - numpy=1.19.1=py37h8960a57_0

  <   - cryptography=2.9.2=py37hb09aad4_0
  >   - cryptography=3.0=py37hb09aad4_0

  <   - python=3.7.6=h8356626_5_cpython
  >   - python=3.7.8=h6f2ec95_1_cpython

  <   - nbval=0.9.5=py_0
  >   - nbval=0.9.6=pyh9f0ad1d_0

  <   - pytest=5.4.3=py37hc8dfbb8_0
  >   - pytest=6.0.1=py37hc8dfbb8_0
  ```

[1.10.3](https://github.com/bird-house/birdhouse-deploy/tree/1.10.3) (2020-07-21)
------------------------------------------------------------------------------------------------------------------
- `proxy`: increase timeout for reading a response from the proxied server

  Fixes https://github.com/Ouranosinc/raven/issues/286

  "there seems to be a problem with the size of the ncml and the timeout
  if I use more than 10-12 years as the historical data. I get a :
  "Netcdf: DAP failure" error if I use too many years."

  ```
  ________________________________________________________ TestBiasCorrect.test_bias_correction ________________________________________________________
  Traceback (most recent call last):
    File "/zstore/repos/raven/tests/test_bias_correction.py", line 20, in test_bias_correction
      ds = (xr.open_dataset(hist_data).sel(lat=slice(lat + 1, lat - 1),lon=slice(lon - 1, lon + 1), time=slice(dt.datetime(1991,1,1), dt.datetime(2010,12,31))).mean(dim={"lat", "lon"}, keep_attrs=True))
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/xarray/core/common.py", line 84, in wrapped_func
      func, dim, skipna=skipna, numeric_only=numeric_only, **kwargs
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/xarray/core/dataset.py", line 4313, in reduce
      **kwargs,
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/xarray/core/variable.py", line 1586, in reduce
      input_data = self.data if allow_lazy else self.values
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/xarray/core/variable.py", line 349, in data
      return self.values
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/xarray/core/variable.py", line 457, in values
      return _as_array_or_item(self._data)
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/xarray/core/variable.py", line 260, in _as_array_or_item
      data = np.asarray(data)
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/numpy/core/_asarray.py", line 83, in asarray
      return array(a, dtype, copy=False, order=order)
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/xarray/core/indexing.py", line 677, in __array__
      self._ensure_cached()
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/xarray/core/indexing.py", line 674, in _ensure_cached
      self.array = NumpyIndexingAdapter(np.asarray(self.array))
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/numpy/core/_asarray.py", line 83, in asarray
      return array(a, dtype, copy=False, order=order)
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/xarray/core/indexing.py", line 653, in __array__
      return np.asarray(self.array, dtype=dtype)
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/numpy/core/_asarray.py", line 83, in asarray
      return array(a, dtype, copy=False, order=order)
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/xarray/core/indexing.py", line 557, in __array__
      return np.asarray(array[self.key], dtype=None)
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/xarray/backends/netCDF4_.py", line 73, in __getitem__
      key, self.shape, indexing.IndexingSupport.OUTER, self._getitem
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/xarray/core/indexing.py", line 837, in explicit_indexing_adapter
      result = raw_indexing_method(raw_key.tuple)
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/xarray/backends/netCDF4_.py", line 85, in _getitem
      array = getitem(original_array, key)
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/xarray/backends/common.py", line 54, in robust_getitem
      return array[key]
    File "netCDF4/_netCDF4.pyx", line 4408, in netCDF4._netCDF4.Variable.__getitem__
    File "netCDF4/_netCDF4.pyx", line 5352, in netCDF4._netCDF4.Variable._get
    File "netCDF4/_netCDF4.pyx", line 1887, in netCDF4._netCDF4._ensure_nc_success
  RuntimeError: NetCDF: DAP failure
  ```

[1.10.2](https://github.com/bird-house/birdhouse-deploy/tree/1.10.2) (2020-07-18)
------------------------------------------------------------------------------------------------------------------
- `jupyter`: new build and add nc-time-axis

  Corresponding change to deploy the new Jupyter env to PAVICS.

  Noticeable changes:
  ```diff
  <   - dask=2.17.2=py_0
  >   - dask=2.20.0=py_0

  >   - nc-time-axis=1.2.0=py_1

  <   - xarray=0.15.1=py_0
  >   - xarray=0.16.0=py_0

  <     - xclim==0.17.0
  >     - xclim==0.18.0
  ```

  See PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/47
  (commit
  https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/commit/4e03a674930f0974e13724940eee7a608c2158c0)
  for more info.

[1.10.1](https://github.com/bird-house/birdhouse-deploy/tree/1.10.1) (2020-07-11)
------------------------------------------------------------------------------------------------------------------
- Monitoring: add alert rules and alert handling (deduplicate, group, route, silence, inhibit).

  This is a follow up to the previous PR https://github.com/bird-house/birdhouse-deploy/pull/56 that added the monitoring itself.

  Added cAdvisor and Node-exporter collection of alert rules found here https://awesome-prometheus-alerts.grep.to/rules with a few fixing because of errors in the rules and tweaking to reduce false positive alarms (see list of commits).  Great collection of sample of ready-made rules to hit the ground running and learn PromML query language on the way.

  ![2020-07-08-090953_474x1490_scrot](https://user-images.githubusercontent.com/11966697/86926000-8b086c80-c0ff-11ea-92d0-6f5ccfe2b8e1.png)

  Added Alertmanager to handle the alerts (deduplicate, group, route, silence, inhibit).  Currently the only notification route configured is email but Alertmanager is able to route alerts to Slack and any generic services accepting webhooks.

  ![2020-07-08-091150_1099x669_scrot](https://user-images.githubusercontent.com/11966697/86926213-cd31ae00-c0ff-11ea-8b2a-d33803ad3d5d.png)

  ![2020-07-08-091302_1102x1122_scrot](https://user-images.githubusercontent.com/11966697/86926276-dc186080-c0ff-11ea-9377-bda03b69640e.png)

  This is an initial attempt at alerting.  There are several ways to tweak the system without changing the code:

  * To add more Prometheus alert rules, volume-mount more *.rules files to the prometheus container.
  * To disable existing Prometheus alert rules, add more Alertmanager inhibition rules using `ALERTMANAGER_EXTRA_INHIBITION` via `env.local` file.
  * Other possible Alertmanager configs via `env.local`: `ALERTMANAGER_EXTRA_GLOBAL, ALERTMANAGER_EXTRA_ROUTES, ALERTMANAGER_EXTRA_RECEIVERS`.

  What more could be done after this initial attempt:

  * Possibly add more graphs to Grafana dashboard since we have more alerts on metrics that we do not have matching Grafana graph. Graphs are useful for historical trends and correlation with other metrics, so not required if we do not need trends and correlation.

  * Only basic metrics are being collected currently.  We could collect more useful metrics like SMART status and alert when a disk is failing.

  * The autodeploy mechanism can hook into this monitoring system to report pass/fail status and execution duration, with alerting for problems.  Then we can also correlate any CPU, memory, disk I/O spike, when the autodeploy runs and have a trace of previous autodeploy executions.

  I had to test these alerts directly in prod to tweak for less false positive alert and to debug not working rules to ensure they work on prod so these changes are already in prod !   This also test the SMTP server on the network.

  See rules on Prometheus side: http://pavics.ouranos.ca:9090/rules, http://medus.ouranos.ca:9090/rules

  Manage alerts on Alertmanager side: http://pavics.ouranos.ca:9093/#/alerts, http://medus.ouranos.ca:9093/#/alerts

  Part of issue https://github.com/bird-house/birdhouse-deploy/issues/12

[1.10.0](https://github.com/bird-house/birdhouse-deploy/tree/1.10.0) (2020-07-02)
------------------------------------------------------------------------------------------------------------------
- Monitoring for host and each docker container.

  ![Screenshot_2020-06-19 Docker and system monitoring - Grafana](https://user-images.githubusercontent.com/11966697/85206384-c7f6f580-b2ef-11ea-848d-46490eb95886.png)

  For host, using Node-exporter to collect metrics:
  * uptime
  * number of container
  * used disk space
  * used memory, available memory, used swap memory
  * load
  * cpu usage
  * in and out network traffic
  * disk I/O

  For each container, using cAdvisor to collect metrics:
  * in and out network traffic
  * cpu usage
  * memory and swap memory usage
  * disk usage

  Useful visualisation features:
  * zoom in one graph and all other graph update to match the same "time range" so we can correlate event
  * view each graph independently for more details
  * mouse over each data point will show value at that moment

  Prometheus is used as the time series DB and Grafana is used as the visualization dashboard.

  Node-exporter, cAdvisor and Prometheus are exposed so another Prometheus on the network can also scrape those same metrics and perform other analysis if required.

  The whole monitoring stack is a separate component so user is not forced to enable it if there is already another monitoring system in place.  Enabling this monitoring stack is done via `env.local` file, like all other components.

  The Grafana dashboard is taken from https://grafana.com/grafana/dashboards/893 with many fixes (see commits) since most of the metric names have changed over time.  Still it was much quicker to hit the ground running than learning the Prometheus query language and Grafana visualization options from scratch.  Not counting there are lots of metrics exposed, had to filter out which one are relevant to graph.  So starting from a broken dashboard was still a big win.  Grafana has a big collection of existing but probably un-maintained dashboards we can leverage.

  So this is a first draft for monitoring.  Many things I am not sure or will need tweaking or is missing:
  * Probably have to add more metrics or remove some that might be irrelevant, with time we will see.
  * Probably will have to tweak the scrape interval and the retention time, to keep the disk storage requirement reasonable, again we'll see with time.
  * Missing alerting.  With all the pretty graph, we are not going to look at them all day, we need some kind of alerting mechanism.

  Test system: http://lvupavicsmaster.ouranos.ca:3001/d/pf6xQMWGz/docker-and-system-monitoring?orgId=1&refresh=5m, user: admin, passwd: the default passwd

  Also tested on Medus: http://medus.ouranos.ca:3001/d/pf6xQMWGz/docker-and-system-monitoring?orgId=1&refresh=5m (on Medus had to perform full yum update to get new kernel and new docker engine for cAdvisor to work properly).

  Part of issue https://github.com/bird-house/birdhouse-deploy/issues/12

[1.9.6](https://github.com/bird-house/birdhouse-deploy/tree/1.9.6) (2020-06-15)
------------------------------------------------------------------------------------------------------------------
- flyingpigeon: update to version 1.6

  Deploy the new Flyingpigeon 1.6 on PAVICS.

  Has been deployed to Medus test environment.

  flyingpigeon changelog from release commit
  https://github.com/bird-house/flyingpigeon/commit/a6f54ed0c20919485c2420295729e30f914cfa15
  (PR https://github.com/bird-house/flyingpigeon/pull/332)

  1.6 (2020-06-10)
  ================
  * remove eggshell dependency
  * notebooks are part of the test suite
  * improved plot processes
  * remove mosaic option for subset processes
  * polygon subset processes files separately instead of an entire data-set at once
  * multiple outputs listed in Metalink output
  * update pywps to 4.2.3
  * use cruft to keep up-to-date with the cookie-cutter template

[1.9.5](https://github.com/bird-house/birdhouse-deploy/tree/1.9.5) (2020-06-12)
------------------------------------------------------------------------------------------------------------------
- `jupyter`: new image for additional plugins

  Matching PR to deploy the new Jupyter image to PAVICS.

  Added:

  * https://github.com/hadim/jupyter-archive
    Download entire folder as archive.

  * https://blog.jupyter.org/a-visual-debugger-for-jupyter-914e61716559

  * https://github.com/plotly/jupyter-dash
    Develop Plotly Dash apps interactively from within Jupyter environments.

  Noticeable changes:
  ```diff
  >   - jupyter-archive=0.6.2=py_0
  >   - jupyter-dash=0.2.1.post1=py_0

  <   - owslib=0.19.2=py_1
  >   - owslib=0.20.0=py_0

  >   - xeus-python=0.7.1=py37h99015e2_1
  ```

  See PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/46 (commit
  https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/commit/441edde3b381eff7ce82e5a171323b31196553be)
  for more info.

[1.9.4](https://github.com/bird-house/birdhouse-deploy/tree/1.9.4) (2020-06-03)
------------------------------------------------------------------------------------------------------------------
- `jupyter`: updated build and fix for pyviz jupyterlab extension

  @tlogan2000 matching PR to actually deploy the new Jupyter env to PAVICS.

  Noticeable changes:

  ```diff
  <   - dask=2.15.0=py_0
  >   - dask=2.17.2=py_0

  <     - xclim==0.16.0
  >     - xclim==0.17.0
  ```

  See PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/45 (commit
  https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/commit/a93f3b50cc6d108638d232fe9465b2f060e21314)
  for more info.

[1.9.3](https://github.com/bird-house/birdhouse-deploy/tree/1.9.3) (2020-05-07)
------------------------------------------------------------------------------------------------------------------
- `jupyter`: update to pavics/workflow-tests:200507

  Raven PR https://github.com/Ouranosinc/raven/pull/266 (commit
  https://github.com/Ouranosinc/raven/commit/0763bf52abec1bc0a70927de3a2dc2cc1cf77ec3)
  removed salem dependency and replaced with rioxarray.

  Also add packages for the
  [`custom_climate_portraits`](https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/tree/custom_climate_portraits)
  branch  (PR
  https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/35).

  Noticeable changes:
  ```diff
    # conda release of bokeh seems to trail behind pypi
  >   - bokeh=2.0.1=py37hc8dfbb8_0
  <     - bokeh==2.0.2
  >   - jupyter_bokeh=2.0.1=py_0

    # should already exist, not sure why conda env export report this as new
  >   - dask=2.15.0=py_0

    # unpinned since salem is removed
  <   - pandas=0.25.3=py37hb3f55d8_0
  >   - pandas=1.0.3=py37h0da4684_1

  <     - salem==0.2.4
  >   - rioxarray=0.0.26=py_0

    # packages for custom_climate_portraits branch
  >   - geoviews=1.8.1=py_0
  >   - h5netcdf=0.8.0=py_0
  >   - holoviews=1.13.2=pyh9f0ad1d_0
  >   - panel=0.9.5=py_1
  >   - hvplot=0.5.2=py_0
  >   - pscript=0.7.3=py_0
  >   - siphon=0.8.0=py37_1002
  >     - ipython-blocking==0.2.1
  ```

  See PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/44
  (commit
  https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/commit/bb81982e3fd92bff437eddc5d4ae28202b3ef07c)
  for more info.

[1.9.2](https://github.com/bird-house/birdhouse-deploy/tree/1.9.2) (2020-04-29)
------------------------------------------------------------------------------------------------------------------
-
  jupyter: update to pavics/workflow-tests:200427 image

  See PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/43 (commit https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/commit/446b2f1ba3342106e3ad3d2dfe16aece7365c492) for more info.

  Noticeable changes:
  ```diff
  <   - geopandas=0.6.2=py_0
  >     - geopandas==0.7.0

  <   - xarray=0.15.0=py_0
  >   - xarray=0.15.1=py_0

  <   - owslib=0.19.1=py_0
  >   - owslib=0.19.2=py_1

  <   - dask-core=2.12.0=py_0
  >   - dask-core=2.15.0=py_0

  <     - distributed==2.12.0
  >     - distributed==2.15.0

  <     - xclim==0.14.0
  >     - xclim==0.16.0
  ```

[1.9.1](https://github.com/bird-house/birdhouse-deploy/tree/1.9.1) (2020-04-24)
------------------------------------------------------------------------------------------------------------------
-
  Fix notebook autodeploy wipe already deployed notebook when GitHub down.

  Fixes https://github.com/bird-house/birdhouse-deploy/issues/43

  Fail early with any unexpected error to not wipe already deployed notebooks.

  Check source dir not empty before wiping dest dir containing already deployed notebooks.

  Reduce cleaning verbosity for more concise logging.

  To fix this error found in production logs when Github is down today:
  ```
  notebookdeploy START_TIME=2020-04-23T10:01:01-0400
  ++ mktemp -d -t notebookdeploy.XXXXXXXXXXXX
  + TMPDIR=/tmp/notebookdeploy.ICk70Vto2LaE
  + cd /tmp/notebookdeploy.ICk70Vto2LaE
  + mkdir tutorial-notebooks
  + cd tutorial-notebooks
  + wget --quiet https://raw.githubusercontent.com/Ouranosinc/PAVICS-e2e-workflow-tests/master/downloadrepos
  + chmod a+x downloadrepos
  chmod: cannot access ‘downloadrepos’: No such file or directory
  + wget --quiet https://raw.githubusercontent.com/Ouranosinc/PAVICS-e2e-workflow-tests/master/default_build_params
  + wget --quiet https://raw.githubusercontent.com/Ouranosinc/PAVICS-e2e-workflow-tests/master/binder/reorg-notebooks
  + chmod a+x reorg-notebooks
  chmod: cannot access ‘reorg-notebooks’: No such file or directory
  + wget --quiet --output-document - https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/archive/master.tar.gz
  + tar xz

  gzip: stdin: unexpected end of file
  tar: Child returned status 1
  tar: Error is not recoverable: exiting now
  + ./downloadrepos
  /etc/cron.hourly/PAVICS-deploy-notebooks: line 63: ./downloadrepos: No such file or directory
  + ./reorg-notebooks
  /etc/cron.hourly/PAVICS-deploy-notebooks: line 64: ./reorg-notebooks: No such file or directory
  + mv -v 'PAVICS-e2e-workflow-tests-master/notebooks/*.ipynb' ./
  mv: cannot stat ‘PAVICS-e2e-workflow-tests-master/notebooks/*.ipynb’: No such file or directory
  + rm -rfv PAVICS-e2e-workflow-tests-master
  + rm -rfv downloadrepos default_build_params reorg-notebooks
  + TMP_SCRIPT=/tmp/notebookdeploy.ICk70Vto2LaE/deploy-notebook
  + cat
  + chmod a+x /tmp/notebookdeploy.ICk70Vto2LaE/deploy-notebook
  + docker pull bash
  Using default tag: latest
  latest: Pulling from library/bash
  Digest: sha256:febb3d74f41f2405fe21b7c7b47ca1aee0eda0a3ffb5483ebe3423639d30d631
  Status: Image is up to date for bash:latest
  + docker run --rm --name deploy_tutorial_notebooks -u root -v /tmp/notebookdeploy.ICk70Vto2LaE/deploy-notebook:/deploy-notebook:ro -v /tmp/notebookdeploy.ICk70Vto2LaE/tutorial-notebooks:/tutorial-notebooks:ro -v /data/jupyterhub_user_data:/notebook_dir:rw --entrypoint /deploy-notebook bash
  + cd /notebook_dir
  + rm -rf tutorial-notebooks/WCS_example.ipynb tutorial-notebooks/WFS_example.ipynb tutorial-notebooks/WMS_example.ipynb tutorial-notebooks/WPS_example.ipynb tutorial-notebooks/catalog_search.ipynb tutorial-notebooks/dap_subset.ipynb tutorial-notebooks/esgf-compute-api-examples-devel tutorial-notebooks/esgf-dap.ipynb tutorial-notebooks/finch-usage.ipynb tutorial-notebooks/hummingbird.ipynb tutorial-notebooks/opendap.ipynb tutorial-notebooks/pavics_thredds.ipynb tutorial-notebooks/raven-master tutorial-notebooks/rendering.ipynb tutorial-notebooks/subsetting.ipynb
  + cp -rv '/tutorial-notebooks/*' tutorial-notebooks
  cp: can't stat '/tutorial-notebooks/*': No such file or directory
  + chown -R root:root tutorial-notebooks
  + set +x
  removed directory: ‘/tmp/notebookdeploy.ICk70Vto2LaE/tutorial-notebooks’
  removed ‘/tmp/notebookdeploy.ICk70Vto2LaE/deploy-notebook’
  removed directory: ‘/tmp/notebookdeploy.ICk70Vto2LaE’

  notebookdeploy finished START_TIME=2020-04-23T10:01:01-0400
  notebookdeploy finished   END_TIME=2020-04-23T10:02:12-0400
  ```

[1.9.0](https://github.com/bird-house/birdhouse-deploy/tree/1.9.0) (2020-04-24)
------------------------------------------------------------------------------------------------------------------
-
  vagrant: add centos7 and LetsEncrypt SSL cert support, fix scheduler autodeploy remaining issues

  Fixes https://github.com/bird-house/birdhouse-deploy/issues/27.

  Centos7 support added to Vagrant to reproduce problems found on Medus in PR https://github.com/bird-house/birdhouse-deploy/pull/39 (commit https://github.com/bird-house/birdhouse-deploy/commit/6036dbd5ff072544d902e7b84b5eff361b00f78b):

  Problem 1: wget httpS url not working in bash docker image breaking the notebook autodeploy when running under the new scheduler autodeploy: **not reproducible**

  Problem 2: all containers are destroyed and recreated when alternating between manually running `./pavics-compose.sh up -d` locally and when the same command is executed automatically by the scheduler autodeploy inside its own container: **not reproducible**

  Problem 3: `sysctl: error: 'net.ipv4.tcp_tw_reuse' is an unknown key` on `./pavics-compose.sh up -d` when executed automatically by the scheduler autodeploy inside its own container: **reproduced** but seems **harmless** so **not fixing** it.

  Problem 4: current user lose write permission to birdhouse-deploy checkout and other checkout in `AUTODEPLOY_EXTRA_REPOS` when using scheduler autodeploy: **fixed**

  Problem 5: no documentation for the new scheduler autodeploy: **fixed**

  Another autodeploy fix found while working on this PR: notebook autodeploy broken when `/data/jupyterhub_user_data/tutorial-notebooks` dir do not pre-exist.  Regression from this commit https://github.com/bird-house/birdhouse-deploy/pull/16/commits/6ddaddc74d384299e45b0dc8d50a63e59b3cc0d5 (PR https://github.com/bird-house/birdhouse-deploy/pull/16): before that commit the entire dir was copied, not just the content, so the dir was created automatically.

  Centos7 Vagrant box experience is not completely automated as Ubuntu box, even when using the same vagrant-disksize Vagrant plugin as Ubuntu box.  Manual disk resize instruction is provided.  Candidate for automation later if we destroy and recreate Centos7 box very often.  Hopefully the problem is not there for Centos8 so we can forget about this annoyance.

  Automatic generation of SSL certificate from LetsEncrypt is also added for both Ubuntu and Centos Vagrant box.  Can be used outside of Vagrant so Medus and Boreas can also benefit next time, if needed.  Later docker image of `certbot` is used so should already be using ACMEv2 protocol (ACMEv1 is being deprecated).

  Pagekite is also preserved for both boxes for when exposing port 80 and 443 directly on the internet is not possible but PAVICS still need a real SSL certificate.

  Test server: https://lvupavicsmaster.ouranos.ca (Centos7, on internet with LetsEncrypt SSL cert).

  Jenkins run only have known errors: http://jenkins.ouranos.ca/job/ouranos-staging/job/lvupavicsmaster.ouranos.ca/4/console

  ![2020-04-22-070604_1299x1131_scrot](https://user-images.githubusercontent.com/11966697/79974607-a2707b80-8467-11ea-85b6-3b03f198ce9b.png)

[1.8.10](https://github.com/bird-house/birdhouse-deploy/tree/1.8.10) (2020-04-09)
------------------------------------------------------------------------------------------------------------------
- Autodeploy the autodeploy phase 2: everything operational but a few compatibility issues remain

  Part of https://github.com/bird-house/birdhouse-deploy/issues/27

  Activating the `./components/scheduler` will do everything.  All configurations are centralized in the `env.local` file.

  One missing feature is piece-wise choice of platform or notebook autodeploy only, like with the old manual `install-*` stcripts under https://github.com/bird-house/birdhouse-deploy/tree/master/birdhouse/deployment.  Right now it's all or nothing.  I can work on this if you guys think it's needed.

  Remaining compatibility issues with Medus (Vagrant box works fine):

  * Notebook autodeploy do not work. It looks like using the `bash` docker image, I am unable to wget any httpS address.  This same `docker run` command works fine on my Vagrant box as well.  So there's something on Medus.

  ```
  $ docker run --rm --name debug_wget_httpS -u root bash bash -c "wget https://google.com -O -"
  Connecting to google.com (172.217.13.206:443)
  wget: error getting response: Connection reset by peer
  ```

  * All the containers are being recreated when `./pavics-compose.sh` runs inside the container (first migration to the new autodeploy mechanism).  To investigate but I suspect this might be due to older version of `docker` and `docker-compose` on Medus.

  * This one looks like due to older kernel on Medus:
  ```
  sysctl: error: 'net.ipv4.tcp_tw_reuse' is an unknown key
  sh: 0: unknown operand
  ```

  * All the files updated by `git pull` are now owned by `root` (the user inside the container).  I'll have to undo this ownership change, somehow.  This one is super weird, I should have got it on my Vagrant box.  Probably Vagrant did some magic to always ensure files under `/vagrant` is always owned by the user even if changed by user `root`.

  * Documentation: update README and list relevant configuration variables in `env.local` for this new `./component/scheduler`.


  Migrating to this new mechanism requires manual deletion of all the artifacts created by the old install scripts: `sudo rm /etc/cron.d/PAVICS-deploy /etc/cron.hourly/PAVICS-deploy-notebooks /etc/logrotate.d/PAVICS-deploy /usr/local/sbin/triggerdeploy.sh`.  Both can not co-exist at the same time.

  Maximum backward-compatibility has been kept with the old existing install scripts style:
  * Still log to the same existing log files under `/var/log/PAVICS`.
  * Old single ssh deploy key is still compatible, but the new mechanism allows for different ssh deploy keys for each extra repos (again, public repos should use https clone path to avoid dealing with ssh deploy keys in the first place)
  * Old install scripts are kept

  Features missing in old existing install scripts or how this improves on the old install scripts:
  * Autodeploy of the autodeploy itself !  This is the biggest win.  Previously, if `triggerdeploy.sh` or `PAVICS-deploy-notebooks` script changes, they have to be deployed manually.  It's very annoying.  Now they are volume-mount in so are fresh on each run.
  * `env.local` now drive absolutely everything, source control that file and we've got a true DevOPS pipeline.
  * Configurable platform and notebook autodeploy frequency.  Previously, this means manually editing the generated cron file, less ideal.
  * Do not need any support on the local host other than `docker` and `docker-compose`.  cron/logrotate/git/ssh versions are all locked-down in the docker images used by the autodeploy.  Recall previously we had to deal with git version too old on some hosts.
  * Each cron job run in its own docker image meaning the runtime environment is traceable and reproducible.
  * The newly introduced scheduler component is made extensible so other jobs can added into it as well (ex: backup), via `env.local`, which should source control, meaning all surrounding maintenance related tasks can also be traceable and reproducible.

  This is a rather large PR.  For a less technical overview, start with the diff of README.md, env.local.example, common.env.  If a change looks funny to you, read the commit description that introduce that change, the reasoning should be there.

[1.8.9](https://github.com/bird-house/birdhouse-deploy/tree/1.8.9) (2020-04-08)
------------------------------------------------------------------------------------------------------------------
- finch: update to 0.5.2

  Fix following 2 Jenkins failures:

  Tested in this Jenkins run http://jenkins.ouranos.ca/job/ouranos-staging/job/lvupavics-lvu.pagekite.me/20/console

  ```
    _________ finch-master/docs/source/notebooks/dap_subset.ipynb::Cell 9 __________
    Notebook cell execution failed
    Cell 9: Cell outputs differ

    Input:
    resp = wps.sdii(pr + sub)
    out = resp.get(asobj=True)
    out.output_netcdf.sdii

    Traceback:
     mismatch 'text/html'

     assert reference_output == test_output failed:

      '<pre>&lt;xar...vera...</pre>' == '<pre>&lt;xar...vera...</pre>'
      Skipping 350 identical leading characters in diff, use -v to show
        m/day
      -     cell_methods:   time: mean (interval: 30 minutes)
            history:        pr=max(0,pr) applied to raw data;\n[DATE_TIME] ...
      +     cell_methods:   time: mean (interval: 30 minutes)
            standard_name:  lwe_thickness_of_precipitation_amount
            long_name:      Average precipitation during wet days (sdii)
            description:    Annual simple daily intensity index (sdii) : annual avera...</pre>
  ```

  ```
    _________ finch-master/docs/source/notebooks/finch-usage.ipynb::Cell 1 _________
    Notebook cell execution failed
    Cell 1: Cell outputs differ

    Input:
    help(wps.frost_days)

    Traceback:
     mismatch 'stdout'

     assert reference_output == test_output failed:

      'Help on meth...ut files.\n\n' == 'Help on meth...ut files.\n\n'
      Skipping 399 identical leading characters in diff, use -v to show
      -    freq : string
      +    freq : {'YS', 'MS', 'QS-DEC', 'AS-JUL'}string
                Resampling frequency

            Returns
            -------
            output_netcdf : ComplexData:mimetype:`application/x-netcdf`
                The indicator values computed on the original input grid.
            output_log : ComplexData:mimetype:`text/plain`
                Collected logs during process run.
            ref : ComplexData:mimetype:`application/metalink+xml; version=4.0`
                Metalink file storing all references to output files.
  ```

[1.8.8](https://github.com/bird-house/birdhouse-deploy/tree/1.8.8) (2020-03-20)
------------------------------------------------------------------------------------------------------------------
- `jupyter`: make configurable public demo user name, passwd, resource limit, login banner

  For security reasons, the public demo username and password are not hardcoded anymore.

  Compromising of one PAVICS deployment should not compromise all other PAVICS deployments if each deployment use a different password.

  The password is set when the public demo user is created in Magpie, see the `birdhouse/README.md` update.

  The login banner do not display the public demo password anymore.  If one really want to display the password, can use the top or bottom section of the login banner that is customizable via `env.local`.

  Login banner is updated with more notices, please review wording.

  Resource limits (only memory limit seems to work with the `DockerSpawner`) is also customizable.

  All changes to `env.local` are live after a `./pavics-compose.sh up -d`.

  Test server: https://lvupavics-lvu.pagekite.me/jupyter/ (ask me privately for the password :D)

[1.8.7](https://github.com/bird-house/birdhouse-deploy/tree/1.8.7) (2020-03-19)
------------------------------------------------------------------------------------------------------------------
- finch: update to v0.5.1

[1.8.6](https://github.com/bird-house/birdhouse-deploy/tree/1.8.6) (2020-03-16)
------------------------------------------------------------------------------------------------------------------
- Thredds: New "Datasets" top level for NCML files

  http://lvupavics-lvu.pagekite.me/twitcher/ows/proxy/thredds/catalog/datasets/catalog.html (only gridded_obs/nrcan.ncml works on my dev server).

  Add a new top-level "Datasets" at the same level as the existing "Birdhouse".

  The content of the new top-level comes from `/data/ncml` from the host.  For comparison content of existing "Birdhouse" was coming from `/data/datasets`.

[1.8.5](https://github.com/bird-house/birdhouse-deploy/tree/1.8.5) (2020-03-13)
------------------------------------------------------------------------------------------------------------------
- `jupyter`: update to pavics/workflow-tests:200312 for Raven notebooks

[1.8.4](https://github.com/bird-house/birdhouse-deploy/tree/1.8.4) (2020-03-10)
------------------------------------------------------------------------------------------------------------------
- raven: upgrade to pavics/raven:0.10.0

[1.8.3](https://github.com/bird-house/birdhouse-deploy/tree/1.8.3) (2020-02-17)
------------------------------------------------------------------------------------------------------------------
- catalog: fix pavicsearch broken due to typo in config

  The `thredds_host` should be the exact prefix of each document url found
  in Solr, otherwise it is removed from the search result.

  This explains why pavicsearch was returning nothing.

  This will fix the `catalog_search.ipynb` notebook that keeps failing on Jenkins.

  The typo was introduced in PR
  https://github.com/bird-house/birdhouse-deploy/pull/5, commit
  https://github.com/bird-house/birdhouse-deploy/commit/83c839178fff170dbcb4c4e0586e67d19b9cfbc5

[1.8.2](https://github.com/bird-house/birdhouse-deploy/tree/1.8.2) (2020-02-10)
------------------------------------------------------------------------------------------------------------------
- Optionally monitor all components behind Twitcher using canarie api.

  Fixes https://github.com/bird-house/birdhouse-deploy/issues/8

  The motivation was the need for some quick dashboard for the working state of all the components, not to get more stats.

  Right now we bypassing Twitcher, which is not real life, it's not what real users will experience.

  This is ultra cheap to add and provide very fast and up-to-date (every minute) result. It's like an always on sanity check that can quickly help debugging any connectivity issues between the components.

  It is optional because it assumes all components are publicly accessible.  Might not be the case for everyone.  We can also override the override :D

  All components in config/canarie-api/docker_configuration.py.template that do not have public (behind Twitcher) monitoring are added.

  Also added Hummingbird and ncWMS2 public monitoring.

  @tlogan2000 This will catch accidental Thredds public url breakage like last time and will leverage the existing monitoring on https://pavics.ouranos.ca/canarie/node/service/stats by @moulab88.

  @davidcaron @dbyrns This is optional so if the CRIM do not want to enable it, it's fine.

  New node monitoring page:

  ![Screenshot_2020-02-07 Ouranos - Node Service](https://user-images.githubusercontent.com/11966697/74055606-4a6cc180-49ae-11ea-9cba-887118dbaae6.png)

[1.8.1](https://github.com/bird-house/birdhouse-deploy/tree/1.8.1) (2020-02-06)
------------------------------------------------------------------------------------------------------------------
- Increase JupyterHub security.

  ab56994 jupyter: limit memory of public user to 500 MB
  90c1950 jupyter: prevent user from loading user-owned config at spawner server startup
  e8f2fa3 jupyter: avoid terminating user running jobs on Hub update
  3f97cc7 jupyter: get ready to prevent browser session re-use even if password changed
  e2ebcc3 jupyter: disable notebook terminal for security reasons

[1.8.0](https://github.com/bird-house/birdhouse-deploy/tree/1.8.0) (2020-02-03)
------------------------------------------------------------------------------------------------------------------
- jupyter data migration: touch new location else jupyterhub won't bind mount them

  See PR https://github.com/bird-house/birdhouse-deploy/pull/16
  or commit
  https://github.com/bird-house/birdhouse-deploy/commit/53576cc9d36642c50e4a649ca58fc8339559fd4a

  See the `if os.path.exists` in the `jupyterhub_config.py`:
  https://github.com/bird-house/birdhouse-deploy/blob/53576cc9d36642c50e4a649ca58fc8339559fd4a/birdhouse/config/jupyterhub/jupyterhub_config.py.template#L36-L48

[1.7.1](https://github.com/bird-house/birdhouse-deploy/tree/1.7.1) (2020-01-30)
------------------------------------------------------------------------------------------------------------------
- `jupyter`: update various packages and add threddsclient

  Noticeable changes:
  ```diff
  <     - bokeh==1.4.0
  >   - bokeh=1.4.0=py36_0

  <   - python=3.7.3=h33d41f4_1
  >   - python=3.6.7=h357f687_1006

  >   - threddsclient=0.4.2=py_0

  <     - xarray==0.13.0
  >   - xarray=0.14.1=py_1

  <     - dask==2.8.0
  >     - dask==2.9.2

  <     - xclim==0.12.2
  >     - xclim==0.13.0
  ```

  See PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/34 for more info.

[1.7.0](https://github.com/bird-house/birdhouse-deploy/tree/1.7.0) (2020-01-22)
------------------------------------------------------------------------------------------------------------------
- backup solr: should save all of /data/solr, not just the index


Prior Versions
------------------------------------------------------------------------------------------------------------------

All versions prior to [1.7.0](https://github.com/bird-house/birdhouse-deploy/tree/1.7.0) were not officially tagged.
Is it strongly recommended employing later versions to ensure better traceability of changes that could impact behavior
and potential issues on new server instances. 
