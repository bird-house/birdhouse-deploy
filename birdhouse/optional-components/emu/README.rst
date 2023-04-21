Emu WPS service for testing
---------------------------

Preconfigured for Emu but can also be used to quickly deploy any birds
temporarily without changing code.  Good to preview new birds or test
alternative configuration of existing birds.

No Postgres DB configured.  If need Postgres DB, use generic_bird component
instead.

How to enable Emu in ``env.local`` (a copy from env.local.example_
(:download:`download </birdhouse/env.local.example>`)):

* Add ``./optional-components/emu`` to ``EXTRA_CONF_DIRS``.
* Optionally set ``EMU_IMAGE``, ``EMU_PORT``,
  ``EMU_NAME``, ``EMU_INTERNAL_PORT``,
  ``EMU_WPS_OUTPUTS_VOL`` in ``env.local`` for further customizations.
  Default values are in `optional-components/emu/default.env <emu/default.env>`_
  (:download:`download </birdhouse/optional-components/emu/default.env>`).

Emu service will be available at ``http://PAVICS_FQDN:EMU_PORT/wps`` or
``https://PAVICS_FQDN_PUBLIC/TWITCHER_PROTECTED_PATH/EMU_NAME`` where
``PAVICS_FQDN``\ , ``PAVICS_FQDN_PUBLIC`` and ``TWITCHER_PROTECTED_PATH`` are defined
in your ``env.local``.

Magpie will be automatically configured to give complete public anonymous
access for this Emu WPS service.

CANARIE monitoring will also be automatically configured for this Emu WPS
service.