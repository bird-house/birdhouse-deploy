def get_samples(metrics, metric_name):
    """Get samples for a Counter metric."""
    for metric in metrics:
        if metric.name == metric_name:
             for sample in metric.samples:
                 if sample.name == metric_name + "_total":
                    yield sample


# plex is a fixture (see conftest.py) that provides the prometheus log exporter module.
def test_550(plex):
    log = """172.20.0.1 - - [2025-06-17T03:08:02+00:00] "GET /thredds/catalog.html HTTP/1.1" 302 0 "-" "python-requests/2.31.0" "-"
    172.20.0.1 - - [2025-06-17T03:08:02+00:00] "GET /twitcher/ows/proxy/thredds/catalog/catalog.html HTTP/1.0" 200 4200 "-" "python-requests/2.31.0" "172.20.0.1"
    172.20.0.1 - - [2025-06-17T03:08:02+00:00] "GET /thredds/catalog/catalog.html HTTP/1.1" 200 4219 "-" "python-requests/2.31.0" "-"
    172.20.0.1 - - [2025-06-17T03:08:04+00:00] "GET /twitcher/ows/proxy/thredds/wms/birdhouse/testdata/ta_Amon_MRI-CGCM3_decadal1980_r1i1p1_199101-200012.nc?service=WMS&version=1.3.0&request=GetCapabilities HTTP/1.1" 200 19320 "-" "python-requests/2.31.0" "-"
    172.20.0.1 - - [2025-06-17T03:08:06+00:00] "GET /twitcher/ows/proxy/thredds/wms/birdhouse/testdata/ta_Amon_MRI-CGCM3_decadal1980_r1i1p1_199101-200012.nc?service=WMS&version=1.3.0&request=GetCapabilities HTTP/1.1" 200 19320 "-" "python-requests/2.31.0" "-"
    172.20.0.1 - - [2025-06-17T03:08:07+00:00] "GET /twitcher/ows/proxy/thredds/wms/birdhouse/testdata/ta_Amon_MRI-CGCM3_decadal1980_r1i1p1_199101-200012.nc?service=WMS&version=1.3.0&request=GetCapabilities HTTP/1.1" 200 19320 "-" "python-requests/2.31.0" "-"
    192.168.0.45 - - [2025-06-17T03:08:32+00:00] "GET /twitcher/ows/proxy/thredds/dodsC/birdhouse/testdata/ta_Amon_MRI-CGCM3_decadal1980_r1i1p1_199101-200012.nc.dds HTTP/1.1" 200 584 "-" "oc4.9.2" "-"
    192.168.0.45 - - [2025-06-17T03:08:32+00:00] "GET /twitcher/ows/proxy/thredds/dodsC/birdhouse/testdata/ta_Amon_MRI-CGCM3_decadal1980_r1i1p1_199101-200012.nc.das HTTP/1.1" 200 3684 "-" "oc4.9.2" "-"
    192.168.0.45 - - [2025-06-17T03:08:32+00:00] "GET /twitcher/ows/proxy/thredds/dodsC/birdhouse/testdata/ta_Amon_MRI-CGCM3_decadal1980_r1i1p1_199101-200012.nc.dds HTTP/1.1" 200 584 "-" "oc4.9.2" "-"
    192.168.0.45 - - [2025-06-17T03:08:32+00:00] "GET /twitcher/ows/proxy/thredds/dodsC/birdhouse/testdata/ta_Amon_MRI-CGCM3_decadal1980_r1i1p1_199101-200012.nc.dods?time,time_bnds,plev,lat,lat_bnds,lon,lon_bnds HTTP/1.1" 200 15027 "-" "oc4.9.2" "-"
    """
    for line in log.strip().splitlines():
        plex.parse_line(line.strip())

    samples = list(get_samples(plex.counter.collect(), "thredds_transfer_size_kb"))
    assert len(samples) == 2

    s1, s2 = samples
    assert s1.value == (584 + 3684 + 584)/1024, "Total size does not match expected value"
    assert s1.labels["dataset"] == "birdhouse/testdata/ta_Amon_MRI-CGCM3_decadal1980_r1i1p1_199101-200012.nc"
    assert s1.labels["tds_service"] == "dodsC", "Service type does not match expected value"
    assert s1.labels["variable"] == ""

    assert s2.value == 15027 / 1024
    assert s2.labels["variable"] == "time,time_bnds,plev,lat,lat_bnds,lon,lon_bnds"


def test_dodsC(plex):
    log = """70.27.245.58 - - [2025-06-03T13:59:39+00:00] "GET /twitcher/ows/proxy/thredds/dodsC/datasets/reanalyses/day_ERA5-Land_NAM.ncml.dods?tasmin.tasmin%5b13870:14234%5d%5b300:399%5d%5b1000:1099%5d HTTP/1.1" 200 14628694 "-" "oc4.8.1" "-"
    70.27.245.58 - - [2025-06-03T13:59:39+00:00] "GET /twitcher/ows/proxy/thredds/dodsC/datasets/reanalyses/day_ERA5-Land_NAM.ncml.dods?pr%5b5040:6839%5d%5b1%5d%5b2%5d,lat%5b1%5d,lon%5b2%5d,time%5b5040:6839%5d HTTP/1.1" 200 14628694 "-" "oc4.8.1" "-""
    """
    for line in log.strip().splitlines():
        plex.parse_line(line.strip())

    samples = get_samples(plex.counter.collect(), "thredds_transfer_size_kb")
    s = next(samples)

    assert s.labels["tds_service"] == "dodsC"
    assert s.labels["dataset"] == "datasets/reanalyses/day_ERA5-Land_NAM.ncml"
    assert s.labels["variable"] == "tasmin"

    s = next(samples)
    assert s.labels["variable"] == "pr,lat,lon,time"


