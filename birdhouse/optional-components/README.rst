Optional components
===================


.. contents::


Monitor all components in CANARIE node, both public and internal url
--------------------------------------------------------------------

So that the url ``https://<BIRDHOUSE_FQDN>/canarie/node/service/stats`` also return
what the end user really see (a component might work but is not accessible to
the end user).

This assume all the WPS services are public.  If not the case, make a copy of
this config and adjust accordingly.

How to enable this config in ``env.local`` (a copy from env.local.example_
(:download:`download </birdhouse/env.local.example>`)):

* Add ``./optional-components/canarie-api-full-monitoring`` to ``BIRDHOUSE_EXTRA_CONF_DIRS``.


Emu WPS service for testing
---------------------------

Preconfigured for Emu but can also be used to quickly deploy any birds
temporarily without changing code.  Good to preview new birds or test
alternative configuration of existing birds.

No Postgres DB configured.  If need Postgres DB, use generic_bird component
instead.

How to enable Emu in ``env.local`` (a copy from env.local.example_
(:download:`download </birdhouse/env.local.example>`)):

* Add ``./optional-components/emu`` to ``BIRDHOUSE_EXTRA_CONF_DIRS``.
* Optionally set ``EMU_IMAGE``,
  ``EMU_NAME``, ``EMU_INTERNAL_PORT``,
  ``EMU_WPS_OUTPUTS_VOL`` in ``env.local`` for further customizations.
  Default values are in `optional-components/emu/default.env <emu/default.env>`_
  (:download:`download </birdhouse/optional-components/emu/default.env>`).

Emu service will be available at ``http://BIRDHOUSE_FQDN:EMU_PORT/wps`` or
``https://BIRDHOUSE_FQDN_PUBLIC/TWITCHER_PROTECTED_PATH/EMU_NAME`` where
``BIRDHOUSE_FQDN``\ , ``BIRDHOUSE_FQDN_PUBLIC`` and ``TWITCHER_PROTECTED_PATH`` are defined
in your ``env.local``.

Magpie will be automatically configured to give complete public anonymous
access for this Emu WPS service.

CANARIE monitoring will also be automatically configured for this Emu WPS
service.


A second THREDDS server for testing
-----------------------------------

How to enable in ``env.local`` (a copy from env.local.example_ (:download:`download </birdhouse/env.local.example>`)):

* Add ``./optional-components/testthredds`` to ``BIRDHOUSE_EXTRA_CONF_DIRS``.

* Optionally set ``TESTTHREDDS_IMAGE``\ , ``TESTTHREDDS_PORT``\ ,
  ``TESTTHREDDS_CONTEXT_ROOT``\ , ``TESTTHREDDS_WARFILE_NAME``\ ,
  ``TESTTHREDDS_INTERNAL_PORT``\ , ``TESTTHREDDS_NAME``\ ,  in ``env.local`` for further
  customizations.  Default values are in: `optional-components/testthredds/default.env <testthredds/default.env>`_ (:download:`download </birdhouse/optional-components/testthredds/default.env>`).

Test THREDDS service will be available at
``http://BIRDHOUSE_FQDN:TESTTHREDDS_PORT/TESTTHREDDS_CONTEXT_ROOT`` or
``https://BIRDHOUSE_FQDN_PUBLIC/TESTTHREDDS_CONTEXT_ROOT`` where ``BIRDHOUSE_FQDN`` and
``BIRDHOUSE_FQDN_PUBLIC`` are defined in your ``env.local``.

Use same docker image as regular THREDDS by default but can be customized.

New container have new ``TestDatasets`` with volume-mount to ``/data/testdatasets``
on the host.  So your testing ``.nc`` and ``.ncml`` files should be added to
``/data/testdatasets`` on the host for them to show up on this Test THREDDs
server.

``TestWps_Output`` dataset is for other WPS services to write to, similar to
``birdhouse/wps_outputs`` dataset in the production THREDDs.  With Emu, add
``export EMU_WPS_OUTPUTS_VOL=testwps_outputs`` to ``env.local`` for Emu to write to
``TestWps_Output`` dataset.

