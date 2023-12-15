HUMMINGBIRD_VERSION = "0.5_dev"
HUMMINGBIRD_RELEASE = get_release_time_from_repo_tag("docker", "pavics/hummingbird", HUMMINGBIRD_VERSION)

SERVICES['hummingbird'] = {
    'info': {
        'name': 'Climatology compliance checker.',
        'synopsis': (
            'A Web Processing Service for compliance checks used in the climate science community.'
        ),
        'version': HUMMINGBIRD_VERSION,
        'institution': 'bird-house',
        'releaseTime': HUMMINGBIRD_RELEASE,
        'researchSubject': 'Climatology',
        'supportEmail': 'helpdesk@example.com',
        'category': 'Processing',
        'tags': ['Climatology', 'Checker', 'Compliance', 'CF-conventions', 'WPS', 'OGC'],
    },
    'stats': {
        'method': '.*',
        'route': '/twitcher/ows/proxy/hummingbird.*'
    },
    'redirect': {
        'doc': 'https://hummingbird.readthedocs.io/',
        'releasenotes': 'https://github.com/bird-house/hummingbird/blob/master/CHANGES.rst',
        'support': 'https://github.com/bird-house/hummingbird/issues',
        'source': 'https://github.com/bird-house/hummingbird',
        'tryme': 'https://10.0.2.15/twitcher/ows/proxy/hummingbird/wps?service=WPS&version=1.0.0&request=GetCapabilities',
        'licence': 'https://github.com/bird-house/hummingbird/blob/master/LICENSE.txt',
        'provenance': 'https://github.com/bird-house/hummingbird'
    },
    'monitoring': {
        'Hummingbird': {
            'request': {
                'url': 'http://hummingbird:8080/wps?service=WPS&version=1.0.0&request=GetCapabilities'
            }
        },
    }
}
