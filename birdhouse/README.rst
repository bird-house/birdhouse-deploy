.. contents::


Docker instructions
-------------------

Requirements
^^^^^^^^^^^^

* Centos 7, RockyLinux 8, Ubuntu 20.04, 22.04, 24.04 known to work.

* Hostname of Docker host must exist on the network.  Must use bridge
  networking if Docker host is a Virtual Machine.

* User running ``BIRDHOUSE_COMPOSE`` below must not be ``root`` but a regular user
  belonging to the ``docker`` group.

* `Install latest version of docker <https://docs.docker.com/engine/install/>`_ for the chosen distro 
   (not the version from the distro).

  * Please ensure the latest versions of the following packages and any of their dependencies
    are installed for your distro:

    * docker engine
    * docker CLI
    * docker compose plugin (``v2.20.2+`` is required)
  
* Have a real SSL Certificate, self-signed SSL Certificate do not work properly.
  Let's Encrypt offers free SSL Certificate.

* If using Let's Encrypt, port 80 and 443 and hostname should be accessible publicly
  over the internet before requesting a certificate with Let's Encrypt. Let's Encrypt
  will need to access your hostname at port 80 and 443 in order to verify and provide
  the SSL certificate.

Command Line Interface (CLI)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The command line interface for interacting with the Birdhouse software can be found in
`bin/birdhouse <bin/birdhouse>`_ (:download:`download </bin/birdhouse`).

This CLI provides utilities to manage the Birdhouse software like a docker compose project, display build information,
etc. It also provides a mechanism to execute commands in the Birdhouse configuration environment so that you can ensure
that external scripts run with the current configuration settings enabled.

For a full description of the CLI usage run the CLI with the ``--help`` flag:

.. code-block:: shell

  ./bin/birdhouse --help

For convenience we recommend adding the ``birdhouse-deploy/bin/`` directory to your ``PATH``:

.. code-block:: shell

  export PATH="$(readlink -f ./bin):$PATH"

  # Now instead of running (from the root directory of this project):

  ./bin/birdhouse --help

  # you can run (from anywhere):

  birdhouse --help

  # To ensure that your PATH variable always includes this directory in login shells:

  echo "export PATH=$(readlink -f ./bin)"':$PATH' >> ~/.profile

.. warning::
  It is no longer recommended to call scripts other than
  `bin/birdhouse <bin/birdhouse>`_ (:download:`download </bin/birdhouse`) directly. In previous versions, we recommended
  interacting with the platform by calling scripts (like ``birdhouse-compose.sh`` or ``read-configs.include.sh``)
  directly. These scripts have been left in place for backwards compatibility **for now** but may be moved or modified
  in some future version. We recommend updating any external scripts to use the CLI as soon as possible.

Quick-start
^^^^^^^^^^^

.. code-block:: shell

  # Assuming Docker already installed, networking, hostname, firewall, open ports configured properly.

  git clone https://github.com/bird-house/birdhouse-deploy.git
  cd birdhouse-deploy/birdhouse
  cp env.local.example env.local
  
  $EDITOR env.local
  # Set the following variables at the minimun:
  #BIRDHOUSE_SSL_CERTIFICATE='/path/to/cert.pem'
  #BIRDHOUSE_FQDN='<full qualified hostname of the current host>'
  # Only needed if using LetsEncrypt SSL certificate
  #BIRDHOUSE_SUPPORT_EMAIL='a real email to receivez LetsEncrypt renewal notification'

  # Get the SSL Cert from LetsEncrypt, written to path of var BIRDHOUSE_SSL_CERTIFICATE.
  FORCE_CERTBOT_E2E=1 FORCE_CERTBOT_E2E_NO_START_PROXY=1 deployment/certbotwrapper

  # Start the full stack.
  ./bin/birdhouse compose up -d

Further explanations
^^^^^^^^^^^^^^^^^^^^

To run ``docker-compose`` for Birdhouse, the `bin/birdhouse <bin/birdhouse>`_ (:download:`download </bin/birdhouse`) file can be run with the ``compose`` argument.
This will source the ``env.local`` file, apply the appropriate variable substitutions on all the configuration files
".template", and run ``docker-compose`` with all the command line arguments after the ``compose`` argument.
See `env.local.example <env.local.example>`_ (:download:`download </birdhouse/env.local.example>`) for more details on what can go into the ``env.local`` file.

If the file `env.local` is somewhere else, symlink it here, next to `docker-compose.yml <docker-compose.yml>`_ (:download:`download </birdhouse/docker-compose.yml>`) because many scripts assume this location.