No Twitcher/Magpie access control, this Test THREDDS is directly behind the
Nginx proxy.

CANARIE monitoring will also be automatically configured for this second
THREDDS server.


A generic bird WPS service
--------------------------

Can be used to quickly deploy any birds temporarily without changing code.
Good to preview new birds or test alternative configuration of existing birds.

How to enable in ``env.local`` (a copy from env.local.example_ (:download:`download </birdhouse/env.local.example>`)):

* Add ``./optional-components/generic_bird`` to ``BIRDHOUSE_EXTRA_CONF_DIRS``.

* Optionally set ``GENERIC_BIRD_IMAGE``, ``GENERIC_BIRD_PORT``,
  ``GENERIC_BIRD_NAME``, ``GENERIC_BIRD_INTERNAL_PORT``, and
  ``GENERIC_BIRD_POSTGRES_IMAGE`` in ``env.local`` for further customizations.
  Default values are in `optional-components/generic_bird/default.env <generic_bird/default.env>`_
  (:download:`download </birdhouse/optional-components/generic_bird/default.env>`).

The WPS service will be available at ``http://BIRDHOUSE_FQDN:GENERIC_BIRD_PORT/wps``
or ``https://BIRDHOUSE_FQDN_PUBLIC/TWITCHER_PROTECTED_PATH/GENERIC_BIRD_NAME`` where
``BIRDHOUSE_FQDN``\ , ``BIRDHOUSE_FQDN_PUBLIC`` and ``TWITCHER_PROTECTED_PATH`` are defined
in your ``env.local``.

Use same docker image as regular Finch by default but can be customized.

Use a separate Postgres DB for this optional component to be completely
self-contained and to allow experimenting with different versions of Postgres
DB. This Postgres DB will be named ``generic_bird`` by default but can be customized by
setting the ``BIRDHOUSE_GENERIC_BIRD_POSTGRES_DB`` environment variable in ``env.local``
in case that name clashes with the ``BIRDHOUSE_POSTGRES_DB`` variable.

Magpie will be automatically configured to give complete public anonymous
access for this WPS service.

CANARIE monitoring will also be automatically configured for this WPS service.


Enable health checks for WPS services
--------------------------------------------------------

At any given time, WPS services could stop responding. Using the ``healthcheck`` feature from ``docker-compose``, it is
possible to monitor the services at regular intervals to ensure they remain accessible. Using this, it is possible to
rapidly identify if a service might be misbehaving.

Since the various WPS services are executed using a different applications and dependencies in their respective
Docker images, the method required to validate their status can vary a lot for each case. This optional component
defines all the appropriate ``healthcheck`` for all known WPS services in Birdhouse.

How to enable in ``env.local`` (a copy from env.local.example_ (:download:`download </birdhouse/env.local.example>`)):

* Add ``./optional-components/wps-healthchecks`` to ``BIRDHOUSE_EXTRA_CONF_DIRS``.

Once enabled, every WPS service will be monitored at regular intervals and ``docker-compose`` will indicate in their
health status. Command ``birdhouse-compose ps`` can be employed to list running images, and along with it, the statuses
reported by each ``healthcheck``.


.. _magpie-public-access-config:

Give public access to all resources for testing purposes
--------------------------------------------------------

By enabling this component, all WPS services and data on THREDDS are completely public, please beware.
Once enabled, if you need to revert the change, you have to do it manually by logging into Magpie.
Just disabling this component will not revert the change.
Alternatively, you can create a similar file to |magpie-public-perms|_ and replace all desired ``action: create``
entries by ``action: remove`` to make sure the permissions are removed at startup if they exist.

This optional component is required for the test suite at
https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests.

How to enable in ``env.local`` (a copy from `env.local.example`_ (:download:`download </birdhouse/env.local.example>`)):

* Add ``./optional-components/all-public-access`` to ``BIRDHOUSE_EXTRA_CONF_DIRS``.

The anonymous user will now have all the permissions described in |magpie-public-perms|_
(:download:`download </birdhouse/optional-components/all-public-access/all-public-access-magpie-permission.cfg>`).