def test_wcs(plex):
    log = """18.207.79.144 - - [2025-06-03T13:59:15+00:00] "GET /twitcher/ows/proxy/thredds/wcs/birdhouse/disk2/ouranos/CORDEX/CMIP6/DD/NAM-12/OURANOS/MPI-ESM1-2-LR/historical/r1i1p1f1/CRCM5/v1-r1/1hr/vas/v20231129/vas_NAM-12_MPI-ESM1-2-LR_historical_r1i1p1f1_OURANOS_CRCM5_v1-r1_1hr_198601010000-198612312300.nc?request=GetCapabilities&service=WCS&version=1.0.0 HTTP/1.1" 200 3272 "-" "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Amazonbot/0.1; +https://developer.amazon.com/support/amazonbot) Chrome/119.0.6045.214 Safari/537.36" "-"
    """
    for line in log.strip().splitlines():
        plex.parse_line(line.strip())

    s = next(get_samples(plex.counter.collect(), "thredds_transfer_size_kb"))

    assert s.labels["tds_service"] == "wcs"
    assert s.labels["dataset"] == "birdhouse/disk2/ouranos/CORDEX/CMIP6/DD/NAM-12/OURANOS/MPI-ESM1-2-LR/historical/r1i1p1f1/CRCM5/v1-r1/1hr/vas/v20231129/vas_NAM-12_MPI-ESM1-2-LR_historical_r1i1p1f1_OURANOS_CRCM5_v1-r1_1hr_198601010000-198612312300.nc"
    assert s.labels["variable"] == ""


def test_fileserver(plex):
    log = """35.171.141.42 - - [2025-06-03T13:59:03+00:00] "GET /twitcher/ows/proxy/thredds/fileServer/birdhouse/disk2/ouranos/CORDEX/CMIP6/DD/NAM-12/OURANOS/MPI-ESM1-2-LR/ssp370/r2i1p1f1/CRCM5/v1-r1/1hr/tas/v20250325/tas_NAM-12_MPI-ESM1-2-LR_ssp370_r2i1p1f1_OURANOS_CRCM5_v1-r1_1hr_206101010000-206112312300.nc HTTP/1.1" 200 417457 "-" "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Amazonbot/0.1; +https://developer.amazon.com/support/amazonbot) Chrome/119.0.6045.214 Safari/537.36" "-"
    """
    for line in log.strip().splitlines():
        plex.parse_line(line.strip())

    s = next(get_samples(plex.counter.collect(), "thredds_transfer_size_kb"))

    assert s.labels["tds_service"] == "fileServer"
    assert s.labels["dataset"] == "birdhouse/disk2/ouranos/CORDEX/CMIP6/DD/NAM-12/OURANOS/MPI-ESM1-2-LR/ssp370/r2i1p1f1/CRCM5/v1-r1/1hr/tas/v20250325/tas_NAM-12_MPI-ESM1-2-LR_ssp370_r2i1p1f1_OURANOS_CRCM5_v1-r1_1hr_206101010000-206112312300.nc"
    assert s.labels["variable"] == ""


def test_ncss(plex):
    # Not a real request
    log = """20.171.207.150 - - [2025-06-03T13:59:22+00:00] "GET /twitcher/ows/proxy/thredds/ncss/point/birdhouse/wps_outputs/59aca2ba-0f4e-11ed-84db-0242ac1d0013/out.nc/dataset.html HTTP/1.1" 302 145 "-" "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; GPTBot/1.2; +https://openai.com/gptbot)" "-"
    20.171.207.151 - - [2025-06-03T13:59:22+00:00] "GET /twitcher/ows/proxy/thredds/ncss/grid/datasets/simulations/bias_adjusted/cmip6/ouranos/ESPO-G/ESPO-G6-E5Lv1.0.0/day_ESPO-G6-E5L_v1.0.0_CMIP6_ScenarioMIP_NAM_AS-RCEC_TaiESM1_ssp370_r1i1p1f1_1950-2100.ncml?var=tasmin&north=83.350&west=-179.950&east=-9.950&south=9.950&horizStride=1&time_start=1950-01-01T00:00:00Z&time_end=2100-12-31T00:00:00Z&&&accept=netcdf3 HTTP/1.1" 302 145 "-" "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; GPTBot/1.2; +https://openai.com/gptbot)" "-"
    """
    for line in log.strip().splitlines():
        plex.parse_line(line.strip())

    samples = get_samples(plex.counter.collect(), "thredds_transfer_size_kb")

    s = next(samples)
    assert s.labels["tds_service"] == "ncss/point"
    assert s.labels["dataset"] == "birdhouse/wps_outputs/59aca2ba-0f4e-11ed-84db-0242ac1d0013/out.nc"
    assert s.labels["variable"] == ""

    s = next(samples)
    assert s.labels["tds_service"] == "ncss/grid"
    assert s.labels["dataset"] == "datasets/simulations/bias_adjusted/cmip6/ouranos/ESPO-G/ESPO-G6-E5Lv1.0.0/day_ESPO-G6-E5L_v1.0.0_CMIP6_ScenarioMIP_NAM_AS-RCEC_TaiESM1_ssp370_r1i1p1f1_1950-2100.ncml"
    assert s.labels["variable"] == "tasmin"
