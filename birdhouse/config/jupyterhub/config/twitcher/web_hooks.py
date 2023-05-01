#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
These hooks will be running within Twitcher, using MagpieAdapter context, applied for Jupyterhub requests.

The code below can make use of any package that is installed by Magpie/Twitcher.

.. seealso::
    Documentation about Magpie/Twitcher request/response hooks is available here:
    https://pavics-magpie.readthedocs.io/en/latest/configuration.html#service-hooks
"""

from typing import TYPE_CHECKING
from magpie.utils import get_header, get_logger

if TYPE_CHECKING:
    from pyramid.request import Request, Response


LOGGER = get_logger("birdhouse-jupyterhub-hooks")


def add_x_remote_user(request):
    # type: (Request) -> Request
    """
    Apply the ``X-REMOTE-USER`` header for identifying the logged-in user.
    """
    if request.user:
        user_name = request.user.user_name
        LOGGER.debug(f"X-REMOTE-USER header set to {user_name}")
        request.headers["X-REMOTE-USER"] = user_name
    return request


def pass_through_cookie(response):
    # type: (Response) -> Response
    """
    Pass the cookie set by jupyterhub through twitcher to the browser session.
    """
    pass