.. note::
    If using the ``./components/stac`` feature, the corresponding ``./optional-components/stac-public-access``
    must be applied as well to obtain similar functionalities to ``./optional-components/all-public-access``.
    This optional component is kept separate since ``./components/stac`` is not required by default, and therefore
    cannot be enforced as a component dependency.

.. _magpie-public-perms: ./all-public-access/all-public-access-magpie-permission.cfg
.. |magpie-public-perms| replace:: optional-components/all-public-access/all-public-access-magpie-permission.cfg
.. _env.local.example: ../env.local.example


Control secured access to WPS outputs
--------------------------------------------------------

By default, all outputs of WPS processes (i.e.: ``/wpsoutputs``) are publicly accessible. This is to preserve
backward compatibility with previous instances. However, enabling this optional component adds secured access to data
stored under ``/wpsoutputs``.

To provide secured access, all requests sent to ``/wpsoutputs`` require a prior authorization from a new service added
to Magpie, called ``secure-data-proxy``. As shown below, this service should replicate the file system directory
hierarchy defined to store the data. A file located under ``/wpsoutputs/weaver/public`` for example would use the
corresponding resources and user/group permissions defined under this service to validate that the authenticated
request user can obtain access to it.

.. image:: secure-data-proxy/images/magpie-service.png

How to enable in ``env.local`` (a copy from `env.local.example`_ (:download:`download </birdhouse/env.local.example>`)):

* Add ``./optional-components/secure-data-proxy`` to ``BIRDHOUSE_EXTRA_CONF_DIRS``.

Once enabled, users will *NOT* have public access to files under ``/wpsoutputs`` anymore, except for items defined
with authorized ``read`` permissions for the ``anonymous`` group under |secure-data-proxy-perms|_. As any other Magpie
configuration file, any combination of user/group/resource/permission could be defined for the ``secure-data-proxy``
service to customize specific user access control to stored data files.

.. _secure-data-proxy-perms: ./secure-data-proxy/config/magpie/config.yml.template
.. |secure-data-proxy-perms| replace:: optional-components/secure-data-proxy/config/magpie/config.yml.template


Control secured access to resources example
--------------------------------------------------------

Optional configuration |magpie-secure-perms|_ is provided as example to illustrate how to apply permissions on specific
THREDDS resources to limit their access publicly. This permission configuration can be combined with others, such as
`magpie-public-access-config`_ ones to formulate specific permissions schemes that matches your data structure and
desired access rules.

How to enable in ``env.local`` (a copy from `env.local.example`_ (:download:`download </birdhouse/env.local.example>`)):

* Add ``./optional-components/secure-thredds`` to ``BIRDHOUSE_EXTRA_CONF_DIRS``.

The anonymous user will *NOT* have access anymore to THREDDS test directory ``birdhouse/testdata/secure`` and any other
directories and files under it. Directories above and next to ``secure`` will still be accessible if
`magpie-public-access-config`_ component was also enabled.

On a typical server, custom and private permission rules should be provided in a similar fashion to ensure that
each time a new instance is booted, the same scheme of access configuration is applied. Permissions applied manually
into Magpie will not be replicated onto other server instance.

.. _magpie-secure-perms: ./secure-thredds/secure-access-magpie-permission.cfg
.. |magpie-secure-perms| replace:: optional-components/secure-thredds/secure-access-magpie-permission.cfg


Control public exposure of database ports
--------------------------------------------------------

Because databases may contain sensitive of private data, they should never be directly exposed.
On the other hand, accessing them remotely can be practical for testing such as in a staging server environment.

This component is intended to automatically map the databases (``PostgreSQL``, ``MongoDB``) as such.

How to enable in ``env.local`` (a copy from env.local.example_ (:download:`download </birdhouse/env.local.example>`)):

* Add ``./optional-components/database-external-ports`` to ``BIRDHOUSE_EXTRA_CONF_DIRS``.

That's it. Databases will be accessible using the mapped ports in then optional component configuration.


Test Permissions for Weaver
--------------------------------------------------------

