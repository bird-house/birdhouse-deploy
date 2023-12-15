SERVICES['Magpie'] = {
    'info': {
        'name': 'Magpie',
        'synopsis': (
            'Magpie is service for AuthN/AuthZ accessible via a REST API. '
            'It allows you to manage User/Group/Service/Resource/Permission management '
            'and integrates with Twitcher.'
        ),
        'version': "3.38.0",
        'institution': 'Ouranos',
        'releaseTime': get_release_time_from_repo_tag("github", "Ouranosinc/Magpie", "3.38.0"),
        'researchSubject': 'Security',
        'supportEmail': 'helpdesk@example.com',
        'category': 'Security',
        'tags': ['Security', 'Management', 'Access', 'Policy Decision Point']
    },
    'stats': {
        'method': '.*',
        'route': "/magpie/.*"
    },
    'redirect': {
        'doc': 'https://pavics-magpie.readthedocs.io/',
        'releasenotes': 'https://github.com/Ouranosinc/Magpie/blob/master/CHANGES.rst',
        'support': 'https://github.com/Ouranosinc/Magpie/issues',
        'source': 'https://github.com/Ouranosinc/Magpie',
        'tryme': 'https://10.0.2.15/magpie/',
        'licence': 'https://github.com/Ouranosinc/Magpie/blob/3.38.0/LICENSE',
        'provenance': 'https://ouranosinc.github.io/pavics-sdi/provenance/index.html'
    },
    "monitoring": {
        "Magpie": {
            'request': {
                'url': 'https://10.0.2.15/magpie/version'
            },
            'response': {
                'text': r'\{.*"code": 200.*"type": "application/json".*\}'
            }
        }
    }
}

CANARIE_STATS_ROUTES.append('magpie')