To follow infrastructure-as-code, it is encouraged to source control the above
`env.local` file and any override needed to customized this Birdhouse deployment
for your organization.  For an example of possible override, see how the `emu service <optional-components/emu/docker-compose-extra.yml>`_ (:download:`download </birdhouse/optional-components/emu/docker-compose-extra.yml>`)
(`README <optional-components/README.rst#emu-wps-service-for-testing>`_) can be optionally added to the deployment via the `override mechanism <https://docs.docker.com/compose/extends/>`_.
Ouranos specific override can be found in this `birdhouse-deploy-ouranos <https://github.com/bird-house/birdhouse-deploy-ouranos>`_ repo.

Suggested deployment layout:

.. code-block::

   ├── birdhouse-deploy/  # this repo
   │   ├── bin/
   │   │   ├── birdhouse
   │   ├── birdhouse/
   │   │   ├── env.local  # relative symlink to env.local.real below
   │   │   ├── (...)
   ├── private-config/    # your private config and override: sibling level of this repo
   │   ├── docker-compose-extra.yml
   │   ├── env.local.real
   │   ├── .git/

The automatic deployment is able to handle multiple repos, so will trigger if
this repo or your private-personalized-config repo changes, giving you
automated continuous deployment.  See the continuous deployment setup section
below and the variable ``BIRDHOUSE_AUTODEPLOY_EXTRA_REPOS`` in `env.local.example <env.local.example>`_ (:download:`download </birdhouse/env.local.example>`).

The automatic deployment of the Birdhouse platform, of the Jupyter tutorial
notebooks and of the automatic deployment mechanism itself can all be
enabled by following the `scheduling instructions <components/README.rst#scheduler>`_.

Resource usage monitoring (CPU, memory, ..) and alerting for the host and each
of the containers can be enabled by following the `monitoring instructions <components/README.rst#monitoring>`_.

To launch all the containers, use the following command:

.. code-block::

   ./bin/birdhouse compose up -d

If you get a ``'No applicable error code, please check error log'`` error from the WPS processes, please make sure that the WPS databases exists in the
postgres instance. See `create-wps-pgsql-databases.sh <scripts/create-wps-pgsql-databases.sh>`_ (:download:`download </birdhouse/scripts/create-wps-pgsql-databases.sh>`).


Production deployment hardware recommendations
----------------------------------------------

RAM: at least 128 GB, Thredds 32+ GB, Geoserver 8+ GB, leaving spaces for other components and all the various Jupyter users

CPU: at least 48 cores for parallel computations

Disk: at least 100 TB, depending how much data is hosted on Thredds and Geoserver and storage for the various Jupyter users

In general, the more users, the more cpu cores and memory needed.  The more data, more memory and bigger and faster disks needed.


Note about WPS request timeout
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* All WPS requests should be completed within ``proxy_read_timeout`` of the
  Nginx proxy, see `nginx.conf`_ (:download:`download <birdhouse/components/proxy/nginx.conf>`).
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
  ``https://<BIRDHOUSE_FQDN>/magpie/ui/login`` and login with the ``MAGPIE_ADMIN_USERNAME`` user. The password should be in ``env.local``.

* Then go to ``https://<BIRDHOUSE_FQDN>/magpie/ui/users/add``.

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
also need to be enabled in ``env.local`` using ``BIRDHOUSE_EXTRA_CONF_DIRS`` variable.

ESGF login is also needed for
https://github.com/Ouranosinc/pavics-sdi/blob/master/docs/source/notebooks/esgf-dap.ipynb
part of test suite.  ESGF credentials can be given to Jenkins via
https://github.com/Ouranosinc/jenkins-config/blob/aafaf6c33ea60faede2a32850604c07c901189e8/env.local.example#L11-L13

The canarie monitoring link
``https://<BIRDHOUSE_FQDN>/canarie/node/service/stats`` can be used to confirm the
instance is ready to run the automated end-to-end test suite.  That link should
return the HTTP response code ``200``.


Vagrant instructions
--------------------

Vagrant allows us to quickly spin up a VM to easily reproduce the runtime
environment for testing or to have multiple flavors of Birdhouse with slightly
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
   # Birdhouse platform
   vagrant up

   # get bridged IP address
   vagrant ssh -c "ip addr show enp0s8|grep 'inet '"

   # get inside the VM
   # useful to manage the Birdhouse platform as if Vagrant is not there
   # and use `birdhouse compose` as before
   # ex: birdhouse compose ps
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

Deploy locally for development or test purposes
-----------------------------------------------

If you are developing this code base or want to test out a new feature locally on a machine, you may want to deploy 
the Birdhouse stack locally.

There are two strategies available to deploy the Birdhouse stack locally:

- `Use HTTP scheme deployment`_
- `Use a Self-Signed SSL certificate`_ 

Use HTTP scheme deployment
^^^^^^^^^^^^^^^^^^^^^^^^^^

To deploy locally, enable the :ref:`local-dev-test` component. Also set the following two variables in your local
environment file:

