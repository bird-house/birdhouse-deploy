SERVICES['Cowbird'] = {
    'info': {
        'name': 'Cowbird',
        'synopsis': 'Cowbird is a middleware that manages interactions between various birds of the bird-house stack.',
        'version': "1.1.0",
        'institution': 'Ouranos, CRIM',
        'releaseTime': get_release_time_from_repo_tag("github", "Ouranosinc/cowbird", "1.1.0"),
        'researchSubject': 'Any',
        'supportEmail': 'helpdesk@example.com',
        'category': 'Security',
        'tags': ['Security', 'Management', 'Access', 'Policy Decision Point']
    },
    'stats': {
        'method': '.*',
        'route': "/cowbird/.*"
    },
    'redirect': {
        'doc': 'https://pavics-cowbird.readthedocs.io/',
        'releasenotes': 'https://github.com/Ouranosinc/cowbird//blob/master/CHANGES.rst',
        'support': 'https://github.com/Ouranosinc/cowbird//issues',
        'source': 'https://github.com/Ouranosinc/cowbird/',
        'tryme': 'https://10.0.2.15/cowbird/',
        'licence': 'https://github.com/Ouranosinc/cowbird//blob/1.1.0/LICENSE',
        'provenance': 'https://github.com/Ouranosinc/cowbird/'
    },
    "monitoring": {
        "Cowbird": {
            'request': {
                'url': 'http://cowbird:7000/'
            },
            'response': {
                'text': '\{.*"title":.*"Cowbird REST API".*\}'
            }
        }
    }
}

# vi: tabstop=8 expandtab shiftwidth=4 softtabstop=4 syntax=python
