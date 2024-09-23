.. contents::

Migration Guide
===============

Version 2.4
-----------

Version 2.4 renames files and variables that included the string PAVICS.

For historical reasons the name PAVICS was used in variable names, constants and filenames in this repo to refer to
the software stack in general. This was because, for a long time, the PAVICS deployment of this stack was the only one
that was being used in production. However, now that multiple deployments of this software exist in production (that are
not named PAVICS), we remove unnecessary references to PAVICS in order to reduce confusion for maintainers and developers
who may not be aware of the historical reasons for the PAVICS name.

To upgrade to version 2.4 from an earlier version, please follow these steps:

  - Update ``env.local`` file to replace all variables that contain ``PAVICS`` with ``BIRDHOUSE``.
    Variable names have also been updated to ensure that they start with the prefix ``BIRDHOUSE_``.

    * see `birdhouse/env.local.example <birdhouse/env.local.example>`_ to see new variable names
    * see the ``BIRDHOUSE_BACKWARDS_COMPATIBLE_VARIABLES`` variable (defined in `birdhouse/default.env <birdhouse/default.env>`_)
      for a full list of changed environment variable names.

  - Update any external scripts that access the old variable names directly to use the updated variable names.
  - Update any external scripts that access any of the following files to use the new file name:

    .. list-table::
        :header-rows: 1

        * - old file name
          - new file name
        * - pavics-compose.sh
          - birdhouse-compose.sh
        * - PAVICS-deploy.logrotate
          - birdhouse-deploy.logrotate
        * - configure-pavics.sh
          - configure-birdhouse.sh
        * - trigger-pavicscrawler
          - trigger-birdhousecrawler

  - Update any external scripts that called ``pavics-compose.sh`` or ``read-configs.include.sh`` to use the CLI
    entrypoint in ``bin/birdhouse`` instead.
  - The following default values have changed. If your deployment was using the old default value, update your
    ``env.local`` file to explicitly set the old default values.

    .. list-table::
        :header-rows: 1

        * - old variable name
          - new variable name
          - old default value
          - new default value
        * - POSTGRES_PAVICS_USERNAME
          - BIRDHOUSE_POSTGRES_USERNAME
          - postgres-pavics
          - postgres-birdhouse
        * - THREDDS_DATASET_LOCATION_ON_CONTAINER
          - (no change)
          - /pavics-ncml
          - /birdhouse-ncml
        * - THREDDS_SERVICE_DATA_LOCATION_ON_CONTAINER
          - (no change)
          - /pavics-data
          - /birdhouse-data
        * - (hardcoded)
          - BIRDHOUSE_POSTGRES_DB
          - pavics
          - birdhouse
        * - PAVICS_LOG_DIR
          - BIRDHOUSE_LOG_DIR
          - /var/log/PAVICS
          - /var/log/birdhouse
        * - (hardcoded)
          - GRAFANA_DEFAULT_PROVIDER_FOLDER
          - Local-PAVICS
          - Local-Birdhouse
        * - (hardcoded)
          - GRAFANA_DEFAULT_PROVIDER_FOLDER_UUID
          - local-pavics
          - local-birdhouse
        * - (hardcoded)
          - GRAFANA_PROMETHEUS_DATASOURCE_UUID
          - local_pavics_prometheus
          - local_birdhouse_prometheus

    Note that the ``PAVICS_LOG_DIR`` variable was actually hardcoded as ``/var/log/PAVICS`` in some scripts. If
    ``PAVICS_LOG_DIR`` was set to anything other than ``/var/log/PAVICS`` you'll end up with inconsistent log outputs as
    previously some logs would have been sent to ``PAVICS_LOG_DIR`` and others to ``/var/log/PAVICS``. We recommend merging
    these two log files. Going forward, all logs will be sent to ``BIRDHOUSE_LOG_DIR``.

  - Update any jupyter notebooks that make use of the ``PAVICS_HOST_URL`` environment variable to use the new
    ``BIRDHOUSE_HOST_URL`` instead.
  - Set the ``BIRDHOUSE_POSTGRES_DB`` variable to ``pavics`` in the ``env.local`` file. This value was previously
    hardcoded to the string ``pavics`` so to maintain backwards compatibility with any existing databases this should be
    kept the same. If you do want to update to the new database name, you will need to rename the existing database.
    For example, the following will update the existing database named ``pavics`` to ``birdhouse`` (assuming the old
    default values for the postgres username):

    .. code-block:: shell

        docker exec -it postgres psql -U postgres-pavics -d postgres -c 'ALTER DATABASE pavics RENAME TO birdhouse'


    You can then update the ``env.local`` file to the new variable name and restart the stack
  - Set the ``BIRDHOUSE_POSTGRES_USER`` variable to ``postgres-pavics`` in the ``env.local`` file if you would like to
    preserve the old default value. If you would like to change the value of ``BIRDHOUSE_POSTGRES_USER`` then also
    update the name for any running postgres instances. For example, the following will update the user named
    ``postgres-pavics`` to ``postgres-birdhouse``:

    .. code-block:: shell

        docker exec -it postgres psql -U postgres-pavics -d postgres -c 'CREATE USER "tmpsuperuser" WITH SUPERUSER'
        docker exec -it postgres psql -U tmpsuperuser -d postgres -c 'ALTER ROLE "postgres-pavics" RENAME TO "postgres-birdhouse"'
        docker exec -it postgres psql -U tmpsuperuser -d postgres -c 'ALTER ROLE "postgres-birdhouse" WITH PASSWORD '\''postgres-qwerty'\'
        docker exec -it postgres psql -U postgres-birdhouse -d postgres -c 'DROP ROLE "tmpsuperuser"'


    Note that the ``postgres-qwerty`` value is meant just for illustration, you should replace this with the value of
    the ``BIRDHOUSE_POSTGRES_PASSWORD`` variable.
    Note that you'll need to do the same for the ``stac-db`` service as well (assuming that you weren't previously
    overriding the ``STAC_POSTGRES_USER`` with a custom value).
