import os
import re

import prometheus_client


# This matches a request to the THREDDS data services as defined in birdhouse/components/thredds/catalog.xml.template

# Examples:

## OpenDAP:
# /twitcher/ows/proxy/thredds/dodsC/datasets/reanalyses/day_ERA5-Land_NAM.ncml.dods?tasmin.tasmin%5b24820:25184%5d%5b300:399%5d%5b1000:1099%5d

## NCSS
# /twitcher/ows/proxy/thredds/ncss/point/birdhouse/wps_outputs/59aca2ba-0f4e-11ed-84db-0242ac1d0013/out.nc/dataset.html

## File Server
# /twitcher/ows/proxy/thredds/fileServer/birdhouse/disk2/ouranos/CORDEX/CMIP6/DD/NAM-12/OURANOS/MPI-ESM1-2-LR/ssp370/r2i1p1f1/CRCM5/v1-r1/1hr/tas/v20250325/tas_NAM-12_MPI-ESM1-2-LR_ssp370_r2i1p1f1_OURANOS_CRCM5_v1-r1_1hr_206101010000-206112312300.nc

## WCS
# /twitcher/ows/proxy/thredds/wcs/birdhouse/disk2/ouranos/CORDEX/CMIP6/DD/NAM-12/OURANOS/MPI-ESM1-2-LR/historical/r1i1p1f1/CRCM5/v1-r1/1hr/vas/v20231129/vas_NAM-12_MPI-ESM1-2-LR_historical_r1i1p1f1_OURANOS_CRCM5_v1-r1_1hr_198601010000-198612312300.nc?request=GetCapabilities&service=WCS&version=1.0.0

THREDDS_REQ_URI_REGEX = (r'\/[^\s]+\/thredds\/'
                         r'(?P<tds_service>dodsC|fileServer|ncss/(?:grid|point)|wcs)\/'
                         r'(?P<dataset>[^\s\?]*)'
                         r'(?:\?(?P<thredds_request>\S+))?')

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

LABEL_KEYS = ("remote_addr", "tds_service", "dataset", "variable")

counter = prometheus_client.Counter(
    name="thredds_transfer_size_bytes",
    documentation="THREDDS data transferred",
    labelnames=LABEL_KEYS,
    unit="bytes",
)

def parse_line(line):
    match = REGEX.match(line)
    if match:
        groups = match.groupdict()
        # Note that `variable` is not extracted by the regex, but by the logic below.
        labels = {k: groups.get(k, "") for k in LABEL_KEYS}
        # Tweaks
        if labels["tds_service"] == "dodsC":
            labels["dataset"] = (labels["dataset"].removesuffix(".dods")
                .removesuffix(".dds")
                .removesuffix(".das"))
            if (req := match.group("thredds_request")) is not None:
                labels["variable"] = ",".join(re.findall(r"(\w+)(?:\.\w+)?(?:%[^,]+)?", req))
        elif labels["tds_service"].startswith("ncss"):
            # The NCSS regexp consumes the access method (e.g., point, grid) as part of the service name.
            labels["dataset"] = labels["dataset"].removesuffix("/dataset.html")
            if (req := match.group("thredds_request")) is not None:
                if m := re.search("var=([^&]+)", req):
                    labels["variable"] = m.group(1)

        if body_byte_sent := match.group("body_byte_sent"):
            body_byte_sent = int(body_byte_sent)
            counter.labels(**labels).inc(body_byte_sent)

LOG_PARSER_CONFIG = {f"/var/log/proxy/{os.getenv('PROXY_LOG_FILE')}": [parse_line]}
