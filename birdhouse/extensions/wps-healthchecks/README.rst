Enable health checks for WPS services
--------------------------------------------------------

At any given time, WPS services could stop responding. Using the ``healthcheck`` feature from ``docker-compose``, it is
possible to monitor the services at regular intervals to ensure they remain accessible. Using this, it is possible to
rapidly identify if a service might be misbehaving.

Since the various WPS services are executed using a different applications and dependencies in their respective
Docker images, the method required to validate their status can vary a lot for each case. This optional component
defines all the appropriate ``healthcheck`` for all known WPS services in PAVICS.

How to enable in ``env.local`` (a copy from env.local.example_ (:download:`download </birdhouse/env.local.example>`)):

* Add ``./extensions/wps-healthchecks`` to ``EXTRA_CONF_DIRS``.

Once enabled, every WPS service will be monitored at regular intervals and ``docker-compose`` will indicate in their
health status. Command ``pavics-compose ps`` can be employed to list running images, and along with it, the statuses
reported by each ``healthcheck``.


.. _magpie-public-access-config:
