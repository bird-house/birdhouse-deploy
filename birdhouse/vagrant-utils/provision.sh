#!/bin/sh -x

cd /vagrant/birdhouse || exit 1
vagrant-utils/install-docker.sh
vagrant-utils/configure-birdhouse.sh
vagrant-utils/configure-pagekite
