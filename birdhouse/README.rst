Docker instructions
-------------------

Requirements:


* 
  Centos 7 or Ubuntu Bionic (18.04), other distros untested.

* 
  Hostname of Docker host must exist on the network.  Must use bridge
  networking if Docker host is a Virtual Machine.

* 
  User running ``pavics-compose.sh`` below must not be ``root`` but a regular user
  belonging to the ``docker`` group.

* 
  Install latest docker-ce and docker-compose for the chosen distro (not the
  version from the distro).

To run ``docker-compose`` for PAVICS, the `pavics-compose.sh <birdhouse/pavics-compose.sh>`_ wrapper script must be used.
This script will source the ``env.local`` file, apply the appropriate variable substitutions on all the configuration files
".template", and run ``docker-compose`` with all the command line arguments given to `pavics-compose.sh <birdhouse/pavics-compose.sh>`_.
See `env.local.example <birdhouse/env.local.example>`_ for more details on what can go into the ``env.local`` file.

If the file `env.local` is somewhere else, symlink it here, next to `docker-compose.yml <birdhouse/docker-compose.yml>`_ because many scripts assume this location.

To follow infrastructure-as-code, it is encouraged to source control the above
`env.local` file and any override needed to customized this PAVICS deployment
for your organization.  For an example of possible override, see how the `emu service <birdhouse/optional-components/emu/docker-compose-extra.yml>`_
(`README <birdhouse/optional-components/README.md>`_) can be optionally added to the deployment via the `override mechanism <https://docs.docker.com/compose/extends/>`_.
Ouranos specific override can be found in this `birdhouse-deploy-ouranos <https://github.com/bird-house/birdhouse-deploy-ouranos>`_ repo.

Suggested deployment layout:

.. code-block::

   ├── birdhouse-deploy/  # this repo
   │   ├── birdhouse/
   │   │   ├── env.local  # relative symlink to env.local.real below
   │   │   ├── pavics-compose.sh
   │   │   ├── (...)
   ├── private-config/    # your private config and override: sibling level of this repo
   │   ├── docker-compose-extra.yml
   │   ├── env.local.real
   │   ├── .git/

The automatic deployment is able to handle multiple repos, so will trigger if
this repo or your private-personalized-config repo changes, giving you
automated continuous deployment.  See the continuous deployment setup section
below and the variable ``AUTODEPLOY_EXTRA_REPOS`` in `env.local.example <birdhouse/env.local.example>`_.

The automatic deployment of the PAVICS platform, of the Jupyter tutorial
notebooks and of the automatic deployment mechanism itself can all be
enabled by following the `scheduling instructions <birdhouse/components/README.rst#scheduler>`_.

Resource usage monitoring (CPU, memory, ..) and alerting for the host and each
of the containers can be enabled by following the `monitoring instructions <birdhouse/components/README.rst#monitoring>`_.

To launch all the containers, use the following command:

.. code-block::

   ./pavics-compose.sh up -d

If you get a ``'No applicable error code, please check error log'`` error from the WPS processes, please make sure that the WPS databases exists in the
postgres instance. See `create-wps-pgsql-databases.sh <birdhouse/scripts/create-wps-pgsql-databases.sh>`_.

Manual steps post deployment
----------------------------

Change geoserver default admin password
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


* 
  Go to
  ``https://<PAVICS_FQDN>/geoserver/web/wicket/bookmarkable/org.geoserver.security.web.UserGroupRoleServicesPage`` (Security -> Users, Groups, and Roles)

* 
  Login using the default username ``admin`` and default password ``geoserver``.

* 
  Click on tab "Users/Groups".

* 
  Click on user "admin".

* 
  Change the password.

* 
  Click "Save".

Create public demo user in Magpie for JupyterHub login
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use `create-magpie-users <birdhouse/scripts/create-magpie-users>`_ or follow manual
instructions below.

``config.yml`` file if using ``create-magpie-users``\ :

.. code-block::

   users:
     - username: < value of JUPYTER_DEMO_USER in `env.local` >
       password: < you decide, at least 12 in length >
       email: < anything is fine >
       group: anonymous

Manual instructions:


