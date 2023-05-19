Monitor all components in CANARIE node, both public and internal url
--------------------------------------------------------------------

So that the url ``https://<BIRDHOUSE_FQDN>/canarie/node/service/stats`` also return
what the end user really see (a component might work but is not accessible to
the end user).

This assume all the WPS services are public.  If not the case, make a copy of
this config and adjust accordingly.

How to enable this config in ``env.local`` (a copy from env.local.example_
(:download:`download </birdhouse/env.local.example>`)):

* Add ``./extensions/canarie-api-full-monitoring`` to ``EXTRA_CONF_DIRS``.
