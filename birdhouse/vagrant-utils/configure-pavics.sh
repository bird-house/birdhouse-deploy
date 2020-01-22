#!/bin/sh -x

if [ ! -f certkey.pem ]; then
    openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout key.pem -out cert.pem \
        -subj "/C=CA/ST=Quebec/L=Montreal/O=RnD/CN=${VM_HOSTNAME}.$VM_DOMAIN"
    cp cert.pem certkey.pem
    cat key.pem >> certkey.pem
    USE_SELF_SIGN_SSL="true"
else
    echo "existing certkey.pem file, not overriding"
fi

if [ ! -f env.local ]; then
    cp env.local.example env.local
    cat <<EOF >> env.local
# override with values needed for vagrant
export SSL_CERTIFICATE='./certkey.pem'  # path to the nginx ssl certificate, path and key bundle
export PAVICS_FQDN='${VM_HOSTNAME}.$VM_DOMAIN' # Fully qualified domain name of this Pavics installation
EOF
    if [ -n "$KITENAME" -a -n "$KITESUBDOMAIN" ]; then
    cat <<EOF >> env.local
export PAVICS_FQDN_PUBLIC="$KITESUBDOMAIN-$KITENAME"
export ALLOW_UNSECURE_HTTP="True"
EOF
    fi
    if [ x"$USE_SELF_SIGN_SSL" = xtrue ]; then
    cat <<EOF >> env.local
export VERIFY_SSL="false"
EOF
    fi
else
    echo "existing env.local file, not overriding"
fi

./pavics-compose.sh up -d
