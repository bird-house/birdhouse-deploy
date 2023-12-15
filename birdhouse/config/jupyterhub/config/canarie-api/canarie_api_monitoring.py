SERVICES['Jupyter'] = {
    'info': {
        'name': 'Jupyter',
        'synopsis': 'Jupyter notebooks portal.',
        'version': "${JUPYTER_VERSION}",
        'releaseTime': get_release_time_from_repo_tag("docker", "pavics/jupyterhub", "latest"),
        'institution': 'Ouranos',
        'researchSubject': 'Any',
        'supportEmail': 'helpdesk@example.com',
        'category': 'Research',
        'tags': ['Development', 'Research', 'Notebooks']
    },
    'stats': {
        'method': '.*',
        'route': '/jupyter/.*'
    },
    'redirect': {
        'doc': 'https://jupyter.org/hub',
        'releasenotes': 'https://github.com/Ouranosinc/jupyterhub/tags',  # no CHANGES file available
        'support': 'https://github.com/Ouranosinc/jupyterhub/issues',
        'source': 'https://github.com/Ouranosinc/jupyterhub',
        'tryme': 'https://10.0.2.15/jupyter/',
        'licence': 'https://github.com/Ouranosinc/jupyterhub/blob/latest/LICENSE',
        'provenance': ''
    },
    "monitoring": {
        "Jupyter": {
            'request': {
                'url': 'https://10.0.2.15/jupyter/hub/login'
            },
        }
    }
}

CANARIE_STATS_ROUTES.append('jupyter')
