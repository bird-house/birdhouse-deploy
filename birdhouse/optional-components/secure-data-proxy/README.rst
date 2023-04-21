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

* Add ``./optional-components/secure-data-proxy`` to ``EXTRA_CONF_DIRS``.

Once enabled, users will *NOT* have public access to files under ``/wpsoutputs`` anymore, except for items defined
with authorized ``read`` permissions for the ``anonymous`` group under |secure-data-proxy-perms|_. As any other Magpie
configuration file, any combination of user/group/resource/permission could be defined for the ``secure-data-proxy``
service to customize specific user access control to stored data files.

.. _secure-data-proxy-perms: ./secure-data-proxy/config/magpie/config.yml.template
.. |secure-data-proxy-perms| replace:: optional-components/secure-data-proxy/config/magpie/config.yml.template
