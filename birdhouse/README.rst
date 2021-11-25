.. contents::


Docker instructions
-------------------

Requirements:

* Centos 7 or Ubuntu Bionic (18.04), other distros untested.

* Hostname of Docker host must exist on the network.  Must use bridge
  networking if Docker host is a Virtual Machine.

* User running ``pavics-compose.sh`` below must not be ``root`` but a regular user
  belonging to the ``docker`` group.

* Install latest docker-ce and docker-compose for the chosen distro (not the
  version from the distro).

To run ``docker-compose`` for PAVICS, the `pavics-compose.sh <pavics-compose.sh>`_ (:download:`download </birdhouse/pavics-compose.sh>`) wrapper script must be used.
This script will source the ``env.local`` file, apply the appropriate variable substitutions on all the configuration files
".template", and run ``docker-compose`` with all the command line arguments given to `pavics-compose.sh <pavics-compose.sh>`_ (:download:`download </birdhouse/pavics-compose.sh>`).
See `env.local.example <env.local.example>`_ (:download:`download </birdhouse/env.local.example>`) for more details on what can go into the ``env.local`` file.

If the file `env.local` is somewhere else, symlink it here, next to `docker-compose.yml <docker-compose.yml>`_ (:download:`download </birdhouse/docker-compose.yml>`) because many scripts assume this location.

To follow infrastructure-as-code, it is encouraged to source control the above
`env.local` file and any override needed to customized this PAVICS deployment
for your organization.  For an example of possible override, see how the `emu service <optional-components/emu/docker-compose-extra.yml>`_ (:download:`download </birdhouse/optional-components/emu/docker-compose-extra.yml>`)
(`README <optional-components/README.rst#emu-wps-service-for-testing>`_) can be optionally added to the deployment via the `override mechanism <https://docs.docker.com/compose/extends/>`_.
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
below and the variable ``AUTODEPLOY_EXTRA_REPOS`` in `env.local.example <env.local.example>`_ (:download:`download </birdhouse/env.local.example>`).

The automatic deployment of the PAVICS platform, of the Jupyter tutorial
notebooks and of the automatic deployment mechanism itself can all be
enabled by following the `scheduling instructions <components/README.rst#scheduler>`_.

Resource usage monitoring (CPU, memory, ..) and alerting for the host and each
of the containers can be enabled by following the `monitoring instructions <components/README.rst#monitoring>`_.

To launch all the containers, use the following command:

.. code-block::

   ./pavics-compose.sh up -d

If you get a ``'No applicable error code, please check error log'`` error from the WPS processes, please make sure that the WPS databases exists in the
postgres instance. See `create-wps-pgsql-databases.sh <scripts/create-wps-pgsql-databases.sh>`_ (:download:`download </birdhouse/scripts/create-wps-pgsql-databases.sh>`).


Note
----

* All WPS requests should be completed within ``proxy_read_timeout`` of the
  Nginx proxy, see `nginx.conf`_ (:download:`download <birdhouse/config/proxy/nginx.conf>`).
  Any WPS requests that will take longer should use the async mode.

  Default value ``PROXY_READ_TIMEOUT_VALUE`` in `default.env`_ (:download:`download <birdhouse/default.env>`).

  Overrideable in ``env.local`` file, as usual for all values in ``default.env`` file.


Manual steps post deployment
----------------------------

Create public demo user in Magpie for JupyterHub login
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use `create-magpie-users <scripts/create-magpie-users>`_ (:download:`download </birdhouse/scripts/create-magpie-users>`) or follow manual
instructions below.

``config.yml`` file if using ``create-magpie-users``:

.. code-block::

   users:
     - username: < value of JUPYTER_DEMO_USER in `env.local` >
       password: < you decide, at least 12 in length >
       email: < anything is fine >
       group: anonymous

Manual instructions:

* Go to
  ``https://<PAVICS_FQDN>/magpie/ui/login`` and login with the ``admin`` user. The password should be in ``env.local``.

