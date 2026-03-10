#!/usr/bin/env sh

THIS_FILE="$(readlink -f "$0" || realpath "$0")"
THIS_DIR="$(dirname "${THIS_FILE}")"
BIRDHOUSE_EXE="${THIS_DIR}/../../bin/birdhouse"

USAGE="Usage: $0 <bucket-name>"
HELP="$USAGE

Create a new bucket for the s3 service and create the equivalent resources on Magpie for this new bucket.

This will also set the s3 ACLs and permissions appropriately so that the bucket can be accessed through 
the birdhouse proxy.

If you have already created a bucket manually (not through this script) you should still run this script 
afterwards to ensure that the bucket is accessible through the birdhouse proxy.
"

if [ -z "$1" ]; then 
    >&2 echo $USAGE
    exit 1
fi
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "$HELP"
    exit
fi

${BIRDHOUSE_EXE} compose run -e S3_BUCKET_NAME="$1" --rm --name "create-s3-bucket-${1}" --entrypoint sh s3-cli -c ' \
    aws s3api head-bucket --bucket thredds || aws s3api create-bucket --bucket "${S3_BUCKET_NAME}" --object-ownership BucketOwnerPreferred; \
    aws s3api put-bucket-ownership-controls --bucket "${S3_BUCKET_NAME}" --ownership-controls "Rules=[{ObjectOwnership=ObjectWriter}]"; \
    aws s3api put-bucket-acl --bucket "${S3_BUCKET_NAME}" --acl public-read' || exit 1

TMP_CONFIG_FILE="${TMP_CONFIG_FILE:-/tmp/create-s3-bucket.yml}"

echo "
permissions:
  - service: s3
    resource: /$1
    permission: read
    group: administrators
    action: create
" > ${TMP_CONFIG_FILE} || exit 1

${BIRDHOUSE_EXE} configs -c 'docker run --name create-magpie-s3-bucket-resource --rm \
    -v '"${TMP_CONFIG_FILE}"':/config.yml \
    -e MAGPIE_URL=${BIRDHOUSE_PROXY_SCHEME}://${BIRDHOUSE_FQDN_PUBLIC}/magpie \
    -e MAGPIE_ADMIN_USER=${MAGPIE_ADMIN_USERNAME} \
    -e MAGPIE_ADMIN_PASSWORD=${MAGPIE_ADMIN_PASSWORD} \
    ${MAGPIE_IMAGE} \
    magpie_batch_update_permissions --config /config.yml'
