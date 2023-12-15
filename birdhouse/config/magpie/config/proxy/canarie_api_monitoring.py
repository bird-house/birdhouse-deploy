SERVICES['node']['monitoring'].update({'Magpie': {
    'request': {
        'url': 'https://10.0.2.15/magpie/version'
    },
    'response': {
        'text': '\{.*"code": 200.*"type": "application/json".*\}'
    }
}})
CANARIE_STATS_ROUTES.append('magpie')
