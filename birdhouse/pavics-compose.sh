#!/bin/sh

YELLOW=$(tput setaf 3)
RED=$(tput setaf 1)
NORMAL=$(tput sgr0)

# list of all variables to be substituted in templates
VARS='
  $PAVICS_FQDN
  $DOC_URL
  $MAGPIE_SECRET
  $MAGPIE_ADMIN_USERNAME
  $MAGPIE_ADMIN_PASSWORD
  $TWITCHER_PROTECTED_PATH
  $PHOENIX_PASSWORD
  $PHOENIX_PASSWORD_HASH
  $TOMCAT_NCWMS_PASSWORD
  $SUPPORT_EMAIL
  $CMIP5_THREDDS_ROOT
  $JUPYTERHUB_ADMIN_USERS
  $CATALOG_USERNAME
  $CATALOG_PASSWORD
  $CATALOG_THREDDS_SERVICE
  $POSTGRES_PAVICS_USERNAME
  $POSTGRES_PAVICS_PASSWORD
  $POSTGRES_MAGPIE_USERNAME
  $POSTGRES_MAGPIE_PASSWORD
'

# list of vars to be substituted in template but they do not have to be set in
# env.local
OPTIONAL_VARS='
  $PAVICS_FQDN_PUBLIC
  $INCLUDE_FOR_PORT_80
  $ENABLE_JUPYTERHUB_MULTI_NOTEBOOKS
  $EXTRA_PYWPS_CONFIG
  $THREDDS_ORGANIZATION
  $GITHUB_CLIENT_ID
  $GITHUB_CLIENT_SECRET
  $MAGPIE_DB_NAME
  $VERIFY_SSL
  $JUPYTER_DEMO_USER
  $JUPYTER_LOGIN_BANNER_TOP_SECTION
  $JUPYTER_LOGIN_BANNER_BOTTOM_SECTION
  $AUTODEPLOY_EXTRA_REPOS_AS_DOCKER_VOLUMES
  $AUTODEPLOY_PLATFORM_FREQUENCY
  $AUTODEPLOY_NOTEBOOK_FREQUENCY
'

# we switch to the real directory of the script, so it still works when used from $PATH
# tip: ln -s /path/to/pavics-compose.sh ~/bin/
cd $(dirname $(readlink -f $0 || realpath $0))

. ./common.env

# we source local configs, if present
# we don't use usual .env filename, because docker-compose uses it
[ -f env.local ] && . ./env.local

for i in ${VARS}
do
  v="${i}"
  if [ -z "`eval "echo ${v}"`" ]
  then
    echo "${RED}Error${NORMAL}: Required variable $v is not set. Check env.local file."
    exit 1
  fi
done

if [ ! -f docker-compose.yml ]
then
  echo "Error, this script must be ran from the folder containing the docker-compose.yml file"
  exit 1
fi

## check fails when root access is required to access this file.. workaround possible by going through docker daemon... but
# will add delay
# if [ ! -f $SSL_CERTIFICATE ]
# then
#   echo "Error, SSL certificate file $SSL_CERTIFICATE is missing"
#   exit 1
# fi

TIMEWAIT_REUSE=$(/sbin/sysctl -n  net.ipv4.tcp_tw_reuse)
if [ ${TIMEWAIT_REUSE} -eq 0 ]
then
  echo "${YELLOW}Warning:${NORMAL} the sysctl net.ipv4.tcp_tw_reuse is not enabled"
  echo "         It it suggested to set it to 1, otherwise the pavicscrawler may fail"
fi

if [ -z "$PAVICS_FQDN_PUBLIC" ]; then
  # default value before instantiating template configs
  export PAVICS_FQDN_PUBLIC="$PAVICS_FQDN"
fi

if [ x"$ALLOW_UNSECURE_HTTP" = x"True" ]; then
  export INCLUDE_FOR_PORT_80="include /etc/nginx/conf.d/all-services.include;"
else
  export INCLUDE_FOR_PORT_80="include /etc/nginx/conf.d/redirect-to-https.include;"
fi

if [ -z "$THREDDS_ORGANIZATION" ]; then
  # default value before instantiating template configs
  export THREDDS_ORGANIZATION="Birdhouse"
fi

if [ -z "$MAGPIE_DB_NAME" ]; then
  # default value before instantiating template configs
  export MAGPIE_DB_NAME="magpiedb"
fi

if [ -z "$VERIFY_SSL" ]; then
  # default value before instantiating template configs
  export VERIFY_SSL="true"
fi

export AUTODEPLOY_EXTRA_REPOS_AS_DOCKER_VOLUMES=""
for adir in $AUTODEPLOY_EXTRA_REPOS; do
  # 4 spaces in front of '--volume' is important
  AUTODEPLOY_EXTRA_REPOS_AS_DOCKER_VOLUMES="$AUTODEPLOY_EXTRA_REPOS_AS_DOCKER_VOLUMES
    --volume ${adir}:${adir}:rw"
done
export AUTODEPLOY_EXTRA_REPOS_AS_DOCKER_VOLUMES

# we apply all the templates
find ./config ./components ./optional-components -name '*.template' |
  while read FILE
  do
    DEST=${FILE%.template}
    cat ${FILE} | envsubst "$VARS" | envsubst "$OPTIONAL_VARS" > ${DEST}
  done

if [ x"$1" = x"up" ]; then
  # this is external in docker-compose.yml so have to create here
  # no error if already exist, just an error message
  docker network create jupyterhub_network

  # no error if already exist
  # create externally so nothing will delete these data volume automatically
  docker volume create jupyterhub_data_persistence  # jupyterhub db and cookie secret
  docker volume create thredds_persistence  # logs, cache
fi

COMPOSE_CONF_LIST="-f docker-compose.yml"
for adir in ${EXTRA_CONF_DIRS}; do
  if [ -f "$adir/docker-compose-extra.yml" ]; then
    COMPOSE_CONF_LIST="${COMPOSE_CONF_LIST} -f $adir/docker-compose-extra.yml"
  fi
done
echo "COMPOSE_CONF_LIST=${COMPOSE_CONF_LIST}"

# the PROXY_SECURE_PORT is a little trick to make the compose file invalid without the usage of this wrapper script
PROXY_SECURE_PORT=443 HOSTNAME=${PAVICS_FQDN} docker-compose ${COMPOSE_CONF_LIST} $*
ERR=$?

# execute post-compose function if exists and no error occurred
type post-compose 2>&1 | grep 'post-compose is a function' > /dev/null
if [ $? -eq 0 ]
then
  [ ${ERR} -gt 0 ] && { echo "Error occurred with docker-compose, not running post-compose"; exit $?; }
  post-compose $*
fi


while [ $# -gt 0 ]
do
  if [ x"$1" = x"up" ]; then
    # we restart the proxy after an up to make sure nginx continue to work if any container IP address changes
    PROXY_SECURE_PORT=443 HOSTNAME=${PAVICS_FQDN} docker-compose restart proxy

    # run postgres post-startup setup script
    postgres_id=$(PROXY_SECURE_PORT=443 HOSTNAME=${PAVICS_FQDN} docker-compose ${COMPOSE_CONF_LIST} ps -q postgres)
    if [ ! -z "$postgres_id" ]; then
      docker exec ${postgres_id} /postgres-setup.sh
    fi

    # Note: This command should stay last, as it can take a while depending on network and drive speeds
    # immediately cache the new notebook image for faster startup by JupyterHub
    docker pull ${DOCKER_NOTEBOOK_IMAGE}
  fi
  shift
done


# vi: tabstop=8 expandtab shiftwidth=2 softtabstop=2
