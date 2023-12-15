SERVICES['Malleefowl'] = {
    'info': {
        'name': 'Malleefowl',
        'synopsis': 'A Web Processing Service for Climate Data Access and Workflows.',
        'version': "pavics-0.3.5",
        'releaseTime': get_release_time_from_repo_tag("github", "Ouranosinc/malleefowl", "pavics-0.3.5"),
        'institution': 'Ouranos',
        'researchSubject': 'Climatology',
        'supportEmail': 'helpdesk@example.com',
        'category': 'Resource/Cloud Management',
        'tags': ['Climatology']
    },
    'stats': {
        'method': '.*',
        'route': '/malleefowl/.*'
    },
    'redirect': {
        'doc': 'https://malleefowl.readthedocs.io/en/latest/',
        'releasenotes': 'https://github.com/Ouranosinc/malleefowl/blob/master/CHANGES.rst',
        'support': 'https://github.com/Ouranosinc/malleefowl/issues',
        'source': 'https://github.com/Ouranosinc/malleefowl',
        'tryme': 'https://10.0.2.15/malleefowl/',
        'licence': '',
        'provenance': ''
    },
    'monitoring': {
        "Malleefowl": {
            'request': {
                # FIXME: remove port by design (https://github.com/bird-house/birdhouse-deploy/issues/222)
                'url': 'http://10.0.2.15:8091/wps?service=WPS&version=1.0.0&request=GetCapabilities'
            }
        }
    }
}