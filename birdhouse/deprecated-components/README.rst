Deprecated Components
#####################

.. shared references by multiple components definitions
.. |deprecated-scripts| replace:: ``scripts/deprecated``
.. _deprecated-scripts: ../scripts/deprecated/
.. |optional-components| replace:: ``birdhouse/optional-components``
.. _optional-components: ../optional-components/
.. |optional-components-all-public-access| replace:: ``./optional-components/all-public-access``
.. _optional-components-all-public-access: ../optional-components/README.rst#all-public-access

.. contents::

All components in this directory are not actively maintained.

If you wish to include these components in the deployed stack, additional work
may be required to make them compatible with the current stack.

Components in this directory may be removed from this repository at any time.

This directory also contains additional configurations for these deprecated components in:

- ``deprecated-components/<component>/config/canarie-api/``
- ``deprecated-components/<component>/config/magpie/`` (corresponding to |optional-components-all-public-access|_ definitions)
- ``deprecated-components/wps-healthchecks``

These contain the settings to extend the deprecated components that have been moved from the corresponding
directories under |optional-components|_.

To enable these additional configurations; add them to the ``BIRDHOUSE_EXTRA_CONF_DIRS`` variable (in ``env.local``)
as you would to enable any component. For example, to enable the deprecated malleefowl component as well as the
``wps-healthchecks`` for malleefowl. The ``BIRDHOUSE_EXTRA_CONF_DIRS`` variable should contain:

.. code-block:: shell

  ./deprecated-components/malleefowl
  ./wps-healthchecks-deprecated


Similarly, some of the associated scripts to these components can be found under the |deprecated-scripts|_.
