Weaver
======

By enabling this component, the `Weaver`_ service will be integrated into the stack.

This component offers `OGC API - Processes`_ interface to WPS components (a.k.a `WPS-REST bindings` and
`WPS-T (Transactional)` support).
This provides a RESTful JSON interface with asynchronous WPS processes execution over remote instances.
Other WPS components of the birdhouse stack (`finch`_, `flyingpigeon`_, etc.) will also all be registered
under `Weaver`_ in order to provide a common endpoint to retrieve all available processes, and dispatch
their execution to the corresponding service.
Finally, `Weaver`_ also adds `Docker` image execution capabilities as a WPS process, allowing deployment
and execution of custom applications and workflows.

.. image:: weaver/images/component-diagram.png

Usage
-----

Once this component is enabled, `Weaver`_ will be accessible at ``https://<BIRDHOUSE_FQDN_PUBLIC>/weaver`` endpoint,
where ``BIRDHOUSE_FQDN_PUBLIC`` is defined in your ``env.local`` file.

Full process listing (across WPS providers) should be available using request:

.. code-block::

    GET https://<BIRDHOUSE_FQDN_PUBLIC>/weaver/processes?providers=true

Please refer to the `Weaver OpenAPI`_ for complete description of available requests.
This description will also be accessible via ``https://<BIRDHOUSE_FQDN_PUBLIC>/weaver/api`` once the instance is started.

For any specific details about `Weaver`_ configuration parameters, functionalities or questions, please refer to its
`documentation <https://pavics-weaver.readthedocs.io/en/latest/>`_.

How to Enable the Component
---------------------------

- Edit ``env.local`` (a copy of `env.local.example`_)

  - Add ``"./services/weaver"`` to ``EXTRA_CONF_DIRS``.


Customizing the Component
-------------------------

- Edit ``env.local`` (a copy of `env.local.example`_)

  - Optionally, set any additional environment variable overrides amongst values defined in `weaver/default.env`_.

  - Optionally, mount any additional `Weaver`_-specific configuration files
    (see contents of ``birdhouse/components/weaver/config/weaver``) if extended functionalities need to be defined.
    Further ``docker-compose-extra.yml`` could be needed to define
    any other ``volumes`` entries where these component would need to be mounted to.



.. _finch: https://github.com/bird-house/finch
.. _flyingpigeon: https://github.com/bird-house/flyingpigeon
.. _Weaver: https://github.com/crim-ca/weaver
.. _Weaver OpenAPI: https://pavics-weaver.readthedocs.io/en/latest/api.html
.. _weaver/default.env: ./weaver/default.env
.. _OGC API - Processes: https://github.com/opengeospatial/ogcapi-processes
.. _env.local.example: ../env.local.example
.. _fix-write-perm: ../deployment/fix-write-perm
.. _deploy.sh: ../deployment/deploy.sh
.. _triggerdeploy.sh: ../deployment/triggerdeploy.sh
.. _monitoring_default.env: monitoring/default.env
