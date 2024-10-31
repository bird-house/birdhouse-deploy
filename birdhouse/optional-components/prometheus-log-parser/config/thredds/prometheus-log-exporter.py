import os
import re

import prometheus_client


# This matches a request to the THREDDS data services as defined in birdhouse/components/thredds/catalog.xml.template 
THREDDS_REQ_URI_REGEX = r'\/[^\s]+\/thredds\/(?P<tds_service>dodsC|fileServer|ncss)\/(?P<dataset>[^\s]*)(?:\?(?P<variable>\w+))?'

# This matches the nginx log_fomat as defined in birdhouse/components/proxy/nginx.conf.template
REGEX = re.compile(
    r'(?P<remote_addr>(?:^|\b(?<!\.))(?:1?\d\d?|2[0-4]\d|25[0-5])(?:\.(?:1?\d\d?|2[0-4]\d|25[0-5])){3}(?=$|[^\w.]))\s'
    r'-\s'
    r'(?P<remote_usr>-|[a-z_][a-z0-9_]{0,30})\s'
    r'(?P<date_time>\[(?P<date>\d\d\d\d-\d\d-\d\d)T(?P<time>\d\d:\d\d:\d\d).*\])\s'
    r'(?P<request>\"'
        r'(?P<req_method>GET|POST|HEAD|PUT|DELETE|CONNECT|OPTIONS|TRACE|PATCH)\s'
        fr'(?P<req_uri>{THREDDS_REQ_URI_REGEX})\s'
        r'(?P<http_ver>HTTP/\d\.\d)'
        r'\")\s'
    r'(?P<status>\d{3})\s'
    r'(?P<body_byte_sent>\d+)\s'
    r'\"(?P<http_referer>[^\s]+)\"\s'
    r'\"(?P<user_agent>[^\"]+)\"\s'
    r'\"(?P<forward_for>[^\"]+)\"')

LABEL_KEYS = ("remote_addr", "date", "tds_service", "dataset", "variable")

Counter = prometheus_client.Counter(
    name="thredds_transfer_size_kb",
    documentation="THREDDS data transferred",
    labelnames=LABEL_KEYS,
    unit="kb",
)

def parse_line(line):
    match = REGEX.match(line)
    if match:
        labels = {label: match.group(label) or "" for label in LABEL_KEYS}
        if body_byte_sent := match.group("body_byte_sent") is not None:
            body_byte_sent = int(body_byte_sent) / 1024
            Counter.labels(**labels).inc(body_byte_sent)

LOG_PARSER_CONFIG = {f"/var/log/proxy/{os.getenv('PROXY_LOG_FILE')}": [parse_line]}
