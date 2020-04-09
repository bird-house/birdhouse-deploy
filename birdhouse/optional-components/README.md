# Optional components

## Monitor all components in Canarie node, both public and internal url

So that the url https://<PAVICS_FQDN>/canarie/node/service/stats also return
what the end user really see (a component might work but is not accessible to
the end user).

This assume all the WPS services are public.  If not the case, make a copy of
this config and adjust accordingly.

How to enable this config in `env.local` (a copy from
[`env.local.example`](../env.local.example)):

* Add `./optional-components/canarie-api-full-monitoring` to `EXTRA_CONF_DIRS`.


## Emu WPS service for testing

How to enable Emu in `env.local` (a copy from
[`env.local.example`](../env.local.example)):

* Add `./optional-components/emu` to `EXTRA_CONF_DIRS`.
* Set `EMU_IMAGE`.

Emu service will be available at `http://PAVICS_FQDN:8888/wps` or
`https://PAVICS_FQDN_PUBLIC/twitcher/ows/proxy/emu` where `PAVICS_FQDN`
and `PAVICS_FQDN_PUBLIC` are defined in your `env.local`.


## A second Thredds server for testing

How to enable in `env.local` (a copy from
[`env.local.example`](../env.local.example)):

* Add `./optional-components/testthredds` to `EXTRA_CONF_DIRS`.

Test Thredds service will be available at `http://PAVICS_FQDN:8084/testthredds`
or `https://PAVICS_FQDN_PUBLIC/testthredds` where `PAVICS_FQDN` and
`PAVICS_FQDN_PUBLIC` are defined in your `env.local`.

New container have new `TestDatasets` with volume-mount to `/data/testdatasets`
on the host.  So your testing `.nc` and `.ncml` files should be added to
`/data/testdatasets` on the host for them to show up on this Test Thredds
server.

`TestWps_Output` dataset is for other WPS services to write to, similar to
`birdhouse/wps_outputs` dataset in the production Thredds.  With Emu, add
`export EMU_WPS_OUTPUTS_VOL=testwps_outputs` to `env.local` for Emu to write to
`TestWps_Output` dataset.

No Twitcher/Magpie access control, this Test Thredds is directly behind the
Nginx proxy.


## A second Finch server for testing

How to enable in `env.local` (a copy from
[`env.local.example`](../env.local.example)):

* Add `./optional-components/finch2` to `EXTRA_CONF_DIRS`.

Second Finch service will be available at `http://PAVICS_FQDN:8010/wps`
or `https://PAVICS_FQDN_PUBLIC/twitcher/ows/proxy/finch2` where `PAVICS_FQDN` and
`PAVICS_FQDN_PUBLIC` are defined in your `env.local`.

Use same docker image as regular Finch.

Use sqlite DB instead of Postgres like the regular Finch.

Magpie will be automatically configured to give complete public anonymous
access for this second Finch.

Canarie monitoring will also be automatically configured for this second Finch.
