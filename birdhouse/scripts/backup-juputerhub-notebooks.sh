#!/bin/sh -x
# Backup to /tmp/jupyterhub_user_persistence.tgz with default values.

if [ -z "$BACKUP_OUT_DIR" ]; then
    BACKUP_OUT_DIR=/tmp
fi

./backup-datavolume.sh "$JUPYTERHUB_USER_DATA_DIR" "$BACKUP_OUT_DIR"


# vi: tabstop=8 expandtab shiftwidth=4 softtabstop=4
