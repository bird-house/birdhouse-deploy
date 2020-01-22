# Optional components

## Emu WPS service for testing

How to enable Emu in `env.local` (a copy from
[`env.local.example`](../env.local.example)):

* Add `./optional-components/emu` to `EXTRA_CONF_DIRS`.
* Set `EMU_IMAGE`.

Emu service will be available at `http://PAVICS_FQDN:8888/wps` or
`https://PAVICS_FQDN_PUBLIC/twitcher/ows/proxy/emu` where `PAVICS_FQDN`
and `PAVICS_FQDN_PUBLIC` are defined in your `env.local`.
