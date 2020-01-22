#!/bin/sh
# Script to automate local deployment process.
#
# Still have to ssh to target machine but at least this single script
# takes care of all the common steps for a standard deployment (see corner
# cases not handled below).
#
# One time Setup for a *private* PAVICS repository:
#
# * create a ssh deploy key (do not re-use your personal key)
#   `ssh-keygen -b 4096 -t rsa -f ~/.ssh/id_rsa_git_ssh_read_only` (no passphrase)
#
# * add the public key ~/.ssh/id_rsa_git_ssh_read_only.pub to the repo as read-only deploy key
#   see https://developer.github.com/v3/guides/managing-deploy-keys/#deploy-keys
#
# * if on host with git version less than 2.3 (no support for GIT_SSH_COMMAND),
#   have to configure your ~/.ssh/config  with the following:
#     Host github.com
#     IdentityFile ~/.ssh/id_rsa_git_ssh_read_only
#     UserKnownHostsFile /dev/null
#     StrictHostKeyChecking no
#
# * make sure your git remote uses ssh, and not https, like documented at:
#   https://help.github.com/en/github/using-git/changing-a-remotes-url#switching-remote-urls-from-https-to-ssh
#   running `git remote -v` should show this format: git@github.com:USERNAME/REPOSITORY.git
#   if https is used, fetching from the remote in the deployment script will not 
#   work because git will prompt for the username and password.
#
# In the case of a *public* repository, make sure your git remote url is using https, and not ssh
# because configuring an ssh key is not required and the connection will be refused if it's not correctly configured. 
# 
# Usage:
#
#   Just run this script pointing to the checkout repo and optionally the env.local file.
#
#   It will find the rest that it needs from the checkout repo.  Only external
#   depency is ~/.ssh/id_rsa_git_ssh_read_only.
#
# Corner cases not handled:
#
# * docker images using `latest` or `stable` tags
#
# * changes to env.local.example file that will need manual update to
#   env.local
#
# Improvement possible:
#
# * restart only affected containers.  Currently restarting all containers to
#   make sure any config files update that are volume-mount into the container
#   are re-read.  docker-compose is not aware of any changes outside of the
#   docker-compose.yml file.


GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
RED=$(tput setaf 1)
NORMAL=$(tput sgr0)


usage() {
    echo "USAGE: $0 <path to folder with docker-compose.yml file> [path to env.local]"
}

COMPOSE_DIR="$1"
ENV_LOCAL_FILE="$2"

if [ -z "$COMPOSE_DIR" ]; then
    echo "${RED}ERROR:${NORMAL} please provide path to PAVICS docker-compose dir." 1>&2
    usage
    exit 2
else
    shift
fi

if [ -z "$ENV_LOCAL_FILE" ]; then
    ENV_LOCAL_FILE="$COMPOSE_DIR/env.local"
else
    shift
fi

COMPOSE_DIR="`realpath "$COMPOSE_DIR"`"
REPO_ROOT="`realpath "$COMPOSE_DIR/.."`"

if [ ! -f "$COMPOSE_DIR/docker-compose.yml" -o \
     ! -f "$COMPOSE_DIR/pavics-compose.sh" ]; then
    echo "${RED}ERROR:${NORMAL} missing docker-compose.yml or pavics-compose.sh file in '$COMPOSE_DIR'" 1>&2
    exit 2
fi

if [ ! -f "$ENV_LOCAL_FILE" ]; then
    echo "${RED}ERROR:${NORMAL} env.local '$ENV_LOCAL_FILE' not found, please instantiate from '$COMPOSE_DIR/env.local.example'" 1>&2
    exit 2
fi

SSH_DEPLOY_KEY="$HOME/.ssh/id_rsa_git_ssh_read_only"

if [ ! -f "$SSH_DEPLOY_KEY" ]; then
    echo "${RED}ERROR:${NORMAL} '$SSH_DEPLOY_KEY' not found, please create it and set it up for this repo" 1>&2
    exit 2
fi

if [ -f "$COMPOSE_DIR/docker-compose.override.yml" ]; then
    echo "${YELLOW}WARNING:${NORMAL} docker-compose.override.yml found, should use EXTRA_CONF_DIRS in env.local instead"
fi

START_TIME="`date -Isecond`"
echo "deploy START_TIME=$START_TIME"

# Read AUTODEPLOY_EXTRA_REPOS
. $ENV_LOCAL_FILE

set -x

for adir in $COMPOSE_DIR $AUTODEPLOY_EXTRA_REPOS; do
    if [ -d "$adir" ]; then
        cd $adir

        # fail fast if unclean checkout
        if [ ! -z "`git status -u --porcelain`" ]; then
            echo "${RED}ERROR:${NORMAL} unclean repo '$adir'" 1>&2
            exit 1
        fi
    else
        echo "${YELLOW}WARNING:${NORMAL} extra repo '$adir' do not exist"
    fi
done

cd $COMPOSE_DIR

. ./common.env

# stop all to force reload any changed config that are volume-mount into the containers
./pavics-compose.sh stop

# this container is not managed by docker-compose, have to handle it manually
# rm and not just stop to force spawning newer image
docker stop jupyter-public
docker rm jupyter-public

# override git ssh command because this repo is private and need proper credentials
#
# https://git-scm.com/docs/git-config#Documentation/git-config.txt-sshvariant
export GIT_SSH_COMMAND="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o IdentityFile=$SSH_DEPLOY_KEY"

for adir in $COMPOSE_DIR $AUTODEPLOY_EXTRA_REPOS; do
    if [ -d "$adir" ]; then
        cd $adir

        # pull the current branch, so this deploy script supports any branches, not just master
        git pull
    else
        echo "${YELLOW}WARNING:${NORMAL} extra repo '$adir' do not exist"
    fi
done

cd $COMPOSE_DIR

# reload again after git pull because this file could be changed by the pull
. ./common.env

# restart everything, only changed containers will be destroyed and recreated
./pavics-compose.sh up -d

# immediately cache the new notebook image for faster startup by JupyterHub
docker pull $DOCKER_NOTEBOOK_IMAGE

# deploy new README.ipynb to Jupyter instance
docker run --rm --name deploy_README_ipynb \
    -v $DOCKER_JUPYTERHUB_USER_PERSISTENCE_VOLUME:/notebook_dir \
    -v $REPO_ROOT/docs/source/notebooks:/nb:ro \
    -u root \
    bash \
    bash -c "cp -v /nb/README.ipynb /notebook_dir/.; \
             chown root:root /notebook_dir/README.ipynb"

set +x

echo "
deploy finished START_TIME=$START_TIME
deploy finished   END_TIME=`date -Isecond`"


# vi: tabstop=8 expandtab shiftwidth=4 softtabstop=4
