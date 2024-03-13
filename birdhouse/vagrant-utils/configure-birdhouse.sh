#!/bin/sh -x

if [ -f env.local ]; then
    # Get BIRDHOUSE_SSL_CERTIFICATE from existing env.local.
    . ./env.local
fi

if [ -z "$BIRDHOUSE_SSL_CERTIFICATE" ]; then
    # Overridable by existing env.local or existing env var.
    BIRDHOUSE_SSL_CERTIFICATE="/home/vagrant/certkey.pem"
fi

if [ ! -f env.local ]; then
    cp env.local.example env.local
    cat <<EOF >> env.local

# override with values needed for vagrant
export BIRDHOUSE_SSL_CERTIFICATE='$BIRDHOUSE_SSL_CERTIFICATE'  # *absolute* path to the nginx ssl certificate, path and key bundle
export BIRDHOUSE_FQDN='${VM_HOSTNAME}.$VM_DOMAIN' # Fully qualified domain name of this Birdhouse installation
EOF

    if [ -n "$LETSENCRYPT_EMAIL" ]; then
    cat <<EOF >> env.local
export BIRDHOUSE_SUPPORT_EMAIL="$LETSENCRYPT_EMAIL"

# Modify schedule so test systems do not hit LetsEncrypt at the same time as
# prod systems to avoid loading LetsEncrypt server (be a nice netizen).
RENEW_LETSENCRYPT_SSL_SCHEDULE="22 9 * * *"  # UTC

# This repo will be volume-mount at /vagrant so can not go higher.
RENEW_LETSENCRYPT_SSL_NUM_PARENTS_MOUNT="/"

# Only source if file exist.  Allow for config file to be backward-compat with
# older version of the repo where the .env file do not exist yet.
# Keep this sourcing of renew_letsencrypt_ssl_cert_extra_job.env after
# latest definition of BIRDHOUSE_SSL_CERTIFICATE because it needs the valid value of
# BIRDHOUSE_SSL_CERTIFICATE.
if [ -f "$PWD/components/scheduler/renew_letsencrypt_ssl_cert_extra_job.env" ]; then
    . $PWD/components/scheduler/renew_letsencrypt_ssl_cert_extra_job.env
fi
EOF
    elif [ -n "$KITENAME" -a -n "$KITESUBDOMAIN" ]; then
    cat <<EOF >> env.local
export BIRDHOUSE_FQDN_PUBLIC="$KITESUBDOMAIN-$KITENAME"
export BIRDHOUSE_ALLOW_UNSECURE_HTTP="True"
EOF
    fi

else
    echo "existing env.local file, not overriding"
fi

if [ ! -f "$BIRDHOUSE_SSL_CERTIFICATE" ]; then
    . ./env.local
    if [ -n "$LETSENCRYPT_EMAIL" ]; then

        if [ -n "$VM_DEFAULT_GATEWAY" ]; then
            # Make VM visible for LetsEncrypt.
            sudo route add default gw "$VM_DEFAULT_GATEWAY"
        fi

        FORCE_CERTBOT_E2E=1 FORCE_CERTBOT_E2E_NO_START_PROXY=1 \
            deployment/certbotwrapper
    else
        openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout key.pem -out cert.pem \
            -subj "/C=CA/ST=Quebec/L=Montreal/O=RnD/CN=${VM_HOSTNAME}.$VM_DOMAIN"
        cp cert.pem "$BIRDHOUSE_SSL_CERTIFICATE"
        cat key.pem >> "$BIRDHOUSE_SSL_CERTIFICATE"
        if [ -z "$BIRDHOUSE_VERIFY_SSL" ]; then
            cat <<EOF >> env.local
export BIRDHOUSE_VERIFY_SSL="false"
EOF
        fi
    fi
else
    echo "existing '$BIRDHOUSE_SSL_CERTIFICATE' file, not overriding"
fi

export PATH="$(readlink -f ../bin):$PATH"

birdhouse compose up -d