* 
  Go to
  ``https://<PAVICS_FQDN>/magpie/ui/login`` and login with the ``admin`` user. The password should be in ``env.local``.

* 
  Then go to ``https://<PAVICS_FQDN>/magpie/ui/users/add``.

* 
  Fill in:

  * User name: <value of JUPYTER_DEMO_USER in ``env.local``\ >
  * Email: < anything is fine >
  * Password: < you decide >
  * User group: ``anonymous``

* 
  Click "Add User".

Optional: prepare instance to run automated end-to-end test suite
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An end-to-end integration test suite is available at
https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests with pre-configured
Jenkins at https://github.com/Ouranosinc/jenkins-config.

For that test suite to pass, run the script
`bootstrap-instance-for-testsuite <birdhouse/scripts/bootstrap-instance-for-testsuite>`_
to prepare your new instance.  Further documentation inside the script.

Optional component
`all-public-access <birdhouse/optional-components#give-public-access-to-all-resources-for-testing-purposes>`_
also need to be enabled in ``env.local``.

ESGF login is also needed for
https://github.com/Ouranosinc/pavics-sdi/blob/master/docs/source/notebooks/esgf-dap.ipynb
part of test suite.  ESGF credentails can be given to Jenkins via
https://github.com/Ouranosinc/jenkins-config/blob/aafaf6c33ea60faede2a32850604c07c901189e8/env.local.example#L11-L13

The canarie monitoring link
``https://<PAVICS_FQDN>/canarie/node/service/stats`` can be used to confirm the
instance is ready to run the automated end-to-end test suite.  That link should
return the HTTP response code ``200``.

Vagrant instructions
--------------------

Vagrant allows us to quickly spin up a VM to easily reproduce the runtime
environment for testing or to have multiple flavors of PAVICS with slightly
different combinations of the parts all running simultaneously in their
respective VM, allowing us to see the differences in behavior.

See `vagrant_variables.yml.example <../vagrant_variables.yml.example>`_ for what's
configurable with Vagrant.

If using Centos box, follow `disk-resize <birdhouse/vagrant-utils/disk-resize>`_ after
first ``vagrant up`` failure due to disk full.  Then ``vagrant reload && vagrant
provision`` to continue.  If using Ubuntu box, no manual steps required,
everything just works.

Install `VirtualBox <https://www.virtualbox.org/wiki/Downloads>`_\ , both the
platform and the extension pack, and
`Vagrant <https://www.vagrantup.com/downloads.html>`_.

One time setup:

.. code-block::

   # Clone this repo and checkout the desired branch.

   # Follow instructions and fill up infos in vagrant_variables.yml
   cd ..  # to the folder having the Vagrantfile
   cp vagrant_variables.yml.example vagrant_variables.yml

Starting and managing the lifecycle of the VM:

.. code-block::

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

   # power-off VM
   vagrant halt

   # delete VM
   vagrant destroy

   # reload Vagrant config if vagrant_variables.yml or Vagrantfile changes
   vagrant reload

   # provision again (because all subsequent vagrant up won't provision again)
   # useful to test all provisioning scripts or to bring a VM at unknown state,
   # maybe because it was provisioned too long ago, to the latest state.
   # not needed normally during tight development loop
   vagrant provision

Tagging policy
--------------

We are trying to follow the standard of `semantic versioning <https://semver.org/>`_.

The standard is for one application.  Here we have a collection of several apps
with different versions and we want to track which combination of versions works
together.  So we need a slight modification to the definition of the standard.

Given a version number MAJOR.MINOR.PATCH, increment the:


#. 
   MAJOR version when the API or user facing UI changes that requires
   significant documentation update and/or re-training of the users.  Also
   valid when a big milestone has been reached (ex: DACCS is released).

#. 
   MINOR version when we add new components or update existing components
   that also require change to other existing components (ex: new Magpie that
   also force Twitcher and/or Frondend update) or the change to the existing
   component is a major one (ex: major refactoring of Twitcher, big merge
   with corresponding upstream component from birdhouse project).

#. 
   PATCH version when we update existing components without impact on other
   existing components and the change is a minor change for the existing
   component.
