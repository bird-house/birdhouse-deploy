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

* Add ``./test-helpers/all-public-access`` to ``EXTRA_CONF_DIRS``.

The anonymous user will now have all the permissions described in |magpie-public-perms|_
(:download:`download </birdhouse/optional-components/all-public-access/all-public-access-magpie-permission.cfg>`).


.. _magpie-public-perms: ./all-public-access/all-public-access-magpie-permission.cfg
.. |magpie-public-perms| replace:: optional-components/all-public-access/all-public-access-magpie-permission.cfg
.. _env.local.example: ../env.local.example
