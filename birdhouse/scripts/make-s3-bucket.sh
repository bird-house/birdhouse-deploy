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

TMP_LOG_FILE="${TMP_LOG_FILE:-/tmp/create-s3-bucket.log}"
eval "$(${BIRDHOUSE_EXE} configs --print-log-command)"

log INFO "Creating S3 bucket named ${1}"
${BIRDHOUSE_EXE} --quiet --log-file "${TMP_LOG_FILE}" compose run -e S3_BUCKET_NAME="$1" --rm --name "create-s3-bucket-${1}" --entrypoint sh s3-cli -c ' \
    aws s3api head-bucket --bucket "${S3_BUCKET_NAME}" &>/dev/null || aws s3api create-bucket --bucket "${S3_BUCKET_NAME}" --object-ownership BucketOwnerPreferred; \
    aws s3api put-bucket-ownership-controls --bucket "${S3_BUCKET_NAME}" --ownership-controls "Rules=[{ObjectOwnership=ObjectWriter}]" && \
    aws s3api put-bucket-acl --bucket "${S3_BUCKET_NAME}" --acl public-read'

if [ "$?" -eq 0 ]; then
    log INFO "S3 bucket successfully created"
else
    log ERROR "S3 bucket creation failed. See ${TMP_LOG_FILE} for more log output."
    exit 1
fi

TMP_CONFIG_FILE="${TMP_CONFIG_FILE:-/tmp/create-s3-bucket.yml}"

# Note empty users and groups added to suppress error message that they are not found
echo "
users: {}
groups: {}
permissions:
  - service: s3
    resource: /$1
    permission: read
    group: administrators
    action: create
" > ${TMP_CONFIG_FILE} || exit 1

log INFO "Adding resource for bucket named ${1} to Magpie"

# Note: PYTHONWARNINGS=ignore because magpie shows a bunch of deprecation warnings which are not relevant to the user at this point
# This may be removed in the future when Magpie is updated.
${BIRDHOUSE_EXE} --quiet --log-file "${TMP_LOG_FILE}" configs -c 'docker run -e PYTHONWARNINGS=ignore --name create-magpie-s3-bucket-resource --rm \
    -v '"${TMP_CONFIG_FILE}"':/config.yml \
    -e MAGPIE_URL=${BIRDHOUSE_PROXY_SCHEME}://${BIRDHOUSE_FQDN_PUBLIC}/magpie \
    -e MAGPIE_ADMIN_USER=${MAGPIE_ADMIN_USERNAME} \
    -e MAGPIE_ADMIN_PASSWORD=${MAGPIE_ADMIN_PASSWORD} \
    ${MAGPIE_IMAGE} \
    magpie_batch_update_permissions --config /config.yml'

if [ "$?" -eq 0 ]; then
    log INFO "Magpie resource successfully created"
else
    log ERROR "Magpie resource creation failed. See ${TMP_LOG_FILE} for more log output."
    exit 1
fi
