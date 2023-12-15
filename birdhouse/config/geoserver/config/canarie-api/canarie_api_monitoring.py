SERVICES['GeoServer'] = {
    'info': {
        'name': 'GeoServer',
        'synopsis': (
            'GeoServer is the reference implementation of the Open Geospatial Consortium (OGC) '
            'Web Feature Service (WFS) and Web Coverage Service (WCS) standards, as well as a high performance '
            'certified compliant Web Map Service (WMS), compliant Catalog Service for the Web (CSW) and '
            'implementing Web Processing Service (WPS). GeoServer forms a core component of the Geospatial Web.'
        ),
        'version': "2.22.2",
        'institution': 'Ouranos',
        'releaseTime': get_release_time_from_repo_tag("docker", "pavics/geoserver", "2.22.2-kartoza-build20230226-r7-allow-change-context-root-and-fix-missing-stable-plugins-and-avoid-chown-datadir"),
        'researchSubject': 'Geospatial',
        'supportEmail': 'helpdesk@example.com',
        'category': 'Data Catalog',
        'tags': ['Data', 'Geospatial', 'Catalog', 'OGC', 'WFS', 'WMS', 'WPS']
    },
    'stats': {
        'method': '.*',
        'route': "/geoserver/.*"
    },
    'redirect': {
        'doc': 'https://docs.geoserver.org/',
        'releasenotes': 'https://geoserver.org/release/2.22.2/',
        'support': 'https://github.com/kartoza/docker-geoserver/issues',
        'source': 'https://github.com/kartoza/docker-geoserver',
        'tryme': 'https://10.0.2.15/geoserver/',
        'licence': 'https://github.com/geoserver/geoserver/blob/2.22.2/LICENSE.txt',
        'provenance': 'https://github.com/kartoza/docker-geoserver'
    },
    "monitoring": {
        "GeoServer": {
            'request': {
                'url': 'https://10.0.2.15/geoserver/web/'
            }
        }
    }
}

CANARIE_STATS_ROUTES.append('geoserver')
