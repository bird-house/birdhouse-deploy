SERVICES['Solr'] = {
    'info': {
        'name': 'Solr',
        'synopsis': (
            'SOLR is a search platform part of the Apache Lucene project. '
            'It is used in this project for its faceted search capability. '
            'Search queries are relayed from the UI or WPS processes to the SOLR database, '
            'which returns a json file with the links to matching files.'
        ),
        'version': "5.2.1",
        'institution': 'Ouranos',
        'releaseTime': get_release_time_from_repo_tag("docker", "pavics/solr", "5.2.1"),
        'researchSubject': 'Climatology',
        'supportEmail': 'helpdesk@example.com',
        'category': 'Data Manipulation',
        'tags': ['Indexation', 'Search']
    },
    'stats': {
        'method': '.*',
        'route': '/solr/.*'
    },
    'redirect': {
        'doc': 'https://ouranosinc.github.io/pavics-sdi/arch/backend.html#indexation',
        'releasenotes': 'https://github.com/Ouranosinc/PAVICS/tags',
        'support': 'https://github.com/Ouranosinc/PAVICS/issues',
        'source': 'https://github.com/Ouranosinc/PAVICS/tree/master/birdhouse/docker/solr',
        'tryme': 'http://10.0.2.15:8983/solr/',
        'licence': 'https://github.com/bird-house/finch/blob/master/LICENSE.txt',
        'provenance': 'https://ouranosinc.github.io/pavics-sdi/arch/backend.html#indexation'
    },
    "monitoring": {
        'Solr': {
            'request': {
                # FIXME: remove port by design (https://github.com/bird-house/birdhouse-deploy/issues/222)
                'url': 'http://10.0.2.15:8983/solr/birdhouse/select'
            }
        },
    }
}