* Then go to ``https://<PAVICS_FQDN>/magpie/ui/users/add``.

* Fill in:

  * User name: <value of JUPYTER_DEMO_USER in ``env.local``\ >
  * Email: < anything is fine >
  * Password: < you decide >
  * User group: ``anonymous``

* Click "Add User".

Optional: prepare instance to run automated end-to-end test suite
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An end-to-end integration test suite is available at
https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests with pre-configured
Jenkins at https://github.com/Ouranosinc/jenkins-config.

For that test suite to pass, run the script
`scripts/bootstrap-instance-for-testsuite <scripts/bootstrap-instance-for-testsuite>`_ (:download:`download </birdhouse/scripts/bootstrap-instance-for-testsuite>`)
to prepare your new instance.  Further documentation inside the script.

Optional components
`all-public-access <./optional-components#give-public-access-to-all-resources-for-testing-purposes>`_
and `secure-thredds <./optional-components/#control-secured-access-to-resources-example>`_
also need to be enabled in ``env.local`` using ``EXTRA_CONF_DIRS`` variable.

ESGF login is also needed for
https://github.com/Ouranosinc/pavics-sdi/blob/master/docs/source/notebooks/esgf-dap.ipynb
part of test suite.  ESGF credentials can be given to Jenkins via
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

See `vagrant_variables.yml.example </vagrant_variables.yml.example>`_ (:download:`download </vagrant_variables.yml.example>`) for what's
configurable with Vagrant.

If using Centos box, follow `disk-resize <vagrant-utils/disk-resize>`_ (:download:`download </birdhouse/vagrant-utils/disk-resize>`) after
first ``vagrant up`` failure due to disk full.  Then ``vagrant reload && vagrant
provision`` to continue.  If using Ubuntu box, no manual steps required,
everything just works.

Install `VirtualBox <https://www.virtualbox.org/wiki/Downloads>`_, both the
platform and the extension pack, and `Vagrant <https://www.vagrantup.com/downloads.html>`_.

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


#. MAJOR version when the API or user facing UI changes that requires
   significant documentation update and/or re-training of the users.  Also
   valid when a big milestone has been reached (ex: DACCS is released).

#. MINOR version when we add new components or update existing components
   that also require change to other existing components (ex: new Magpie that
   also force Twitcher and/or Frontend update) or the change to the existing
   component is a major one (ex: major refactoring of Twitcher, big merge
   with corresponding upstream component from birdhouse project).

#. PATCH version when we update existing components without impact on other
   existing components and the change is a minor change for the existing
   component.


To help properly update versions in all files that could reference to the latest tag,
the `bump2version <https://github.com/c4urself/bump2version>`_ utility is employed.
Running this tool will modify versions in files referencing to the latest revision
(as defined in `.bumpversion.cfg`_) and apply change logs
updates by moving ``Unreleased`` items under a new version matching the new version.

One of the following commands should be used to generate a new version.
The local `.bumpversion.cfg`_ file should be detected automatically when
calling the command from the root of the repository (otherwise, pass the path with ``--config-file``).

.. code-block:: shell

    # bump to a specific semantic version
    bump2version --new-version "<MAJOR>.<MINOR>.<PATCH>" patch

    # bump to a one increment above the corresponding part (eg: minor for 1.0.1 -> 1.1.0)
    bump2version [major|minor|patch]

    # test result without applying it
    bump2version --verbose --dry-run <other options>


Once the version as been bumped and the PR is merged, a corresponding version tag should be added
to the commit generated by the merge. This step is intentionally manual instead of leaving it up
to ``bump2version`` to auto-generated the tag in other to apply it directly on ``master`` branch
after the merge, instead of onto the commits in the PR prior merging.


.. _nginx.conf: ./config/proxy/nginx.conf
.. _default.env: ./default.env
.. _`.bumpversion.cfg`: ../.bumpversion.cfg
