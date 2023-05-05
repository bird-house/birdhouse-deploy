A second THREDDS server for testing
-----------------------------------

How to enable in ``env.local`` (a copy from env.local.example_ (:download:`download </birdhouse/env.local.example>`)):

* Add ``./test-helpers/testthredds`` to ``EXTRA_CONF_DIRS``.

* Optionally set ``TESTTHREDDS_IMAGE``\ , ``TESTTHREDDS_PORT``\ ,
  ``TESTTHREDDS_CONTEXT_ROOT``\ , ``TESTTHREDDS_WARFILE_NAME``\ ,
  ``TESTTHREDDS_INTERNAL_PORT``\ , ``TESTTHREDDS_NAME``\ ,  in ``env.local`` for further
  customizations.  Default values are in: `optional-components/testthredds/default.env <testthredds/default.env>`_ (:download:`download </birdhouse/optional-components/testthredds/default.env>`).

Test THREDDS service will be available at
``http://PAVICS_FQDN:TESTTHREDDS_PORT/TESTTHREDDS_CONTEXT_ROOT`` or
``https://PAVICS_FQDN_PUBLIC/TESTTHREDDS_CONTEXT_ROOT`` where ``PAVICS_FQDN`` and
``PAVICS_FQDN_PUBLIC`` are defined in your ``env.local``.

Use same docker image as regular THREDDS by default but can be customized.

New container have new ``TestDatasets`` with volume-mount to ``/data/testdatasets``
on the host.  So your testing ``.nc`` and ``.ncml`` files should be added to
``/data/testdatasets`` on the host for them to show up on this Test THREDDs
server.

``TestWps_Output`` dataset is for other WPS services to write to, similar to
``birdhouse/wps_outputs`` dataset in the production THREDDs.  With Emu, add
``export EMU_WPS_OUTPUTS_VOL=testwps_outputs`` to ``env.local`` for Emu to write to
``TestWps_Output`` dataset.

No Twitcher/Magpie access control, this Test THREDDS is directly behind the
Nginx proxy.

CANARIE monitoring will also be automatically configured for this second
THREDDS server.