- ``export BIRDHOUSE_FQDN=host.docker.internal``
- ``export BIRDHOUSE_HTTP_ONLY=True``

This will allow you to access the Birdhouse software in a browser on your local machine using 
the URL ``http://host.docker.internal`` without the need for an SSL certificate or to expose ports 80 and 443 
publicly.

Use a Self-Signed SSL certificate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The `Use HTTP scheme deployment`_ strategy described above will send all information over ``http`` instead of using 
``https``.

If there are any features that you want to test locally using ``https``, you can deploy locally using a self-signed
SSL certificate.

You may also need to add the following to the ``docker compose`` settings for the ``twitcher`` component if you're 
not able to access protected URLs:

.. code:: yaml

  services:
    twitcher:
      environment:
        REQUESTS_CA_BUNDLE: "${BIRDHOUSE_SSL_CERTIFICATE}"
      volumes:
        - "${BIRDHOUSE_SSL_CERTIFICATE}:${BIRDHOUSE_SSL_CERTIFICATE}:ro"


.. warning::

  Self-signed certificates are not fully supported by the components of the Birdhouse stack and some features may
  not be fully functional when self-signed certificates are enabled. For example, accessing other components through
  the JupyterLab interface may fail with an ``SSLError``.

Framework tests
---------------

Core features of the platform has tests to prevent regressions.

To run the tests:

.. code-block:: shell

    python3 -m pip install -r tests/requirements.txt
    pytest tests/

Some tests require internet access (to access JSON schemas used to validate
JSON structure). If you need to run tests offline, you can skip the tests that
require internet access by using the `-k 'not online'` pytest option.


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

In order to handle auto-update of the ``releaseTime`` value simultaneously to the
generated release version, the ``bump2version`` call is wrapped in `Makefile <../Makefile>`_.

One of the following commands should be used to generate a new version.

.. code-block:: shell

    # bump to a specific semantic version
    make VERSION="<MAJOR>.<MINOR>.<PATCH>" bump

    # bump the next semantic version automatically
    make bump (major|minor|patch)

    # test result without applying it
    make VERSION="<MAJOR>.<MINOR>.<PATCH>" bump dry

To validate, you can look up the resulting version and release time that
will be written to `RELEASE.txt <../RELEASE.txt>`_. The current version can also be requested
using the following command.

.. code-block:: shell

    make version

Once the version as been bumped and the PR is merged, a corresponding version tag should be added
to the commit generated by the merge. This step is intentionally manual instead of leaving it up
to ``bump2version`` to auto-generate the tag in other to apply it directly on ``master`` branch
(onto the merge commit itself), instead of onto the commits in the PR prior merging.


Release Procedure
-----------------

* Pull/merge latest ``master`` to make sure modifications are applied in
  CHANGES.md_, in next step, are under the most recent "unreleased" section.

* Update CHANGES.md_, commit, push.

* Open a PR with the new content from CHANGES.md_ as the PR description.  PR
  description can have more pertinent info, ex: test results, staging server
  location, other discussion topics, that might or might not be relevant in
  CHANGES.md_.  Use your judgement.

* Wait for a PR approval.

* Review PR description if something needs to be added or updated after the PR
  review process.  The goal is for the PR description to capture all the
  essential informations for someone else not participating in the PR review
  process to understand it easily.  This "someone else" might even be your
  future self trying to understand what was going through your mind when you
  opened this PR :)

* Only when you are ready to merge the PR immediately, you can continue with
  the following steps to.  Doing the following steps too early and you might
  lose the "push race" if someone else is also trying to release at the same
  time.  Also, in the spirit of not losing the "push race", execute all these
  steps together, do not take a break in the middle.

  * Merge with ``master`` branch, if needed, so next ``make bump <major|minor|patch>`` step will
    bump to the proper next version. Might need to review the places where
    CHANGES.md_ items were inserted following merge to make sure the new ones by
    this PR are under "unreleased".

  * Run ``make bump <major|minor|patch>`` with appropriate options, as described in "Tagging
    policy" section above.  Push.

  * Merge this PR, copying the entire PR description into the merge commit
    description.  This is so that the page
    https://github.com/bird-house/birdhouse-deploy/tags will contain relevant
    info nicely.  That page was previously used as an ad-hoc changelog before
    CHANGES.md_ was formally introduced.

  * Run ``git tag`` on the commit created the by merge, with the same tag as
    ``make bump <major|minor|patch>`` generated.

  * Run ``git push --tags`` to upload the new version.

.. backups::

Backups
-------

Backups of data used by the birdhouse stack can be generated using the ``bin/birdhouse backup`` command
and its various subcommands.

This allows users to backup and restore:

* application data, user data, and log data for all components
* birdhouse logs
* docker container logs
* local environement file

