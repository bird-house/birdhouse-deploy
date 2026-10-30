#!/bin/bash

mkdir -p $SCRIPTS_LOCKFILE_DIR

# Set lockfile for existing data
if [ -f /opt/geoserver/data_dir/security/usergroup/default/users.xml ]; then
    touch -v $SCRIPTS_LOCKFILE_DIR/.security.lock
fi

# Chain with existing entrypoint
/bin/bash /scripts/entrypoint.sh
