#!/bin/sh -x

# Those config files need to have proper ownership and permissions, else the
# deamon will not run.
deploy_config() {
    srcfile="$1"
    destfile="$2"
    cp -v "$srcfile" "$destfile"
    chown root:root "$destfile"
    chmod 644 "$destfile"
}


deploy_config /file/cron.d/logrotate /etc/cron.d/logrotate
deploy_config /file/logrotate.d/nginx /etc/logrotate.d/nginx

cron
