#!/bin/sh
# Script to deploy the automated unattended continuous deployment.
#
#
# Will deploy:
#
# * cron job to periodically check if a deployment is needed
#   (/etc/cron.d/PAVICS-deploy), update check frequency here
#
# * script called by cron job (/usr/local/sbin/triggerdeploy.sh)
#
# * deploy check logs can be found in /var/log/PAVICS/autodeploy.log
#
#
# 2 cron frequency presets are available:
#
# * daily: check nighly and perform deployment if needed, intended for
#   production to not deploy during the day and disrupt users
#
# * 5-mins: check every 5 mins and perform deployment if needed, this option
#   provides real continuous deployment
#
# Possibility to set any cron frequencies, read code below.
#

usage() {
    echo "USAGE: $0 pavics-checkout owner-pavics-checkout [daily | 5-mins]"
}

if [ -z "$1" ]; then
    echo "ERROR: please supply mandatory arguments" 1>&2
    usage
    exit 2
fi


REPO_ROOT="`realpath "$1"`"; shift  # path to PAVICS checkout
REPO_OWNER="$1"; shift  #  user owning (have write access) the PAVICS checkout
CRON_FREQUENCY="$1"

# defaults, overridable
if [ -z "$CRON_FREQUENCY_TXT" ]; then
    CRON_FREQUENCY_TXT="daily at 5:07 AM"
fi
if [ -z "$CRON_SCHEDULE" ]; then
    CRON_SCHEDULE="7 5 * * *"
fi

# presets
if [ x"$CRON_FREQUENCY" = x"5-mins" ]; then
    CRON_FREQUENCY_TXT="every 5 mins"
    CRON_SCHEDULE="*/5 * * * *"
elif [ x"$CRON_FREQUENCY" = x"daily" ]; then
    CRON_FREQUENCY_TXT="daily at 5:07 AM"
    CRON_SCHEDULE="7 5 * * *"
elif [ -n "$CRON_FREQUENCY" ]; then
    echo "ERROR: unknown cron frequency preset '$CRON_FREQUENCY'" 1>&2
    usage
    exit 2
fi

if [ ! -e "$REPO_ROOT/birdhouse/deployment/triggerdeploy.sh" ]; then
    echo "ERROR: bad/wrong pavics-checkout '$REPO_ROOT' " 1>&2
    usage
    exit 2
fi


set -x

sudo cp -v $REPO_ROOT/birdhouse/deployment/triggerdeploy.sh /usr/local/sbin/


CRON_FILE="/etc/cron.d/PAVICS-deploy"

export CRON_FREQUENCY_TXT="$CRON_FREQUENCY_TXT"
export CRON_SCHEDULE="$CRON_SCHEDULE"
export OWNER_PAVICS_CHECKOUT="$REPO_OWNER"
export PATH_TO_PAVICS_CHECKOUT="$REPO_ROOT"

[ ! -d "/var/log/PAVICS" ] && echo "WARNING: The logging directory doesn't exist. Run 'install-logrotate-config'."

cat $REPO_ROOT/birdhouse/deployment/cron.template | envsubst | sudo tee $CRON_FILE
sudo chown root:root $CRON_FILE
sudo chmod 644 $CRON_FILE
