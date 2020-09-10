#!/bin/sh -x

if [ -z "$SSL_CERTIFICATE" ]; then
    # Overridable
    SSL_CERTIFICATE="/home/vagrant/certkey.pem"
fi

if [ ! -f env.local ]; then
    cp env.local.example env.local
    cat <<EOF >> env.local

# override with values needed for vagrant
export SSL_CERTIFICATE='$SSL_CERTIFICATE'  # *absolute* path to the nginx ssl certificate, path and key bundle
export PAVICS_FQDN='${VM_HOSTNAME}.$VM_DOMAIN' # Fully qualified domain name of this Pavics installation
EOF

    if [ -n "$LETSENCRYPT_EMAIL" ]; then
    cat <<EOF >> env.local
export SUPPORT_EMAIL="$LETSENCRYPT_EMAIL"
EOF
    elif [ -n "$KITENAME" -a -n "$KITESUBDOMAIN" ]; then
    cat <<EOF >> env.local
export PAVICS_FQDN_PUBLIC="$KITESUBDOMAIN-$KITENAME"
export ALLOW_UNSECURE_HTTP="True"
EOF
    fi

else
    echo "existing env.local file, not overriding"
fi

if [ ! -f "$SSL_CERTIFICATE" ]; then
    . ./env.local
    if [ -n "$LETSENCRYPT_EMAIL" ]; then
        FORCE_CERTBOT_E2E=1 FORCE_CERTBOT_E2E_NO_START_PROXY=1 \
            deployment/certbotwrapper
    else
        openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout key.pem -out cert.pem \
            -subj "/C=CA/ST=Quebec/L=Montreal/O=RnD/CN=${VM_HOSTNAME}.$VM_DOMAIN"
        cp cert.pem "$SSL_CERTIFICATE"
        cat key.pem >> "$SSL_CERTIFICATE"
        if [ -z "$VERIFY_SSL" ]; then
            cat <<EOF >> env.local
export VERIFY_SSL="false"
EOF
        fi
    fi
else
    echo "existing '$SSL_CERTIFICATE' file, not overriding"
fi

./pavics-compose.sh up -d
