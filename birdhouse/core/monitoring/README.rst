Monitoring
==========

This component provides monitoring and alerting for the Birdhouse physical host and containers.

Prometheus stack is used:

* Node-exporter to collect host metrics.
* cAdvisor to collect containers metrics.
* Prometheus to scrape metrics, to store them and to query them.
* AlertManager to manage alerts: deduplicate, group, route, silence, inhibit.
* Grafana to provide visualization dashboard for the metrics.


Usage
-----

- Grafana to view metric graphs: http://BIRDHOUSE_FQDN:3001/d/pf6xQMWGz/docker-and-system-monitoring
- Prometheus alert rules: http://BIRDHOUSE_FQDN:9090/rules
- AlertManager to manage alerts: http://BIRDHOUSE_FQDN:9093

The paths above are purposely not behind the proxy to not expose them publicly,
assuming only ports 80 and 443 are publicly exposed on the internet.  All other
ports are not exposed.

Only Grafana has authentication, Prometheus alert rules and AlertManager have
no authentication at all so had they been behind the proxy, anyone will be
able to access them.


How to Enable the Component
---------------------------

- Edit ``env.local`` (a copy of `env.local.example`_ (:download:`download <../env.local.example>`))

  - Add "./core/monitoring" to ``EXTRA_CONF_DIRS``
  - Set ``GRAFANA_ADMIN_PASSWORD`` to login to Grafana
  - Set ``ALERTMANAGER_ADMIN_EMAIL_RECEIVER`` for receiving alerts
  - Set ``SMTP_SERVER`` for sending alerts
  - Optionally set

    - ``ALERTMANAGER_EXTRA_GLOBAL`` to further configure AlertManager
    - ``ALERTMANAGER_EXTRA_ROUTES`` to add more routes than email notification
    - ``ALERTMANAGER_EXTRA_INHIBITION`` to disable rule from firing
    - ``ALERTMANAGER_EXTRA_RECEIVERS`` to add more receivers than the admin emails

  - Alert thresholds can be customized by setting the various ``PROMETHEUS_*_ALERT``
    vars in ``env.local``.  The list of ``PROMETHEUS_*_ALERT`` vars are in
    monitoring_default.env_ (:download:`download <monitoring/default.env>`).


Grafana Dashboard
-----------------

.. image:: monitoring/images/grafana-dashboard.png

For host, using Node-exporter to collect metrics:

- uptime
- number of container
- used disk space
- used memory, available memory, used swap memory
- load
- cpu usage
- in and out network traffic
- disk I/O

For each container, using cAdvisor to collect metrics:

- in and out network traffic
- cpu usage
- memory and swap memory usage
- disk usage

Useful visualisation features:

- zoom in one graph and all other graph update to match the same "time range" so we can correlate event
- view each graph independently for more details
- mouse over each data point will show value at that moment


Prometheus Alert Rules
----------------------

.. image:: monitoring/images/prometheus-alert-rules.png


AlertManager for Alert Dashboard and Silencing
----------------------------------------------

.. image:: monitoring/images/alertmanager-dashboard.png
.. image:: monitoring/images/alertmanager-silence-alert.png


Customizing the Component
-------------------------

- To add more Grafana dashboard, volume-mount more ``*.json`` files to the
  grafana container.

- To add more Prometheus alert rules, volume-mount more ``*.rules`` files to
  the prometheus container.

- To disable existing Prometheus alert rules, add more Alertmanager inhibition
  rules using ``ALERTMANAGER_EXTRA_INHIBITION`` via ``env.local`` file.

- Other possible Alertmanager configs via ``env.local``:
  ``ALERTMANAGER_EXTRA_GLOBAL``, ``ALERTMANAGER_EXTRA_ROUTES`` (can route to
  Slack or other services accepting webhooks), ``ALERTMANAGER_EXTRA_RECEIVERS``.