In order to test functionalities offered by `Weaver` component ``./components/weaver``, this optional component
adds `Magpie` permissions to a test server in order to grant access to specific endpoints.
This will open public access to specified resources in file |test-weaver-perms|_.

.. warning::
    It also disables SSL verification for the corresponding process that is granted public access to allow `Weaver` to
    requests its WPS execution through the providers reference without error. This is mainly to ignore test servers
    self-signed SSL certificates. This should be avoided on production servers by using a real and valid SSL certificate
    and leaving verification active to avoid man-in-the-middle attacks.

This optional component is intended to be employed in combination with test notebook |pavics-sdi-weaver|_.

How to enable in ``env.local`` (a copy from `env.local.example`_ (:download:`download </birdhouse/env.local.example>`)):

* Add ``./optional-components/test-weaver`` to ``BIRDHOUSE_EXTRA_CONF_DIRS``

.. note::
    Definition ``./components/weaver`` is also expected to be in ``BIRDHOUSE_EXTRA_CONF_DIRS`` for permissions to have any effect.
    Ensure that ``./optional-components/test-weaver`` is placed **AFTER** ``./components/weaver``. Otherwise, the
    ``request_options.yml`` override applied by this optional component will be discarded by the main component.

.. _test-weaver-perms: ./optional-components/test-weaver/config/magpie/test-weaver-permission.cfg
.. |test-weaver-perms| replace:: optional-components/test-weaver/config/magpie/test-weaver-permission.cfg
.. _pavics-sdi-weaver|: https://github.com/Ouranosinc/pavics-sdi/blob/master/docs/source/notebook-components/weaver_example.ipynb
.. |pavics-sdi-weaver| replace:: Ouranosinc/pavics-sdi Weaver Example


Test Geoserver Secured Access
-----------------------------

This optional component adds a new provider and location for Geoserver, ``test-geoserver-secured-access``, 
in order to test secured access to this service before it is moved behind Twitcher (undetermined date).

The old ``/geoserver`` path is still available, so current workflows are not affected.

The new ``/geoserver-secured`` path is available for testing once the optional component is activated.

To test the ``geoserver-secured`` service through Magpie, each workspace needs to be added to the new service and then 
permissions can be set on a per-workspace or even layer basis.

A ``GetFeature`` request for a layer in a public workspace (named public in this example) will succeed for any user 
using any of these two request types:

* {BASE_URL}/geoserver-secured/wfs?version=2.0.0&request=GetFeature&typeNames=public:{LAYER_NAME}
* {BASE_URL}/geoserver-secured/public/wfs?version=2.0.0&request=GetFeature&typeNames={LAYER_NAME}

Whereas access to a private workspace will require a user or group be given explicit permissions through the ``Magpie``
interface.

See |geoserver_secured_pr|_. for more details.

.. _geoserver_secured_pr: https://github.com/bird-house/birdhouse-deploy/pull/242
.. |geoserver_secured_pr| replace:: Pull Request


Test user workspace in JupyterLab when using Cowbird
----------------------------------------------------

This optional component is used to prepare the related |test_cowbird_jupyter|_ test, where a user workspace is
validated in a JupyterLab environment spawned from JupyterHub and where Cowbird is used to prepare the user workspace.

The component will start a Docker container specifically made to run a Python script, where the different test
requirements are initialized. This includes creating a test user, preparing different test files and setting permissions
correctly. This component also customizes the JupyterHub config according to the test requirements.

.. warning::
    This component should never be used in non-test environments, as it opens public access for certain endpoints,
    defines admin-tokens for a JupyterHub user for which credentials are clearly visible in the script, and enforces
    use of root access for the test preparation container. The component is for validation only. If used in a prod
    stack, it would create a security vulnerability.

.. _test_cowbird_jupyter: https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/blob/master/notebooks-auth/test_cowbird_jupyter.ipynb
.. |test_cowbird_jupyter| replace:: notebook


Populate STAC catalog with sample data
--------------------------------------------------------

STAC Populator contains the workflow logic to ingest sample STAC item into the STAC catalog.