Backups are stored in a `restic <https://restic.readthedocs.io/en/stable/>`_ repository and can be restored
either to a named volume (determined by the ``BIRDHOUSE_BACKUP_VOLUME`` configuration variable) or in the case
of user data and application data, it can directly overwrite the current data with the backup.

For details about the backup and restore commands run any of the following:

.. code-block:: shell

    bin/birdhouse backup --help
    bin/birdhouse backup create --help
    bin/birdhouse backup restore --help

Configure the restic repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Backups are stored in a `restic <https://restic.readthedocs.io/en/stable/>`_ repository which can be 
configured by creating a file at the location determined by the ``BIRDHOUSE_BACKUP_RESTIC_ENV_FILE`` configuration
variable (default: ``birdhouse/restic.env``). 

This file contains environment variables which are used by restic to determine how to create and access the 
repository where backups are stored. 

A list of all environment variables that are used by restic can be found in the 
`documentation <https://restic.readthedocs.io/en/stable/040_backup.html#environment-variables>`_.

Restic supports backing up data locally, remotely using the SFTP protocol, as well as remotely to a variety of 
repository types including AWS, Azure, S3, restic REST server, and many more.

Depending on which repository type and access method you want to use, different environment variables may be required.

Some basic examples can be found in the ``birdhouse/restic.env.example`` file but please refer to the 
`documentation <https://restic.readthedocs.io/en/stable/040_backup.html#environment-variables>`_ for all available
options.

Additional backup/restore workflows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When running the ``backup create`` command, the files to be backed up are first written to a working directory 
(determined by the ``BIRDHOUSE_BACKUP_VOLUME`` configuration variable). Then they are backed up from there to 
the restic repository.

Alternatively, you can specify the ``--no-restic`` command line option to skip the step that backs up the files to 
the restic repository. You can then choose to access the files to backup directly in the working directory.

This allows users to inspect the files, integrate them into a different custom backup solution, etc.

Similarly, when restoring files from restic with the ``backup restore`` command, the files are first restored
to the same working directory before being copied to the appropriate location in the birdhouse stack. 

For example, restoring the ``magpie`` database will first restore the backup file from restic to the working
directory and then overwrite the ``magpie`` database with the information contained in the backup file.

If you want to skip the step that overwrites the current data in the birdhouse stack, you can specify the 
``--no-clobber`` command line option. This will still restore the files to the working directory.

.. note::
    Even without the ``--no-restic`` and ``--no-clobber`` options, the files will be written
    to the working directory every time you run backup and restore.

Additional configuration options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following configuration variables can be set in the local environment file to further configure
the backup and restore jobs.

* ``BIRDHOUSE_BACKUP_SSH_KEY_DIR``

  * The location of a directory that contains an SSH key used to access a remote machine where the restic repository
    is hosted. Required if accessing a restic repository using the sftp protocol.

* ``BIRDHOUSE_BACKUP_RESTIC_BACKUP_ARGS``

  * Additional options to pass to the restic backup command when running the birdhouse backup create command.

  * For example: ``'--skip-if-unchanged --exclude-file "file-i-do-not-want-backedup.txt"``

* ``BIRDHOUSE_BACKUP_RESTIC_FORGET_ARGS``

  * Additional options to pass to the ``restic forget`` command after running the backup job. 
  
  * This allows you to ensure that restic deletes old backups according to your backup retention policy.

  * If this is set, then restic will also run the ``restic prune`` command after every backup to clean up 
    old backup files.

  * For example, to store backups daily for 1 week, weekly for 1 month, and monthly for a year:
    ``'--keep-daily=7 --keep-weekly=4 --keep-monthly=12'``

* ``BIRDHOUSE_BACKUP_RESTIC_EXTRA_DOCKER_OPTIONS``

  * Additional options to pass to the ``docker run`` command that runs the restic commands.

  * This can be useful if you want to mount additional directories to the container running restic
    in order to back up data not directly managed by Birdhouse.

    * For example, to backup files in a directory named `/home/other_project/` you could run:
      ``BIRDHOUSE_BACKUP_RESTIC_EXTRA_DOCKER_OPTIONS='-v /home/other_project:/backup2' birdhouse backup restic backup /backup2``

    * Note: in the example above, ``birdhouse backup restic`` runs the ``restic`` command in a docker container.
      The ``backup /backup2`` arguments tell the ``restic`` command to backup the ``/backup2`` folder to a restic
      repository. See the ``restic`` documentation for details regarding all the available restic command options.

  * Warning! Using this option may overwrite other docker options that are required for restic to run properly.
    Make sure you are familiar with restic commands and know what you are doing before using this feature.

.. _nginx.conf: ./components/proxy/nginx.conf
.. _default.env: ./default.env
.. _`.bumpversion.cfg`: ../.bumpversion.cfg
.. _CHANGES.md: ../CHANGES.md
