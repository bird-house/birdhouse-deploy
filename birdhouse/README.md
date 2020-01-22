## Docker instructions

Requirements:

* Centos 7 or Ubuntu Bionic (18.04), other distros untested.

* Hostname of Docker host must exist on the network.  Must use bridge
  networking if Docker host is a Virtual Machine.

* User running `pavics-compose.sh` below must not be `root` but a regular user
  belonging to the `docker` group.

* Install latest docker-ce and docker-compose for the chosen distro (not the
  version from the distro).

To run `docker-compose` for PAVICS, the [`pavics-compose.sh`](pavics-compose.sh) wrapper script must be used.
This script will source the `env.local` file, apply the appropriate variable substitutions on all the configuration files ".template", and run `docker-compose` with all the command line arguments given to `pavics-compose.sh`. See [`env.local.example`](env.local.example) for more details on what can go into the `env.local` file.

If the file `env.local` is somewhere else, symlink it here, next to
`docker-compose.yml` because many scripts assume this location.

To follow infrastructure-as-code, it is encouraged to source control the above
`env.local` file and any override needed to customized this PAVICS deployment
for your organization.  For an example of possible override, see how the [emu
service](optional-components/emu/docker-compose-extra.yml)
([README](optional-components/README.md)) can be optionally added to the
deployment via the [override
mechanism](https://docs.docker.com/compose/extends/).

The automatic deployment is able to handle multiple repos, so will trigger if
this repo or your private-personalized-config repo changes, giving you
automated continuous deployment.  See the continuous deployment setup section
below and the variable `AUTODEPLOY_EXTRA_REPOS` in
[`env.local.example`](env.local.example).

To launch all the containers, use the following command:
```
./pavics-compose.sh up -d
```

If you get a `'No applicable error code, please check error log'` error from the WPS processes, please make sure that the WPS databases exists in the
postgres instance. See [`scripts/create-wps-pgsql-databases.sh`](scripts/create-wps-pgsql-databases.sh).


## Manual steps post deployment

Change geoserver default admin password:

* Go to
  https://<PAVICS_HOST>/geoserver/web/wicket/bookmarkable/org.geoserver.security.web.UserGroupRoleServicesPage (Security -> Users, Groups, and Roles)

* Login using the default username `admin` and password `geoserver`.

* Click on tab "Users/Groups".

* Click on user "admin".

* Change the password.

* Click "Save".


## Mostly automated unattended continuous deployment

Automated unattended continuous deployment means if code change in the checkout
of this repo, on the same currently checkout branch (ex: config changes,
`docker-compose.yml` changes) a deployment will be performed automatically
without human intervention.

The trigger for the deployment is new code change on the server on the current
branch (PR merged, push).  New code change locally will not trigger deployment
so local development workflow is also supported.

Note: there are still cases where a human intervention is needed.  See note in
script [`deployment/deploy.sh`](deployment/deploy.sh).

Configure logrotate for all following automations to prevent disk full:
```
deployment/install-logrotate-config .. $USER
```

To enable continuous deployment of PAVICS:

```
deployment/install-automated-deployment.sh .. $USER [daily|5-mins]
# read the script for more options/details
```

If you want to manually force a deployment of PAVICS (note this might not use
latest version of deploy.sh script):
```
deployment/deploy.sh .
# read the script for more options/details
```

To enable continuous deployment of tutorial Jupyter notebooks:

```
deployment/install-deploy-notebook .. $USER
# read the script for more details
```

To trigger tutorial Jupyter notebooks deploy manually:
```
# configure logrotate before because this script will log to
# /var/log/PAVICS/notebookdeploy.log

deployment/trigger-deploy-notebook
# read the script for more details
```


## Vagrant instructions

Vagrant allows us to quickly spin up a VM to easily reproduce the runtime
environment for testing or to have multiple flavors of PAVICS with slightly
different combinations of the parts all running simultaneously in their
respective VM, allowing us to see the differences in behavior.

See [`vagrant_variables.yml.example`](../vagrant_variables.yml.example) for what's
configurable with Vagrant.

Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads), both the
platform and the extension pack, and
[Vagrant](https://www.vagrantup.com/downloads.html).

One time setup:
```
# Clone this repo and checkout the desired branch.

# Follow instructions and fill up infos in vagrant_variables.yml
cd ..  # to the folder having the Vagrantfile
cp vagrant_variables.yml.example vagrant_variables.yml
```

Starting and managing the lifecycle of the VM:
```
# start everything, this is the only command needed to bring up the entire
# PAVICS platform
vagrant up

# get bridged IP address
vagrant ssh -c "ip addr show enp0s8|grep 'inet '"

# get inside the VM
# useful to manage the PAVICS platform as if Vagrant is not there
# and use pavics-compose.sh as before
# ex: cd /vagrant/birdhouse; ./pavics-compose.sh ps
vagrant ssh

# poweroff VM
vagrant halt

# delete VM
vagrant destroy

# reload Vagrant config if vagrant_variables.yml or Vagrantfile changes
vagrant reload

# provision again (because all subsequent vagrant up won't provision again)
# useful to test all provisionning scripts or to bring a VM at unknown state,
# maybe because it was provisioned too long ago, to the latest state.
# not needed normally during tight development loop
vagrant provision
```


## Tagging policy

We are trying to follow the standard of [semantic versioning](https://semver.org/).

The standard is for one application.  Here we have a collection of several apps
with different versions and we want to track which combination of versions works
together.  So we need a slight modification to the definition of the standard.

Given a version number MAJOR.MINOR.PATCH, increment the:

  1. MAJOR version when the API or user facing UI changes that requires
     significant documentation update and/or re-training of the users.  Also
     valid when a big milestone has been reached (ex: DACCS is released).

  1. MINOR version when we add new components or update existing components
     that also require change to other existing components (ex: new Magpie that
     also force Twitcher and/or Frondend update) or the change to the existing
     component is a major one (ex: major refactoring of Twitcher, big merge
     with corresponding upstream component from birdhouse project).

  1. PATCH version when we update existing components without impact on other
     existing components and the change is a minor change for the existing
     component.
