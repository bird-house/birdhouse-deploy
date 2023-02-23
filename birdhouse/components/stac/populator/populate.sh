#!/usr/bin/env bash
set -e

if [[ -z "${BASE_PATH}" ]]; then
  echo "[INFO] BASE_PATH environment variable not set. Using ''"
  BASE_PATH=""
fi

if [[ -z "${STAC_ASSET_GENERATOR_TIMEOUT}" ]]; then
  echo "[INFO] STAC_ASSET_GENERATOR_TIMEOUT environment variable not set. Using '30'"
  STAC_ASSET_GENERATOR_TIMEOUT="30"
fi

if [[ -z "${STAC_HOST}" ]]; then
  echo "[INFO] STAC_HOST environment variable not set. Using '127.0.0.1'"
  STAC_HOST="127.0.0.1"
fi

cd $BASE_PATH/populator

# create collections
python3 ./collection_processor.py collections.yaml

cd $BASE_PATH/stac-generator-example

# replace STAC host name of asset generators
sed -i "/host:/c\      host: $STAC_HOST" conf/thredds-cmip6-asset-generator.yaml
sed -i "/host:/c\      host: $STAC_HOST" conf/thredds-cmip5-asset-generator.yaml

# add items
timeout $STAC_ASSET_GENERATOR_TIMEOUT bash -c "python3 -m stac_generator.scripts.stac_generator conf/thredds-cmip6-asset-generator.yaml" || true &
PID_CMIP6=$!
timeout $STAC_ASSET_GENERATOR_TIMEOUT bash -c "python3 -m stac_generator.scripts.stac_generator conf/thredds-cmip5-asset-generator.yaml" || true &
PID_CMIP5=$!

# kill the asset generators if CTRL-C is sent
trap "kill -2 ${PID_CMIP6} ${PID_CMIP5} 2> /dev/null; exit 1" INT

echo "Running STAC asset generator for $STAC_ASSET_GENERATOR_TIMEOUT seconds..."
wait $PID_CMIP6
wait $PID_CMIP5

cd $BASE_PATH/populator

# update collection summaries
python3 collection_processor.py collections.yaml

echo "STAC asset generator ran for $STAC_ASSET_GENERATOR_TIMEOUT seconds. Exiting."
