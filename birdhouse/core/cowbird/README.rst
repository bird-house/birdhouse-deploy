Cowbird
=======

Cowbird is a middleware that manages interactions between various *birds* of the `bird-house`_ stack.

It relies on the existence of other services under a common architecture, but applies changes to the resources under
those services such that the complete ecosystem can seamlessly operate together (see |cowbird-diagram|_).

The code of this service is located in |cowbird-repo|_. Its documentation is provided on |cowbird-rtd|_.

.. _bird-house: https://github.com/bird-house/birdhouse-deploy
.. |cowbird-diagram| replace:: Components Diagram
.. _cowbird-diagram: https://github.com/Ouranosinc/cowbird/blob/master/docs/_static/cowbird_components.png
.. |cowbird-repo| replace:: Ouranosinc/cowbird
.. _cowbird-repo: https://github.com/Ouranosinc/cowbird
.. |cowbird-rtd| replace:: ReadTheDocs
.. _cowbird-rtd: https://pavics-cowbird.readthedocs.io/

Operations Performed by Cowbird
-------------------------------

- Synchronize Magpie user and group permissions between "corresponding files" located under different services.
  For example, THREDDS user-workspace files visualized in the catalog will be accessible by the same user under
  the corresponding user-workspace under GeoServer.
- Synchronize Weaver endpoints to retrieve equivalent definitions under various paths and access to generated WPS
  outputs following a job execution by a given user.
- Synchronize permissions between API endpoints and local storage files.
- Synchronize permissions and references based on event triggers and request callbacks.

Usage
-----

Cowbird is intended to work on its own, behind the scene, to apply any required resource synchronization between
the various services of the platform when changes are detected. Therefore, it does not require any explicit interaction
from users.

In case the platform maintainer desires to perform manual syncing operations with Cowbird, its REST API should be used.
It will be accessible under ``https://{BIRDHOUSE_FQDN_PUBLIC}/cowbird`` and details of available endpoints will be served
under ``/cowbird/api``. Note that Magpie administrator credentials will be required to access those endpoints.

How to Enable the Component
---------------------------

- Edit ``env.local`` (a copy of `env.local.example`_)
- Add ``"./core/cowbird"`` to ``EXTRA_CONF_DIRS``.

Customizing the Component
-------------------------

Cowbird can be affected by multiple variables defined globally on the
stack (i.e.: ``env.local``, a copy of `env.local.example`_). It also considers variables of other services such as
THREDDS, GeoServer, Magpie, etc. in order to perform required interactions between them.

By default, variables defined in |cowbird-default|_ will be used unless overridden in ``env.local``. To apply changes
define your custom values in ``env.local`` directly.

.. |cowbird-default| replace:: cowbird/default.env
.. _cowbird-default: ./cowbird/default.env
