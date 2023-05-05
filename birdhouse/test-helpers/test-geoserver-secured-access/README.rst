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
