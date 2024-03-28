#!/bin/sh -x

cd /vagrant/birdhouse
vagrant-utils/install-docker.sh
vagrant-utils/configure-birdhouse.sh
vagrant-utils/configure-pagekite
