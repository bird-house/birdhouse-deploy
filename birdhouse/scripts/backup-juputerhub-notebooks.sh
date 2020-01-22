#!/bin/sh -x
# Backup to /tmp/jupyterhub_user_persistence.tgz with default values.

if [ -z "$BACKUP_OUT_DIR" ]; then
    BACKUP_OUT_DIR=/tmp
fi

if [ -z "$DOCKER_JUPYTERHUB_USER_PERSISTENCE_VOLUME" ]; then
    # dupe with pavics-compose.sh
    DOCKER_JUPYTERHUB_USER_PERSISTENCE_VOLUME=jupyterhub_user_persistence
fi

./backup-datavolume.sh "$DOCKER_JUPYTERHUB_USER_PERSISTENCE_VOLUME" "$BACKUP_OUT_DIR"


# vi: tabstop=8 expandtab shiftwidth=4 softtabstop=4
