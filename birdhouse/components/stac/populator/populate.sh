#!/bin/sh
set -e

BASE_PATH=""
STAC_ASSET_GENERATOR_TIMEOUT=20

# create collections
python3 ./collection_processor.py collections.yaml

cd $BASE_PATH/stac-generator-example

# add items
timeout -s HUP $STAC_ASSET_GENERATOR_TIMEOUT bash -c "python3 -m stac_generator.scripts.stac_generator conf/thredds-cmip6-asset-generator.yaml" &
PID_CMIP6=$!
timeout -s HUP $STAC_ASSET_GENERATOR_TIMEOUT bash -c "python3 -m stac_generator.scripts.stac_generator conf/thredds-cmip5-asset-generator.yaml" &
PID_CMIP5=$!

# kill the asset generators if CTRL-C is sent
trap "kill -2 ${PID_CMIP6} ${PID_CMIP5} 2> /dev/null; exit 1" INT

echo "Running STAC asset generator for $STAC_ASSET_GENERATOR_TIMEOUT seconds..."
wait $PID_CMIP6
wait $PID_CMIP5

cd $BASE_PATH/

# update collection summaries
python3 collection_processor.py collections.yaml

echo "STAC asset generator ran for $STAC_ASSET_GENERATOR_TIMEOUT seconds. Exiting."
