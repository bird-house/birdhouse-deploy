#!/bin/sh -x
# Backup DATA_VOL_NAME to BACKUP_OUT_DIR/DATA_VOL_NAME.tgz

DATA_VOL_NAME="$1"; shift
BACKUP_OUT_DIR="$1"; shift

docker run --rm \
  --name "backup_data_vol_${DATA_VOL_NAME}" \
  -u root \
  -v "${BACKUP_OUT_DIR}":/backups \
  -v "${DATA_VOL_NAME}":/data_vol_to_backup:ro \
  bash:5.1.4 \
  tar czvf "/backups/${DATA_VOL_NAME}.tgz" -C /data_vol_to_backup .

# vi: tabstop=8 expandtab shiftwidth=4 softtabstop=4
