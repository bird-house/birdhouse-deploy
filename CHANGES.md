# Changes

[//]: # (NOTES:)
[//]: # ( - comments are added here this way because comments in '.bumpversion.cfg' get wiped when it self-updates)
[//]: # ( - headers at level 2 must be with '---', not ##, to avoid comment-interpretation errors with bumpversion)
[//]: # (   see: https://github.com/c4urself/bump2version/issues/99)
[//]: # ( - bump2version will not tag automatically, so it must be done manually after PR is merged and approved)
[//]: # (   This is to ensure that new tags are applied directly on merge-commit, an not a commit within the PR)
[//]: # (   see decission: https://github.com/bird-house/birdhouse-deploy/pull/161#discussion_r661746230)

[//]: # (**DEFINE LATEST CHANGES UNDER BELOW 'Unreleased' SECTION - THEY WILL BE INTEGRATED IN NEXT RELEASE VERSION**)
[//]: # (  bump2version will take care to generate a new empty 'Unreleased' section after version bump)

[Unreleased](https://github.com/bird-house/birdhouse-deploy/tree/master) (latest)
------------------------------------------------------------------------------------------------------------------

[//]: # (list changes here, using '-' for each new entry, remove this when items are added)

[1.22.4](https://github.com/bird-house/birdhouse-deploy/tree/1.22.4) (2022-11-08)
------------------------------------------------------------------------------------------------------------------

## Changes:

- autodeploy: allow repos to optionally decide if a deploy is required

  Useful when only a subset of file changes in a repo will actually impact deployment.

  Without this mechanism any file changes in a repo will trigger a deployment, which
  would cost a full platform restart for no reason.

  Var `GIT_CHANGED_FILES` is given to optional script `<repo_root>/autodeploy/conditional-trigger`
  and only an exit code 0 will trigger deploy.

- fix-geoserver-data-dir-perm: allow overriding data dir to use on another instance of Geoserver


[1.22.3](https://github.com/bird-house/birdhouse-deploy/tree/1.22.3) (2022-10-25)
------------------------------------------------------------------------------------------------------------------

## Fixes:

- jupyter env: reap defunct processes with proper pid 1 init process

    Before, process hierarchy:

    ```sh
    $ docker exec jupyter-lvu ps -efH
    UID          PID    PPID  C STIME TTY          TIME CMD
    jenkins       88       0  0 21:01 ?        00:00:00 ps -efH
    jenkins        1       0  0 18:57 ?        00:00:00 /opt/conda/bin/python /opt/conda/bin/conda run -n birdy /usr/local/bin/start-notebook.sh --ip=0.0.0.0 --port=8888 --notebook-dir=/notebook_dir --SingleUserNotebookApp.default_url=/lab --debug --disable-user-config --NotebookApp.terminals_enabled=False --NotebookApp.shutdown_no_activity_timeout=345600 --MappingKernelManager.cull_idle_timeout=86400 --MappingKernelManager.cull_connected=True
    jenkins        7       1  0 18:57 ?        00:00:00   /bin/bash /tmp/tmpmx46emji
    jenkins       21       7  0 18:57 ?        00:00:27     /opt/conda/envs/birdy/bin/python3.8 /opt/conda/envs/birdy/bin/jupyterhub-singleuser --ip=0.0.0.0 --port=8888 --notebook-dir=/notebook_dir --SingleUserNotebookApp.default_url=/lab --debug --disable-user-config --NotebookApp.terminals_enabled=False --NotebookApp.shutdown_no_activity_timeout=345600 --MappingKernelManager.cull_idle_timeout=86400 --MappingKernelManager.cull_connected=True
    ```

    Before, reproducible defunct firefox-esr processes:
    ```sh
    True
    [{'pid': 302, 'create_time': 1666550504.76, 'name': 'firefox-esr'}, {'pid': 303, 'create_time': 1666550504.8, 'name': 'firefox-esr'}]

    True
    [{'pid': 302, 'create_time': 1666550504.76, 'name': 'firefox-esr'}, {'pid': 303, 'create_time': 1666550504.8, 'name': 'firefox-esr'}, {'pid': 692, 'create_time': 1666550867.43, 'name': 'firefox-esr'}, {'pid': 693, 'create_time': 1666550867.45, 'name': 'firefox-esr'}]

    $ docker exec jupyter-lvu ps
        PID TTY          TIME CMD
          1 ?        00:00:00 conda
          7 ?        00:00:00 bash
         21 ?        00:00:20 jupyterhub-sing
        296 ?        00:00:00 geckodriver <defunct>
        302 ?        00:00:00 firefox-esr <defunct>
        303 ?        00:00:45 firefox-esr <defunct>
        379 ?        00:00:00 Web Content <defunct>
        407 ?        00:00:04 WebExtensions <defunct>
        486 ?        00:00:00 Web Content <defunct>
        507 ?        00:00:38 file:// Content <defunct>
        581 ?        00:00:15 python
        686 ?        00:00:00 geckodriver
        692 ?        00:00:00 firefox-esr <defunct>
        693 ?        00:00:34 firefox-esr
        768 ?        00:00:00 Web Content
        796 ?        00:00:04 WebExtensions
        874 ?        00:00:13 file:// Content
        902 ?        00:00:00 Web Content
        961 ?        00:00:00 ps
    ```

    After, process hierarchy:

    ```sh
    $ docker exec jupyter-lvu2 ps -efH
    UID          PID    PPID  C STIME TTY          TIME CMD
    jenkins       49       0  0 21:01 ?        00:00:00 ps -efH
    jenkins        1       0  0 21:00 ?        00:00:00 /sbin/docker-init -- conda run -n birdy /usr/local/bin/start-notebook.sh --ip=0.0.0.0 --port=8888 --notebook-dir=/notebook_dir --SingleUserNotebookApp.default_url=/lab --debug --disable-user-config --NotebookApp.terminals_enabled=False --NotebookApp.shutdown_no_activity_timeout=345600 --MappingKernelManager.cull_idle_timeout=86400 --MappingKernelManager.cull_connected=True
    jenkins        7       1  0 21:00 ?        00:00:00   /opt/conda/bin/python /opt/conda/bin/conda run -n birdy /usr/local/bin/start-notebook.sh --ip=0.0.0.0 --port=8888 --notebook-dir=/notebook_dir --SingleUserNotebookApp.default_url=/lab --debug --disable-user-config --NotebookApp.terminals_enabled=False --NotebookApp.shutdown_no_activity_timeout=345600 --MappingKernelManager.cull_idle_timeout=86400 --MappingKernelManager.cull_connected=True
    jenkins        8       7  0 21:00 ?        00:00:00     /bin/bash /tmp/tmp6chrvz_j
    jenkins       22       8  9 21:00 ?        00:00:06       /opt/conda/envs/birdy/bin/python3.8 /opt/conda/envs/birdy/bin/jupyterhub-singleuser --ip=0.0.0.0 --port=8888 --notebook-dir=/notebook_dir --SingleUserNotebookApp.default_url=/lab --debug --disable-user-config --NotebookApp.terminals_enabled=False --NotebookApp.shutdown_no_activity_timeout=345600 --MappingKernelManager.cull_idle_timeout=86400 --MappingKernelManager.cull_connected=True
    ```

    After, unable to reproduce defunct firefox-esr processes:
    ```sh
    False
    []

    True
    [{'create_time': 1666550929.17, 'pid': 962, 'name': 'firefox-esr'}]

    $ docker exec jupyter-lvu2 ps
        PID TTY          TIME CMD
          1 ?        00:00:00 docker-init
          6 ?        00:00:00 conda
          7 ?        00:00:00 bash
         21 ?        00:00:20 jupyterhub-sing
        928 ?        00:00:11 python
        955 ?        00:00:00 geckodriver
        962 ?        00:00:46 firefox-esr
       1035 ?        00:00:00 Web Content
       1061 ?        00:00:03 WebExtensions
       1176 ?        00:00:00 Web Content
       1223 ?        00:00:21 file:// Content
       1327 ?        00:00:00 ps
    ```

    How to reproduce defunct firefox-esr processes (run twice to create defunct processes from first run):
    ```python
    import psutil
    import panel as pn
    import numpy as np
    import xarray as xr

    pn.extension()

    def checkIfProcessRunning(processName):
        '''
        Check if there is any running process that contains the given name processName.
        '''
        #Iterate over the all the running process
        for proc in psutil.process_iter():

            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True

        return False;

    def findProcessIdByName(processName):
        '''
        Get a list of all the PIDs of a all the running process whose name contains
        the given string processName
        '''
        listOfProcessObjects = []
        #Iterate over the all the running process
        for proc in psutil.process_iter():

           pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
           # Check if process name contains the given name string.
           if processName.lower() in pinfo['name'].lower() :
               listOfProcessObjects.append(pinfo)

        return listOfProcessObjects;

    print(checkIfProcessRunning('firefox-esr'))
    print(findProcessIdByName('firefox-esr'))

    import hvplot.xarray
    panel = pn.Column()
    data = xr.DataArray(np.random.rand(200,400), name='data')
    app = pn.Column(data.hvplot.quadmesh())
    app.save('test.html')
    for ii in range(0,10):
        data = xr.DataArray(np.random.rand(200,400), name='data')
        app = pn.Column(data.hvplot.quadmesh())
        app.save(f"test{ii}.png")
    print(checkIfProcessRunning('firefox-esr'))
    print(findProcessIdByName('firefox-esr'))
    ```


[1.22.2](https://github.com/bird-house/birdhouse-deploy/tree/1.22.2) (2022-09-19)
------------------------------------------------------------------------------------------------------------------

## Changes:

- `deploy-data`: allow `post_actions` to vary depending on files changed on subsequent run

  Useful for `post_actions` to know the git version change between the current
  and the previous run and which files are impacted.

  Actions can perform extra git commands if needed or simply used the
  provide git diff output and/or rsync output to decide what to do next.

  **Non-breaking changes**
  - `deploy-data` script: add new vars `GIT_PREVIOUS_COMMIT_HASH`, `GIT_NEW_COMMIT_HASH`, `GIT_CHANGED_FILES`,
    `RSYNC_OUTPUT`, accessible to `post_actions` scripts.


[1.22.1](https://github.com/bird-house/birdhouse-deploy/tree/1.22.1) (2022-09-01)
------------------------------------------------------------------------------------------------------------------

## Changes:

- birdhouse-deploy: fix bump versioning methodology to auto-update `releaseTime` accordingly.
  
  ### Relevant changes
  * Adds `Makefile` to run basic DevOps maintenance commands on the repository.
  * Adds `RELEASE.txt` with the active release tag and datetime.
  * Replace `now:` directives by `utcnow:` to report time properly according to employed ISO format.
  * Update contribution guidelines regarding methodology to create a new revision.

[1.22.0](https://github.com/bird-house/birdhouse-deploy/tree/1.22.0) (2022-08-24)
------------------------------------------------------------------------------------------------------------------

## Changes:
- Geoserver: Adds `./optional-components/test-geoserver-secured-access`, to test Twitcher-protected access to Geoserver
  
  Relevant changes:
  - New Provider (Magpie) : geoserver-secured
  - New Location (Proxy) : /geoserver-secured
  - Copied current WFS GetCapabilities and DescribeFeatureType permissions to new Provider

[1.21.1](https://github.com/bird-house/birdhouse-deploy/tree/1.21.1) (2022-08-24)
------------------------------------------------------------------------------------------------------------------

## Changes

- birdhouse-deploy: fix invalid `canarie-api-full-monitoring` endpoints adding double `/` when substituting variables.
- birdhouse-deploy: add optional variables `MAGPIE_LOG_LEVEL` and `TWITCHER_LOG_LEVEL` (both `INFO` by default) to 
  allow instead to customize reported details by instances for debugging purposes. Note that setting `DEBUG` will leak
  sensible details in their logs and should be reserved only for testing environments.

[1.21.0](https://github.com/bird-house/birdhouse-deploy/tree/1.21.0) (2022-08-19)
------------------------------------------------------------------------------------------------------------------

## Changes

- Cowbird: add new service [Ouranosinc/cowbird](https://github.com/Ouranosinc/cowbird/) to the stack.

  ### Relevant changes
  * Cowbird can be integrated to the instance using [components/cowbird](./birdhouse/components/cowbird) 
    when added to in ``EXTRA_CONF_DIRS`` in the ``env.local`` variable definitions.
  * Offers syncing operations between various other *birds* in order to apply user/group permissions between
    corresponding files, granting access to them seamlessly through distinct services.
  * Allows event and callback triggers to sync permissions and volume paths between API endpoints and local storages.

- Nginx: add missing `X-Forwarded-Host` header to allow `Twitcher` to report the proper server host location when the
  service to be accessed uses an internal Docker network reference through the service private URL defined in `Magpie`.

- birdhouse-deploy: fix missing `GEOSERVER_ADMIN_USER` variable templating 
  from [pavics-compose.sh](./birdhouse/pavics-compose.sh).

[1.20.4](https://github.com/bird-house/birdhouse-deploy/tree/1.20.4) (2022-08-19)
------------------------------------------------------------------------------------------------------------------

## Changes:

- Weaver: update `weaver` component default version to [4.22.0](https://github.com/crim-ca/weaver/tree/4.22.0).

  ### Relevant changes
  * Minor improvements to facilitate retrieval of XML and JSON Process definition and their seamless execution with 
    XML or JSON request contents using either WPS or *OGC API - Processes* REST endpoints interchangeably.
  * Fixes to WPS remote provider parsing registered in Weaver to successfully perform the relevant process executions.
  * Add WPS remote provider retry conditions to handle known problematic cases during process execution (on remote)
    that can lead to sporadic failures of the monitored job. When possible, retried submission leading to successful
    execution will result in the monitored job to complete successfully and transparently to the user. Relevant errors
    and retry attempts are provided in the job logs.
  * Add WPS remote provider status exception response as XML message from the failed remote execution within the
    monitored local job logs to help users understand how to resolve any encountered issue on the remote service.
  * Bump version ``OWSLib==0.26.0`` to fix ``processVersion`` attribute resolution from WPS remote provider definition
    to populate ``Process.version`` property employed in converted `Process` description to `OGC API - Process` schema
    (relates to `geopython/OWSLib#794 <https://github.com/geopython/OWSLib/pull/794>`_).

[1.20.3](https://github.com/bird-house/birdhouse-deploy/tree/1.20.3) (2022-08-18)
------------------------------------------------------------------------------------------------------------------

## Fixes:
- Canarie-api: fix unable to verify LetsEncrypt SSL certs

  LetsEncrypt older root certificate "DST Root CA X3" expired on September 30,
  2021, see https://letsencrypt.org/docs/dst-root-ca-x3-expiration-september-2021/

  All the major browsers and OS platform has previously added the new root
  certificate "ISRG Root X1" ahead of time so the transition to the new
  root certificate is seemless for all clients.

  Python `requests` package bundle their own copy of known root
  certificates and is late to add this new root cert "ISRG Root X1".  Had
  it automatically fallback to the OS copy of the root cert bundle, this
  would have been seemless.

  The fix is to force `requests` to use the OS copy of the root cert bundle.

  Fix for this error:
  ```
  $ docker exec proxy python -c "import requests; requests.request('GET', 'https://lvupavicsmaster.ouranos.ca/geoserver')"
  Traceback (most recent call last):
    File "<string>", line 1, in <module>
    File "/usr/local/lib/python2.7/dist-packages/requests/api.py", line 50, in request
      response = session.request(method=method, url=url, **kwargs)
    File "/usr/local/lib/python2.7/dist-packages/requests/sessions.py", line 468, in request
      resp = self.send(prep, **send_kwargs)
    File "/usr/local/lib/python2.7/dist-packages/requests/sessions.py", line 576, in send
      r = adapter.send(request, **kwargs)
    File "/usr/local/lib/python2.7/dist-packages/requests/adapters.py", line 433, in send
      raise SSLError(e, request=request)
  requests.exceptions.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:661)
  ```

  Default SSL root cert bundle of `requests`:
  ```
  $ docker exec proxy python -c "import requests; print requests.certs.where()"
  /usr/local/lib/python2.7/dist-packages/requests/cacert.pem
  ```

  Confirm the fix works:
  ```
  $ docker exec -it proxy bash
  root@37ed3a2a03ae:/opt/local/src/CanarieAPI/canarieapi# REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt python -c "import requests; requests.request('GET', 'https://lvupavicsmaster.ouranos.ca/geoserver')"
  root@37ed3a2a03ae:/opt/local/src/CanarieAPI/canarieapi#

  $ docker exec proxy env |grep REQ
  REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
  ```

  Fixes https://github.com/bird-house/birdhouse-deploy/issues/198


[1.20.2](https://github.com/bird-house/birdhouse-deploy/tree/1.20.2) (2022-08-17)
------------------------------------------------------------------------------------------------------------------

## Changes:
- birdhouse-deploy: fix missing bump of server version reported in ``canarie`` service configuration

[1.20.1](https://github.com/bird-house/birdhouse-deploy/tree/1.20.1) (2022-08-11)
------------------------------------------------------------------------------------------------------------------

## Changes:
- GeoServer: enable metadata-plugin for modifying layer metadata, including bulk modifications

  See plugin documentation at https://docs.geoserver.org/2.19.x/en/user/community/metadata/index.html

  Related to issue https://github.com/Ouranosinc/pavics-sdi/issues/234

  Add new "Metadata" tab in Layer Edit page:
  ![Screenshot 2022-01-25 at 00-25-45 GeoServer Edit Layer](https://user-images.githubusercontent.com/11966697/150916419-fce99147-2903-414b-8b83-551709ef87d6.png)


[1.20.0](https://github.com/bird-house/birdhouse-deploy/tree/1.20.0) (2022-08-10)
------------------------------------------------------------------------------------------------------------------

## Changes

- Weaver: update `weaver` component default version from [4.12.0](https://github.com/crim-ca/weaver/tree/4.12.0)
  to [4.20.0](https://github.com/crim-ca/weaver/tree/4.20.0).
  See [full CHANGELOG](https://github.com/crim-ca/weaver/blob/4.20.0/CHANGES.rst) for details.

  ### Breaking changes
  * Docker commands that target `weaver-worker` to start or use `celery` must be adjusted according to how its new CLI
    resolves certain global parameters. Since the [celery-healthcheck](./birdhouse/components/weaver/celery-healthcheck)
    script uses this CLI, `celery` commands were adjusted to consider those changes. If custom scripts or command
    overrides are used to call `celery`, similar changes will need to be applied according to employed Weaver version.
    See details in [Weaver 4.15.0 changes](https://github.com/crim-ca/weaver/blob/master/CHANGES.rst#4150-2022-04-20).

  ### Relevant changes
  * Support OpenAPI-based `schema` field for Process I/O definitions to align with latest *OGC API - Processes* changes.
  * Support `Prefer` header to define execution mode of jobs according to latest *OGC API - Processes* recommendations.
  * Support `transmissionMode` to return file-based outputs by HTTP `Link` header references as desired.
  * Support deployment of new processes using YAML and CWL based request contents directly to remove the need to
    convert and indirectly embed their definitions in specific JSON schema structures.
  * Support process revisions allowing users to iteratively update process metadata and their definitions without full
    un/re-deployment of the complete process for each change. This also allows multiple process revisions to live
    simultaneously on the instance, which can be described or launched for job executions with specific tagged versions.
  * Add control query parameters to retrieve outputs in different JSON schema variations according to desired structure.
  * Add statistics collection following job execution to obtain machine resource usage by the executed process.
  * Improve handling of Content-Type definitions for reporting inputs, outputs and logs retrieval from job executions.
  * Fixes related to reporting of job results with different formats and URL references based on requested execution
    methods and control parameters.
  * Fixes to resolve pending vulnerabilities or feature integrations by package dependencies (`celery`, `pywps`, etc.).
  * Fixes related to parsing of WPS-1/2 remote providers URL from a CWL definition using `GetCapabilities` endpoint.
  * Fixes and addition of multiple Weaver CLI capabilities to employ new features.


[1.19.2](https://github.com/bird-house/birdhouse-deploy/tree/1.19.2) (2022-07-20)
------------------------------------------------------------------------------------------------------------------

## Changes

- Finch: new release for new Xclim

  Finch release notes:

  0.9.2 (2022-07-19)
  ------------------
  * Fix Finch unable to startup in the Docker image.

  0.9.1 (2022-07-07)
  ------------------
  * Avoid using a broken version of ``libarchive`` in the Docker image.

  0.9.0 (2022-07-06)
  ------------------
  * Fix use of ``output_name``, add ``output_format`` to xclim indicators.
  * Change all outputs to use ``output`` as the main output field name (instead of ``output_netcdf``).
  * Updated to xclim 0.37:

      - Percentile inputs of xclim indicators have been renamed with generic names, excluding an explicit mention to the target percentile.
      - In ensemble processes, these percentiles can now be chosen through ``perc_[var]`` inputs. The default values are inherited from earlier versions of xclim.
  * Average shape process downgraded to be single-threaded, as ESMF seems to have issues with multithreading.
  * Removed deprecated processes ``subset_ensemble_bbox_BCCAQv2``, ``subset_ensemble_BCCAQv2`` and ``BCCAQv2_heat_wave_frequency_gridpoint``.
  * Added ``csv_precision`` to all processes allowing CSV output. When given, it controls the number of decimal places in the output.


[1.19.1](https://github.com/bird-house/birdhouse-deploy/tree/1.19.1) (2022-07-19)
------------------------------------------------------------------------------------------------------------------

## Changes

- Various changes to get the new production host up and running

    **Non-breaking changes**
    - Bootstrap testsuite: only crawl the subset enough to pass canarie-api monitoring: faster when system under test has too much other stuff.
    - New script: `check-autodeploy-repos`: to ensure autodeploy will trigger normally.
    - New script: `sync-data`: to pull data from existing production host to a new production host or to a staging host to emulate the production host.
    - thredds, geoserver, generic_bird: set more appropriate production values, taken from https://github.com/Ouranosinc/birdhouse-deploy/commit/316439e310e915e0a4ef35d25744cab76722fa99
    - monitoring: fix redundant `network_mode: host` and `ports` binding since host network_mode will already automatically perform port bindings

    **Breaking changes**
    - None

## Related Issue / Discussion

- https://github.com/bird-house/birdhouse-deploy-ouranos/pull/16
- https://github.com/Ouranosinc/pavics-vdb/pull/48
- https://github.com/Ouranosinc/ouranos-ansible/pull/2


[1.19.0](https://github.com/bird-house/birdhouse-deploy/tree/1.19.0) (2022-06-08)
------------------------------------------------------------------------------------------------------------------

## Changes:

- Magpie/Twitcher: update `magpie` service
  from [3.21.0](https://github.com/Ouranosinc/Magpie/tree/3.21.0)
  to [3.26.0](https://github.com/Ouranosinc/Magpie/tree/3.26.0) and
  bundled `twitcher` from [0.6.2](https://github.com/bird-house/twitcher/tree/v0.6.2)
  to [0.7.0](https://github.com/bird-house/twitcher/tree/v0.7.0).
  
  - Adds [Service Hooks](https://pavics-magpie.readthedocs.io/en/latest/configuration.html#service-hooks) allowing 
    Twitcher to apply HTTP pre-request/post-response modifications to requested services and resources in accordance
    to `MagpieAdapter` implementation and using plugin Python scripts when matched against specific request parameters.

  - Using *Service Hooks*, inject ``X-WPS-Output-Context`` header in Weaver job submission requests through the proxied
    request by Twitcher and `MagpieAdapter`. This header contains the user ID that indicates to Weaver were to store 
    job output results, allowing to save them in the corresponding user's workspace directory under `wpsoutputs` path.
    More details found in PR https://github.com/bird-house/birdhouse-deploy/pull/244.

  - Using *Service Hooks*, filter processes returned by Weaver in JSON response from ``/processes`` endpoint using
    respective permissions applied onto each ``/processes/{processID}`` for the requesting user. Users will only be able
    to see processes for which they have read access to retrieve the process description.
    More details found in PR https://github.com/bird-house/birdhouse-deploy/pull/245.

  - Using *Service Hooks*, automatically apply permissions for the user that successfully deployed a Weaver process 
    using ``POST /processes`` request, granting it direct access to this process during process listing, process 
    description request and for submitting job execution of this process.
    Only this user deploying the process will have access to it until further permissions are added in Magpie to share
    or publish it with other users, groups and/or publicly. The user must have the necessary permission to deploy a new
    process in the first place. More details found in PR https://github.com/bird-house/birdhouse-deploy/pull/247.

[1.18.13](https://github.com/bird-house/birdhouse-deploy/tree/1.18.13) (2022-06-07)
------------------------------------------------------------------------------------------------------------------

## Changes:

- deploy-data: new env var DEPLOY_DATA_RSYNC_USER_GRP to avoid running cronjobs as root

  When `deploy-data` is used by the `scheduler` component, it is run as
  `root`.  This new env var will force the rsync process to run as a regular user to
  follow security best practice to avoid running as root when not needed.

  Note that the `git checkout` step done by `deploy-data` is still run as root.
  This is because `deploy-data` is currently still run as root so it can
  execute `docker` commands (ex: spawning the `rsync` command above in its own
  docker container).

  To fix this limitation, the regular user inside the `deploy-data` container
  need to have docker access inside the container and outside on the host at
  the same time.  If we make that regular user configurable so the script
  `deploy-data` is generic and can work for any organisations, this is tricky
  for the moment so will have to be handle in another PR.

  So for the moment we have not achieved full non-root user in cronjobs
  launched by the `scheduler` compoment but the most important part, the part
  that perform the actual job (rsync or execute custom command using an
  external docker container) is running as non-root.

  See PR https://github.com/bird-house/birdhouse-deploy-ouranos/pull/18 that
  make use of this new env var.

  When `deploy-data` is invoking an external script that itself spawn a new
  `docker run`, then it is up to this external script to ensure the proper
  non-root user is used by `docker run`.
  See PR https://github.com/Ouranosinc/pavics-vdb/pull/50 that handle that
  case.


[1.18.12](https://github.com/bird-house/birdhouse-deploy/tree/1.18.12) (2022-05-05)
------------------------------------------------------------------------------------------------------------------

## Changes:

- Jupyter env: new build for new XClim and to get Dask dashboard and Panel server app to work

  Deploy new Jupyter env from PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/105 on PAVICS.

  Detailed changes can be found at https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/105.

  Dask dashboard no manual URL mangling required:

  ![Screenshot from 2022-04-13 22-37-49](https://user-images.githubusercontent.com/11966697/163303916-f781ac23-d10a-4cd6-807c-b10c8703afc3.png)

  "Render with Panel" button works:
  ![Screenshot from 2022-05-04 15-18-03](https://user-images.githubusercontent.com/11966697/166810160-f6989da4-6e8f-4407-8fd5-4ef71770e1f2.png)


  Relevant changes:

  ```diff
  # new
  >   - dask-labextension=5.2.0=pyhd8ed1ab_0
  >   - jupyter-panel-proxy=0.2.0a2=py_0
  >   - jupyter-server-proxy=3.2.1=pyhd8ed1ab_0
  
  # removed, interfere with panel
  <     - handcalcs==1.4.1
  
  <   - xclim=0.34.0=pyhd8ed1ab_0
  >   - xclim=0.36.0=pyhd8ed1ab_0
  
  <   - cf_xarray=0.6.3=pyhd8ed1ab_0
  >   - cf_xarray=0.7.2=pyhd8ed1ab_0
  
  <   - clisops=0.8.0=pyh6c4a22f_0
  >   - clisops=0.9.0=pyh6c4a22f_0
  
  # downgrade by clisops
  <   - pandas=1.4.1=py38h43a58ef_0
  >   - pandas=1.3.5=py38h43a58ef_0
  
  <   - rioxarray=0.10.3=pyhd8ed1ab_0
  >   - rioxarray=0.11.1=pyhd8ed1ab_0
  
  <   - nc-time-axis=1.4.0=pyhd8ed1ab_0
  >   - nc-time-axis=1.4.1=pyhd8ed1ab_0
  
  <   - roocs-utils=0.5.0=pyh6c4a22f_0
  >   - roocs-utils=0.6.1=pyh6c4a22f_0
  
  <   - panel=0.12.7=pyhd8ed1ab_0
  >   - panel=0.13.1a2=py_0
  
  <   - plotly=5.6.0=pyhd8ed1ab_0
  >   - plotly=5.7.0=pyhd8ed1ab_0
  ```


[1.18.11](https://github.com/bird-house/birdhouse-deploy/tree/1.18.11) (2022-04-21)
------------------------------------------------------------------------------------------------------------------

## Changes:

- Finch: new release for dask performance problem

  PR to deploy new Finch releases in https://github.com/bird-house/finch/pull/233 on PAVICS.

  See the Finch PR for more info.

  Finch release notes:

  0.8.3 (2022-04-21)
  ------------------
  * Preserve RCP dimension in ensemble processes, even when only RCP is selected.
  * Pin ``dask`` and ``distributed`` at ``2022.1.0``, see https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/issues/100


[1.18.10](https://github.com/bird-house/birdhouse-deploy/tree/1.18.10) (2022-04-07)
------------------------------------------------------------------------------------------------------------------

## Changes:

- Jupyter env: new xlrd, pre-commit, pin dask, distributed, cf_xarray, latest of everything else

  Deploy new Jupyter env from PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/101 on PAVICS.

  Detailed changes can be found at https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/101.

  Relevant changes:
  ```diff
  >   - pre-commit=2.17.0=py38h578d9bd_0
  >   - xlrd=2.0.1=pyhd8ed1ab_3
  
  <   - xclim=0.32.1=pyhd8ed1ab_0
  >   - xclim=0.34.0=pyhd8ed1ab_0
  
  <   - cfgrib=0.9.9.1=pyhd8ed1ab_1
  >   - cfgrib=0.9.10.1=pyhd8ed1ab_0
  
  <   - cftime=1.5.1.1=py38h6c62de6_1
  >   - cftime=1.6.0=py38h3ec907f_0
  
  <   - intake-xarray=0.5.0=pyhd8ed1ab_0
  >   - intake-xarray=0.6.0=pyhd8ed1ab_0
  
  <   - pandas=1.3.5=py38h43a58ef_0
  >   - pandas=1.4.1=py38h43a58ef_0
  
  <   - regionmask=0.8.0=pyhd8ed1ab_1
  >   - regionmask=0.9.0=pyhd8ed1ab_0
  
  <   - rioxarray=0.9.1=pyhd8ed1ab_0
  >   - rioxarray=0.10.3=pyhd8ed1ab_0
  
  <   - xarray=0.20.2=pyhd8ed1ab_0
  >   - xarray=2022.3.0=pyhd8ed1ab_0
  
  <   - zarr=2.10.3=pyhd8ed1ab_0
  >   - zarr=2.11.1=pyhd8ed1ab_0
  ```


[1.18.9](https://github.com/bird-house/birdhouse-deploy/tree/1.18.9) (2022-03-16)
------------------------------------------------------------------------------------------------------------------

## Changes:

- Finch: update `finch` component 
  from [0.7.7](https://github.com/bird-house/finch/releases/tag/v0.7.7)
  to [0.8.2](https://github.com/bird-house/finch/releases/tag/v0.8.2)

  Relevant Changes:
  - v0.8.0
    - Add hourly_to_daily process
    - Avoid annoying warnings by updating birdy (environment-docs)
    - Upgrade to clisops 0.8.0 to accelerate spatial averages over regions. 
    - Upgrade to xesmf 0.6.2 to fix spatial averaging bug not weighing correctly cells with varying areas. 
    - Update to PyWPS 4.5.1 to allow the creation of recursive directories for outputs.
  - v0.8.2
    - Add ``geoseries_to_netcdf`` process, converting a geojson (like a OGC-API request) to a CF-compliant netCDF. 
    - Add ``output_name`` argument to most processes (excepted subsetting and averaging processes), to control 
      the name (or prefix) of the output file. 
    - New dependency ``python-slugify`` to ensure filenames are safe and valid. 
    - Pinning dask to ``<=2022.1.0`` to avoid a performance issue with ``2022.1.1``.

[1.18.8](https://github.com/bird-house/birdhouse-deploy/tree/1.18.8) (2022-03-09)
------------------------------------------------------------------------------------------------------------------

## Changes:

- Weaver: fix tests
  
  Relevant changes:
  - Increase default timeout (`60s -> 120s`) for
    [components/weaver/post-docker-compose-up](./birdhouse/components/weaver/post-docker-compose-up) script to allow it
    to complete with many WPS bird taking a long time to boot. Before this fix, test instances only managed to register 
    `catalog`, `finch`, and `flyingpigeon` providers, but timed out for `hummingbird` and following WPS birds.

    This resolves the first few cell tests by having birds ready for use:

    ```text
    [2022-03-09T02:13:34.966Z] pavics-sdi-master/docs/source/notebook-components/weaver_example.ipynb . [ 57%]
    [2022-03-09T02:13:46.069Z] .......FF.                                                               [ 61%]
    ```

  - Add override ``request_options.yml`` in
    [birdhouse/optional-components/test-weaver](./birdhouse/optional-components/test-weaver)
    that disables SSL verification specifically for the remaining 2 `F` cell above. Error is related to the job 
    execution itself on the test instance, which fails when Weaver sends requests to `hummingbird`'s `ncdump` process. 
    An SSL verification error happens, because the test instance uses a self-signed SSL certificate.

[1.18.7](https://github.com/bird-house/birdhouse-deploy/tree/1.18.7) (2022-03-08)
------------------------------------------------------------------------------------------------------------------

## Changes:
- Weaver: update `weaver` component
  from [4.5.0](https://github.com/crim-ca/weaver/tree/4.5.0)
  to [4.12.0](https://github.com/crim-ca/weaver/tree/4.12.0).

  Relevant changes:
  - Adds `WeaverClient` and *Weaver CLI*. Although not strictly employed by the platform itself to offer *Weaver* as a
    service, these can be employed to interact with *Weaver* using Python or shell commands, providing access to all
    WPS *birds* offered by the platform using the common [OGC API - Processes][ogcapi-proc] interface through
    [Weaver Providers](https://pavics-weaver.readthedocs.io/en/latest/processes.html#remote-provider).
  - Adds [Vault](https://pavics-weaver.readthedocs.io/en/latest/processes.html#vault) functionality allowing temporary
    and secure storage to upload files for single-use process execution.
  - Various bugfixes and conformance resolution related to [OGC API - Processes][ogcapi-proc].
  - Fix `weaver-mongodb` link references for `weaver-worker`. New default variables `WEAVER_MONGODB_[HOST|PORT|URL]`
    are defined to construct different INI configuration formats employed by `weaver` and `weaver-worker` images.
  - Fix missing `EXTRA_VARS` variables in [Weaver's default.env](./birdhouse/components/weaver/default.env).
  - Fix [celery-healthcheck](./birdhouse/components/weaver/celery-healthcheck) of `weaver-worker` to consider
    multiple tasks.

[ogcapi-proc]: https://github.com/opengeospatial/ogcapi-processes

[1.18.6](https://github.com/bird-house/birdhouse-deploy/tree/1.18.6) (2022-03-08)
------------------------------------------------------------------------------------------------------------------

- Magpie: update `magpie` service
  from [3.19.1](https://github.com/Ouranosinc/Magpie/tree/3.19.1)
  to [3.21.0](https://github.com/Ouranosinc/Magpie/tree/3.21.0).

  Relevant changes:
  - Update *WFS*, *WMS* and *WPS* related services to properly implement the relevant *Permissions* and *Resources*
    according to their specific implementation details. For example, *GeoServer*-based *WMS* implementation supports
    *Workspaces* and additional operations that are not offered by standard *OGC*-based *WMS*. Some of these
    implementation specific operations can be taken advantage of with improved *Permissions* and *Resources* resolution.
  - Add multi-*Resource* effective access resolution for *Services* that support it.
    For example, accessing multiple *Layers* under a permission-restricted *WFS* with parameters that allow multiple
    values within a single request is now possible, if the user is granted to all specified *Resources*.
    Previously, users would require to access each *Layer Resource* individually with distinct requests.
  - Magpie's API and UI are more verbose about supported hierarchical *Resource* structure under a given *Service* type.
    When creating *Resources*, specific structures have to be respected, and only valid cases are proposed in the UI.
  - Minor UI fixes.

[1.18.5](https://github.com/bird-house/birdhouse-deploy/tree/1.18.5) (2022-01-27)
------------------------------------------------------------------------------------------------------------------

## Changes:
- Jupyter: update Jupyter env for latest XClim, RavenPy and all packages

  Deploy new Jupyter env from PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/95 on PAVICS.

  Detailed changes can be found at https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/95.

  Relevant changes:
  ```diff
  <   - xclim=0.31.0=pyhd8ed1ab_0
  >   - xclim=0.32.1=pyhd8ed1ab_0
  
  <   - ravenpy=0.7.5=pyhff6ddc9_0
  >   - ravenpy=0.7.8=pyh8a188c0_0
  
  <   - python=3.7.12=hb7a2778_100_cpython
  >   - python=3.8.12=hb7a2778_2_cpython
  
  # removed
  <   - vcs=8.2.1=pyh9f0ad1d_0
  
  <   - numpy=1.21.4=py37h31617e3_0
  >   - numpy=1.21.5=py38h87f13fb_0
  
  <   - xarray=0.20.1=pyhd8ed1ab_0
  >   - xarray=0.20.2=pyhd8ed1ab_0
  
  <   - rioxarray=0.8.0=pyhd8ed1ab_0
  >   - rioxarray=0.9.1=pyhd8ed1ab_0
  
  <   - cf_xarray=0.6.1=pyh6c4a22f_0
  >   - cf_xarray=0.6.3=pyhd8ed1ab_0
  
  <   - gdal=3.3.2=py37hd5a0ba4_2
  >   - gdal=3.3.3=py38hcf2042a_0
  
  <   - rasterio=1.2.6=py37hc20819c_2
  >   - rasterio=1.2.10=py38hfd64e68_0
  
  <   - climpred=2.1.6=pyhd8ed1ab_1
  >   - climpred=2.2.0=pyhd8ed1ab_0
  
  <   - clisops=0.7.0=pyh6c4a22f_0
  >   - clisops=0.8.0=pyh6c4a22f_0
  
  <   - xesmf=0.6.0=pyhd8ed1ab_0
  >   - xesmf=0.6.2=pyhd8ed1ab_0
  
  <   - birdy=v0.8.0=pyh6c4a22f_1
  >   - birdy=0.8.1=pyh6c4a22f_1
  
  <   - cartopy=0.20.0=py37hbe109c4_0
  >   - cartopy=0.20.1=py38hf9a4893_1
  
  <   - dask=2021.11.2=pyhd8ed1ab_0
  >   - dask=2022.1.0=pyhd8ed1ab_0
  
  <   - numba=0.53.1=py37hb11d6e1_1
  >   - numba=0.55.0=py38h4bf6c61_0
  
  <   - pandas=1.3.4=py37he8f5f7f_1
  >   - pandas=1.3.5=py38h43a58ef_0
  ```


[1.18.4](https://github.com/bird-house/birdhouse-deploy/tree/1.18.4) (2022-01-25)
------------------------------------------------------------------------------------------------------------------

## Changes:
- vagrant: support RockyLinux

  RockyLinux 8 is the successor to Centos 7.

  Centos 8 has become like a "RHEL 8 beta" than the equivalent of RHEL 8.

  RockyLinux 8 is the new equivalent of RHEL 8, following the original spirit
  of the Centos project.

  More info at https://rockylinux.org/about.


[1.18.3](https://github.com/bird-house/birdhouse-deploy/tree/1.18.3) (2021-12-17)
------------------------------------------------------------------------------------------------------------------

## Changes:
- Jupyter: new build with latest changes

  See PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/94 for
  more info.

  Change summary:

  ```diff
  <   - xclim=0.28.1=pyhd8ed1ab_0
  >   - xclim=0.31.0=pyhd8ed1ab_0
  
  <   - ravenpy=0.7.4=pyh7f9bfb9_0
  >   - ravenpy=0.7.5=pyhff6ddc9_0
  
  <   - xarray=0.19.0=pyhd8ed1ab_1
  >   - xarray=0.20.1=pyhd8ed1ab_0
  
  <   - rasterio=1.2.1=py37ha549118_0
  >   - rasterio=1.2.6=py37hc20819c_2
  
  <   - bokeh=2.3.3=py37h89c1867_0
  >   - bokeh=2.4.2=py37h89c1867_0
  
  <   - cartopy=0.19.0.post1=py37h0c48da3_1
  >   - cartopy=0.20.0=py37hbe109c4_0
  
  <   - cffi=1.14.6=py37hc58025e_0
  >   - cffi=1.15.0=py37h036bc23_0
  
  <   - climpred=2.1.5.post1=pyhd8ed1ab_0
  >   - climpred=2.1.6=pyhd8ed1ab_1
  
  <   - clisops=0.6.5=pyh6c4a22f_0
  >   - clisops=0.7.0=pyh6c4a22f_0
  
  <   - dask=2021.9.0=pyhd8ed1ab_0
  >   - dask=2021.11.2=pyhd8ed1ab_0
  
  <   - gdal=3.1.4=py37h2ec2946_8
  >   - gdal=3.3.2=py37hd5a0ba4_2
  
  <   - geopandas=0.9.0=pyhd8ed1ab_1
  >   - geopandas=0.10.2=pyhd8ed1ab_0
  
  <   - nc-time-axis=1.3.1=pyhd8ed1ab_2
  >   - nc-time-axis=1.4.0=pyhd8ed1ab_0
  
  <   - pandas=1.2.5=py37h219a48f_0
  >   - pandas=1.3.4=py37he8f5f7f_
  
  <   - poppler=0.89.0=h2de54a5_5
  >   - poppler=21.09.0=ha39eefc_3
  
  <   - rioxarray=0.7.0=pyhd8ed1ab_0
  >   - rioxarray=0.8.0=pyhd8ed1ab_0
  
  <   - roocs-utils=0.4.2=pyh6c4a22f_0
  >   - roocs-utils=0.5.0=pyh6c4a22f_0
  ```

[1.18.2](https://github.com/bird-house/birdhouse-deploy/tree/1.18.2) (2021-12-13)
------------------------------------------------------------------------------------------------------------------

## Fixes
- Thredds: update for Log4j Vulnerability CVE-2021-44228

  Quebec gouvernment has shutdown its website due to this vulnerability so it's pretty serious
  (https://montrealgazette.com/news/quebec/quebec-government-shutting-down-websites-report).

  Thredds release notes: https://github.com/Unidata/thredds/releases
  
  https://www.oracle.com/security-alerts/alert-cve-2021-44228.html
  
  **Oracle Security Alert Advisory - CVE-2021-44228 Description**
  
  This Security Alert addresses CVE-2021-44228, a remote code execution
  vulnerability in Apache Log4j. It is remotely exploitable without
  authentication, i.e., may be exploited over a network without the need for a
  username and password.
  
  Due to the severity of this vulnerability and the publication of exploit code
  on various sites, Oracle strongly recommends that customers apply the updates
  provided by this Security Alert as soon as possible.
  
  **Affected Products and Versions**
  Apache Log4j, versions 2.0-2.14.1
  
  We have 4 Java component but only 1 is vulnerable: Thredds:
  
  **After fix**:
  ```
  $ docker run -it --rm unidata/thredds-docker:4.6.18 bash
  root@f65aadd2955c:/usr/local/tomcat# find -iname '**log4j**'
  ./webapps/thredds/WEB-INF/classes/log4j2.xml
  ./webapps/thredds/WEB-INF/lib/log4j-api-2.15.0.jar
  ./webapps/thredds/WEB-INF/lib/log4j-core-2.15.0.jar
  ./webapps/thredds/WEB-INF/lib/log4j-slf4j-impl-2.15.0.jar
  ./webapps/thredds/WEB-INF/lib/log4j-web-2.15.0.jar
  ```
  
  **Before fix (unidata/thredds-docker:4.6.15)**:
  ```
  $ docker exec -it thredds find / -iname '**log4j**'
  find: ‘/proc/1/map_files’: Operation not permitted
  find: ‘/proc/12/map_files’: Operation not permitted
  find: ‘/proc/20543/map_files’: Operation not permitted
  /usr/local/tomcat/webapps/twitcher#ows#proxy#thredds/WEB-INF/classes/log4j2.xml
  /usr/local/tomcat/webapps/twitcher#ows#proxy#thredds/WEB-INF/lib/log4j-api-2.13.3.jar
  /usr/local/tomcat/webapps/twitcher#ows#proxy#thredds/WEB-INF/lib/log4j-core-2.13.3.jar
  /usr/local/tomcat/webapps/twitcher#ows#proxy#thredds/WEB-INF/lib/log4j-slf4j-impl-2.13.3.jar
  /usr/local/tomcat/webapps/twitcher#ows#proxy#thredds/WEB-INF/lib/log4j-web-2.13.3.jar
  ```
  
  **Other components (ncwms2, geoserver, solr) have log4j older than version 2.0
  so supposedly not affected**:
  
  ```
  $ docker exec -it ncwms2 find / -iname '**log4j**'
  /opt/conda/envs/birdhouse/opt/apache-tomcat/webapps/ncWMS2/WEB-INF/classes/log4j.properties
  /opt/conda/envs/birdhouse/opt/apache-tomcat/webapps/ncWMS2/WEB-INF/lib/log4j-1.2.17.jar
  /opt/conda/envs/birdhouse/opt/apache-tomcat/webapps/ncWMS2/WEB-INF/lib/slf4j-log4j12-1.7.2.jar
  
  $ docker exec -it geoserver find / -iname '**log4j**'
  /build_data/log4j.properties
  find: ‘/etc/ssl/private’: Permission denied
  find: ‘/proc/tty/driver’: Permission denied
  find: ‘/proc/1/map_files’: Operation not permitted
  find: ‘/proc/15/task/47547’: No such file or directory
  find: ‘/proc/15/map_files’: Operation not permitted
  find: ‘/proc/47492/map_files’: Operation not permitted
  find: ‘/root’: Permission denied
  /usr/local/tomcat/log4j.properties
  /usr/local/tomcat/webapps/geoserver/WEB-INF/lib/log4j-1.2.17.jar
  /usr/local/tomcat/webapps/geoserver/WEB-INF/lib/metrics-log4j-3.0.2.jar
  /usr/local/tomcat/webapps/geoserver/WEB-INF/lib/slf4j-log4j12-1.6.4.jar
  find: ‘/var/cache/apt/archives/partial’: Permission denied
  find: ‘/var/cache/ldconfig’: Permission denied
  
  $ docker exec -it solr find / -iname '**log4j**'
  /data/solr/log4j.properties
  /opt/birdhouse/eggs/birdhousebuilder.recipe.solr-0.1.5-py2.7.egg/birdhousebuilder/recipe/solr/templates/log4j.properties
  /opt/conda/envs/birdhouse/opt/solr/docs/solr-core/org/apache/solr/logging/log4j
  /opt/conda/envs/birdhouse/opt/solr/docs/solr-core/org/apache/solr/logging/log4j/Log4jInfo.html
  /opt/conda/envs/birdhouse/opt/solr/docs/solr-core/org/apache/solr/logging/log4j/Log4jWatcher.html
  /opt/conda/envs/birdhouse/opt/solr/docs/solr-core/org/apache/solr/logging/log4j/class-use/Log4jInfo.html
  /opt/conda/envs/birdhouse/opt/solr/docs/solr-core/org/apache/solr/logging/log4j/class-use/Log4jWatcher.html
  /opt/conda/envs/birdhouse/opt/solr/example/resources/log4j.properties
  /opt/conda/envs/birdhouse/opt/solr/licenses/log4j-1.2.17.jar.sha1
  /opt/conda/envs/birdhouse/opt/solr/licenses/log4j-LICENSE-ASL.txt
  /opt/conda/envs/birdhouse/opt/solr/licenses/log4j-NOTICE.txt
  /opt/conda/envs/birdhouse/opt/solr/licenses/slf4j-log4j12-1.7.7.jar.sha1
  /opt/conda/envs/birdhouse/opt/solr/server/lib/ext/log4j-1.2.17.jar
  /opt/conda/envs/birdhouse/opt/solr/server/lib/ext/slf4j-log4j12-1.7.7.jar
  /opt/conda/envs/birdhouse/opt/solr/server/resources/log4j.properties
  /opt/conda/envs/birdhouse/opt/solr/server/scripts/cloud-scripts/log4j.properties
  /opt/conda/pkgs/solr-5.2.1-1/opt/solr/docs/solr-core/org/apache/solr/logging/log4j
  /opt/conda/pkgs/solr-5.2.1-1/opt/solr/docs/solr-core/org/apache/solr/logging/log4j/Log4jInfo.html
  /opt/conda/pkgs/solr-5.2.1-1/opt/solr/docs/solr-core/org/apache/solr/logging/log4j/Log4jWatcher.html
  /opt/conda/pkgs/solr-5.2.1-1/opt/solr/docs/solr-core/org/apache/solr/logging/log4j/class-use/Log4jInfo.html
  /opt/conda/pkgs/solr-5.2.1-1/opt/solr/docs/solr-core/org/apache/solr/logging/log4j/class-use/Log4jWatcher.html
  /opt/conda/pkgs/solr-5.2.1-1/opt/solr/example/resources/log4j.properties
  /opt/conda/pkgs/solr-5.2.1-1/opt/solr/licenses/log4j-1.2.17.jar.sha1
  /opt/conda/pkgs/solr-5.2.1-1/opt/solr/licenses/log4j-LICENSE-ASL.txt
  /opt/conda/pkgs/solr-5.2.1-1/opt/solr/licenses/log4j-NOTICE.txt
  /opt/conda/pkgs/solr-5.2.1-1/opt/solr/licenses/slf4j-log4j12-1.7.7.jar.sha1
  /opt/conda/pkgs/solr-5.2.1-1/opt/solr/server/lib/ext/log4j-1.2.17.jar
  /opt/conda/pkgs/solr-5.2.1-1/opt/solr/server/lib/ext/slf4j-log4j12-1.7.7.jar
  /opt/conda/pkgs/solr-5.2.1-1/opt/solr/server/resources/log4j.properties
  /opt/conda/pkgs/solr-5.2.1-1/opt/solr/server/scripts/cloud-scripts/log4j.properties
  ```

[1.18.1](https://github.com/bird-house/birdhouse-deploy/tree/1.18.1) (2021-12-08)
------------------------------------------------------------------------------------------------------------------

## Fixes
- Update `Mapgie` version [3.19.0](https://github.com/Ouranosinc/Magpie/blob/master/CHANGES.rst#3190-2021-12-02)  
  to [3.19.1](https://github.com/Ouranosinc/Magpie/blob/master/CHANGES.rst#3191-2021-12-08) with fix of unhandled
  request concurrent cleanup with adapter caching, as observed in [bird-house/birdhouse-deploy#224 (comment)](
  https://github.com/bird-house/birdhouse-deploy/pull/224#issuecomment-985668339).

[1.18.0](https://github.com/bird-house/birdhouse-deploy/tree/1.18.0) (2021-12-08)
------------------------------------------------------------------------------------------------------------------

## Changes
- Upgrade default `Weaver` version to [4.5.0](https://github.com/crim-ca/weaver/blob/master/CHANGES.rst#450-2021-11-25) 
  (from [4.2.1](https://github.com/crim-ca/weaver/blob/master/CHANGES.rst#421-2021-10-20)) for new features and fixes.
  Most notable changes are: 
  - Adds support of `X-WPS-Output-Context` header to define the WPS output nested directory (for user context).
  - Adds support of `X-Auth-Docker` header to define a private Docker registry authentication token when the 
    referenced Docker image in the deployed Application Package requires it to fetch it for Process execution. 
  - Require `MongoDB==5.0` Docker image for Weaver's database.
  - Fixes related to handling `dismiss` operation of job executions and retrieval of their results.
  - Fixes related to fetching remote files and propagation of intermediate results between Workflow steps.

## Important
Because of the new `MongoDB==5.0` database requirement for Weaver that uses (potentially) distinct version from other 
birds (notably `phoenix` with `MongoDB==3.4`), a separate Docker image is employed only for Weaver. If some processes, 
jobs, or other Weaver-related data was already defined on one of your server instances, manual transfer between the 
generic `${DATA_PERSIST_ROOT}/mongodb_persist` to new  `${DATA_PERSIST_ROOT}/mongodb_weaver_persist` directory must 
be accomplished. The data in the new directory should then be migrated to the new version following the procedure 
described in [Database Migration](https://pavics-weaver.readthedocs.io/en/latest/installation.html?#database-migration).

## Legal Notice
While migrating from ``MongoDB==3.4`` to ``MongoDB==5.0``, its license changes from AGPL to SSPL
(reference: [mongodb/mongo@6ea81c8/README#L89-L95](https://github.com/mongodb/mongo/blob/6ea81c88/README#L89-L95)).
This should not impact users using the platform for public and Open Source uses, but should be considered otherwise.

[1.17.6](https://github.com/bird-house/birdhouse-deploy/tree/1.17.6) (2021-12-03)
------------------------------------------------------------------------------------------------------------------

## Changes
- Upgrade Magpie/Twitcher to 3.19.0, and add new related environment variables.
  * Adjust Twitcher runner to employ `gunicorn` instead of `waitress`.
  * Add new environment variables to handle email usage, used for features such as 
    user registration/approval and user assignment to groups with terms and conditions.
  * Add expiration variable for temporary tokens.

[1.17.5](https://github.com/bird-house/birdhouse-deploy/tree/1.17.5) (2021-11-16)
------------------------------------------------------------------------------------------------------------------

## Changes
- Upgrade Finch to 0.7.7
  [Release notes for 0.7.7](https://github.com/bird-house/finch/releases/tag/v0.7.7)
- [Release notes for 0.7.6](https://github.com/bird-house/finch/releases/tag/v0.7.6)
  
[1.17.4](https://github.com/bird-house/birdhouse-deploy/tree/1.17.4) (2021-11-03)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Add missing ``config/canarie-api/weaver_config.py`` entry to ``.gitignore`` of ``./components/weaver``
  that is generated from the corresponding template file.

  If upgrading from previous `1.17.x` version, autodeploy will not resume automatically even with this fix because of 
  the *dirty* state of the repository. A manual `git pull` will be required to fix subsequent autodeploy triggers.

[1.17.3](https://github.com/bird-house/birdhouse-deploy/tree/1.17.3) (2021-11-03)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Minor fix to `install-docker.sh` and comment update for other scripts due to Magpie upgrade

  `install-docker.sh`: fix to work with users with sudo privilege.  Before it needed user `root`.

  Other comments in scripts are due to new Magpie in PR https://github.com/bird-house/birdhouse-deploy/pull/107.


[1.17.2](https://github.com/bird-house/birdhouse-deploy/tree/1.17.2) (2021-11-03)
------------------------------------------------------------------------------------------------------------------

## Changes

- scripts: add `extract-jupyter-users-from-magpie-db`

  Extract Jupyter users from Magpie DB so we can send announcements to all Jupyter users.

  Sample output:

  ```
  $ ./scripts/extract-jupyter-users-from-magpie-db  > /tmp/out
  + echo SELECT email,user_name FROM users ORDER BY email
  + docker exec -i postgres-magpie psql -U postgres-magpie magpiedb

  $ cat /tmp/out
           email          |   user_name
  ------------------------+---------------
   admin-catalog@mail.com | admin-catalog
   admin@mail.com         | admin
   anonymous@mail.com     | anonymous
   authtest@example.com   | authtest
  (4 rows)
  ```


[1.17.1](https://github.com/bird-house/birdhouse-deploy/tree/1.17.1) (2021-11-02)
------------------------------------------------------------------------------------------------------------------

## Fixes

- Apply ``mongodb`` network to ``mongodb`` image in order to allow ``phoenix`` to properly reference it.
- Remove ``mongodb`` definition from ``./components/weaver`` since the extended ``mongodb`` network is already provided.

[1.17.0](https://github.com/bird-house/birdhouse-deploy/tree/1.17.0) (2021-11-01)
------------------------------------------------------------------------------------------------------------------

## Changes

- Adds [Weaver](https://github.com/crim-ca/weaver) to the stack (optional) when ``./components/weaver`` 
  is added to ``EXTRA_CONF_DIRS``. For more details, refer to 
  [Weaver Component](https://github.com/bird-house/birdhouse-deploy/blob/master/birdhouse/components/README.rst#Weaver)
  Following happens when enabled:
    
  * Service ``weaver`` (API) gets added with endpoints ``/twitcher/ows/proxy/weaver`` and ``/weaver``.
      
  * All *birds* offering a WPS 1.x/2.x endpoint are automatically added as providers known by `Weaver`
    (birds: ``catalog``, ``finch``, ``flyingpigeon``, ``hummingbird``, ``malleefowl`` and ``raven``).
    This offers an automatic mapping of WPS 1.x/2.x requests of process descriptions and execution nested under
    the *birds* to corresponding [OGC-API - Processes](https://github.com/opengeospatial/ogcapi-processes/) 
    RESTful interface (and added functionalities). 
    
  * New processes can be deployed and executed using 
    Dockerized [Application Packages](https://pavics-weaver.readthedocs.io/en/latest/package.html).
    Additionally, all existing processes (across *bird* providers and Dockerized Application Packages) 
    can be chained into [Workflows](https://pavics-weaver.readthedocs.io/en/latest/processes.html#workflow)
      
  * Images ``weaver-worker`` (`Weaver`'s job executor) and ``docker-proxy`` (sibling Docker container dispatcher)
    are added to the stack to support above functionalities.
      
  * Adds `Magpie` permissions and service for `Weaver` endpoints.
  
  * Adds ``./optional-components/test-weaver`` for even more `Magpie` extended permissions for `Weaver` 
    for getting access to resources for functionalities required by [Weaver Testing notebook][weaver-test-notebook].

[weaver-test-notebook]: https://github.com/Ouranosinc/pavics-sdi/blob/master/docs/source/notebook-components/weaver_example.ipynb


[1.16.2](https://github.com/bird-house/birdhouse-deploy/tree/1.16.2) (2021-10-27)
------------------------------------------------------------------------------------------------------------------

## Changes

- geoserver: enable geopkg plugin

  https://docs.geoserver.org/latest/en/user/community/geopkg/

  ==========

  This plugin brings in the ability to write GeoPackage files in GeoServer.
  Reading GeoPackage files is part of the core functionality of GeoServer, and
  does not require this extension.

  GeoPackage is an SQLite based standard format that is able to hold multiple
  vector and raster data layers in a single file.

  GeoPackage can be used as an output format for WFS GetFeature (creating one
  vector data layer) as well as WMS GetMap (creating one raster data layer). The
  GeoServer GeoPackage extension also allows to create a completely custom made
  GeoPackage with multiple layers, using the GeoPackage process.

  ==========

  Concretely this plugin adds a new GeoPackage download format, see screenshot below:
  ![Screenshot from 2021-10-27 17-09-05](https://user-images.githubusercontent.com/11966697/139147774-ffd320e4-0d70-4246-a532-f66e065fcd4c.png)


[1.16.1](https://github.com/bird-house/birdhouse-deploy/tree/1.16.1) (2021-10-25)
------------------------------------------------------------------------------------------------------------------

## Changes

- Thredds: Enable Netcdf Subset Service (NCSS)

  "The Netcdf Subset Service (NCSS) is one of the ways that the TDS can serve data. It is an experimental REST protocol for returning subsets of CDM datasets." https://www.unidata.ucar.edu/software/tds/current/reference/NetcdfSubsetServiceConfigure.html
  
  More NCSS docs: https://www.unidata.ucar.edu/software/tds/current/reference/NetcdfSubsetServiceReference.html

  Briefly, the advantage to enable NCSS is to be able to perform subsetting directly in the browser (manipulating URL parameters), avoiding the overhead for using OpenDAP (needs another client than the existing browser).  This even works for `.ncml` files.

  Recall previously using "HTTPServer" link type, we were able to download directly the `.nc` files but for `.ncml` we got the xml content instead. With this new "NetcdfSubset" link type, we can actually download the NetCDF content of a `.ncml` file directly from the browser.
  
  Sample screenshots:
  
  ![Screenshot 2021-10-21 at 21-32-14 Catalog Services](https://user-images.githubusercontent.com/11966697/138379386-c658cf05-09a2-44dd-ae6e-9337800212d0.png)
  
  ![Screenshot 2021-10-21 at 21-31-13 NetCDF Subset Service for Grids](https://user-images.githubusercontent.com/11966697/138379396-de6cdedf-6bc7-44b8-9da8-42d496abbdf2.png)
  
  dataset.xml:
  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <gridDataset location="/twitcher/ows/proxy/thredds/ncss/birdhouse/testdata/flyingpigeon/cmip3/tasmin.sresa2.miub_echo_g.run1.atm.da.nc" path="path">
    <axis name="lat" shape="6" type="double" axisType="Lat">
      <attribute name="units" value="degrees_north"/>
      <attribute name="long_name" value="latitude"/>
      <attribute name="standard_name" value="latitude"/>
      <attribute name="bounds" value="lat_bnds"/>
      <attribute name="axis" value="Y"/>
      <attribute name="_ChunkSizes" type="int" value="6"/>
      <attribute name="_CoordinateAxisType" value="Lat"/>
      <values>42.67760468 46.38855743 50.09945297 53.81027222 57.52099228 61.2315712</values>
    </axis>
    <axis name="lon" shape="7" type="double" axisType="Lon">
      <attribute name="units" value="degrees_east"/>
      <attribute name="long_name" value="longitude"/>
      <attribute name="standard_name" value="longitude"/>
      <attribute name="bounds" value="lon_bnds"/>
      <attribute name="axis" value="X"/>
      <attribute name="_ChunkSizes" type="int" value="7"/>
      <attribute name="_CoordinateAxisType" value="Lon"/>
      <values start="281.25" increment="3.75" npts="7"/>
    </axis>
    <axis name="time" shape="7200" type="double" axisType="Time">
      <attribute name="units" value="days since 1860-1-1"/>
      <attribute name="calendar" value="360_day"/>
      <attribute name="bounds" value="time_bnds"/>
      <attribute name="_ChunkSizes" type="int" value="7200"/>
      <attribute name="_CoordinateAxisType" value="Time"/>
      <values start="66960.5" increment="1.0" npts="7200"/>
    </axis>
    <gridSet name="time lat lon">
      <projectionBox>
        <minx>279.375</minx>
        <maxx>305.625</maxx>
        <miny>40.82210731506348</miny>
        <maxy>63.08675956726074</maxy>
      </projectionBox>
      <axisRef name="time"/>
      <axisRef name="lat"/>
      <axisRef name="lon"/>
      <grid name="tasmin" desc="Minimum Daily Surface Air Temperature" shape="time lat lon" type="float">
        <attribute name="original_name" value="T2MIN"/>
        <attribute name="coordinates" value="height"/>
        <attribute name="long_name" value="Minimum Daily Surface Air Temperature"/>
        <attribute name="standard_name" value="air_temperature"/>
        <attribute name="cell_methods" value="time: minimum (interval: 30 minutes)"/>
        <attribute name="units" value="K"/>
        <attribute name="missing_value" type="float" value="1.0E20"/>
        <attribute name="history" value="tas=max(195,tas) applied to raw data; min of 194.73 detected;"/>
        <attribute name="_ChunkSizes" type="int" value="7200 6 7"/>
      </grid>
    </gridSet>
    <LatLonBox>
      <west>-78.7500</west>
      <east>-56.2500</east>
      <south>42.6776</south>
      <north>61.2315</north>
    </LatLonBox>
    <TimeSpan>
      <begin>2046-01-01T12:00:00Z</begin>
      <end>2065-12-30T12:00:00Z</end>
    </TimeSpan>
    <AcceptList>
      <GridAsPoint>
        <accept displayName="xml">xml</accept>
        <accept displayName="xml (file)">xml_file</accept>
        <accept displayName="csv">csv</accept>
        <accept displayName="csv (file)">csv_file</accept>
        <accept displayName="geocsv">geocsv</accept>
        <accept displayName="geocsv (file)">geocsv_file</accept>
        <accept displayName="netcdf">netcdf</accept>
        <accept displayName="netcdf4">netcdf4</accept>
      </GridAsPoint>
      <Grid>
        <accept displayName="netcdf">netcdf</accept>
        <accept displayName="netcdf4">netcdf4</accept>
      </Grid>
    </AcceptList>
  </gridDataset>
  ```


[1.16.0](https://github.com/bird-house/birdhouse-deploy/tree/1.16.0) (2021-10-20)
------------------------------------------------------------------------------------------------------------------

## Changes

- Upgrade geoserver to latest upstream kartoza/geoserver:2.19.0

  Completely removed our geoserver custom Docker build.  Upgrade will be much easier next time.  Fixes https://github.com/Ouranosinc/pavics-sdi/issues/197

  **Backward-incompatible** change:
  * new mandatory var `GEOSERVER_ADMIN_PASSWORD` needed in `env.local`
  * manual deployment upgrade procedure required for existing Geoserver datadir (`/data/geoserver/`) to match user inside the Geoserver docker image (`1000:10001`)
  ```
  # destroy geoserver container so we can work on its datadir /data/geoserver/
  ./pavics-compose.sh stop geoserver && ./pavics-compose.sh rm -vf geoserver

  # checkout this new code to have fix-geoserver-data-dir-perm
  git checkout 1.16.0  # tag containing this PR

  # chown -R 1000:10001 /data/geoserver/
  # this can take a while depending how big /data/geoserver/ is and how fast is your disk
  ./deployment/fix-geoserver-data-dir-perm

  # bring up the new geoserver version
  ./pavics-compose.sh up -d
  ```

  What is cool with this new upstream version, from deployment perspective:

  * many plugins are pre-downloaded, we just have to enable them, see https://github.com/kartoza/docker-geoserver/blob/553ed2982685f366ddcbac3d3e1626cb493cf84b/scripts/setup.sh#L13-L41, no need for our custom build to add plugins anymore !!!
    * full plugin list we can enable https://github.com/kartoza/docker-geoserver/blob/553ed2982685f366ddcbac3d3e1626cb493cf84b/build_data/stable_plugins.txt and https://github.com/kartoza/docker-geoserver/blob/553ed2982685f366ddcbac3d3e1626cb493cf84b/build_data/community_plugins.txt

  * admin password can be set via config, no need for manual step post deployment anymore, sweet !!!

  What might be different from the previous version:

  * Jai and Jai_ImageIO might be different from previous version.  The previous version (https://github.com/bird-house/birdhouse-deploy/tree/c0ffb413a3dff70bbe2c98c38690d6e919f11386/birdhouse/docker/geoserver/resources) we added them manually and there is a "native" component.
    * The new GeoServer seems to have switched to "JAI-EXT, a set of replacement operations with bug fixes and NODATA support, for all image processing. In case there is no interest in NODATA support, one can disable JAI-EXT and install the native JAI extensions to improve raster processing performance." excerpt from https://github.com/geoserver/geoserver/blob/770dc6f7023bc2ab32597cfc7a3a9cc35ff3b608/doc/en/user/source/production/java.rst#outdated-install-native-jai-and-imageio-extensions.
    * Also see https://docs.geoserver.org/stable/en/user/configuration/image_processing/index.html.
    * I have no idea what is the actual performance impact of this change.
  * No more manual install of various NetCDF system libraries (zlib, hdf5, archive), see our previous custom build https://github.com/bird-house/birdhouse-deploy/blob/c0ffb413a3dff70bbe2c98c38690d6e919f11386/birdhouse/docker/geoserver/Dockerfile#L26-L35
    * Since we can enable `netcdf-plugin` on the fly so I am guessing those system libraries are not needed anymore but I do not know the actual real impact of this change.

  Blocking issues and PRs:
  * https://github.com/Ouranosinc/pavics-sdi/issues/220
  * https://github.com/Ouranosinc/raven/pull/397
  * https://github.com/CSHS-CWRA/RavenPy/pull/118

  Related issues:
  * https://github.com/kartoza/docker-geoserver/issues/232
  * https://github.com/kartoza/docker-geoserver/issues/233
  * https://github.com/kartoza/docker-geoserver/issues/250


[1.15.2](https://github.com/bird-house/birdhouse-deploy/tree/1.15.2) (2021-09-22)
------------------------------------------------------------------------------------------------------------------

  ## Changes
  
  - Finch: update to version 0.7.5

    Changelog https://github.com/bird-house/finch/blob/master/CHANGES.rst#075-2021-09-07

    ### 0.7.5 (2021-09-07)
    * Update to xclim 0.27
    * Added ``empirical_quantile_mapping`` process calling ``xclim.sdba.EmpiricalQuantileMapping``.
    * Update to PyWPS 4.4.5


[1.15.1](https://github.com/bird-house/birdhouse-deploy/tree/1.15.1) (2021-09-21)
------------------------------------------------------------------------------------------------------------------
  ## Changes
  
  - Finch: Increase ``maxrequestsize`` from 100mb to 400mb to enable ERA5 data subset. Should be possible to bring this back down with smarter averaging processes. 

[1.15.0](https://github.com/bird-house/birdhouse-deploy/tree/1.15.0) (2021-09-20)
------------------------------------------------------------------------------------------------------------------

## Changes

*  **Backward-incompatible change**: do not, by default, volume-mount the Jupyter env README file since that file has been deleted in this repo.  That file is fairly specific to Ouranos while we want this repo to be generic.  PR https://github.com/Ouranosinc/PAVICS-landing/pull/31 restored that file in PAVICS-landing repo that is Ouranos specific.
    * Previous default added as a comment in `env.local` for existing deployment to restore the previous behavior.  Although the README file has been deleted in this PR, it has already been previously deployed so existing system can restore the previous behavior of having the existing README file.  This file will simply be not updated anymore.

* Delete the deployment of that README file as well since that README file is deleted. PR https://github.com/bird-house/birdhouse-deploy-ouranos/pull/15 restore the deployment for Ouranos.

* Each Org will be responsible for the deployment of their own README file.  PR https://github.com/bird-house/birdhouse-deploy-ouranos/pull/15 can be used as a working example from Ouranos.

* Add sample code for simple and naive notebook sharing between Jupyter users.

### Notebook sharing details

Shared notebooks will be visible to all users logged in, even the public demo user so do not share any notebooks containing sensitive private info.

Can not share to a specific user.

Anyone will see the login id of everyone else so if the login id needs to be kept private, change this sample code.

Inside Jupyter, user will have the following additional folders:

```
.
├── mypublic/  # writable by current user
│   ├── current-user-public-share-file.ipynb
│   ├── (...)
├── public/  # read-only for everyone
│   ├── loginid-1-public/
│   │   └── loginid-1-shared-file.ipynb
│   │   └── (...)
│   ├── loginid-2-public/
│   │   └── loginid-2-shared-file.ipynb
│   │   └── (...)
│   ├── (...)-public/
│   │   └── (...)
```

User can drop their files to be shared under folder `mypublic` and see other users share under `public/{other-loginid}-public`.

Matching PR https://github.com/Ouranosinc/PAVICS-landing/pull/31 updating README inside the Jupyter env to explain this new sharing mechanism.

Deployed to https://medus.ouranos.ca/jupyter/ for acceptance testing.


[1.14.4](https://github.com/bird-house/birdhouse-deploy/tree/1.14.4) (2021-09-10)
------------------------------------------------------------------------------------------------------------------

  ## Changes

  - Jupyter: update for new RavenPy and other new packages

    Bokeh png export now also works.

    Other noticeable changes:
    ```diff
    <   - ravenpy=0.7.0=pyh1bb2064_0
    >   - ravenpy=0.7.4=pyh7f9bfb9_0

    <   - xclim=0.28.0=pyhd8ed1ab_0
    >   - xclim=0.28.1=pyhd8ed1ab_0

    >   - geckodriver=0.29.1=h3146498_0
    >   - selenium=3.141.0=py37h5e8e339_1002
    >   - nested_dict=1.61=pyhd3deb0d_0
    >   - paramiko=2.7.2=pyh9f0ad1d_0
    >   - scp=0.14.0=pyhd8ed1ab_0
    >   - s3fs=2021.8.1=pyhd8ed1ab_0

    # Downgrade !
    <   - pandas=1.3.1=py37h219a48f_0
    >   - pandas=1.2.5=py37h219a48f_0

    <   - owslib=0.24.1=pyhd8ed1ab_0
    >   - owslib=0.25.0=pyhd8ed1ab_0

    <   - cf_xarray=0.6.0=pyh6c4a22f_0
    >   - cf_xarray=0.6.1=pyh6c4a22f_0

    <   - rioxarray=0.5.0=pyhd8ed1ab_0
    >   - rioxarray=0.7.0=pyhd8ed1ab_0

    <   - climpred=2.1.4=pyhd8ed1ab_0
    >   - climpred=2.1.5.post1=pyhd8ed1ab_0

    <   - dask=2021.7.1=pyhd8ed1ab_0
    >   - dask=2021.9.0=pyhd8ed1ab_0
    ```

    See PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/89 for more info.
  
[1.14.3](https://github.com/bird-house/birdhouse-deploy/tree/1.14.3) (2021-09-08)
------------------------------------------------------------------------------------------------------------------

  ## Changes

  - Raven: update to version 0.14.2

    Changelog https://github.com/Ouranosinc/raven/blob/master/CHANGES.rst#0142

    0.14.2
    ------
    * Update to RavenPy 0.7.4 (pin climpred below version 2.1.6)
    * Fixed a process-breaking bug in `wps_hydrobasins_shape_selection`

    0.14.1
    ------
    * Update to RavenPy 0.7.3 (pin xclim version 0.28.1)

    0.14
    ----

    * Update to RavenPy 0.7.2
    * Use new OWSlib WFS topological filters
    * More informative install documentation
    * Upgrade to PyWPS 4.4.5

    Jenkins build only known error (`Full_process_example_1.ipynb`):
    http://jenkins.ouranos.ca/job/ouranos-staging/job/lvupavicsmaster.ouranos.ca/59/console


[1.14.2](https://github.com/bird-house/birdhouse-deploy/tree/1.14.2) (2021-09-01)
------------------------------------------------------------------------------------------------------------------

  ## Changes

  - Re-enables the caching feature of `Twitcher` that was disabled temporarily in 
    [#182](https://github.com/bird-house/birdhouse-deploy/pull/182). 
    Handles issue [Ouranosinc/Magpie#433](https://github.com/Ouranosinc/Magpie/issues/433).

[1.14.1](https://github.com/bird-house/birdhouse-deploy/tree/1.14.1) (2021-08-31)
------------------------------------------------------------------------------------------------------------------

- monitoring: make some prometheus alert threshold configurable via env.local

  Default values are previous hardcoded values so this is fully backward compatible.

  Different organizations with different policies and hardware can now
  adapt the alert threshold to their specific needs, decreasing false
  positive alerts.

  Too much false positive alerts will decrease the importance and
  usefulness of each alert. Alerts should not feel like spams.

  Not all alert thresholds are changed to make configurable.  Only thresholds
  that are most likely to need customization or that logically should be
  configurable are made configurable.

  Fixes https://github.com/bird-house/birdhouse-deploy/issues/66.


[1.14.0](https://github.com/bird-house/birdhouse-deploy/tree/1.14.0) (2021-08-02)
------------------------------------------------------------------------------------------------------------------

  ### Changes

  - Add request caching settings in `TWitcher` INI configuration to work with `Magpie` to help reduce permission and
    access control computation time.
    
  - Add `magpie` logger under `Twitcher` INI configuration to provide relevant logging details provided 
    by `MagpieAdapter` it employs for service and resource access resolution.

  - Change logging level of `sqlalchemy.engine` under `Magpie` INI configuration to `WARN` in order to avoid by default
    over verbose database queries.

  - Update `Magpie` version to 3.14.0 with corresponding `Twitcher` using `MagpieAdapter` to obtain fixes about
    request caching and logging improvements during `Twitcher` security check failure following raised exception.
    
    Please note that because the previous default version was 3.12.0, a security fix introduced in 3.13.0 is included.
    (see details here: [3.13.0 (2021-06-29)](https://github.com/Ouranosinc/Magpie/blob/master/CHANGES.rst#3130-2021-06-29))
    
    This security fix explicitly disallows duplicate emails for different user accounts, which might require manual 
    database updates if such users exist on your server instance. To look for possible duplicates, the following command
    can be used. Duplicate entries must be updated or removed such that only unique emails are present.
    
    ```shell
    echo "select email,user_name from users" | \
    docker exec -i postgres-magpie psql -U $POSTGRES_MAGPIE_USERNAME magpiedb | \
    sort > /tmp/magpie_users.txt
    ```

  ### Fixes

  - Adjust incorrect `magpie.url` value in `Magpie` INI configuration.


[1.13.14](https://github.com/bird-house/birdhouse-deploy/tree/1.13.14) (2021-07-29)
------------------------------------------------------------------------------------------------------------------

- jupyter: update for JupyterLab v3, fix memory monitor display and RavenPy-0.7.0

  See PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/85 for more info.

  Relevant changes:
  ```diff
  <   - jupyterlab=2.2.9=pyhd8ed1ab_0
  >   - jupyterlab=3.1.0=pyhd8ed1ab_0

  <   - jupyterlab_server=1.2.0=py_0
  >   - jupyterlab_server=2.6.1=pyhd8ed1ab_0

  <   - jupyter-archive=2.2.0=pyhd8ed1ab_0
  >   - jupyter-archive=3.0.1=pyhd8ed1ab_0

  <   - jupyter_bokeh=2.0.4=pyhd8ed1ab_0
  >   - jupyter_bokeh=3.0.2=pyhd8ed1ab_0

  <   - jupyterlab-git=0.24.0=pyhd8ed1ab_0
  >   - jupyterlab-git=0.31.0=pyhd8ed1ab_0

  <   - nbdime=2.1.0=py_0
  >   - nbdime=3.1.0=pyhd8ed1ab_0

  # Pip to Conda package
  <     - nbresuse==0.4.0
  >   - nbresuse=0.4.0=pyhd8ed1ab_0

  >   - nbclassic=0.3.1=pyhd8ed1ab_1

  >   - jupyterlab-system-monitor=0.8.0=pyhd8ed1ab_1
  >   - jupyter-resource-usage=0.5.1=pyhd8ed1ab_0
  >   - jupyterlab-topbar=0.6.1=pyhd8ed1ab_2
  >     - jupyterlab-logout=0.5.0

  <   - jupyter_conda=5.1.1=hd8ed1ab_0

  <   - ravenpy=0.6.0=pyh1bb2064_2
  >   - ravenpy=0.7.0=pyh1bb2064_0

  <   - pandas=1.2.5=py37h219a48f_0
  >   - pandas=1.3.1=py37h219a48f_0

  <   - xarray=0.18.2=pyhd8ed1ab_0
  >   - xarray=0.19.0=pyhd8ed1ab_1

  <   - dask=2021.7.0=pyhd8ed1ab_0
  >   - dask=2021.7.1=pyhd8ed1ab_0

  <   - regionmask=0.6.2=pyhd8ed1ab_0
  >   - regionmask=0.7.0=pyhd8ed1ab_0
  ```

[1.13.13](https://github.com/bird-house/birdhouse-deploy/tree/1.13.13) (2021-07-26)
------------------------------------------------------------------------------------------------------------------

  ###  Changes

  - jupyter: update for RavenPy-0.6.0, Xclim-0.28.0 and latest of everything else

    See PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/84 for more info.

    Relevant changes:
    ```diff
    <   - ravenpy=0.5.2=pyh7f9bfb9_0
    >   - ravenpy=0.6.0=pyh1bb2064_2
    
    <   - xclim=0.27.0=pyhd8ed1ab_0
    >   - xclim=0.28.0=pyhd8ed1ab_0
    
    # birdy rebuild
    <   - birdy=v0.8.0=pyh6c4a22f_0
    >   - birdy=v0.8.0=pyh6c4a22f_1
    
    <   - cf_xarray=0.5.2=pyh6c4a22f_0
    >   - cf_xarray=0.6.0=pyh6c4a22f_0
    
    <   - cftime=1.4.1=py37h902c9e0_0
    >   - cftime=1.5.0=py37h6f94858_0
    
    <   - dask=2021.6.0=pyhd8ed1ab_0
    >   - dask=2021.7.0=pyhd8ed1ab_0
    
    <   - nc-time-axis=1.2.0=py_1
    >   - nc-time-axis=1.3.1=pyhd8ed1ab_2
    
    <   - rioxarray=0.4.1.post0=pyhd8ed1ab_0
    >   - rioxarray=0.5.0=pyhd8ed1ab_0
    
    <   - numpy=1.20.3=py37h038b26d_1
    >   - numpy=1.21.1=py37h038b26d_0
    
    <   - pandas=1.2.4=py37h219a48f_0
    >   - pandas=1.2.5=py37h219a48f_0
    
    <   - plotly=4.14.3=pyh44b312d_0
    >   - plotly=5.1.0=pyhd8ed1ab_1
    
    <     - nbconvert==5.6.1
    >   - nbconvert=6.1.0=py37h89c1867_0
    ```

[1.13.12](https://github.com/bird-house/birdhouse-deploy/tree/1.13.12) (2021-07-13)
------------------------------------------------------------------------------------------------------------------

  ###  Changes

  - Add `csv` files to Thredds filter

[1.13.11](https://github.com/bird-house/birdhouse-deploy/tree/1.13.11) (2021-07-06)
------------------------------------------------------------------------------------------------------------------

  ### Changes

  - Notebook deployment: allow to specify required branch for any tutorial
    notebook repos in `env.local`.

    Example: set `WORKFLOW_TESTS_BRANCH` and any other
    notebook deploy config like `PAVICS_LANDING_BRANCH` in `env.local`.

    To support testing of this PR
    https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/79.

  - jupyter: minor update to add `unzip` package

    `unzip` needed to test PAVICS-landing notebooks under Jenkins.  No other
    package updates.

    See PR
    https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/79
    for more details.

[1.13.10](https://github.com/bird-house/birdhouse-deploy/tree/1.13.10) (2021-06-30)
------------------------------------------------------------------------------------------------------------------

  ### Changes
  
  - Add `bump2version` configuration to allow self-update of files that refer to new version releases 
    and apply update of features listed in this changelog.
  - Add this `CHANGES.md` file with all previous version details extracted for PR merge commit messages.
  - Add listing of change history to generated documentation on
    [bird-house/birdhouse-deploy ReadTheDocs](https://birdhouse-deploy.readthedocs.io/en/latest/).
  - Update ``CONTRIBUTING.rst`` file to include note about updating this changelog for future PR.
  
  ### Fixes
  
  - Resolves [#157](https://github.com/bird-house/birdhouse-deploy/issues/157)

[1.13.9](https://github.com/bird-house/birdhouse-deploy/tree/1.13.9) (2021-06-18)
------------------------------------------------------------------------------------------------------------------

- `jupyter`: update for raven notebooks

  To deploy the new Jupyter env to PAVICS.

  Given it's an incremental build, these are the only differences:

  ```diff
  >   - intake-geopandas=0.2.4=pyhd8ed1ab_0
  >   - intake-thredds=2021.6.16=pyhd8ed1ab_0
  >   - intake-xarray=0.5.0=pyhd8ed1ab_0
  ```

  See PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/76.

[1.13.8](https://github.com/bird-house/birdhouse-deploy/tree/1.13.8) (2021-06-15)
------------------------------------------------------------------------------------------------------------------

- `jupyter`: new version for updated `ravenpy`, `birdy` and `xclim`

  PR to deploy the new Jupyter env to PAVICS.

  See PR [Ouranosinc/PAVICS-e2e-workflow-tests#75](https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/75)
  for more details.

  ### Changes

  ```diff
  <   - ravenpy=0.4.2=py37_1
  >   - ravenpy=0.5.2=pyh7f9bfb9_0

  # Renamed.
  <   - raven=3.0.4.318=hc9bffa2_2
  >   - raven-hydro=3.0.4.322=h516393e_0

  <   - ostrich=21.03.16=h2bc3f7f_0
  >   - ostrich=21.03.16=h4bd325d_1

  <   - xclim=0.25.0=pyhd8ed1ab_0
  >   - xclim=0.27.0=pyhd8ed1ab_0

  # Old version was from pip.
  <     - birdhouse-birdy==0.7.0
  >   - birdy=v0.8.0=pyh6c4a22f_0

  # Was previously included in another package, now it is standalone.
  >   - pydantic=1.8.2=py37h5e8e339_0

  # New libs for upcoming Raven notebooks
  >   - gcsfs=2021.6.0=pyhd8ed1ab_0
  >   - intake=0.6.2=pyhd8ed1ab_0
  >   - intake-esm=2021.1.15=pyhd8ed1ab_0
  >   - zarr=2.8.3=pyhd8ed1ab_0

  <   - xarray=0.17.0=pyhd8ed1ab_0
  >   - xarray=0.18.2=pyhd8ed1ab_0

  <   - owslib=0.23.0=pyhd8ed1ab_0
  >   - owslib=0.24.1=pyhd8ed1ab_0

  <   - cf_xarray=0.5.1=pyh44b312d_0
  >   - cf_xarray=0.5.2=pyh6c4a22f_0

  <   - clisops=0.6.3=pyh44b312d_0
  >   - clisops=0.6.5=pyh6c4a22f_0

  <   - dask=2021.2.0=pyhd8ed1ab_0
  >   - dask=2021.6.0=pyhd8ed1ab_0

  # Downgrade !
  <   - gdal=3.2.1=py37hc5bc4e4_7
  >   - gdal=3.1.4=py37h2ec2946_8

  # Downgrade !
  <   - rasterio=1.2.2=py37hd5c4cce_0
  >   - rasterio=1.2.1=py37ha549118_0

  <   - hvplot=0.7.1=pyh44b312d_0
  >   - hvplot=0.7.2=pyh6c4a22f_0

  <   - rioxarray=0.3.1=pyhd8ed1ab_0
  >   - rioxarray=0.4.1.post0=pyhd8ed1ab_0

  # Downgrade !
  <   - xskillscore=0.0.19=pyhd8ed1ab_0
  >   - xskillscore=0.0.18=py_1
  ```

  Full diff of `conda env export`:
  [210415-210527.1-update210615-conda-env-export.diff.txt](https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/files/6658638/210415-210527.1-update210615-conda-env-export.diff.txt)

  Full new `conda env export`:
  [210527.1-update210615-conda-env-export.yml.txt](https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/files/6658646/210527.1-update210615-conda-env-export.yml.txt)

[1.13.7](https://github.com/bird-house/birdhouse-deploy/tree/1.13.7) (2021-06-10)
------------------------------------------------------------------------------------------------------------------

- `jupyterhub`: allow config override via env.local

  ### Overview

  This is basically the same as `ENABLE_JUPYTERHUB_MULTI_NOTEBOOKS` but at the bottom of the file so it can 
  override everything.

  `ENABLE_JUPYTERHUB_MULTI_NOTEBOOKS` is kept for backward-compat.

  First useful application is to enable server culling for auto shutdown of idle kernels and idle jupyter single server,
  hopefully fixes [#67](https://github.com/bird-house/birdhouse-deploy/issues/67).

  The culling settings will only take effect the next time user restart their personal Jupyter server because it seems 
  that the Jupyter server is the one culling itself.  JupyterHub do not perform the culling, it simply forwards the 
  culling settings to the Jupyter server.

  ```sh
  $ docker inspect jupyter-lvu --format '{{ .Args }}'
  [run -n birdy /usr/local/bin/start-notebook.sh --ip=0.0.0.0 --port=8888 --notebook-dir=/notebook_dir --SingleUserNotebookApp.default_url=/lab --debug --disable-user-config --NotebookApp.terminals_enabled=False --NotebookApp.shutdown_no_activity_timeout=180 --MappingKernelManager.cull_idle_timeout=180 --MappingKernelManager.cull_connected=True]
  ```

  ### Changes

  **Non-breaking changes**
  - `jupyterhub`: allow config override via env.local

  ### Tests

  Deployed to https://lvupavicsdev.ouranos.ca/jupyter (timeout set to 5 mins)

[1.13.6](https://github.com/bird-house/birdhouse-deploy/tree/1.13.6) (2021-06-02)
------------------------------------------------------------------------------------------------------------------

- Bugfix for autodeploy job

  The new code added with 
  [this merge](https://github.com/bird-house/birdhouse-deploy/commit/d90765acabe248e65c4899929fbe37a9e8661643) 
  created a new bug for the autodeploy job.

  From the autodeploy job's log :
  ```
  triggerdeploy START_TIME=2021-05-13T14:00:03+0000
  Error: DEPLOY_DATA_JOB_SCHEDULE not set
  ```
  If the `AUTODEPLOY_NOTEBOOK_FREQUENCY` variable is not set in the `env.local` file, it would create the error above.
  The variable is set in the `default.env` file, in case it is not defined in the `env.local`, and is then used for the 
  new env file from `pavics-jupyter-base` 
  [here](https://github.com/bird-house/pavics-jupyter-base/blob/1f81480fe90e0a110f0320c6d6cb17f73b657733/scheduler-jobs/deploy_data_pavics_jupyter.env#L15).
  The error happens because the `default.env` was not called in the `triggerdeploy.sh` script, and the variable was not 
  set when running the `env.local`.

  Solution was tested in a test environment and the cronjob seems to be fixed now.

  Tests were executed to see if the same situation could be found anywhere else. 
  From what was observed, `default.env` seems to be called consistently before the `env.local`.
  Only [here](https://github.com/bird-house/birdhouse-deploy/blob/7e2b8cb428be29d52d27b4b1faa73be7017712ea/birdhouse/deployment/deploy.sh#L109), 
  `default.env` doesn't seem to be called. A `default.env` call has also been added in that file.

[1.13.5](https://github.com/bird-house/birdhouse-deploy/tree/1.13.5) (2021-05-19)
------------------------------------------------------------------------------------------------------------------

- magpie 3.x + gunicorn bind

[1.13.4](https://github.com/bird-house/birdhouse-deploy/tree/1.13.4) (2021-05-18)
------------------------------------------------------------------------------------------------------------------

- Update to raven 0.13.0

[1.13.3](https://github.com/bird-house/birdhouse-deploy/tree/1.13.3) (2021-05-11)
------------------------------------------------------------------------------------------------------------------

- - Add new docker-compose optional components
    * `optional-components/database-external-ports`
    * `optional-components/wps-healthchecks`

  Following is the output result when using `optional-components/wps-healthcheck`
  ```
  ubuntu@daccs-instance-26730-daccsci:~$ pavics-compose ps
  reading './components/monitoring/default.env'
  reading './optional-components/testthredds/default.env'
  COMPOSE_CONF_LIST=-f docker-compose.yml -f ./components/monitoring/docker-compose-extra.yml -f ./optional-components/canarie-api-full-monitoring/docker-compose-extra.yml -f ./optional-components/all-public-access/docker-compose-extra.yml -f ./optional-components/testthredds/docker-compose-extra.yml -f ./optional-components/secure-thredds/docker-compose-extra.yml -f ./optional-components/wps-healthchecks/docker-compose-extra.yml -f ./optional-components/database-external-ports/docker-compose-extra.yml
       Name                    Command                  State                                                                                Ports
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  alertmanager      /bin/alertmanager --config ...   Up             0.0.0.0:9093->9093/tcp
  cadvisor          /usr/bin/cadvisor -logtostderr   Up (healthy)   0.0.0.0:9999->8080/tcp
  catalog           /bin/sh -c python /home/do ...   Up (healthy)   0.0.0.0:8086->80/tcp
  finch             gunicorn --bind=0.0.0.0:50 ...   Up (healthy)   0.0.0.0:8095->5000/tcp
  flyingpigeon      /bin/bash -c source activa ...   Up (healthy)   0.0.0.0:8093->8093/tcp
  frontend          /bin/sh -c /bin/bash ./bin ...   Up             0.0.0.0:3000->3000/tcp
  geoserver         /entrypointwrapper               Up             0.0.0.0:8087->8080/tcp
  grafana           /run.sh                          Up             0.0.0.0:3001->3000/tcp
  hummingbird       /usr/bin/tini -- make upda ...   Up (healthy)   0.0.0.0:28097->28097/tcp, 0.0.0.0:38097->38097/tcp, 8000/tcp, 8080/tcp, 0.0.0.0:8097->8097/tcp, 8443/tcp, 0.0.0.0:48097->9001/tcp
  jupyterhub        jupyterhub                       Up             0.0.0.0:8800->8000/tcp
  magpie            /bin/sh -c crond -c $CRON_ ...   Up             0.0.0.0:2001->2001/tcp
  malleefowl        /usr/bin/tini -- make upda ...   Up (healthy)   0.0.0.0:28091->28091/tcp, 0.0.0.0:38091->38091/tcp, 8000/tcp, 8080/tcp, 0.0.0.0:8091->8091/tcp, 8443/tcp, 0.0.0.0:48091->9001/tcp
  mongodb           /entrypoint.sh bash -c cho ...   Up             0.0.0.0:27017->27017/tcp
  ncwms2            /usr/bin/tini -- make upda ...   Up             0.0.0.0:8080->8080/tcp, 0.0.0.0:48080->9001/tcp
  node-exporter     /bin/node_exporter --path. ...   Up
  phoenix           /usr/bin/tini -- make upda ...   Up             0.0.0.0:38443->38443/tcp, 8000/tcp, 8080/tcp, 0.0.0.0:8081->8081/tcp, 0.0.0.0:8443->8443/tcp, 0.0.0.0:9001->9001/tcp
  portainer         /portainer                       Up             0.0.0.0:9000->9000/tcp
  postgis           /bin/sh -c /start-postgis.sh     Up             5432/tcp
  postgres          docker-entrypoint.sh postgres    Up             0.0.0.0:5432->5432/tcp
  postgres-magpie   docker-entrypoint.sh postgres    Up             0.0.0.0:5433->5432/tcp
  project-api       /bin/sh -c npm run bootstr ...   Up             0.0.0.0:3005->3005/tcp
  prometheus        /bin/prometheus --config.f ...   Up             0.0.0.0:9090->9090/tcp
  proxy             /entrypoint                      Up             0.0.0.0:443->443/tcp, 0.0.0.0:80->80/tcp, 0.0.0.0:58079->8079/tcp, 0.0.0.0:58086->8086/tcp, 0.0.0.0:58091->8091/tcp, 0.0.0.0:58093->8093/tcp,
                                                                    0.0.0.0:58094->8094/tcp
  raven             /bin/bash -c source activa ...   Up (healthy)   0.0.0.0:8096->9099/tcp
  solr              /usr/bin/tini -- /bin/sh - ...   Up             0.0.0.0:8983->8983/tcp, 0.0.0.0:48983->9001/tcp
  testthredds       /entrypointwrapper               Up (healthy)   0.0.0.0:8084->8080/tcp, 8443/tcp
  thredds           /entrypointwrapper               Up (healthy)   0.0.0.0:8083->8080/tcp, 8443/tcp
  twitcher          pserve /opt/birdhouse/src/ ...   Up             0.0.0.0:8000->8000/tcp, 8080/tcp, 8443/tcp, 9001/tcp
  ```

[1.13.2](https://github.com/bird-house/birdhouse-deploy/tree/1.13.2) (2021-05-11)
------------------------------------------------------------------------------------------------------------------

- Custom notebooks

[1.13.1](https://github.com/bird-house/birdhouse-deploy/tree/1.13.1) (2021-05-10)
------------------------------------------------------------------------------------------------------------------

- `jupyterhub`: update to ver 1.4.0-20210506

  ### Changes

  **Non-breaking changes**

  - `jupyterhub`: update to ver 1.4.0-20210506

  ### Tests

  - Deployed to https://lvupavics.ouranos.ca/jupyter
  - Able to login
  - Able to start personal Jupyter server

  ## Additional Information

  - Jupyter hub release note: https://github.com/jupyterhub/jupyterhub/blob/1.4.0/docs/source/changelog.md

[1.13.0](https://github.com/bird-house/birdhouse-deploy/tree/1.13.0) (2021-05-06)
------------------------------------------------------------------------------------------------------------------

- bump default log retention to `500m` instead of `2m`, more suitable for prod

  ### Overview

  Bump default log retention to `500m` instead of `2m`, more suitable for prod

  Forgot to push during PR [#152](https://github.com/bird-house/birdhouse-deploy/pull/152).

  ### Changes

  **Non-breaking changes**
  - Bump default log retention to `500m` instead of `2m`, more suitable for prod

[1.12.4](https://github.com/bird-house/birdhouse-deploy/tree/1.12.4) (2021-05-06)
------------------------------------------------------------------------------------------------------------------

- Update to new finch [0.7.4](https://github.com/bird-house/finch/tree/v0.7.4).

  ### Overview

  Updates finch's image to just released [0.7.4](https://github.com/bird-house/finch/tree/v0.7.4).

  ### Changes

  **Non-breaking changes**
  - Updates finch's xclim to 0.26.
  - Finch now has improved metadata handling : output's attributes are read from config and ensemble 
    processes' datasets are included in the attributes of the output.
  - Ensemble processes now compute meaningful statistics for indicators using day-of-year "units".

  ### Tests

  * https://daccs-jenkins.crim.ca/job/PAVICS-e2e-workflow-tests/job/master/392/parameters/ against 
    Ouranos' prod `pavics.ouranos.ca` to baseline the state of things

  * https://daccs-jenkins.crim.ca/job/PAVICS-e2e-workflow-tests/job/master/393/parameters/ against 
    `lvupavicsdev.ouranos.ca` that has this PR deployed.

  Both all passes.

[1.12.3](https://github.com/bird-house/birdhouse-deploy/tree/1.12.3) (2021-05-04)
------------------------------------------------------------------------------------------------------------------

- Change overview:
  * allow customization of `/data` persistence root on disk, retaining current default for existing deployment
  * add data persistence for `mongodb` container

[1.12.2](https://github.com/bird-house/birdhouse-deploy/tree/1.12.2) (2021-04-28)
------------------------------------------------------------------------------------------------------------------

- Add contributions guideline and policy

[1.12.1](https://github.com/bird-house/birdhouse-deploy/tree/1.12.1) (2021-04-28)
------------------------------------------------------------------------------------------------------------------

- `proxy`: allow homepage (location /) to be configurable

[1.12.0](https://github.com/bird-house/birdhouse-deploy/tree/1.12.0) (2021-04-19)
------------------------------------------------------------------------------------------------------------------

- Magpie upgrade strike II

  Strike II of this original PR https://github.com/bird-house/birdhouse-deploy/pull/107.

  Matching notebook fix https://github.com/Ouranosinc/pavics-sdi/pull/218

  Performed test upgrade on staging (Medus) using prod (Boreas) Magpie DB, everything went well and Jenkins passed (http://jenkins.ouranos.ca/job/ouranos-staging/job/medus.ouranos.ca/80/parameters/).  This Jenkins build uses the corresponding branch in https://github.com/Ouranosinc/pavics-sdi/pull/218 and with `TEST_MAGPIE_AUTH` enabled.

  Manual upgrade migration procedure:
  1. Save `/data/magpie_persist` folder from prod `pavics.ouranos.ca`: `cd /data; tar czf magpie_persist.prod.tgz magpie_persist`
  2. scp `magpie_persist.prod.tgz` to `medus`
  3. login to `medus`
  4. `cd /path/to/birdhouse-deploy/birdhouse`
  5. `./pavics-compose.sh down`
  6. `git checkout master`
  7. `cd /data`
  8. `rm -rf magpie_persist`
  9. `tar xzf magpie_persist.prod.tgz`  # restore Magpie DB with prod version
  10. `cd /path/to/birdhouse-deploy/birdhouse`
  11. `./pavics-compose.sh up -d`
  12. Update `env.local` `MAGPIE_ADMIN_PASSWORD` with prod passwd for Twitcher to be able to access Magpie since we juste restore the Magpie DB from prod
  13. `./pavics-compose.sh restart twitcher`  # for Twitcher to get new Magpie admin passwd
  14. Baseline working state: trigger Jenkins test suite, ensure all pass except `pavics_thredds.ipynb` that requires new Magpie
  15. Baseline working state: view existing services permissions on group Anonymous (https://medus.ouranos.ca/magpie/ui/groups/anonymous/default)
  16. `git checkout restore-previous-broken-magpie-upgrade-so-we-can-work-on-a-fix`  # This current branch
  17. `./pavics-compose.sh up -d`  # upgrade to new Magpie
  18. `docker logs magpie`: check no DB migration error
  19. Trigger Jenkins test suite again

[1.11.29](https://github.com/bird-house/birdhouse-deploy/tree/1.11.29) (2021-04-16)
------------------------------------------------------------------------------------------------------------------

- Update Raven and Jupyter env for Raven demo

  Raven release notes in 
  PR [Ouranosinc/raven#374](https://github.com/Ouranosinc/raven/pull/374])
  and [Ouranosinc/raven#382](https://github.com/Ouranosinc/raven/pull/382)

  Jupyter env update in 
  PR [Ouranosinc/PAVICS-e2e-workflow-tests#71](https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/71)

  Other fixes:
  * Fix intermittent Jupyter spawning error by doubling various timeouts config 
    (it's intermittent so hard to test so we are not sure which ones of timeout fixed it)
  * Fix Finch and Raven "Broken pipe" error when the request size is larger than default 3mb (bumped to 100mb) 
    (fixes [Ouranosinc/raven#361](https://github.com/Ouranosinc/raven/issues/361) 
    and Finch related [comment](https://github.com/bird-house/finch/issues/98#issuecomment-811230388))
  * Lower chance to have "Max connection" error for Finch and Raven (bump parallelprocesses from 2 to 10). 
    In prod, the server has the CPU needed to run 10 concurrent requests if needed so this prevent users having to
    "wait" after each other.

[1.11.28](https://github.com/bird-house/birdhouse-deploy/tree/1.11.28) (2021-04-09)
------------------------------------------------------------------------------------------------------------------

- `jupyter`: update for new `clisops`, `xclim`, `ravenpy`

  Matching PR to deploy the new Jupyter env to PAVICS.

  See PR [Ouranosinc/PAVICS-e2e-workflow-tests#68](https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/68)
  for more info.

  Relevant changes:
  ```diff
  <   - clisops=0.5.1=pyhd3deb0d_0
  >   - clisops=0.6.3=pyh44b312d_0

  <   - xclim=0.23.0=pyhd8ed1ab_0
  >   - xclim=0.25.0=pyhd8ed1ab_0

  >   - ostrich=0.1.2=h2bc3f7f_0
  >   - raven=0.1.1=h2bc3f7f_0

  <     - ravenpy==0.2.3  # from pip
  >   - ravenpy=0.3.1=py37_0  # from conda

  >   - aiohttp=3.7.4=py37h5e8e339_0

  <   - roocs-utils=0.1.5=pyhd3deb0d_1
  >   - roocs-utils=0.3.0=pyh6c4a22f_0

  <   - cf_xarray=0.4.0=pyh44b312d_0
  >   - cf_xarray=0.5.1=pyh44b312d_0

  <   - rioxarray=0.2.0=pyhd8ed1ab_0
  >   - rioxarray=0.3.1=pyhd8ed1ab_0

  <   - xarray=0.16.2=pyhd8ed1ab_0
  >   - xarray=0.17.0=pyhd8ed1ab_0

  <   - geopandas=0.8.2=pyhd8ed1ab_0
  >   - geopandas=0.9.0=pyhd8ed1ab_0

  <   - gdal=3.1.4=py37h2ec2946_5
  >   - gdal=3.2.1=py37hc5bc4e4_7

  <   - jupyter_conda=4.1.0=hd8ed1ab_1
  >   - jupyter_conda=5.0.0=hd8ed1ab_0

  <   - python=3.7.9=hffdb5ce_100_cpython
  >   - python=3.7.10=hffdb5ce_100_cpython
  ```

[1.11.27](https://github.com/bird-house/birdhouse-deploy/tree/1.11.27) (2021-04-01)
------------------------------------------------------------------------------------------------------------------

- reverted name of monitoring routes to original

  The Canarie API complains that `stats` are up but don't return the correct response.
  It is assumed that it was because the monitoring key was changed to reflect the actual content.

  Validation service: https://science.canarie.ca/researchsoftware/services/validator/service.html
  Use Managed
  Enter URL: http://pavics.ouranos.ca/canarie/renderer
  Submit

  Deployed on my dev VM, fix worked, thanks !

  ![Screenshot_2021-04-01 CANARIE Research Software Logiciels de recherche de CANARIE](https://user-images.githubusercontent.com/11966697/113295664-7c359b80-92c6-11eb-8c50-5e77f498d84f.png)

[1.11.26](https://github.com/bird-house/birdhouse-deploy/tree/1.11.26) (2021-03-31)
------------------------------------------------------------------------------------------------------------------

- Update canarieAPI doc links

  - Updated components' version number.
  - Replaced links to githubio docs to readthedocs.
  - renderer is provided by THREDDS-WMS.
  - slicer is provided by finch.

[1.11.25](https://github.com/bird-house/birdhouse-deploy/tree/1.11.25) (2021-03-26)
------------------------------------------------------------------------------------------------------------------

- finch: update to version 0.7.1

  See Finch release PR https://github.com/bird-house/finch/pull/164 for more release info.

  This update will fix the following Jenkins error introduced by https://github.com/bird-house/finch/pull/161#discussion_r601975311:

  ```
  12:37:00  _________ finch-master/docs/source/notebooks/finch-usage.ipynb::Cell 1 _________
  12:37:00  Notebook cell execution failed
  12:37:00  Cell 1: Cell outputs differ
  12:37:00
  12:37:00  Input:
  12:37:00  help(wps.frost_days)
  12:37:00
  12:37:00  Traceback:
  12:37:00   mismatch 'stdout'
  12:37:00
  12:37:00   assert reference_output == test_output failed:
  12:37:00
  12:37:00    'Help on meth...ut files.\n\n' == 'Help on meth...ut files.\n\n'
  12:37:00    Skipping 70 identical leading characters in diff, use -v to show
  12:37:00    - min=None, missing_options=None, check_missing='any', thresh='0 degC', freq='YS', variable=None, output_formats=None) method of birdy.client.base.WPSClient instance
  12:37:00    + min=None, check_missing='any', cf_compliance='warn', data_validation='raise', thresh='0 degC', freq='YS', missing_options=None, variable=None, output_formats=None) method of birdy.client.base.WPSClient instance
  12:37:00          Number of days where daily minimum temperatures are below 0.
  12:37:00
  12:37:00          Parameters
  12:37:00          ----------
  12:37:00          tasmin : ComplexData:mimetype:`application/x-netcdf`, :mimetype:`application/x-ogc-dods`
  12:37:00              NetCDF Files or archive (tar/zip) containing netCDF files.
  12:37:00          thresh : string
  12:37:00              Freezing temperature.
  12:37:00          freq : {'YS', 'MS', 'QS-DEC', 'AS-JUL'}string
  12:37:00              Resampling frequency.
  12:37:00          check_missing : {'any', 'wmo', 'pct', 'at_least_n', 'skip', 'from_context'}string
  12:37:00              Method used to determine which aggregations should be considered missing.
  12:37:00          missing_options : ComplexData:mimetype:`application/json`
  12:37:00              JSON representation of dictionary of missing method parameters.
  12:37:00    +     cf_compliance : {'log', 'warn', 'raise'}string
  12:37:00    +         Whether to log, warn or raise when inputs have non-CF-compliant attributes.
  12:37:00    +     data_validation : {'log', 'warn', 'raise'}string
  12:37:00    +         Whether to log, warn or raise when inputs fail data validation checks.
  12:37:00          variable : string
  12:37:00              Name of the variable in the NetCDF file.
  12:37:00
  12:37:00          Returns
  12:37:00          -------
  12:37:00          output_netcdf : ComplexData:mimetype:`application/x-netcdf`
  12:37:00              The indicator values computed on the original input grid.
  12:37:00          output_log : ComplexData:mimetype:`text/plain`
  12:37:00              Collected logs during process run.
  12:37:00          ref : ComplexData:mimetype:`application/metalink+xml; version=4.0`
  12:37:00              Metalink file storing all references to output files.
  ```

  Jenkins build with Finch notebooks passing against newer Finch: http://jenkins.ouranos.ca/job/ouranos-staging/job/lvupavics.ouranos.ca/45/console

[1.11.24](https://github.com/bird-house/birdhouse-deploy/tree/1.11.24) (2021-03-19)
------------------------------------------------------------------------------------------------------------------

- Avoid docker pull since pull rate limit on dockerhub

  Pin bash tag so it is reproducible (previously it was more or less reproducible since we always ensure "latest" tag).

  Avoid the following error:

  ```
  + docker pull bash
  Using default tag: latest
  Error response from daemon: toomanyrequests: You have reached your pull rate limit. You may increase the limit by authenticating and upgrading: https://www.docker.com/increase-rate-limit
  ```

[1.11.23](https://github.com/bird-house/birdhouse-deploy/tree/1.11.23) (2021-03-17)
------------------------------------------------------------------------------------------------------------------

- Custom Jupyter user images

  Adds CRIM's nlp and eo images to the available list of images in JupyterHub

  The base image (pavics-jupyter-base) wasn't added to the list, because it is assumed the users will always be 
  using the other more specialized images.

  We were already able to add/override Jupyter images but this PR makes it more integrated: those image will 
  also be pulled in advanced so startup is much faster for big images since these images will already be cached.

  Backward incompatible changes:
  DOCKER_NOTEBOOK_IMAGE renamed to DOCKER_NOTEBOOK_IMAGES and is now a space separated list of images. 
  Any existing override in env.local using the old name will have to switch to the new name.

[1.11.22](https://github.com/bird-house/birdhouse-deploy/tree/1.11.22) (2021-03-16)
------------------------------------------------------------------------------------------------------------------

- finch: update to 0.7.0

  Require PR https://github.com/bird-house/birdhouse-deploy/pull/131 for extra testdata for the new regridding notebook.

  Regridding notebook will also need to be adjusted for some output to pass Jenkins test suite, 
  PR https://github.com/Ouranosinc/pavics-sdi/pull/206.

  Nbval escape regex also needed for the regridding notebook, 
  PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/63

  See Finch changelog in PR https://github.com/bird-house/finch/pull/158

  Passing Jenkins build 
  http://jenkins.ouranos.ca/job/PAVICS-e2e-workflow-tests/job/update-nbval-sanitize-config-for-pavics-sdi-regridding-notebook/10/console

[1.11.21](https://github.com/bird-house/birdhouse-deploy/tree/1.11.21) (2021-02-19)
------------------------------------------------------------------------------------------------------------------

- Configurable Jupyterhub README

  While 
  the [`README.ipynb`](https://github.com/bird-house/birdhouse-deploy/blob/master/docs/source/notebooks/README.ipynb) 
  provided by `birdhouse-deploy` is good, it does not quite fit our needs at PCIC. This PR allows users to configure 
  their own `README` for Jupyterhub.

  ### Changes
  - Adds `JUPYERHUB_README` as configuration option in the appropriate spots

[1.11.20](https://github.com/bird-house/birdhouse-deploy/tree/1.11.20) (2021-02-19)
------------------------------------------------------------------------------------------------------------------

- `jupyter`: update to version 210216 for xESMF

  Matching PR to deploy https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/61 to PAVICS.

  For regridding notebook, see https://github.com/Ouranosinc/pavics-sdi/pull/201#issuecomment-778329309.

  Noticeable changes:

  ```diff
  >   - xesmf=0.5.2=pyhd8ed1ab_0

  <   - owslib=0.21.0=pyhd8ed1ab_0
  >   - owslib=0.23.0=pyhd8ed1ab_0

  <   - cftime=1.3.1=py37h6323ea4_0
  >   - cftime=1.4.1=py37h902c9e0_0

  <   - dask=2021.1.1=pyhd8ed1ab_0
  >   - dask=2021.2.0=pyhd8ed1ab_0

  <   - rioxarray=0.1.1=pyhd8ed1ab_0
  >   - rioxarray=0.2.0=pyhd8ed1ab_0
  ```

[1.11.19](https://github.com/bird-house/birdhouse-deploy/tree/1.11.19) (2021-02-10)
------------------------------------------------------------------------------------------------------------------

- `proxy`: proxy_read_timeout config should be configurable

  We have a performance problem with the production deployment at Ouranos so we need a longer timeout. 
  Being an Ouranos specific need, it should not be hardcoded as in previous PR https://github.com/bird-house/birdhouse-deploy/pull/122.

  The previous increase was sometime not enough !

  The value is now configurable via `env.local` as most other customizations.  Documentation updated.

  Timeout in Prod:
  ```
  WPS_URL=https://pavics.ouranos.ca/twitcher/ows/proxy/raven/wps FINCH_WPS_URL=https://pavics.ouranos.ca/twitcher/ows/proxy/finch/wps FLYINGPIGEON_WPS
  _URL=https://pavics.ouranos.ca/twitcher/ows/proxy/flyingpigeon/wps pytest --nbval-lax --verbose docs/source/notebooks/Running_HMETS_with_CANOPEX_datas
  et.ipynb --sanitize-with docs/source/output-sanitize.cfg --ignore docs/source/notebooks/.ipynb_checkpoints

  HTTPError: 504 Server Error: Gateway Time-out for url: https://pavics.ouranos.ca/twitcher/ows/proxy/raven/wps

  ===================================================== 11 failed, 4 passed, 1 warning in 249.80s (0:04:09) ===========================================
  ```

  Pass easily on my test VM with very modest hardware (10G ram, 2 cpu):
  ```
  WPS_URL=https://lvupavicsmaster.ouranos.ca/twitcher/ows/proxy/raven/wps FINCH_WPS_URL=https://lvupavicsmaster.ouranos.ca/twitcher/ows/proxy/finch/wp
  s FLYINGPIGEON_WPS_URL=https://lvupavicsmaster.ouranos.ca/twitcher/ows/proxy/flyingpigeon/wps pytest --nbval-lax --verbose docs/source/notebooks/Runni
  ng_HMETS_with_CANOPEX_dataset.ipynb --sanitize-with docs/source/output-sanitize.cfg --ignore docs/source/notebooks/.ipynb_checkpoints

  =========================================================== 15 passed, 1 warning in 33.84s ===========================================================
  ```

  Pass against Medus:
  ```
  WPS_URL=https://medus.ouranos.ca/twitcher/ows/proxy/raven/wps FINCH_WPS_URL=https://medus.ouranos.ca/twitcher/ows/proxy/finch/wps FLYINGPIGEON_WPS_URL=https://medus.ouranos.ca/twitcher/ows/proxy/flyingpigeon/wps pytest --nbval-lax --verbose docs/source/notebooks/Running_HMETS_with_CANOPEX_dataset.ipynb --sanitize-with docs/source/output-sanitize.cfg --ignore docs/source/notebooks/.ipynb_checkpoints

  ============================================== 15 passed, 1 warning in 42.44s =======================================================
  ```

  Pass against `hirondelle.crim.ca`:
  ```
  WPS_URL=https://hirondelle.crim.ca/twitcher/ows/proxy/raven/wps FINCH_WPS_URL=https://hirondelle.crim.ca/twitcher/ows/proxy/finch/wps FLYINGPIGEON_WPS_URL=https://hirondelle.crim.ca/twitcher/ows/proxy/flyingpigeon/wps pytest --nbval-lax --verbose docs/source/notebooks/Running_HMETS_with_CANOPEX_dataset.ipynb --sanitize-with docs/source/output-sanitize.cfg --ignore docs/source/notebooks/.ipynb_checkpoints

  =============================================== 15 passed, 1 warning in 35.61s ===============================================
  ```

  For comparison, a run on Prod without Twitcher (PR https://github.com/bird-house/birdhouse-deploy-ouranos/pull/5):
  ```
  WPS_URL=https://pavics.ouranos.ca/raven/wps FINCH_WPS_URL=https://pavics.ouranos.ca/twitcher/ows/proxy/finch/wps FLYINGPIGEON_WPS_URL=https://pavics
  .ouranos.ca/twitcher/ows/proxy/flyingpigeon/wps pytest --nbval-lax --verbose docs/source/notebooks/Running_HMETS_with_CANOPEX_dataset.ipynb --sanitize
  -with docs/source/output-sanitize.cfg --ignore docs/source/notebooks/.ipynb_checkpoints

  HTTPError: 504 Server Error: Gateway Time-out for url: https://pavics.ouranos.ca/raven/wps

  ================================================ 11 failed, 4 passed, 1 warning in 248.99s (0:04:08) =================================================
  ```

  A run on Prod without Twitcher and Nginx (direct hit Raven):
  ```
  WPS_URL=http://pavics.ouranos.ca:8096/ FINCH_WPS_URL=https://pavics.ouranos.ca/twitcher/ows/proxy/finch/wps FLYINGPIGEON_WPS_URL=https://pavics.oura
  nos.ca/twitcher/ows/proxy/flyingpigeon/wps pytest --nbval-lax --verbose docs/source/notebooks/Running_HMETS_with_CANOPEX_dataset.ipynb --sanitize-with
   docs/source/output-sanitize.cfg --ignore docs/source/notebooks/.ipynb_checkpoints

  ===================================================== 15 passed, 1 warning in 218.46s (0:03:38) ======================================================

[1.11.18](https://github.com/bird-house/birdhouse-deploy/tree/1.11.18) (2021-02-02)
------------------------------------------------------------------------------------------------------------------

- update Raven and Jupyter env

  See https://github.com/Ouranosinc/raven/compare/v0.10.0...v0.11.1 for change details.

  Jupyter env change details: https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/60

  Jenkins run 
  (this Jupyter env `pavics/workflow-tests:210201.2` against a devel version of Raven `0.11.1` + `--nbval-lax`) 
  http://jenkins.ouranos.ca/job/PAVICS-e2e-workflow-tests/job/test-nbval-lax-DO_NOT_MERGE/4/console

  Only known error:
  ```
  20:25:45  =========================== short test summary info ============================
  20:25:45  FAILED pavics-sdi-master/docs/source/notebooks/WMS_example.ipynb::Cell 1
  20:25:45  FAILED pavics-sdi-master/docs/source/notebooks/WMS_example.ipynb::Cell 2
  20:25:45  FAILED pavics-sdi-master/docs/source/notebooks/WMS_example.ipynb::Cell 3
  20:25:45  FAILED pavics-sdi-master/docs/source/notebooks/WMS_example.ipynb::Cell 4
  20:25:45  FAILED pavics-sdi-master/docs/source/notebooks/WMS_example.ipynb::Cell 5
  20:25:45  FAILED pavics-sdi-master/docs/source/notebooks/WMS_example.ipynb::Cell 6
  20:25:45  FAILED pavics-sdi-master/docs/source/notebooks/WMS_example.ipynb::Cell 7
  20:25:45  FAILED raven-master/docs/source/notebooks/Bias_correcting_climate_data.ipynb::Cell 8
  20:25:45  FAILED raven-master/docs/source/notebooks/Bias_correcting_climate_data.ipynb::Cell 9
  20:25:45  FAILED raven-master/docs/source/notebooks/Bias_correcting_climate_data.ipynb::Cell 10
  20:25:45  FAILED raven-master/docs/source/notebooks/Bias_correcting_climate_data.ipynb::Cell 11
  20:25:45  FAILED raven-master/docs/source/notebooks/Full_process_example_1.ipynb::Cell 13
  20:25:45  FAILED raven-master/docs/source/notebooks/Full_process_example_1.ipynb::Cell 17
  20:25:45  FAILED raven-master/docs/source/notebooks/Full_process_example_1.ipynb::Cell 18
  20:25:45  FAILED raven-master/docs/source/notebooks/Full_process_example_1.ipynb::Cell 19
  20:25:45  FAILED raven-master/docs/source/notebooks/Full_process_example_1.ipynb::Cell 20
  20:25:45  FAILED raven-master/docs/source/notebooks/Full_process_example_1.ipynb::Cell 21
  20:25:45  FAILED raven-master/docs/source/notebooks/Multiple_watersheds_simulation.ipynb::Cell 1
  20:25:45  FAILED raven-master/docs/source/notebooks/Multiple_watersheds_simulation.ipynb::Cell 3
  20:25:45  FAILED raven-master/docs/source/notebooks/Multiple_watersheds_simulation.ipynb::Cell 4
  20:25:45  FAILED raven-master/docs/source/notebooks/Multiple_watersheds_simulation.ipynb::Cell 5
  20:25:45  FAILED raven-master/docs/source/notebooks/Region_selection.ipynb::Cell 7
  20:25:45  FAILED raven-master/docs/source/notebooks/Region_selection.ipynb::Cell 8
  20:25:45  FAILED raven-master/docs/source/notebooks/Subset_climate_data_over_watershed.ipynb::Cell 5
  20:25:45  ============ 24 failed, 226 passed, 2 skipped in 2528.69s (0:42:08) ============
  ```

[1.11.17](https://github.com/bird-house/birdhouse-deploy/tree/1.11.17) (2021-01-28)
------------------------------------------------------------------------------------------------------------------

- finch: update to version 0.6.1

  See Finch PR https://github.com/bird-house/finch/pull/147 for release notes.

  Deployed on my dev server, Jenkins run no new errors: http://jenkins.ouranos.ca/job/PAVICS-e2e-workflow-tests/job/master/900/console

[1.11.16](https://github.com/bird-house/birdhouse-deploy/tree/1.11.16) (2021-01-14)
------------------------------------------------------------------------------------------------------------------

- finch: upgrade to version 0.6.0

  See Finch PR for release notes https://github.com/bird-house/finch/pull/138.

  Should fix https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/issues/58.

[1.11.15](https://github.com/bird-house/birdhouse-deploy/tree/1.11.15) (2021-01-14)
------------------------------------------------------------------------------------------------------------------

- `jupyter`: update to version 201214

  Matching PR to deploy the new Jupyter env in PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/56 to PAVICS.

  Relevant changes:

  ```diff
  >   - cfgrib=0.9.8.5=pyhd8ed1ab_0

  <   - clisops=0.3.1=pyh32f6830_1
  >   - clisops=0.4.0=pyhd3deb0d_0

  <   - dask=2.30.0=py_0
  >   - dask=2020.12.0=pyhd8ed1ab_0

  <   - owslib=0.20.0=py_0
  >   - owslib=0.21.0=pyhd8ed1ab_0

  <   - xarray=0.16.1=py_0
  >   - xarray=0.16.2=pyhd8ed1ab_0

  <   - xclim=0.21.0=py_0
  >   - xclim=0.22.0=pyhd8ed1ab_0

  <   - jupyter_conda=3.4.1=pyh9f0ad1d_0
  >   - jupyter_conda=4.1.0=hd8ed1ab_1
  ```

[1.11.14](https://github.com/bird-house/birdhouse-deploy/tree/1.11.14) (2020-12-17)
------------------------------------------------------------------------------------------------------------------
- Add ability to execute post actions for deploy-data script.

  Script `deploy-data` was previously introduced in PR [#72](https://github.com/bird-house/birdhouse-deploy/pull/72) to 
  deploy any files from any git repos to the local host it runs.

  Now it grows the ability to run commands from the git repo it just pulls.

  Being able to run commands open new possibilities:
  * post-processing after files from git repo are deployed (ex: advanced file re-mapping)
  * execute up-to-date scripts from git repos (PR https://github.com/bird-house/birdhouse-deploy-ouranos/pull/2)

  Combining this `deploy-data` with the `scheduler` component means we have a way for cronjobs to 
  automatically always execute the most up-to-date version of any scripts from any git repos.

[1.11.13](https://github.com/bird-house/birdhouse-deploy/tree/1.11.13) (2020-12-14)
------------------------------------------------------------------------------------------------------------------
- `jupyterhub`: update to version 1.3.0 to include login terms patch

  This version of jupyterhub includes the login terms patch originally
  introduced in commit 
  [8be8eeac211d3f5c2de620781db8832fdb8f9093](https://github.com/bird-house/birdhouse-deploy/commit/8be8eeac211d3f5c2de620781db8832fdb8f9093)
  of PR [#104](https://github.com/bird-house/birdhouse-deploy/pull/104).

  This official login terms feature has a few enhancements (see https://github.com/jupyterhub/jupyterhub/pull/3264#discussion_r530466178):

  * no javascript dependency
  * pop-up reminder for user to check the checkbox

  Behavior change is the "Sign in" button is not longer disabled if
  unchecked.  It simply does not work and reminds the user to check the
  checkbox if unchecked.

  Before:

  ![recorded](https://user-images.githubusercontent.com/11966697/99327962-1aa9ee80-2849-11eb-9ce8-3be6a1484e94.gif)

  After:
  ![recorded](https://user-images.githubusercontent.com/11966697/100246404-18115e00-2f07-11eb-9061-d35434ace3aa.gif)

[1.11.12](https://github.com/bird-house/birdhouse-deploy/tree/1.11.12) (2020-11-25)
------------------------------------------------------------------------------------------------------------------
- Fix geoserver not configured properly behind proxy.

  Hitting https://pavics.ouranos.ca/geoserver/wfs?request=GetCapabilities&version=1.1.0

  Before fix (wrong scheme and wrong port):
  ```
  <ows:Operation name="GetCapabilities">
  <ows:DCP>
  <ows:HTTP>
  <ows:Get xlink:href="http://pavics.ouranos.ca:80/geoserver/wfs"/>
  <ows:Post xlink:href="http://pavics.ouranos.ca:80/geoserver/wfs"/>
  </ows:HTTP>
  </ows:DCP>
  ```

  After fix:
  ```
  <ows:Operation name="GetCapabilities">
  <ows:DCP>
  <ows:HTTP>
  <ows:Get xlink:href="https://pavics.ouranos.ca:443/geoserver/wfs"/>
  <ows:Post xlink:href="https://pavics.ouranos.ca:443/geoserver/wfs"/>
  </ows:HTTP>
  </ows:DCP>
  ```

  This config automate manual step to set proxy base url in Geoserver UI 
  https://docs.geoserver.org/2.9.3/user/configuration/globalsettings.html#proxy-base-url

  I had to override the docker image entrypoint to edit the `server.xml` on the fly before starting Geoserver (Tomcat) 
  since setting Java proxy config did not seem to work (see first commit).

  Related to https://github.com/Ouranosinc/raven/issues/297.

[1.11.11](https://github.com/bird-house/birdhouse-deploy/tree/1.11.11) (2020-11-20)
------------------------------------------------------------------------------------------------------------------
- Various small fixes.

  `monitoring`: prevent losing stats when VM auto start from a power failure

  `check-instance-ready`: new script to smoke test instance 
  (use in `bootstrap-instance-for-testsuite` for our automation pipeline).

  jupyter: add CATALOG_USERNAME and anonymous to blocked_users list for security
  See comment https://github.com/bird-house/birdhouse-deploy/pull/102#issuecomment-730109547
  and comment https://github.com/bird-house/birdhouse-deploy/pull/102#issuecomment-730407914

      They are not real Jupyter users and their password is known.

      See config/magpie/permissions.cfg.template that created those users.

      Tested:
      ```
      [W 2020-11-20 13:25:18.924 JupyterHub auth:487] User 'admin-catalog' blocked. Stop authentication
      [W 2020-11-20 13:25:18.924 JupyterHub base:752] Failed login for admin-catalog

      [W 2020-11-20 13:49:18.069 JupyterHub auth:487] User 'anonymous' blocked. Stop authentication
      [W 2020-11-20 13:49:18.070 JupyterHub base:752] Failed login for anonymous
      ```

[1.11.10](https://github.com/bird-house/birdhouse-deploy/tree/1.11.10) (2020-11-18)
------------------------------------------------------------------------------------------------------------------
- Add terms conditions to JupyterHub login page and update to latest JupyterHub version.

  User have to check the checkbox agreeing to the terms and conditions in order to login 
  (fixes [Ouranosinc/pavics-sdi#188](https://github.com/Ouranosinc/pavics-sdi/issues/188)).

  User will have to accept the terms and conditions (the checkbox) each time he needs to login. 
  However, if user do not logout or wipe his browser cookies, the next time he navigate to the login page, 
  he'll just log right in, no password is asked so no terms and conditions to accept either.

  This behavior is optional and only enabled if `JUPYTER_LOGIN_TERMS_URL` in `env.local` is set.

  Had to patch the `login.html` template from jupyterhub docker image for this feature 
  (PR [jupyterhub/jupyterhub#3264](https://github.com/jupyterhub/jupyterhub/pull/3264)).

  Also update jupyterhub docker image to latest version.

  Deployed to my test server https://lvupavics.ouranos.ca/jupyter/hub/login 
  (pointing to a bogus terms and conditions link for now).

  Tested on Firefox and Google Chrome.

  Tested that upgrade from jupyterhub `1.0.0` to `1.2.1` is completely transparent to already logged in jupyter users.
  ```
  [D 2020-11-18 19:53:52.517 JupyterHub app:2055] Verifying that lvu is running at http://172.18.0.3:8888/jupyter/user/lvu/
  [D 2020-11-18 19:53:52.523 JupyterHub utils:220] Server at http://172.18.0.3:8888/jupyter/user/lvu/ responded with 302
  [D 2020-11-18 19:53:52.523 JupyterHub _version:76] jupyterhub and jupyterhub-singleuser both on version 1.2.1
  [I 2020-11-18 19:53:52.524 JupyterHub app:2069] lvu still running
  ```

  ![recorded](https://user-images.githubusercontent.com/11966697/99327962-1aa9ee80-2849-11eb-9ce8-3be6a1484e94.gif)

[1.11.9](https://github.com/bird-house/birdhouse-deploy/tree/1.11.9) (2020-11-13)
------------------------------------------------------------------------------------------------------------------
- `jupyter`: new image with 4 new extensions

  The google drive extension for JupyterLab requires a settings file containing the clientid of the project created 
  in developers.google.com, which give authorization to use google drive.

  This PR's role is to include this file in the birdhouse configs.

  Matching PR [Ouranosinc/PAVICS-e2e-workflow-tests#54](https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/54)
  (commit [5d5a9aa2251386378406efb5b414b3aa6db0b37e](https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/commit/5d5a9aa2251386378406efb5b414b3aa6db0b37e)) 
  for the new image with 4 new extensions: `jupytext`, `jupyterlab-google-drive`, `jupyter_conda` and `jupyterlab-git`

  Matching PR https://github.com/Ouranosinc/pavics-sdi/pull/185 for documentation about the new extensions.

[1.11.8](https://github.com/bird-house/birdhouse-deploy/tree/1.11.8) (2020-11-06)
------------------------------------------------------------------------------------------------------------------
- bump `finch` to version-0.5.3

[1.11.7](https://github.com/bird-house/birdhouse-deploy/tree/1.11.7) (2020-11-06)
------------------------------------------------------------------------------------------------------------------
- bump `thredds-docker` to 4.6.15

[1.11.6](https://github.com/bird-house/birdhouse-deploy/tree/1.11.6) (2020-11-06)
------------------------------------------------------------------------------------------------------------------
- Prepare fresh deployment for automated tests.

  @MatProv is building an automated pipeline that will provision and deploy a full PAVICS stack and run our Jenkins test suite for each PR here.

  So each time his new fresh instance comes up, there are a few steps to perform for the Jenkins test suite to pass.  Those steps are captured in `scripts/bootstrap-instance-for-testsuite`.  @MatProv please call this script, do not perform each steps yourself so any future changes to those steps will be transparent to your pipeline.  A new optional components was also required, done in PR https://github.com/bird-house/birdhouse-deploy/pull/92.

  For security reasons, Jupyterhub will block the test user to login since its password is known publicly.

  Each step are also in their own script so can be assembled differently to prepare the fresh instance if desired.

  Solr query in the canarie monitoring also updated to target the minimal dataset from `bootstrap-testdata` so the canarie monitoring page works on all PAVICS deployment (fixes https://github.com/bird-house/birdhouse-deploy/issues/6).  @MatProv you can use this canarie monitoring page (ex: https://pavics.ouranos.ca/canarie/node/service/status) to confirm the fresh instance is ready to run the Jenkins test suite.

[1.11.5](https://github.com/bird-house/birdhouse-deploy/tree/1.11.5) (2020-10-27)
------------------------------------------------------------------------------------------------------------------
- `jupyter`: new image for python 3.8, new xclim and memory_profiler

  Matching PR to deploy the new Jupyter image to PAVICS.

  Deployed to https://medus.ouranos.ca/jupyter/ for testing.  This one has python 3.8, might worth some manual testing.

  Relevant changes:
  ```diff
  <   - python=3.7.8=h6f2ec95_1_cpython
  >   - python=3.8.6=h852b56e_0_cpython

  <   - xclim=0.20.0=py_0
  >   - xclim=0.21.0=py_0

  <   - dask=2.27.0=py_0
  >   - dask=2.30.0=py_0

  <   - rioxarray=0.0.31=py_0
  >   - rioxarray=0.1.0=py_0

  >   - memory_profiler=0.58.0=py_0
  ```

  More info, see PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/53 (commit https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/commit/f07f1657ed13a0ed92854c5d01f9d3ed785e870d)

[1.11.4](https://github.com/bird-house/birdhouse-deploy/tree/1.11.4) (2020-10-15)
------------------------------------------------------------------------------------------------------------------
- Sync Raven testdata to Thredds for Raven tutorial notebooks.

  Leveraging the cron daemon of the scheduler component, sync Raven testdata to Thredds for Raven tutorial notebooks.

  Activation of the pre-configured cronjob is via `env.local` as usual for infra-as-code.

  New generic `deploy-data` script can clone any number of git repos, sync any number of folders in the git repo to any number of local folders, with ability to cherry-pick just the few files needed (Raven testdata has many types of files, we only need to sync `.nc` files to Thredds, to avoid polluting Thredds storage `/data/datasets/testdata/raven`).

  Limitation of the first version of this `deploy-data` script:
  * Do not handle re-organizing file layout, this is a pure sync only with very limited rsync filtering for now (tutorial notebooks deploy from multiple repos, need re-organizing the file layout)

  So the script has room to grow.  I see it as a generic solution to the repeated problem "take files from various git repos and deploy them somewhere automatically".  If we need to deploy another repo, juste write a new config file, stop writing boilerplate code again.

  Minor unrelated change in this PR:
  * README update to reference the new birdhouse-deploy-ouranos.
  * Make sourcing the various pre-configured cronjob backward-compat with older version of the repo where those cronjob did not exist yet.

[1.11.3](https://github.com/bird-house/birdhouse-deploy/tree/1.11.3) (2020-09-28)
------------------------------------------------------------------------------------------------------------------
- `jupyter`: new build for new xclim with fix for missing clisops dependency

  Matching PR to deploy new Jupyter env from PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/52 (commit https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/commit/18c8397ff30c9ba4b9f56896df4c898c7e9a356e).

  Deployed to https://medus.ouranos.ca/jupyter/ for testing.

  Relevant changes:
  ```diff
  >   - clisops=0.3.1=pyh32f6830_1

  <     - xclim==0.19.0
  >   - xclim=0.20.0=py_0

  <   - xarray=0.16.0py_0
  >   - xarray=0.16.1=py_0

  <   - dask=2.26.0=py_0
  >   - dask=2.27.0=py_0

  <   - fiona=1.8.13=py37h0492a4a_1
  >   - fiona=1.8.17=py37ha3d844c_0

  <   - gdal=3.0.4=py37h4b180d9_10
  >   - gdal=3.1.2=py37h518339e_2

  <   - jupyter_server=0.1.1=py37_0
  >   - jupyter_server=1.0.1=py37hc8dfbb8_0

  >     - jupyternotify==0.1.15

  >     - pytest-tornasync==0.6.0.post2
  ```

  See PR above for full changes.

[1.11.2](https://github.com/bird-house/birdhouse-deploy/tree/1.11.2) (2020-09-15)
------------------------------------------------------------------------------------------------------------------
- Auto-renew LetsEncrypt SSL certificate.

  Auto-renew LetsEncrypt SSL certificate leveraging the cron jobs of the "scheduler" component.  Meaning this feature is self-contained in the PAVICS stack, no dependency on the host's cron jobs.

  Default behavior is to attempt renewal everyday.  `certbot` client in `renew` mode will not hit LetsEncrypt server if renewal is not allowed (not within 1 month of expiry) so this should not put too much stress on LetsEncrypt server.  However, this gives us 30 retry opportunities (1 month) if something is wrong on the first try.

  All configs are centralized in `env.local`, easing reproducibility on multiple deployments of PAVICS and following infra-as-code.

  User can still perform the renewal manually by calling `certbotwrapper` directly. User is not forced to enable the "scheduler" component but will miss out on the automatic renewal.

  Documentation for activating this automatic renewal is in `env.local.example`.

  See `vagrant-utils/configure-pavics.sh` for how it's being used for real in a Vagrant box.

  Logs (`/var/log/PAVICS/renew_letsencrypt_ssl.log`) when no renewal is necessary, proxy down time less than 1 minute:
  [certbot-renew-no-ops.txt](https://github.com/bird-house/birdhouse-deploy/files/5209376/certbot-renew-no-ops.txt)
  ```
  ==========
  certbotwrapper START_TIME=2020-09-11T01:20:02+0000
  + realpath /vagrant/birdhouse/deployment/certbotwrapper
  + THIS_FILE=/vagrant/birdhouse/deployment/certbotwrapper
  + dirname /vagrant/birdhouse/deployment/certbotwrapper
  + THIS_DIR=/vagrant/birdhouse/deployment
  + pwd
  + SAVED_PWD=/
  + . /vagrant/birdhouse/deployment/../default.env
  + export 'DOCKER_NOTEBOOK_IMAGE=pavics/workflow-tests:200803'
  + export 'FINCH_IMAGE=birdhouse/finch:version-0.5.2'
  + export 'THREDDS_IMAGE=unidata/thredds-docker:4.6.14'
  + export 'JUPYTERHUB_USER_DATA_DIR=/data/jupyterhub_user_data'
  + export 'JUPYTER_DEMO_USER=demo'
  + export 'JUPYTER_DEMO_USER_MEM_LIMIT=2G'
  + export 'JUPYTER_DEMO_USER_CPU_LIMIT=0.5'
  + export 'JUPYTER_LOGIN_BANNER_TOP_SECTION='
  + export 'JUPYTER_LOGIN_BANNER_BOTTOM_SECTION='
  + export 'CANARIE_MONITORING_EXTRA_CONF_DIR=/conf.d'
  + export 'THREDDS_ORGANIZATION=Birdhouse'
  + export 'MAGPIE_DB_NAME=magpiedb'
  + export 'VERIFY_SSL=true'
  + export 'AUTODEPLOY_DEPLOY_KEY_ROOT_DIR=/root/.ssh'
  + export 'AUTODEPLOY_PLATFORM_FREQUENCY=7 5 * * *'
  + export 'AUTODEPLOY_NOTEBOOK_FREQUENCY=@hourly'
  + ENV_LOCAL_FILE=/vagrant/birdhouse/deployment/../env.local
  + set +x
  + CERT_DOMAIN=
  + '[' -z  ]
  + CERT_DOMAIN=lvupavicsmaster.ouranos.ca
  + '[' '!' -z 1 ]
  + cd /vagrant/birdhouse/deployment/..
  + docker stop proxy
  proxy
  + cd /
  + CERTBOT_OPTS=
  + '[' '!' -z 1 ]
  + CERTBOT_OPTS=renew
  + docker run --rm --name certbot -v /etc/letsencrypt:/etc/letsencrypt -v /var/lib/letsencrypt:/var/lib/letsencrypt -v /var/log/letsencrypt:/var/log/letsencrypt -p 443:443 -p 80:80 certbot/certbot:v1.3.0 renew
  Saving debug log to /var/log/letsencrypt/letsencrypt.log

  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  Processing /etc/letsencrypt/renewal/lvupavicsmaster.ouranos.ca.conf
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  Cert not yet due for renewal

  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  The following certs are not due for renewal yet:
    /etc/letsencrypt/live/lvupavicsmaster.ouranos.ca/fullchain.pem expires on 2020-11-02 (skipped)
  No renewals were attempted.
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  + RC=0
  + '[' '!' -z 1 ]
  + TMP_SSL_CERT=/tmp/tmp_certbotwrapper_ssl_cert.pem
  + CERTPATH=/etc/letsencrypt/live/lvupavicsmaster.ouranos.ca
  + cd /vagrant/birdhouse/deployment/..
  + docker run --rm --name copy_cert -v /etc/letsencrypt:/etc/letsencrypt bash cat /etc/letsencrypt/live/lvupavicsmaster.ouranos.ca/fullchain.pem /etc/letsencrypt/live/lvupavicsmaster.ouranos.ca/privkey.pem
  + diff /home/vagrant/certkey.pem /tmp/tmp_certbotwrapper_ssl_cert.pem
  + rm -v /tmp/tmp_certbotwrapper_ssl_cert.pem
  removed '/tmp/tmp_certbotwrapper_ssl_cert.pem'
  + '[' -z  ]
  + docker start proxy
  proxy
  + cd /
  + set +x

  certbotwrapper finished START_TIME=2020-09-11T01:20:02+0000
  certbotwrapper finished   END_TIME=2020-09-11T01:20:21+0000
  ```

  Logs when renewal is needed but failed due to firewall, `certbot` adds a random delay so proxy could be down up to 10 mins:
  [certbot-renew-error.txt](https://github.com/bird-house/birdhouse-deploy/files/5209403/certbot-renew-error.txt)

  ```
  ==========
  certbotwrapper START_TIME=2020-09-11T13:00:04+0000
  + realpath /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/certbotwrapper
  + THIS_FILE=/home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/certbotwrapper
  + dirname /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/certbotwrapper
  + THIS_DIR=/home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment
  + pwd
  + SAVED_PWD=/
  + . /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/../default.env
  + export 'DOCKER_NOTEBOOK_IMAGE=pavics/workflow-tests:200803'
  + export 'FINCH_IMAGE=birdhouse/finch:version-0.5.2'
  + export 'THREDDS_IMAGE=unidata/thredds-docker:4.6.14'
  + export 'JUPYTERHUB_USER_DATA_DIR=/data/jupyterhub_user_data'
  + export 'JUPYTER_DEMO_USER=demo'
  + export 'JUPYTER_DEMO_USER_MEM_LIMIT=2G'
  + export 'JUPYTER_DEMO_USER_CPU_LIMIT=0.5'
  + export 'JUPYTER_LOGIN_BANNER_TOP_SECTION='
  + export 'JUPYTER_LOGIN_BANNER_BOTTOM_SECTION='
  + export 'CANARIE_MONITORING_EXTRA_CONF_DIR=/conf.d'
  + export 'THREDDS_ORGANIZATION=Birdhouse'
  + export 'MAGPIE_DB_NAME=magpiedb'
  + export 'VERIFY_SSL=true'
  + export 'AUTODEPLOY_DEPLOY_KEY_ROOT_DIR=/root/.ssh'
  + export 'AUTODEPLOY_PLATFORM_FREQUENCY=7 5 * * *'
  + export 'AUTODEPLOY_NOTEBOOK_FREQUENCY=@hourly'
  + ENV_LOCAL_FILE=/home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/../env.local
  + set +x
  + CERT_DOMAIN=
  + '[' -z  ]
  + CERT_DOMAIN=medus.ouranos.ca
  + '[' '!' -z 1 ]
  + cd /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/..
  + docker stop proxy
  proxy
  + cd /
  + CERTBOT_OPTS=
  + '[' '!' -z 1 ]
  + CERTBOT_OPTS=renew
  + docker run --rm --name certbot -v /etc/letsencrypt:/etc/letsencrypt -v /var/lib/letsencrypt:/var/lib/letsencrypt -v /var/log/letsencrypt:/var/log/letsencrypt -p 443:443 -p 80:80 certbot/certbot:v1.3.0 renew
  Saving debug log to /var/log/letsencrypt/letsencrypt.log

  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  Processing /etc/letsencrypt/renewal/medus.ouranos.ca.conf
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  Cert is due for renewal, auto-renewing...
  Non-interactive renewal: random delay of 10.77459918236335 seconds
  Plugins selected: Authenticator standalone, Installer None
  Renewing an existing certificate
  Performing the following challenges:
  http-01 challenge for medus.ouranos.ca
  Waiting for verification...
  Challenge failed for domain medus.ouranos.ca
  http-01 challenge for medus.ouranos.ca
  Cleaning up challenges
  Attempting to renew cert (medus.ouranos.ca) from /etc/letsencrypt/renewal/medus.ouranos.ca.conf produced an unexpected error: Some challenges have failed.. Skipping.
  All renewal attempts failed. The following certs could not be renewed:
    /etc/letsencrypt/live/medus.ouranos.ca/fullchain.pem (failure)

  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  All renewal attempts failed. The following certs could not be renewed:
    /etc/letsencrypt/live/medus.ouranos.ca/fullchain.pem (failure)
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  1 renew failure(s), 0 parse failure(s)
  IMPORTANT NOTES:
   - The following errors were reported by the server:

     Domain: medus.ouranos.ca
     Type:   connection
     Detail: Fetching
     http://medus.ouranos.ca/.well-known/acme-challenge/F-_TzoOMcgoo5WC9FQvi_QdKuoqdsrQFa7MR2bEdnJE:
     Timeout during connect (likely firewall problem)

     To fix these errors, please make sure that your domain name was
     entered correctly and the DNS A/AAAA record(s) for that domain
     contain(s) the right IP address. Additionally, please check that
     your computer has a publicly routable IP address and that no
     firewalls are preventing the server from communicating with the
     client. If you're using the webroot plugin, you should also verify
     that you are serving files from the webroot path you provided.
  + RC=1
  + '[' '!' -z 1 ]
  + TMP_SSL_CERT=/tmp/tmp_certbotwrapper_ssl_cert.pem
  + CERTPATH=/etc/letsencrypt/live/medus.ouranos.ca
  + cd /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/..
  + docker run --rm --name copy_cert -v /etc/letsencrypt:/etc/letsencrypt bash cat /etc/letsencrypt/live/medus.ouranos.ca/fullchain.pem /etc/letsencrypt/live/medus.ouranos.ca/privkey.pem
  + diff /etc/letsencrypt/live/medus.ouranos.ca/certkey.pem /tmp/tmp_certbotwrapper_ssl_cert.pem
  + rm -v /tmp/tmp_certbotwrapper_ssl_cert.pem
  removed '/tmp/tmp_certbotwrapper_ssl_cert.pem'
  + '[' -z  ]
  + docker start proxy
  proxy
  + cd /
  + set +x

  certbotwrapper finished START_TIME=2020-09-11T13:00:04+0000
  certbotwrapper finished   END_TIME=2020-09-11T13:00:49+0000
  ```

  Logs when renewal is successful, again proxy could be down up to 10 mins due to random delay by `certbot` client:
  [certbot-renew-success-in-2-run-after-file-copy-fix.txt](https://github.com/bird-house/birdhouse-deploy/files/5209924/certbot-renew-success-in-2-run-after-file-copy-fix.txt)

  ```
  ==========
  certbotwrapper START_TIME=2020-09-11T13:10:04+0000
  + realpath /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/certbotwrapper
  + THIS_FILE=/home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/certbotwrapper
  + dirname /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/certbotwrapper
  + THIS_DIR=/home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment
  + pwd
  + SAVED_PWD=/
  + . /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/../default.env
  + export 'DOCKER_NOTEBOOK_IMAGE=pavics/workflow-tests:200803'
  + export 'FINCH_IMAGE=birdhouse/finch:version-0.5.2'
  + export 'THREDDS_IMAGE=unidata/thredds-docker:4.6.14'
  + export 'JUPYTERHUB_USER_DATA_DIR=/data/jupyterhub_user_data'
  + export 'JUPYTER_DEMO_USER=demo'
  + export 'JUPYTER_DEMO_USER_MEM_LIMIT=2G'
  + export 'JUPYTER_DEMO_USER_CPU_LIMIT=0.5'
  + export 'JUPYTER_LOGIN_BANNER_TOP_SECTION='
  + export 'JUPYTER_LOGIN_BANNER_BOTTOM_SECTION='
  + export 'CANARIE_MONITORING_EXTRA_CONF_DIR=/conf.d'
  + export 'THREDDS_ORGANIZATION=Birdhouse'
  + export 'MAGPIE_DB_NAME=magpiedb'
  + export 'VERIFY_SSL=true'
  + export 'AUTODEPLOY_DEPLOY_KEY_ROOT_DIR=/root/.ssh'
  + export 'AUTODEPLOY_PLATFORM_FREQUENCY=7 5 * * *'
  + export 'AUTODEPLOY_NOTEBOOK_FREQUENCY=@hourly'
  + ENV_LOCAL_FILE=/home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/../env.local
  + set +x
  + CERT_DOMAIN=
  + '[' -z  ]
  + CERT_DOMAIN=medus.ouranos.ca
  + '[' '!' -z 1 ]
  + cd /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/..
  + docker stop proxy
  proxy
  + cd /
  + CERTBOT_OPTS=
  + '[' '!' -z 1 ]
  + CERTBOT_OPTS=renew
  + docker run --rm --name certbot -v /etc/letsencrypt:/etc/letsencrypt -v /var/lib/letsencrypt:/var/lib/letsencrypt -v /var/log/letsencrypt:/var/log/letsencrypt -p 443:443 -p 80:80 certbot/certbot:v1.3.0 renew
  Saving debug log to /var/log/letsencrypt/letsencrypt.log

  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  Processing /etc/letsencrypt/renewal/medus.ouranos.ca.conf
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  Cert is due for renewal, auto-renewing...
  Non-interactive renewal: random delay of 459.45712705256506 seconds
  Plugins selected: Authenticator standalone, Installer None
  Renewing an existing certificate
  Performing the following challenges:
  http-01 challenge for medus.ouranos.ca
  Waiting for verification...
  Cleaning up challenges

  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  new certificate deployed without reload, fullchain is
  /etc/letsencrypt/live/medus.ouranos.ca/fullchain.pem
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  Congratulations, all renewals succeeded. The following certs have been renewed:
    /etc/letsencrypt/live/medus.ouranos.ca/fullchain.pem (success)
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  + RC=0
  + '[' '!' -z 1 ]
  + TMP_SSL_CERT=/tmp/tmp_certbotwrapper_ssl_cert.pem
  + CERTPATH=/etc/letsencrypt/live/medus.ouranos.ca
  + cd /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/..
  + docker run --rm --name copy_cert -v /etc/letsencrypt:/etc/letsencrypt bash cat /etc/letsencrypt/live/medus.ouranos.ca/fullchain.pem /etc/letsencrypt/live/medus.ouranos.ca/privkey.pem
  + diff /etc/letsencrypt/live/medus.ouranos.ca/certkey.pem /tmp/tmp_certbotwrapper_ssl_cert.pem
  --- /etc/letsencrypt/live/medus.ouranos.ca/certkey.pem
  +++ /tmp/tmp_certbotwrapper_ssl_cert.pem
  @@ -1,33 +1,33 @@
   -----BEGIN CERTIFICATE-----

  REMOVED for Privacy.

   -----END PRIVATE KEY-----
  + '[' 0 -eq 0 ]
  + cp -v /tmp/tmp_certbotwrapper_ssl_cert.pem /etc/letsencrypt/live/medus.ouranos.ca/certkey.pem
  cp: can't create '/etc/letsencrypt/live/medus.ouranos.ca/certkey.pem': File exists
  + rm -v /tmp/tmp_certbotwrapper_ssl_cert.pem
  removed '/tmp/tmp_certbotwrapper_ssl_cert.pem'
  + '[' -z  ]
  + docker start proxy
  proxy
  + cd /
  + set +x

  certbotwrapper finished START_TIME=2020-09-11T13:10:04+0000
  certbotwrapper finished   END_TIME=2020-09-11T13:18:10+0000
  ==========
  certbotwrapper START_TIME=2020-09-11T15:00:06+0000
  + realpath /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/certbotwrapper
  + THIS_FILE=/home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/certbotwrapper
  + dirname /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/certbotwrapper
  + THIS_DIR=/home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment
  + pwd
  + SAVED_PWD=/
  + . /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/../default.env
  + export 'DOCKER_NOTEBOOK_IMAGE=pavics/workflow-tests:200803'
  + export 'FINCH_IMAGE=birdhouse/finch:version-0.5.2'
  + export 'THREDDS_IMAGE=unidata/thredds-docker:4.6.14'
  + export 'JUPYTERHUB_USER_DATA_DIR=/data/jupyterhub_user_data'
  + export 'JUPYTER_DEMO_USER=demo'
  + export 'JUPYTER_DEMO_USER_MEM_LIMIT=2G'
  + export 'JUPYTER_DEMO_USER_CPU_LIMIT=0.5'
  + export 'JUPYTER_LOGIN_BANNER_TOP_SECTION='
  + export 'JUPYTER_LOGIN_BANNER_BOTTOM_SECTION='
  + export 'CANARIE_MONITORING_EXTRA_CONF_DIR=/conf.d'
  + export 'THREDDS_ORGANIZATION=Birdhouse'
  + export 'MAGPIE_DB_NAME=magpiedb'
  + export 'VERIFY_SSL=true'
  + export 'AUTODEPLOY_DEPLOY_KEY_ROOT_DIR=/root/.ssh'
  + export 'AUTODEPLOY_PLATFORM_FREQUENCY=7 5 * * *'
  + export 'AUTODEPLOY_NOTEBOOK_FREQUENCY=@hourly'
  + ENV_LOCAL_FILE=/home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/../env.local
  + set +x
  + CERT_DOMAIN=
  + '[' -z  ]
  + CERT_DOMAIN=medus.ouranos.ca
  + '[' '!' -z 1 ]
  + cd /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/..
  + docker stop proxy
  proxy
  + cd /
  + CERTBOT_OPTS=
  + '[' '!' -z 1 ]
  + CERTBOT_OPTS=renew
  + docker run --rm --name certbot -v /etc/letsencrypt:/etc/letsencrypt -v /var/lib/letsencrypt:/var/lib/letsencrypt -v /var/log/letsencrypt:/var/log/letsencrypt -p 443:443 -p 80:80 certbot/certbot:v1.3.0 renew
  Saving debug log to /var/log/letsencrypt/letsencrypt.log

  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  Processing /etc/letsencrypt/renewal/medus.ouranos.ca.conf
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  Cert not yet due for renewal

  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  The following certs are not due for renewal yet:
    /etc/letsencrypt/live/medus.ouranos.ca/fullchain.pem expires on 2020-12-10 (skipped)
  No renewals were attempted.
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  + RC=0
  + '[' '!' -z 1 ]
  + TMP_SSL_CERT=/tmp/tmp_certbotwrapper_ssl_cert.pem
  + CERTPATH=/etc/letsencrypt/live/medus.ouranos.ca
  + cd /home/mourad/PROJECTS/birdhouse-deploy/birdhouse/deployment/..
  + docker run --rm --name copy_cert -v /etc/letsencrypt:/etc/letsencrypt bash cat /etc/letsencrypt/live/medus.ouranos.ca/fullchain.pem /etc/letsencrypt/live/medus.ouranos.ca/privkey.pem
  + diff /etc/letsencrypt/live/medus.ouranos.ca/certkey.pem /tmp/tmp_certbotwrapper_ssl_cert.pem
  --- /etc/letsencrypt/live/medus.ouranos.ca/certkey.pem
  +++ /tmp/tmp_certbotwrapper_ssl_cert.pem
  @@ -1,33 +1,33 @@
   -----BEGIN CERTIFICATE-----

  REMOVED for Privacy.

   -----END PRIVATE KEY-----
  + '[' 0 -eq 0 ]
  + cp -v /tmp/tmp_certbotwrapper_ssl_cert.pem /etc/letsencrypt/live/medus.ouranos.ca/certkey.pem
  '/tmp/tmp_certbotwrapper_ssl_cert.pem' -> '/etc/letsencrypt/live/medus.ouranos.ca/certkey.pem'
  + rm -v /tmp/tmp_certbotwrapper_ssl_cert.pem
  removed '/tmp/tmp_certbotwrapper_ssl_cert.pem'
  + '[' -z  ]
  + docker start proxy
  proxy
  + cd /
  + set +x

  certbotwrapper finished START_TIME=2020-09-11T15:00:06+0000
  certbotwrapper finished   END_TIME=2020-09-11T15:00:31+0000
  ```

[1.11.1](https://github.com/bird-house/birdhouse-deploy/tree/1.11.1) (2020-09-15)
------------------------------------------------------------------------------------------------------------------
- `jupyter`: new updated image with new handcalcs package

  Matching PR to deploy the new jupyter image to PAVICS.

  See PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/50
  (commit https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/commit/02333bfa11931f4a0b7c9607b88904bd063bed70)
  that built the new image with the detailed change vs the previous image.

  Add handcalcs https://github.com/connorferster/handcalcs/ and unpin hvplot
  since pinning did not solve violin plot issue, see this comment
  https://github.com/bird-house/birdhouse-deploy/pull/63#issuecomment-668270608

  Successful Jenkins build
  http://jenkins.ouranos.ca/job/PAVICS-e2e-workflow-tests/job/periodic-rebuild-and-add-handcalcs/1/console

  Noticeable changes:
  ```diff
  >     - handcalcs==0.8.1

  <     - xclim==0.18.0
  >     - xclim==0.19.0

  <   - hvplot=0.5.2=py_0
  >   - hvplot=0.6.0=pyh9f0ad1d_0

  <   - dask=2.22.0=py_0
  >   - dask=2.26.0=py_0

  <   - bokeh=2.1.1=py37hc8dfbb8_0
  >   - bokeh=2.2.1=py37hc8dfbb8_0

  <   - numba=0.50.1=py37h0da4684_1
  >   - numba=0.51.2=py37h9fdb41a_0
  ```

[1.11.0](https://github.com/bird-house/birdhouse-deploy/tree/1.11.0) (2020-08-25)
------------------------------------------------------------------------------------------------------------------
- Improved plugable component architecture.

  Before this PR, components needing default values, needing template variable substitution, needing to execute commands pre and post `docker-compose up` are hardcoding their needs directly to the "core" system, basically "leaking" their requirements out even when they are not activated (fixes https://github.com/bird-house/birdhouse-deploy/issues/62).

  This PR provides true plugable architecture for the components so they can provide all their needs without having to modify the code of the "core" system.

  All the components (monitoring, generic_bird, emu, testthredds) are modified to leverage the new plugable architecture, with additional customizations given it is cleaner/easier to have default configuration values.

  Given this PR both changes the architecture and modify many components at the same time, it is best to read each commit separately to easier understand which code change belongs to which "goal".

  Deployed here https://lvupavicsmaster.ouranos.ca with all the impacted components activated to test the change:
  * Canarie: https://lvupavicsmaster.ouranos.ca/canarie/node/service/status
  * Generic bird (using Finch): https://lvupavicsmaster.ouranos.ca/twitcher/ows/proxy/generic_bird?service=WPS&version=1.0.0&request=GetCapabilities
  * Emu: https://lvupavicsmaster.ouranos.ca/twitcher/ows/proxy/emu?service=WPS&version=1.0.0&request=GetCapabilities
  * Test Thredds: https://lvupavicsmaster.ouranos.ca/testthredds/catalog.html
  * Prometheus: http://lvupavicsmaster.ouranos.ca:9090/alerts
  * AlertManager: http://lvupavicsmaster.ouranos.ca:9093/
  * Grafana dashboard: http://lvupavicsmaster.ouranos.ca:3001/d/pf6xQMWGz/docker-and-system-monitoring?orgId=1&refresh=5m

[1.10.4](https://github.com/bird-house/birdhouse-deploy/tree/1.10.4) (2020-08-05)
------------------------------------------------------------------------------------------------------------------
- `jupyter`: new update image with hvplot pinned to older version for violin plot

  See PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/48 (commit https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/commit/4ad6ba6fa2a4ecf6d5d78e0602b39202307bcb76) for more detailed info.

  Deployed to Medus for testing (as regular PAVICS image, not the devel image).  @aulemahal reported back that violin plot still do not work even with the old hvplot pinned in this image.

  I'll release this image as-is since violin plot is also not working in the previous image that had hvplot 0.6.0 so no new regression there.  Will unpin hvplot on next image build because pinning it did not fix violin plot (probably interference from other newer packages in this build).

  Noticeable changes:
  ```diff
  <   - hvplot=0.6.0=pyh9f0ad1d_0
  >   - hvplot=0.5.2=py_0

  <   - dask=2.20.0=py_0
  >   - dask=2.22.0=py_0

  <   - geopandas=0.8.0=py_1
  >   - geopandas=0.8.1=py_0

  <   - pandas=1.0.5=py37h0da4684_0
  >   - pandas=1.1.0=py37h3340039_0

  <   - matplotlib=3.2.2=1
  >   - matplotlib=3.3.0=1

  <   - numpy=1.18.5=py37h8960a57_0
  >   - numpy=1.19.1=py37h8960a57_0

  <   - cryptography=2.9.2=py37hb09aad4_0
  >   - cryptography=3.0=py37hb09aad4_0

  <   - python=3.7.6=h8356626_5_cpython
  >   - python=3.7.8=h6f2ec95_1_cpython

  <   - nbval=0.9.5=py_0
  >   - nbval=0.9.6=pyh9f0ad1d_0

  <   - pytest=5.4.3=py37hc8dfbb8_0
  >   - pytest=6.0.1=py37hc8dfbb8_0
  ```

[1.10.3](https://github.com/bird-house/birdhouse-deploy/tree/1.10.3) (2020-07-21)
------------------------------------------------------------------------------------------------------------------
- `proxy`: increase timeout for reading a response from the proxied server

  Fixes https://github.com/Ouranosinc/raven/issues/286

  "there seems to be a problem with the size of the ncml and the timeout
  if I use more than 10-12 years as the historical data. I get a :
  "Netcdf: DAP failure" error if I use too many years."

  ```
  ________________________________________________________ TestBiasCorrect.test_bias_correction ________________________________________________________
  Traceback (most recent call last):
    File "/zstore/repos/raven/tests/test_bias_correction.py", line 20, in test_bias_correction
      ds = (xr.open_dataset(hist_data).sel(lat=slice(lat + 1, lat - 1),lon=slice(lon - 1, lon + 1), time=slice(dt.datetime(1991,1,1), dt.datetime(2010,12,31))).mean(dim={"lat", "lon"}, keep_attrs=True))
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/xarray/core/common.py", line 84, in wrapped_func
      func, dim, skipna=skipna, numeric_only=numeric_only, **kwargs
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/xarray/core/dataset.py", line 4313, in reduce
      **kwargs,
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/xarray/core/variable.py", line 1586, in reduce
      input_data = self.data if allow_lazy else self.values
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/xarray/core/variable.py", line 349, in data
      return self.values
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/xarray/core/variable.py", line 457, in values
      return _as_array_or_item(self._data)
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/xarray/core/variable.py", line 260, in _as_array_or_item
      data = np.asarray(data)
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/numpy/core/_asarray.py", line 83, in asarray
      return array(a, dtype, copy=False, order=order)
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/xarray/core/indexing.py", line 677, in __array__
      self._ensure_cached()
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/xarray/core/indexing.py", line 674, in _ensure_cached
      self.array = NumpyIndexingAdapter(np.asarray(self.array))
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/numpy/core/_asarray.py", line 83, in asarray
      return array(a, dtype, copy=False, order=order)
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/xarray/core/indexing.py", line 653, in __array__
      return np.asarray(self.array, dtype=dtype)
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/numpy/core/_asarray.py", line 83, in asarray
      return array(a, dtype, copy=False, order=order)
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/xarray/core/indexing.py", line 557, in __array__
      return np.asarray(array[self.key], dtype=None)
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/xarray/backends/netCDF4_.py", line 73, in __getitem__
      key, self.shape, indexing.IndexingSupport.OUTER, self._getitem
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/xarray/core/indexing.py", line 837, in explicit_indexing_adapter
      result = raw_indexing_method(raw_key.tuple)
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/xarray/backends/netCDF4_.py", line 85, in _getitem
      array = getitem(original_array, key)
    File "/home/lvu/.conda/envs/raven/lib/python3.7/site-packages/xarray/backends/common.py", line 54, in robust_getitem
      return array[key]
    File "netCDF4/_netCDF4.pyx", line 4408, in netCDF4._netCDF4.Variable.__getitem__
    File "netCDF4/_netCDF4.pyx", line 5352, in netCDF4._netCDF4.Variable._get
    File "netCDF4/_netCDF4.pyx", line 1887, in netCDF4._netCDF4._ensure_nc_success
  RuntimeError: NetCDF: DAP failure
  ```

[1.10.2](https://github.com/bird-house/birdhouse-deploy/tree/1.10.2) (2020-07-18)
------------------------------------------------------------------------------------------------------------------
- `jupyter`: new build and add nc-time-axis

  Corresponding change to deploy the new Jupyter env to PAVICS.

  Noticeable changes:
  ```diff
  <   - dask=2.17.2=py_0
  >   - dask=2.20.0=py_0

  >   - nc-time-axis=1.2.0=py_1

  <   - xarray=0.15.1=py_0
  >   - xarray=0.16.0=py_0

  <     - xclim==0.17.0
  >     - xclim==0.18.0
  ```

  See PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/47
  (commit
  https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/commit/4e03a674930f0974e13724940eee7a608c2158c0)
  for more info.

[1.10.1](https://github.com/bird-house/birdhouse-deploy/tree/1.10.1) (2020-07-11)
------------------------------------------------------------------------------------------------------------------
- Monitoring: add alert rules and alert handling (deduplicate, group, route, silence, inhibit).

  This is a follow up to the previous PR https://github.com/bird-house/birdhouse-deploy/pull/56 that added the monitoring itself.

  Added cAdvisor and Node-exporter collection of alert rules found here https://awesome-prometheus-alerts.grep.to/rules with a few fixing because of errors in the rules and tweaking to reduce false positive alarms (see list of commits).  Great collection of sample of ready-made rules to hit the ground running and learn PromML query language on the way.

  ![2020-07-08-090953_474x1490_scrot](https://user-images.githubusercontent.com/11966697/86926000-8b086c80-c0ff-11ea-92d0-6f5ccfe2b8e1.png)

  Added Alertmanager to handle the alerts (deduplicate, group, route, silence, inhibit).  Currently the only notification route configured is email but Alertmanager is able to route alerts to Slack and any generic services accepting webhooks.

  ![2020-07-08-091150_1099x669_scrot](https://user-images.githubusercontent.com/11966697/86926213-cd31ae00-c0ff-11ea-8b2a-d33803ad3d5d.png)

  ![2020-07-08-091302_1102x1122_scrot](https://user-images.githubusercontent.com/11966697/86926276-dc186080-c0ff-11ea-9377-bda03b69640e.png)

  This is an initial attempt at alerting.  There are several ways to tweak the system without changing the code:

  * To add more Prometheus alert rules, volume-mount more *.rules files to the prometheus container.
  * To disable existing Prometheus alert rules, add more Alertmanager inhibition rules using `ALERTMANAGER_EXTRA_INHIBITION` via `env.local` file.
  * Other possible Alertmanager configs via `env.local`: `ALERTMANAGER_EXTRA_GLOBAL, ALERTMANAGER_EXTRA_ROUTES, ALERTMANAGER_EXTRA_RECEIVERS`.

  What more could be done after this initial attempt:

  * Possibly add more graphs to Grafana dashboard since we have more alerts on metrics that we do not have matching Grafana graph. Graphs are useful for historical trends and correlation with other metrics, so not required if we do not need trends and correlation.

  * Only basic metrics are being collected currently.  We could collect more useful metrics like SMART status and alert when a disk is failing.

  * The autodeploy mechanism can hook into this monitoring system to report pass/fail status and execution duration, with alerting for problems.  Then we can also correlate any CPU, memory, disk I/O spike, when the autodeploy runs and have a trace of previous autodeploy executions.

  I had to test these alerts directly in prod to tweak for less false positive alert and to debug not working rules to ensure they work on prod so these changes are already in prod !   This also test the SMTP server on the network.

  See rules on Prometheus side: http://pavics.ouranos.ca:9090/rules, http://medus.ouranos.ca:9090/rules

  Manage alerts on Alertmanager side: http://pavics.ouranos.ca:9093/#/alerts, http://medus.ouranos.ca:9093/#/alerts

  Part of issue https://github.com/bird-house/birdhouse-deploy/issues/12

[1.10.0](https://github.com/bird-house/birdhouse-deploy/tree/1.10.0) (2020-07-02)
------------------------------------------------------------------------------------------------------------------
- Monitoring for host and each docker container.

  ![Screenshot_2020-06-19 Docker and system monitoring - Grafana](https://user-images.githubusercontent.com/11966697/85206384-c7f6f580-b2ef-11ea-848d-46490eb95886.png)

  For host, using Node-exporter to collect metrics:
  * uptime
  * number of container
  * used disk space
  * used memory, available memory, used swap memory
  * load
  * cpu usage
  * in and out network traffic
  * disk I/O

  For each container, using cAdvisor to collect metrics:
  * in and out network traffic
  * cpu usage
  * memory and swap memory usage
  * disk usage

  Useful visualisation features:
  * zoom in one graph and all other graph update to match the same "time range" so we can correlate event
  * view each graph independently for more details
  * mouse over each data point will show value at that moment

  Prometheus is used as the time series DB and Grafana is used as the visualization dashboard.

  Node-exporter, cAdvisor and Prometheus are exposed so another Prometheus on the network can also scrape those same metrics and perform other analysis if required.

  The whole monitoring stack is a separate component so user is not forced to enable it if there is already another monitoring system in place.  Enabling this monitoring stack is done via `env.local` file, like all other components.

  The Grafana dashboard is taken from https://grafana.com/grafana/dashboards/893 with many fixes (see commits) since most of the metric names have changed over time.  Still it was much quicker to hit the ground running than learning the Prometheus query language and Grafana visualization options from scratch.  Not counting there are lots of metrics exposed, had to filter out which one are relevant to graph.  So starting from a broken dashboard was still a big win.  Grafana has a big collection of existing but probably un-maintained dashboards we can leverage.

  So this is a first draft for monitoring.  Many things I am not sure or will need tweaking or is missing:
  * Probably have to add more metrics or remove some that might be irrelevant, with time we will see.
  * Probably will have to tweak the scrape interval and the retention time, to keep the disk storage requirement reasonable, again we'll see with time.
  * Missing alerting.  With all the pretty graph, we are not going to look at them all day, we need some kind of alerting mechanism.

  Test system: http://lvupavicsmaster.ouranos.ca:3001/d/pf6xQMWGz/docker-and-system-monitoring?orgId=1&refresh=5m, user: admin, passwd: the default passwd

  Also tested on Medus: http://medus.ouranos.ca:3001/d/pf6xQMWGz/docker-and-system-monitoring?orgId=1&refresh=5m (on Medus had to perform full yum update to get new kernel and new docker engine for cAdvisor to work properly).

  Part of issue https://github.com/bird-house/birdhouse-deploy/issues/12

[1.9.6](https://github.com/bird-house/birdhouse-deploy/tree/1.9.6) (2020-06-15)
------------------------------------------------------------------------------------------------------------------
- flyingpigeon: update to version 1.6

  Deploy the new Flyingpigeon 1.6 on PAVICS.

  Has been deployed to Medus test environment.

  flyingpigeon changelog from release commit
  https://github.com/bird-house/flyingpigeon/commit/a6f54ed0c20919485c2420295729e30f914cfa15
  (PR https://github.com/bird-house/flyingpigeon/pull/332)

  1.6 (2020-06-10)
  ================
  * remove eggshell dependency
  * notebooks are part of the test suite
  * improved plot processes
  * remove mosaic option for subset processes
  * polygon subset processes files separately instead of an entire data-set at once
  * multiple outputs listed in Metalink output
  * update pywps to 4.2.3
  * use cruft to keep up-to-date with the cookie-cutter template

[1.9.5](https://github.com/bird-house/birdhouse-deploy/tree/1.9.5) (2020-06-12)
------------------------------------------------------------------------------------------------------------------
- `jupyter`: new image for additional plugins

  Matching PR to deploy the new Jupyter image to PAVICS.

  Added:

  * https://github.com/hadim/jupyter-archive
    Download entire folder as archive.

  * https://blog.jupyter.org/a-visual-debugger-for-jupyter-914e61716559

  * https://github.com/plotly/jupyter-dash
    Develop Plotly Dash apps interactively from within Jupyter environments.

  Noticeable changes:
  ```diff
  >   - jupyter-archive=0.6.2=py_0
  >   - jupyter-dash=0.2.1.post1=py_0

  <   - owslib=0.19.2=py_1
  >   - owslib=0.20.0=py_0

  >   - xeus-python=0.7.1=py37h99015e2_1
  ```

  See PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/46 (commit
  https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/commit/441edde3b381eff7ce82e5a171323b31196553be)
  for more info.

[1.9.4](https://github.com/bird-house/birdhouse-deploy/tree/1.9.4) (2020-06-03)
------------------------------------------------------------------------------------------------------------------
- `jupyter`: updated build and fix for pyviz jupyterlab extension

  @tlogan2000 matching PR to actually deploy the new Jupyter env to PAVICS.

  Noticeable changes:

  ```diff
  <   - dask=2.15.0=py_0
  >   - dask=2.17.2=py_0

  <     - xclim==0.16.0
  >     - xclim==0.17.0
  ```

  See PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/45 (commit
  https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/commit/a93f3b50cc6d108638d232fe9465b2f060e21314)
  for more info.

[1.9.3](https://github.com/bird-house/birdhouse-deploy/tree/1.9.3) (2020-05-07)
------------------------------------------------------------------------------------------------------------------
- `jupyter`: update to pavics/workflow-tests:200507

  Raven PR https://github.com/Ouranosinc/raven/pull/266 (commit
  https://github.com/Ouranosinc/raven/commit/0763bf52abec1bc0a70927de3a2dc2cc1cf77ec3)
  removed salem dependency and replaced with rioxarray.

  Also add packages for the
  [`custom_climate_portraits`](https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/tree/custom_climate_portraits)
  branch  (PR
  https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/35).

  Noticeable changes:
  ```diff
    # conda release of bokeh seems to trail behind pypi
  >   - bokeh=2.0.1=py37hc8dfbb8_0
  <     - bokeh==2.0.2
  >   - jupyter_bokeh=2.0.1=py_0

    # should already exist, not sure why conda env export report this as new
  >   - dask=2.15.0=py_0

    # unpinned since salem is removed
  <   - pandas=0.25.3=py37hb3f55d8_0
  >   - pandas=1.0.3=py37h0da4684_1

  <     - salem==0.2.4
  >   - rioxarray=0.0.26=py_0

    # packages for custom_climate_portraits branch
  >   - geoviews=1.8.1=py_0
  >   - h5netcdf=0.8.0=py_0
  >   - holoviews=1.13.2=pyh9f0ad1d_0
  >   - panel=0.9.5=py_1
  >   - hvplot=0.5.2=py_0
  >   - pscript=0.7.3=py_0
  >   - siphon=0.8.0=py37_1002
  >     - ipython-blocking==0.2.1
  ```

  See PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/44
  (commit
  https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/commit/bb81982e3fd92bff437eddc5d4ae28202b3ef07c)
  for more info.

[1.9.2](https://github.com/bird-house/birdhouse-deploy/tree/1.9.2) (2020-04-29)
------------------------------------------------------------------------------------------------------------------
-
  jupyter: update to pavics/workflow-tests:200427 image

  See PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/43 (commit https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/commit/446b2f1ba3342106e3ad3d2dfe16aece7365c492) for more info.

  Noticeable changes:
  ```diff
  <   - geopandas=0.6.2=py_0
  >     - geopandas==0.7.0

  <   - xarray=0.15.0=py_0
  >   - xarray=0.15.1=py_0

  <   - owslib=0.19.1=py_0
  >   - owslib=0.19.2=py_1

  <   - dask-core=2.12.0=py_0
  >   - dask-core=2.15.0=py_0

  <     - distributed==2.12.0
  >     - distributed==2.15.0

  <     - xclim==0.14.0
  >     - xclim==0.16.0
  ```

[1.9.1](https://github.com/bird-house/birdhouse-deploy/tree/1.9.1) (2020-04-24)
------------------------------------------------------------------------------------------------------------------
-
  Fix notebook autodeploy wipe already deployed notebook when GitHub down.

  Fixes https://github.com/bird-house/birdhouse-deploy/issues/43

  Fail early with any unexpected error to not wipe already deployed notebooks.

  Check source dir not empty before wiping dest dir containing already deployed notebooks.

  Reduce cleaning verbosity for more concise logging.

  To fix this error found in production logs when Github is down today:
  ```
  notebookdeploy START_TIME=2020-04-23T10:01:01-0400
  ++ mktemp -d -t notebookdeploy.XXXXXXXXXXXX
  + TMPDIR=/tmp/notebookdeploy.ICk70Vto2LaE
  + cd /tmp/notebookdeploy.ICk70Vto2LaE
  + mkdir tutorial-notebooks
  + cd tutorial-notebooks
  + wget --quiet https://raw.githubusercontent.com/Ouranosinc/PAVICS-e2e-workflow-tests/master/downloadrepos
  + chmod a+x downloadrepos
  chmod: cannot access ‘downloadrepos’: No such file or directory
  + wget --quiet https://raw.githubusercontent.com/Ouranosinc/PAVICS-e2e-workflow-tests/master/default_build_params
  + wget --quiet https://raw.githubusercontent.com/Ouranosinc/PAVICS-e2e-workflow-tests/master/binder/reorg-notebooks
  + chmod a+x reorg-notebooks
  chmod: cannot access ‘reorg-notebooks’: No such file or directory
  + wget --quiet --output-document - https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/archive/master.tar.gz
  + tar xz

  gzip: stdin: unexpected end of file
  tar: Child returned status 1
  tar: Error is not recoverable: exiting now
  + ./downloadrepos
  /etc/cron.hourly/PAVICS-deploy-notebooks: line 63: ./downloadrepos: No such file or directory
  + ./reorg-notebooks
  /etc/cron.hourly/PAVICS-deploy-notebooks: line 64: ./reorg-notebooks: No such file or directory
  + mv -v 'PAVICS-e2e-workflow-tests-master/notebooks/*.ipynb' ./
  mv: cannot stat ‘PAVICS-e2e-workflow-tests-master/notebooks/*.ipynb’: No such file or directory
  + rm -rfv PAVICS-e2e-workflow-tests-master
  + rm -rfv downloadrepos default_build_params reorg-notebooks
  + TMP_SCRIPT=/tmp/notebookdeploy.ICk70Vto2LaE/deploy-notebook
  + cat
  + chmod a+x /tmp/notebookdeploy.ICk70Vto2LaE/deploy-notebook
  + docker pull bash
  Using default tag: latest
  latest: Pulling from library/bash
  Digest: sha256:febb3d74f41f2405fe21b7c7b47ca1aee0eda0a3ffb5483ebe3423639d30d631
  Status: Image is up to date for bash:latest
  + docker run --rm --name deploy_tutorial_notebooks -u root -v /tmp/notebookdeploy.ICk70Vto2LaE/deploy-notebook:/deploy-notebook:ro -v /tmp/notebookdeploy.ICk70Vto2LaE/tutorial-notebooks:/tutorial-notebooks:ro -v /data/jupyterhub_user_data:/notebook_dir:rw --entrypoint /deploy-notebook bash
  + cd /notebook_dir
  + rm -rf tutorial-notebooks/WCS_example.ipynb tutorial-notebooks/WFS_example.ipynb tutorial-notebooks/WMS_example.ipynb tutorial-notebooks/WPS_example.ipynb tutorial-notebooks/catalog_search.ipynb tutorial-notebooks/dap_subset.ipynb tutorial-notebooks/esgf-compute-api-examples-devel tutorial-notebooks/esgf-dap.ipynb tutorial-notebooks/finch-usage.ipynb tutorial-notebooks/hummingbird.ipynb tutorial-notebooks/opendap.ipynb tutorial-notebooks/pavics_thredds.ipynb tutorial-notebooks/raven-master tutorial-notebooks/rendering.ipynb tutorial-notebooks/subsetting.ipynb
  + cp -rv '/tutorial-notebooks/*' tutorial-notebooks
  cp: can't stat '/tutorial-notebooks/*': No such file or directory
  + chown -R root:root tutorial-notebooks
  + set +x
  removed directory: ‘/tmp/notebookdeploy.ICk70Vto2LaE/tutorial-notebooks’
  removed ‘/tmp/notebookdeploy.ICk70Vto2LaE/deploy-notebook’
  removed directory: ‘/tmp/notebookdeploy.ICk70Vto2LaE’

  notebookdeploy finished START_TIME=2020-04-23T10:01:01-0400
  notebookdeploy finished   END_TIME=2020-04-23T10:02:12-0400
  ```

[1.9.0](https://github.com/bird-house/birdhouse-deploy/tree/1.9.0) (2020-04-24)
------------------------------------------------------------------------------------------------------------------
-
  vagrant: add centos7 and LetsEncrypt SSL cert support, fix scheduler autodeploy remaining issues

  Fixes https://github.com/bird-house/birdhouse-deploy/issues/27.

  Centos7 support added to Vagrant to reproduce problems found on Medus in PR https://github.com/bird-house/birdhouse-deploy/pull/39 (commit https://github.com/bird-house/birdhouse-deploy/commit/6036dbd5ff072544d902e7b84b5eff361b00f78b):

  Problem 1: wget httpS url not working in bash docker image breaking the notebook autodeploy when running under the new scheduler autodeploy: **not reproducible**

  Problem 2: all containers are destroyed and recreated when alternating between manually running `./pavics-compose.sh up -d` locally and when the same command is executed automatically by the scheduler autodeploy inside its own container: **not reproducible**

  Problem 3: `sysctl: error: 'net.ipv4.tcp_tw_reuse' is an unknown key` on `./pavics-compose.sh up -d` when executed automatically by the scheduler autodeploy inside its own container: **reproduced** but seems **harmless** so **not fixing** it.

  Problem 4: current user lose write permission to birdhouse-deploy checkout and other checkout in `AUTODEPLOY_EXTRA_REPOS` when using scheduler autodeploy: **fixed**

  Problem 5: no documentation for the new scheduler autodeploy: **fixed**

  Another autodeploy fix found while working on this PR: notebook autodeploy broken when `/data/jupyterhub_user_data/tutorial-notebooks` dir do not pre-exist.  Regression from this commit https://github.com/bird-house/birdhouse-deploy/pull/16/commits/6ddaddc74d384299e45b0dc8d50a63e59b3cc0d5 (PR https://github.com/bird-house/birdhouse-deploy/pull/16): before that commit the entire dir was copied, not just the content, so the dir was created automatically.

  Centos7 Vagrant box experience is not completely automated as Ubuntu box, even when using the same vagrant-disksize Vagrant plugin as Ubuntu box.  Manual disk resize instruction is provided.  Candidate for automation later if we destroy and recreate Centos7 box very often.  Hopefully the problem is not there for Centos8 so we can forget about this annoyance.

  Automatic generation of SSL certificate from LetsEncrypt is also added for both Ubuntu and Centos Vagrant box.  Can be used outside of Vagrant so Medus and Boreas can also benefit next time, if needed.  Later docker image of `certbot` is used so should already be using ACMEv2 protocol (ACMEv1 is being deprecated).

  Pagekite is also preserved for both boxes for when exposing port 80 and 443 directly on the internet is not possible but PAVICS still need a real SSL certificate.

  Test server: https://lvupavicsmaster.ouranos.ca (Centos7, on internet with LetsEncrypt SSL cert).

  Jenkins run only have known errors: http://jenkins.ouranos.ca/job/ouranos-staging/job/lvupavicsmaster.ouranos.ca/4/console

  ![2020-04-22-070604_1299x1131_scrot](https://user-images.githubusercontent.com/11966697/79974607-a2707b80-8467-11ea-85b6-3b03f198ce9b.png)

[1.8.10](https://github.com/bird-house/birdhouse-deploy/tree/1.8.10) (2020-04-09)
------------------------------------------------------------------------------------------------------------------
- Autodeploy the autodeploy phase 2: everything operational but a few compatibility issues remain

  Part of https://github.com/bird-house/birdhouse-deploy/issues/27

  Activating the `./components/scheduler` will do everything.  All configurations are centralized in the `env.local` file.

  One missing feature is piece-wise choice of platform or notebook autodeploy only, like with the old manual `install-*` stcripts under https://github.com/bird-house/birdhouse-deploy/tree/master/birdhouse/deployment.  Right now it's all or nothing.  I can work on this if you guys think it's needed.

  Remaining compatibility issues with Medus (Vagrant box works fine):

  * Notebook autodeploy do not work. It looks like using the `bash` docker image, I am unable to wget any httpS address.  This same `docker run` command works fine on my Vagrant box as well.  So there's something on Medus.

  ```
  $ docker run --rm --name debug_wget_httpS -u root bash bash -c "wget https://google.com -O -"
  Connecting to google.com (172.217.13.206:443)
  wget: error getting response: Connection reset by peer
  ```

  * All the containers are being recreated when `./pavics-compose.sh` runs inside the container (first migration to the new autodeploy mechanism).  To investigate but I suspect this might be due to older version of `docker` and `docker-compose` on Medus.

  * This one looks like due to older kernel on Medus:
  ```
  sysctl: error: 'net.ipv4.tcp_tw_reuse' is an unknown key
  sh: 0: unknown operand
  ```

  * All the files updated by `git pull` are now owned by `root` (the user inside the container).  I'll have to undo this ownership change, somehow.  This one is super weird, I should have got it on my Vagrant box.  Probably Vagrant did some magic to always ensure files under `/vagrant` is always owned by the user even if changed by user `root`.

  * Documentation: update README and list relevant configuration variables in `env.local` for this new `./component/scheduler`.


  Migrating to this new mechanism requires manual deletion of all the artifacts created by the old install scripts: `sudo rm /etc/cron.d/PAVICS-deploy /etc/cron.hourly/PAVICS-deploy-notebooks /etc/logrotate.d/PAVICS-deploy /usr/local/sbin/triggerdeploy.sh`.  Both can not co-exist at the same time.

  Maximum backward-compatibility has been kept with the old existing install scripts style:
  * Still log to the same existing log files under `/var/log/PAVICS`.
  * Old single ssh deploy key is still compatible, but the new mechanism allows for different ssh deploy keys for each extra repos (again, public repos should use https clone path to avoid dealing with ssh deploy keys in the first place)
  * Old install scripts are kept

  Features missing in old existing install scripts or how this improves on the old install scripts:
  * Autodeploy of the autodeploy itself !  This is the biggest win.  Previously, if `triggerdeploy.sh` or `PAVICS-deploy-notebooks` script changes, they have to be deployed manually.  It's very annoying.  Now they are volume-mount in so are fresh on each run.
  * `env.local` now drive absolutely everything, source control that file and we've got a true DevOPS pipeline.
  * Configurable platform and notebook autodeploy frequency.  Previously, this means manually editing the generated cron file, less ideal.
  * Do not need any support on the local host other than `docker` and `docker-compose`.  cron/logrotate/git/ssh versions are all locked-down in the docker images used by the autodeploy.  Recall previously we had to deal with git version too old on some hosts.
  * Each cron job run in its own docker image meaning the runtime environment is traceable and reproducible.
  * The newly introduced scheduler component is made extensible so other jobs can added into it as well (ex: backup), via `env.local`, which should source control, meaning all surrounding maintenance related tasks can also be traceable and reproducible.

  This is a rather large PR.  For a less technical overview, start with the diff of README.md, env.local.example, common.env.  If a change looks funny to you, read the commit description that introduce that change, the reasoning should be there.

[1.8.9](https://github.com/bird-house/birdhouse-deploy/tree/1.8.9) (2020-04-08)
------------------------------------------------------------------------------------------------------------------
- finch: update to 0.5.2

  Fix following 2 Jenkins failures:

  Tested in this Jenkins run http://jenkins.ouranos.ca/job/ouranos-staging/job/lvupavics-lvu.pagekite.me/20/console

  ```
    _________ finch-master/docs/source/notebooks/dap_subset.ipynb::Cell 9 __________
    Notebook cell execution failed
    Cell 9: Cell outputs differ

    Input:
    resp = wps.sdii(pr + sub)
    out = resp.get(asobj=True)
    out.output_netcdf.sdii

    Traceback:
     mismatch 'text/html'

     assert reference_output == test_output failed:

      '<pre>&lt;xar...vera...</pre>' == '<pre>&lt;xar...vera...</pre>'
      Skipping 350 identical leading characters in diff, use -v to show
        m/day
      -     cell_methods:   time: mean (interval: 30 minutes)
            history:        pr=max(0,pr) applied to raw data;\n[DATE_TIME] ...
      +     cell_methods:   time: mean (interval: 30 minutes)
            standard_name:  lwe_thickness_of_precipitation_amount
            long_name:      Average precipitation during wet days (sdii)
            description:    Annual simple daily intensity index (sdii) : annual avera...</pre>
  ```

  ```
    _________ finch-master/docs/source/notebooks/finch-usage.ipynb::Cell 1 _________
    Notebook cell execution failed
    Cell 1: Cell outputs differ

    Input:
    help(wps.frost_days)

    Traceback:
     mismatch 'stdout'

     assert reference_output == test_output failed:

      'Help on meth...ut files.\n\n' == 'Help on meth...ut files.\n\n'
      Skipping 399 identical leading characters in diff, use -v to show
      -    freq : string
      +    freq : {'YS', 'MS', 'QS-DEC', 'AS-JUL'}string
                Resampling frequency

            Returns
            -------
            output_netcdf : ComplexData:mimetype:`application/x-netcdf`
                The indicator values computed on the original input grid.
            output_log : ComplexData:mimetype:`text/plain`
                Collected logs during process run.
            ref : ComplexData:mimetype:`application/metalink+xml; version=4.0`
                Metalink file storing all references to output files.
  ```

[1.8.8](https://github.com/bird-house/birdhouse-deploy/tree/1.8.8) (2020-03-20)
------------------------------------------------------------------------------------------------------------------
- `jupyter`: make configurable public demo user name, passwd, resource limit, login banner

  For security reasons, the public demo username and password are not hardcoded anymore.

  Compromising of one PAVICS deployment should not compromise all other PAVICS deployments if each deployment use a different password.

  The password is set when the public demo user is created in Magpie, see the `birdhouse/README.md` update.

  The login banner do not display the public demo password anymore.  If one really want to display the password, can use the top or bottom section of the login banner that is customizable via `env.local`.

  Login banner is updated with more notices, please review wording.

  Resource limits (only memory limit seems to work with the `DockerSpawner`) is also customizable.

  All changes to `env.local` are live after a `./pavics-compose.sh up -d`.

  Test server: https://lvupavics-lvu.pagekite.me/jupyter/ (ask me privately for the password :D)

[1.8.7](https://github.com/bird-house/birdhouse-deploy/tree/1.8.7) (2020-03-19)
------------------------------------------------------------------------------------------------------------------
- finch: update to v0.5.1

[1.8.6](https://github.com/bird-house/birdhouse-deploy/tree/1.8.6) (2020-03-16)
------------------------------------------------------------------------------------------------------------------
- Thredds: New "Datasets" top level for NCML files

  http://lvupavics-lvu.pagekite.me/twitcher/ows/proxy/thredds/catalog/datasets/catalog.html (only gridded_obs/nrcan.ncml works on my dev server).

  Add a new top-level "Datasets" at the same level as the existing "Birdhouse".

  The content of the new top-level comes from `/data/ncml` from the host.  For comparison content of existing "Birdhouse" was coming from `/data/datasets`.

[1.8.5](https://github.com/bird-house/birdhouse-deploy/tree/1.8.5) (2020-03-13)
------------------------------------------------------------------------------------------------------------------
- `jupyter`: update to pavics/workflow-tests:200312 for Raven notebooks

[1.8.4](https://github.com/bird-house/birdhouse-deploy/tree/1.8.4) (2020-03-10)
------------------------------------------------------------------------------------------------------------------
- raven: upgrade to pavics/raven:0.10.0

[1.8.3](https://github.com/bird-house/birdhouse-deploy/tree/1.8.3) (2020-02-17)
------------------------------------------------------------------------------------------------------------------
- catalog: fix pavicsearch broken due to typo in config

  The `thredds_host` should be the exact prefix of each document url found
  in Solr, otherwise it is removed from the search result.

  This explains why pavicsearch was returning nothing.

  This will fix the `catalog_search.ipynb` notebook that keeps failing on Jenkins.

  The typo was introduced in PR
  https://github.com/bird-house/birdhouse-deploy/pull/5, commit
  https://github.com/bird-house/birdhouse-deploy/commit/83c839178fff170dbcb4c4e0586e67d19b9cfbc5

[1.8.2](https://github.com/bird-house/birdhouse-deploy/tree/1.8.2) (2020-02-10)
------------------------------------------------------------------------------------------------------------------
- Optionally monitor all components behind Twitcher using canarie api.

  Fixes https://github.com/bird-house/birdhouse-deploy/issues/8

  The motivation was the need for some quick dashboard for the working state of all the components, not to get more stats.

  Right now we bypassing Twitcher, which is not real life, it's not what real users will experience.

  This is ultra cheap to add and provide very fast and up-to-date (every minute) result. It's like an always on sanity check that can quickly help debugging any connectivity issues between the components.

  It is optional because it assumes all components are publicly accessible.  Might not be the case for everyone.  We can also override the override :D

  All components in config/canarie-api/docker_configuration.py.template that do not have public (behind Twitcher) monitoring are added.

  Also added Hummingbird and ncWMS2 public monitoring.

  @tlogan2000 This will catch accidental Thredds public url breakage like last time and will leverage the existing monitoring on https://pavics.ouranos.ca/canarie/node/service/stats by @moulab88.

  @davidcaron @dbyrns This is optional so if the CRIM do not want to enable it, it's fine.

  New node monitoring page:

  ![Screenshot_2020-02-07 Ouranos - Node Service](https://user-images.githubusercontent.com/11966697/74055606-4a6cc180-49ae-11ea-9cba-887118dbaae6.png)

[1.8.1](https://github.com/bird-house/birdhouse-deploy/tree/1.8.1) (2020-02-06)
------------------------------------------------------------------------------------------------------------------
- Increase JupyterHub security.

  ab56994 jupyter: limit memory of public user to 500 MB
  90c1950 jupyter: prevent user from loading user-owned config at spawner server startup
  e8f2fa3 jupyter: avoid terminating user running jobs on Hub update
  3f97cc7 jupyter: get ready to prevent browser session re-use even if password changed
  e2ebcc3 jupyter: disable notebook terminal for security reasons

[1.8.0](https://github.com/bird-house/birdhouse-deploy/tree/1.8.0) (2020-02-03)
------------------------------------------------------------------------------------------------------------------
- jupyter data migration: touch new location else jupyterhub won't bind mount them

  See PR https://github.com/bird-house/birdhouse-deploy/pull/16
  or commit
  https://github.com/bird-house/birdhouse-deploy/commit/53576cc9d36642c50e4a649ca58fc8339559fd4a

  See the `if os.path.exists` in the `jupyterhub_config.py`:
  https://github.com/bird-house/birdhouse-deploy/blob/53576cc9d36642c50e4a649ca58fc8339559fd4a/birdhouse/config/jupyterhub/jupyterhub_config.py.template#L36-L48

[1.7.1](https://github.com/bird-house/birdhouse-deploy/tree/1.7.1) (2020-01-30)
------------------------------------------------------------------------------------------------------------------
- `jupyter`: update various packages and add threddsclient

  Noticeable changes:
  ```diff
  <     - bokeh==1.4.0
  >   - bokeh=1.4.0=py36_0

  <   - python=3.7.3=h33d41f4_1
  >   - python=3.6.7=h357f687_1006

  >   - threddsclient=0.4.2=py_0

  <     - xarray==0.13.0
  >   - xarray=0.14.1=py_1

  <     - dask==2.8.0
  >     - dask==2.9.2

  <     - xclim==0.12.2
  >     - xclim==0.13.0
  ```

  See PR https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/34 for more info.

[1.7.0](https://github.com/bird-house/birdhouse-deploy/tree/1.7.0) (2020-01-22)
------------------------------------------------------------------------------------------------------------------
- backup solr: should save all of /data/solr, not just the index


Prior Versions
------------------------------------------------------------------------------------------------------------------

All versions prior to [1.7.0](https://github.com/bird-house/birdhouse-deploy/tree/1.7.0) were not officially tagged.
Is it strongly recommended employing later versions to ensure better traceability of changes that could impact behavior
and potential issues on new server instances. 