Once enabled in the stack, this component will run automatically on stack boot time in order to populate the catalog. 
On stack initialization, STAC item generation workflows will run for ``STAC_ASSET_GENERATOR_TIMEOUT`` seconds in order 
to populate the catalog with sample data. Change this timeout as needed, as there are no impact on the stack boot, 
except time required to feed the catalog.

To enable this optional-component:

- Edit ``env.local`` (a copy of `env.local.example`_)
- Add ``./optional-components/stac-populator`` to ``BIRDHOUSE_EXTRA_CONF_DIRS``.


Allow public access to STAC catalog
--------------------------------------------------------

STAC Public Access allows STAC catalog to be accessed by anyone, without authentication.

To enable this optional-component:

- Edit ``env.local`` (a copy of `env.local.example`_)
- Add ``./optional-components/stac-public-access`` to ``BIRDHOUSE_EXTRA_CONF_DIRS``.


Provide a proxy for local STAC asset hosting
--------------------------------------------------------

STAC data proxy allows to host the URL location defined by ``BIRDHOUSE_FQDN_PUBLIC`` and ``STAC_DATA_PROXY_URL_PATH``
to provide access to files contained within ``STAC_DATA_PROXY_DIR_PATH``.

The ``STAC_DATA_PROXY_DIR_PATH`` location can be used to hold STAC Assets defined by the current server node
(in contrast to STAC definitions that would refer to remote locations), such that the node can be the original
location of new data, or to make a new local replication of remote data.

To enable this optional-component:

- Edit ``env.local`` (a copy of `env.local.example`_)
- Add ``./optional-components/stac-data-proxy`` to ``BIRDHOUSE_EXTRA_CONF_DIRS``.
- Optionally, add any other relevant components to control access as desired (see below).

When using this component, access to the endpoint defined by ``STAC_DATA_PROXY_URL_PATH``, and therefore all
corresponding files contained under mapped ``STAC_DATA_PROXY_DIR_PATH`` will depend on how this
feature is combined with ``./optional-components/stac-public-access`` and ``./optional-components/secure-data-proxy``.
Following are the possible combinations and obtained behaviors:

.. list-table::
    :header-rows: 1

    * - Enabled Components
      - Obtained Behaviors

    * - Only ``./optional-components/stac-data-proxy`` is enabled.
      - All data under ``STAC_DATA_PROXY_URL_PATH`` is publicly accessible without authorization control
        and specific resource access cannot be managed per content. However, since STAC-API itself is not made public,
        the STAC Catalog, Collections and Items cannot be accessed publicly
        (*note*: this is most probably never desired).

    * - Both ``./optional-components/stac-data-proxy`` and ``./optional-components/stac-public-access`` are enabled.
      - All data under ``STAC_DATA_PROXY_URL_PATH`` is publicly accessible without possibility to manage per-resource
        access. However, this public access is aligned with publicly accessible STAC-API endpoints and contents.

    * - Both ``./optional-components/stac-data-proxy`` and ``./optional-components/secure-data-proxy`` are enabled.
      - All data under ``STAC_DATA_PROXY_URL_PATH`` is protected (by default, admin-only), but can be granted access
        on a per-user, per-group and per-resource basis according to permissions applied by the administrator.
        Since STAC-API is not made public by default, the administrator can decide whether they grant access only to
        STAC metadata (Catalog, Collection, Items) with permission applied on the ``stac`` Magpie service, only to
        assets data with permission under the ``stac-data-proxy``, or both.

    * - All of ``./optional-components/stac-data-proxy``, ``./optional-components/stac-public-access`` and
        ``./optional-components/secure-data-proxy`` are enabled.
      - Similar to the previous case, allowing full authorization management control by the administrator, but contents
        are publicly accessible by default. To revoke access, a Magpie administrator has to apply a ``deny`` permission.

X-Robots-Tag Header
---------------------------

Applies the ``X-Robots-Tag`` header value defined by the ``X_ROBOTS_TAG_HEADER`` variable globally for the server.

If ``X_ROBOTS_TAG_HEADER`` is not overriden, it uses ``noindex, nofollow`` which will disallow most crawling and
indexing functionalities from robots. If omitting this optional component entirely, no ``X-Robots-Tag`` header
will be applied, which is equivalent to the robots default ``X-Robots-Tag: all``, setting no restrictions regarding
indexing and serving.

