#!/usr/bin/env sh

# Check whether default docker image definitions will work with the dependabot update github actions.

# Default docker images must be defined as an environment variable in the component's default.env file.
# For example:

#   export X_VERSION=1.2.3
#   export X_IMAGE='image_name:${X_VERSION}'

# Or if a component uses the same version to update multiple images, the variable names can optionally include
# a suffix. For example:

#   export X_VERSION=1.2.3
#   export X_IMAGE_MANAGER='image_name:${X_VERSION}-manager'
#   export X_IMAGE_WORKER='image_name:${X_VERSION}-worker'

# What matters is that the shared prefix ``X`` is immediately followed by either ``_IMAGE`` or ``_VERSION``.

# When developing a new component or updating the variables for an existing component, the image and version
# definitions must follow this format in order to be automatically updated.

# If you wish to exclude a component from automatic updates then add the component path to the ``EXCLUDE_COMPONENTS_RE``
# variable defined in ``birdhouse/scripts/dependabot-scripts.include.sh``.

# NOTE: this script is used but pre-commit and is referenced in .pre-commit-config.yaml

THIS_FILE="$(readlink -f "$0" || realpath "$0")"
THIS_DIR="$(dirname "${THIS_FILE}")"
COMPOSE_DIR="${THIS_DIR}/../"

. ${COMPOSE_DIR}/scripts/dependabot-scripts.include.sh

if [ $# -eq 0 ]; then
    COMPOSE_FILES="$(find "${COMPOSE_DIR}/components/" "${COMPOSE_DIR}/optional-components/" -maxdepth 2 -mindepth 2 -name 'docker-compose-extra.yml' | grep -v "${EXCLUDE_COMPONENTS_RE}")"
else
    COMPOSE_FILES="$(echo "$@" | tr ' ' "\n" | grep -v "${EXCLUDE_COMPONENTS_RE}")"
fi

INVALID_IMAGES="$(grep '^[[:space:]]\{1,\}image:' ${COMPOSE_FILES} | grep -v 'image:[[:space:]]*\${[0-9A-Z_]\{1,\}_IMAGE[0-9A-Z_]*}$')"

invalid=0

if [ -n "${INVALID_IMAGES}" ]; then
    echo "Found invalid image definitions for the birdhouse stack"
    echo "Images definitions in docker-compose-extra.yml files must look like:"
    echo '"image: ${X_IMAGE}"' ' where X_IMAGE is an environment variable that contains the docker image tag'
    echo
    echo "$INVALID_IMAGES"
    invalid=1
fi

VERSION_VARS="$(grep '^[[:space:]]\{1,\}image:' ${COMPOSE_FILES} | sed 's/^[^:]\{1,\}:[[:space:]]\{1,\}image: \${\([0-9A-Z_]\{1,\}\)_IMAGE[0-9A-Z_]*}$/\1_VERSION/' | sort | uniq | grep '^[^[:space:]]\{1,\}$')"

for var in $VERSION_VARS; do
    if ! grep -q "^export[[:space:]]\{1,\}${var}=" "${COMPOSE_DIR}"/components/*/default.env "${COMPOSE_DIR}"/optional-components/*/default.env ; then
        echo "Found invalid image and version definition in the birdhouse stack"
        echo "Image definition ${var%*_VERSION}_IMAGE exists but no version variable ${var} can be found"
        invalid=1
    fi
done

[ "$invalid" = '0' ] || exit 1
