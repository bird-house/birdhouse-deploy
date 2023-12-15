SERVICES['Phoenix'] = {
    'info': {
        'name': 'Phoenix',
        'synopsis': 'Legacy authentication. See Magpie/Twitcher instead.',
        'version': "pavics-0.2.3",
        'institution': 'Ouranos',
        'releaseTime': get_release_time_from_repo_tag("docker", "pavics/pyramid-phoenix", "pavics-0.2.3"),
        'researchSubject': 'Authentication',
        'supportEmail': 'helpdesk@example.com',
        'category': 'Authentication',
        'tags': ['Authentication', 'Legacy']
    },
    'stats': {
        'method': '.*',
        'route': '/twitcher/ows/proxy/geoserver/web/.*'  # FIXME: original value doesn't make sense
    },
    'redirect': {
        'doc': 'http://pyramid-phoenix.readthedocs.io/en/latest/index.html',
        'releasenotes': 'https://github.com/ouranosinc/pyramid-phoenix/CHANGES.rst',
        'support': 'https://github.com/ouranosinc/pyramid-phoenix/issues',
        'source': 'https://github.com/ouranosinc/pyramid-phoenix',
        'tryme': 'https://10.0.2.15:8443/',
        'licence': 'https://github.com/ouranosinc/pyramid-phoenix/blob/master/LICENSE.txt',
        'provenance': 'https://ouranosinc.github.io/pavics-sdi/provenance/index.html'
    },
    "monitoring": {
        "Phoenix": {
            'request': {
                # FIXME: remove port by design (https://github.com/bird-house/birdhouse-deploy/issues/222)
                'url': 'https://10.0.2.15:8443/'
            }
        }
    }
}