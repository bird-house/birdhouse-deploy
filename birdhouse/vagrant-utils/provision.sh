#!/bin/sh -x

cd /vagrant/birdhouse
vagrant-utils/install-docker.sh
vagrant-utils/configure-pavics.sh
vagrant-utils/configure-pagekite
deployment/install-deploy-notebook /vagrant
deployment/install-logrotate-config /vagrant vagrant
