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

* Add ``./optional-components/test-weaver`` to ``EXTRA_CONF_DIRS``

.. note::
    Definition ``./components/weaver`` is also expected to be in ``EXTRA_CONF_DIRS`` for permissions to have any effect.
    Ensure that ``./optional-components/test-weaver`` is placed **AFTER** ``./components/weaver``. Otherwise, the
    ``request_options.yml`` override applied by this optional component will be discarded by the main component.

.. _test-weaver-perms: ./optional-components/test-weaver/config/magpie/test-weaver-permission.cfg
.. |test-weaver-perms| replace:: optional-components/test-weaver/config/magpie/test-weaver-permission.cfg
.. _pavics-sdi-weaver|: https://github.com/Ouranosinc/pavics-sdi/blob/master/docs/source/notebook-components/weaver_example.ipynb
.. |pavics-sdi-weaver| replace:: Ouranosinc/pavics-sdi Weaver Example
