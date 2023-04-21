A generic bird WPS service
--------------------------

Can be used to quickly deploy any birds temporarily without changing code.
Good to preview new birds or test alternative configuration of existing birds.

How to enable in ``env.local`` (a copy from env.local.example_ (:download:`download </birdhouse/env.local.example>`)):

* Add ``./optional-components/generic_bird`` to ``EXTRA_CONF_DIRS``.

* Optionally set ``GENERIC_BIRD_IMAGE``, ``GENERIC_BIRD_PORT``,
  ``GENERIC_BIRD_NAME``, ``GENERIC_BIRD_INTERNAL_PORT``, and
  ``GENERIC_BIRD_POSTGRES_IMAGE`` in ``env.local`` for further customizations.
  Default values are in `optional-components/generic_bird/default.env <generic_bird/default.env>`_
  (:download:`download </birdhouse/optional-components/generic_bird/default.env>`).

The WPS service will be available at ``http://PAVICS_FQDN:GENERIC_BIRD_PORT/wps``
or ``https://PAVICS_FQDN_PUBLIC/TWITCHER_PROTECTED_PATH/GENERIC_BIRD_NAME`` where
``PAVICS_FQDN``\ , ``PAVICS_FQDN_PUBLIC`` and ``TWITCHER_PROTECTED_PATH`` are defined
in your ``env.local``.

Use same docker image as regular Finch by default but can be customized.

Use a separate Postgres DB for this optional component to be completely
self-contained and to allow experimenting with different versions of Postgres
DB.

Magpie will be automatically configured to give complete public anonymous
access for this WPS service.

CANARIE monitoring will also be automatically configured for this WPS service.
