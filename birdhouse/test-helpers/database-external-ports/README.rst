Control public exposure of database ports
--------------------------------------------------------

Because databases may contain sensitive of private data, they should never be directly exposed.
On the other hand, accessing them remotely can be practical for testing such as in a staging server environment.

This component is intended to automatically map the databases (``PostgreSQL``, ``MongoDB``) as such.

How to enable in ``env.local`` (a copy from env.local.example_ (:download:`download </birdhouse/env.local.example>`)):

* Add ``./test-helpers/database-external-ports`` to ``EXTRA_CONF_DIRS``.

That's it. Databases will be accessible using the mapped ports in then optional component configuration.
