Control secured access to resources example
--------------------------------------------------------

Optional configuration |magpie-secure-perms|_ is provided as example to illustrate how to apply permissions on specific
THREDDS resources to limit their access publicly. This permission configuration can be combined with others, such as
`magpie-public-access-config`_ ones to formulate specific permissions schemes that matches your data structure and
desired access rules.

How to enable in ``env.local`` (a copy from `env.local.example`_ (:download:`download </birdhouse/env.local.example>`)):

* Add ``./extensions/secure-thredds`` to ``EXTRA_CONF_DIRS``.

The anonymous user will *NOT* have access anymore to THREDDS test directory ``birdhouse/testdata/secure`` and any other
directories and files under it. Directories above and next to ``secure`` will still be accessible if
`magpie-public-access-config`_ component was also enabled.

On a typical server, custom and private permission rules should be provided in a similar fashion to ensure that
each time a new instance is booted, the same scheme of access configuration is applied. Permissions applied manually
into Magpie will not be replicated onto other server instance.

.. _magpie-secure-perms: ./secure-thredds/secure-access-magpie-permission.cfg
.. |magpie-secure-perms| replace:: optional-components/secure-thredds/secure-access-magpie-permission.cfg