.. seealso::
    https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag#directives

How to enable X-Robots-Tag Header in ``env.local`` (a copy from `env.local.example`_
(:download:`download </birdhouse/env.local.example>`)):

* Add ``./optional-components/x-robots-tag-header`` to ``BIRDHOUSE_EXTRA_CONF_DIRS``.
* Optionally set ``X_ROBOTS_TAG_HEADER`` to an alternate directive as desired.
  Default values are in `optional-components/x-robots-tag-header/default.env <x-robots-tag-header/default.env>`_
  (:download:`download </birdhouse/optional-components/x-robots-tag-header/default.env>`).

.. note::
    In order to revert the ``X-Robots-Tag`` header on specific endpoints, the following Nginx configuration can be
    defined (other values than ``all`` are possible as well) under any ``location`` block of the server.

    .. code-block:: nginx

        location /<service-path>/ {
            add_header X-Robots-Tag: "all";
            # ... other nginx operations ...
        }

    Note however that most Nginx configurations are predefined for this stack. Custom definitions would need to be
    added to apply additional operations. One exception to this case is the *Homepage* location
    (i.e.: where the ``/`` location will be redirected), which can take advantage of the ``BIRDHOUSE_PROXY_ROOT_LOCATION``
    environment variable to override the endpoint as follows:

    .. code-block:: shell

        export BIRDHOUSE_PROXY_ROOT_LOCATION='
            add_header X-Robots-Tag: "all";
            alias /data/homepage/;  # or any other desired redirection (e.g.: "return 302 <URL>")
        '

    .. seealso::
        See the `env.local.example`_ file for more details about this ``BIRDHOUSE_PROXY_ROOT_LOCATION`` behaviour.

.. _prometheus-log-parser

Prometheus Log Parser
---------------------

Parses log files from other components and converts their logs to prometheus metrics that are then ingested by the
monitoring Prometheus instance (the one created by the :ref:`Monitoring` component).

For more information on how this component reads log files and converts them to prometheus components see
the log-parser_ documentation.

To configure this component:

    * set the ``PROMETHEUS_LOG_PARSER_POLL_DELAY`` variable to a number of seconds to set how often the log parser
      checks if new lines have been added to log files (default: 1)
    * set the ``PROMETHEUS_LOG_PARSER_TAIL`` variable to ``"true"`` to only parse new lines in log files. If unset,
      this will parse all existing lines in the log file as well (default: ``"true"``)

To view all metrics exported by the log parser:

    * Navigate to the ``https://<BIRDHOUSE_FQDN>/prometheus/graph`` search page
    * Put ``{job="log_parser"}`` in the search bar and click the "Execute" button

For developers, to create a new parser that can be used to track log files:

    1. create a python file that can be mounted as a volume to the ``PROMETHEUS_LOG_PARSER_PARSERS_DIR``
       directory on the ``prometheus-log-parser`` container.
    2. mount any log files that you want to parse as a volume on the ``prometheus-log-parser`` container.
    3. the python script should create at least one `prometheus metric using the prometheus_client 
       library <prometheus_python_metrics>`_ and must contain a global constant named ``LOG_PARSER_CONFIG`` 
       which is a dictionary where keys are paths to log files (mounted in the container) and values are a 
       list of "line parser" functions.
       * a "line parser" is any function that takes a string as a single argument (a single line from a
         log file). These functions are where you'd write the code that parses the line and converts it
         into a prometheus metric.
       * your line parser function should update one of the prometheus metrics you created previously. 

    For an example of a working log parser, see
    `birdhouse/optional-components/prometheus-log-parser/config/thredds/prometheus-log-exporter.py`_
    (:download:`download <birdhouse/optional-components/prometheus-log-parser/config/thredds/prometheus-log-exporter.py>`).

.. _log-parser: https://github.com/DACCS-Climate/log-parser/
.. _prometheus_python_metrics: https://prometheus.github.io/client_python/instrumenting/
