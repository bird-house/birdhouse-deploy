#!/bin/sh
# Script to automate local deployment process.
#
# Log to "/var/log/PAVICS/autodeploy.log" if AUTODEPLOY_SILENT is not empty.
#
# Still have to ssh to target machine but at least this single script
# takes care of all the common steps for a standard deployment (see corner
# cases not handled below).
#
# One time Setup for each *private* repository (not applicable for *public* repos):
#
# * create a ssh deploy key (do not re-use your personal key)
#   `ssh-keygen -b 4096 -t rsa -f ~/.ssh/{repo-name}_deploy_key` (no passphrase)
#
# * add the public key ~/.ssh/{repo-name}_deploy_key.pub to the repo as read-only deploy key
#   see https://developer.github.com/v3/guides/managing-deploy-keys/#deploy-keys
#
# * if on host with git version less than 2.3 (no support for GIT_SSH_COMMAND),
#   have to configure your ~/.ssh/config  with the following:
#     Host github.com
#     IdentityFile ~/.ssh/{repo-name}_deploy_key
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
#   dependencies are the multiple ~/.ssh/{repo-name}_deploy_key (one deploy key
#   for each repo).
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

if [ ! -z "$AUTODEPLOY_SILENT" ]; then
    LOG_FILE="/var/log/PAVICS/autodeploy.log"
    exec >>$LOG_FILE 2>&1
fi

usage() {
    echo "USAGE: $0 <path to folder with docker-compose.yml file> [path to env.local]"
}

COMPOSE_DIR="$1"
ENV_LOCAL_FILE="$2"

if [ -z "$COMPOSE_DIR" ]; then
    echo "ERROR: please provide path to PAVICS docker-compose dir." 1>&2
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
    echo "ERROR: missing docker-compose.yml or pavics-compose.sh file in '$COMPOSE_DIR'" 1>&2
    exit 2
fi

if [ ! -f "$ENV_LOCAL_FILE" ]; then
    echo "ERROR: env.local '$ENV_LOCAL_FILE' not found, please instantiate from '$COMPOSE_DIR/env.local.example'" 1>&2
    exit 2
fi

if [ -f "$COMPOSE_DIR/docker-compose.override.yml" ]; then
    echo "WARNING: docker-compose.override.yml found, should use EXTRA_CONF_DIRS in env.local instead"
fi

# Setup COMPOSE_DIR and PWD for sourcing env.local.
# Prevent un-expected difference when this script is run inside autodeploy
# container and manually from the host.
cd $COMPOSE_DIR

START_TIME="`date -Isecond`"
echo "deploy START_TIME=$START_TIME"

. "$COMPOSE_DIR/read-configs.include.sh"

# Read AUTODEPLOY_EXTRA_REPOS
read_basic_configs_only

set -x

for adir in $COMPOSE_DIR $AUTODEPLOY_EXTRA_REPOS; do
    if [ -d "$adir" ]; then
        cd $adir

        # fail fast if unclean checkout
        if [ ! -z "`git status -u --porcelain`" ]; then
            echo "ERROR: unclean repo '$adir'" 1>&2
            exit 1
        fi
    else
        echo "WARNING: extra repo '$adir' do not exist"
    fi
done

cd $COMPOSE_DIR

read_basic_configs_only

# stop all to force reload any changed config that are volume-mount into the containers
./pavics-compose.sh stop

for adir in $COMPOSE_DIR $AUTODEPLOY_EXTRA_REPOS; do
    if [ -d "$adir" ]; then
        cd $adir

        EXTRA_REPO="`git rev-parse --show-toplevel`"
        DEPLOY_KEY="$AUTODEPLOY_DEPLOY_KEY_ROOT_DIR/`basename "$EXTRA_REPO"`_deploy_key"
        DEFAULT_DEPLOY_KEY="$AUTODEPLOY_DEPLOY_KEY_ROOT_DIR/id_rsa_git_ssh_read_only"
        if [ ! -e "$DEPLOY_KEY" -a -e "$DEFAULT_DEPLOY_KEY" ]; then
            DEPLOY_KEY="$DEFAULT_DEPLOY_KEY"
        fi

        export GIT_SSH_COMMAND=""  # git ver 2.3+
        if [ -e "$DEPLOY_KEY" ]; then
            # override git ssh command for private repos only
            #
            # https://git-scm.com/docs/git-config#Documentation/git-config.txt-sshvariant
            export GIT_SSH_COMMAND="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o IdentityFile=$DEPLOY_KEY"
        else
            unset GIT_SSH_COMMAND
        fi

        # pull the current branch, so this deploy script supports any branches, not just master
        git pull
    else
        echo "WARNING: extra repo '$adir' do not exist"
    fi
done

cd $COMPOSE_DIR

# reload again after git pull because this file could be changed by the pull
. "$COMPOSE_DIR/read-configs.include.sh"

# reload again after default.env since env.local can override default.env
# (ex: JUPYTERHUB_USER_DATA_DIR)
read_basic_configs_only

# restart everything, only changed containers will be destroyed and recreated
./pavics-compose.sh up -d

set +x

echo "
deploy finished START_TIME=$START_TIME
deploy finished   END_TIME=`date -Isecond`"


# vi: tabstop=8 expandtab shiftwidth=4 softtabstop=4
