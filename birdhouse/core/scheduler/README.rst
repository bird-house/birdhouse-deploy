Scheduler
=========

This component provides automated unattended continuous deployment for the
"PAVICS stack" (all the git repos in var ``AUTODEPLOY_EXTRA_REPOS``), for the
tutorial notebooks on the Jupyter environment and for the automated deployment
itself.

It can also be used to schedule other tasks on the PAVICS physical host.

Everything is dockerized, the deployment runs inside a container that will
update all other containers.

Automated unattended continuous deployment means if code change in the remote
repo, matching the same currently checkout branch (ex: config changes,
``docker-compose.yml`` changes) a deployment will be performed automatically
without human intervention.

The trigger for the deployment is new code change on the server on the current
branch (PR merged, push). New code change locally will not trigger deployment
so local development workflow is also supported.

Multiple remote repos are supported so the "PAVICS stack" can be made of
multiple checkouts for modularity and extensibility.  The autodeploy will
trigger if any of the checkouts (configured in ``AUTODEPLOY_EXTRA_REPOS``) is
not up-to-date with its remote repo.

A suggested "PAVICS stack" is made of at least 2 repos, this repo and another
private repo containing the source controlled ``env.local`` file and any other
docker-compose override for true infrastructure-as-code.

Note: there are still cases where a human intervention is needed. See note in
script deploy.sh_ (:download:`download <../deployment/deploy.sh>`).


Usage
-----

Given the unattended nature, there is no UI.  Logs are used to keep trace.

- ``/var/log/PAVICS/autodeploy.log`` is for the PAVICS deployment.

- ``/var/log/PAVICS/notebookdeploy.log`` is for the tutorial notebooks deployment.

- logrotate is enabled for ``/var/log/PAVICS/*.log`` to avoid filling up the
  disk.  Any new ``.log`` files in that folder will get logrotate for free.


How to Enable the Component
---------------------------

- Edit ``env.local`` (a copy of env.local.example_ (:download:`download <../env.local.example>`))

  - Add "./core/scheduler" to ``EXTRA_CONF_DIRS``.
  - Set ``AUTODEPLOY_EXTRA_REPOS``, ``AUTODEPLOY_DEPLOY_KEY_ROOT_DIR``,
    ``AUTODEPLOY_PLATFORM_FREQUENCY``, ``AUTODEPLOY_NOTEBOOK_FREQUENCY`` as desired,
    full documentation in `env.local.example`_.
  - Run once fix-write-perm_ (:download:`download <../deployment/fix-write-perm>`), see doc in script.


Old way to deploy the automatic deployment
------------------------------------------

Superseded by this new ``scheduler`` component.  Keeping for reference only.

Doing it this old way do not need the ``scheduler`` component but lose the
ability for the autodeploy system to update itself.

Configure logrotate for all following automations to prevent disk full::

  deployment/install-logrotate-config .. $USER

To enable continuous deployment of PAVICS::

  deployment/install-automated-deployment.sh .. $USER [daily|5-mins]
  # read the script for more options/details

If you want to manually force a deployment of PAVICS (note this might not use
latest version of deploy.sh_ script (:download:`download <../deployment/deploy.sh>`)::

  deployment/deploy.sh .
  # read the script for more options/details

To enable continuous deployment of tutorial Jupyter notebooks::

  deployment/install-deploy-notebook .. $USER
  # read the script for more details

To trigger tutorial Jupyter notebooks deploy manually::

  # configure logrotate before because this script will log to
  # /var/log/PAVICS/notebookdeploy.log

  deployment/trigger-deploy-notebook
  # read the script for more details

Migrating to the new mechanism requires manual deletion of all the artifacts
created by the old install scripts: ``sudo rm /etc/cron.d/PAVICS-deploy
/etc/cron.hourly/PAVICS-deploy-notebooks /etc/logrotate.d/PAVICS-deploy
/usr/local/sbin/triggerdeploy.sh``.  Both can not co-exist at the same time.


Comparison between the old and new autodeploy mechanism
-------------------------------------------------------

Maximum backward-compatibility has been kept with the old install scripts style:

* Still log to the same existing log files under ``/var/log/PAVICS``.
* Old single ssh deploy key is still compatible, but the new mechanism allows for different ssh deploy keys for each
  extra repos (again, public repos should use https clone path to avoid dealing with ssh deploy keys in the first
  place).
* Old install scripts are kept and can still deploy the old way.

Features missing in old install scripts or how the new mechanism improves on the old install scripts:

* Autodeploy of the autodeploy itself !  This is the biggest win.  Previously, if triggerdeploy.sh_
  (:download:`download <../deployment/triggerdeploy.sh>`)
  or the deployed ``/etc/cron.hourly/PAVICS-deploy-notebooks`` script changes, they have to be deployed manually.
  It's very annoying.  Now they are volume-mount in so are fresh on each run.
* ``env.local`` now drives absolutely everything, source control that file and we've got a true DevOPS pipeline.
* Configurable platform and notebook autodeploy frequency.  Previously, this means manually editing the generated cron
  file, less ideal.
* Do not need any support on the local host other than ``docker`` and ``docker-compose``.  ``cron/logrotate/git/ssh``
  versions are all locked-down in the docker images used by the autodeploy.  Recall previously we had to deal with git
  version too old on some hosts.
* Each cron job run in its own docker image meaning the runtime environment is traceable and reproducible.
* The newly introduced scheduler component is made extensible so other jobs can added into it as well (ex: backup),
  via ``env.local``, which should be source controlled, meaning all surrounding maintenance related tasks can also be
  traceable and reproducible.
