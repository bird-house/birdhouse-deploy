#!/bin/sh -x
# Backup DATA_VOL_DIR to BACKUP_OUT_DIR/DATA_VOL_DIR.tgz

DATA_VOL_DIR="$1"; shift
BACKUP_OUT_DIR="$1"; shift

docker run --rm \
  --name backup_data_volume \
  -u root \
  -v $BACKUP_OUT_DIR:/backups \
  -v $DATA_VOL_DIR:/data_vol_to_backup:ro \
  bash \
  tar czvf /backups/data_volume_backup.tgz -C /data_vol_to_backup .

# vi: tabstop=8 expandtab shiftwidth=4 softtabstop=4
