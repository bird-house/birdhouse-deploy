Deprecated Components
#####################

.. contents::

All components in this directory are not actively maintained.

If you wish to include these components in the deployed stack, additional work
may be required to make them compatible with the current stack.

Components in this directory may be removed from this repository at any time.

This directory also contains additional configurations for these deprecated components in:

- `all-public-access-deprecated/`
- `canarie-api-full-monitoring-deprecated/`
- `wps-healthchecks-deprecated/`

These contain the settings to extend the deprecated components that have been moved from the corresponding
directories under `birdhouse/optional-components`.

To enable these additional configurations; add them to the `EXTRA_CONF_DIRS` variable (in `env.local`)
as you would to enable any component. For example, to enable the deprecated malleefowl component as well as the
wps-healthchecks for malleefowl. The `EXTRA_CONF_DIRS` variable should contain:

.. code-block:: shell

  ./deprecated-components/malleefowl
  ./wps-healthchecks-deprecated
