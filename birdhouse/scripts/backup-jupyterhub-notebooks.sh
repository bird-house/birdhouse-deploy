#!/bin/sh -x
# Backup to /tmp/jupyterhub_user_persistence.tgz with default values.

if [ -z "$BACKUP_OUT_DIR" ]; then
    BACKUP_OUT_DIR=/tmp
fi

if [ -z "$JUPYTERHUB_USER_DATA_DIR" ]; then
    JUPYTERHUB_USER_DATA_DIR=${DATA_PERSIST_ROOT:-/data}/${USER_WORKSPACES}
fi

docker run --rm \
  --name backup_jupyterhub_data \
  -u root \
  -v "$BACKUP_OUT_DIR":/backups \
  -v "$JUPYTERHUB_USER_DATA_DIR":/data_vol_to_backup:ro \
  bash:5.1.4 \
  tar czvf /backups/jupyterhub_user_data.tgz -C /data_vol_to_backup .

# vi: tabstop=8 expandtab shiftwidth=4 softtabstop=4
