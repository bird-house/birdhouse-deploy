# We can only monitor twitcher if there is an endpoint that it is protecting that we can try to access
# If there is at least one other service that provides a route protected by twitcher, monitor that route;
# otherwise do nothing.
if 'flyingpigeon':
    SERVICES['node']['monitoring'].update({'Twitcher': {
        'request': {
            'url': 'https://10.0.2.15/twitcher/ows/proxy/flyingpigeon?service=WPS&version=1.0.0&request=GetCapabilities'
        }
    }})
