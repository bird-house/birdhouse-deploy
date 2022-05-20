#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
These hooks will be running within Twitcher, using MagpieAdapter context, applied for Weaver requests.

The code below can make use of any package that is installed by Magpie/Twitcher.
"""

from typing import TYPE_CHECKING

from magpie.constants import get_constant
from magpie.utils import get_header

if TYPE_CHECKING:
    from pyramid.request import Request


def is_admin(request):
    # type: (Request) -> bool
    admin_group = get_constant("MAGPIE_ADMIN_GROUP", settings_container=request)
    return admin_group in [group.group_name for group in request.user.groups]


def add_x_wps_output_context(request):
    # type: (Request) -> Request
    """
    Apply the ``X-WPS-Output-Context`` for saving outputs in the user-context WPS-outputs directory.
    """
    header = get_header("X-WPS-Output-Context", request.headers)
    # if explicitly provided, ensure it is permitted (admin allow any, otherwise self-user reference only)
    if header is not None:
        if request.user is None:
            header = "public"
        else:
            if not is_admin(request):
                # override disallowed writing to other location
                # otherwise, up to admin to have writen something sensible
                header = "user-" + str(request.user.id)
    else:
        if request.user is None:
            header = "public"
        else:
            header = "user-" + str(request.user.id)
    request.headers["X-WPS-Output-Context"] = header
    return request
