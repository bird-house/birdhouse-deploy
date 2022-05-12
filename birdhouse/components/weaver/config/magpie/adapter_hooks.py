#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyramid.request import Request

    from magpie.typedefs import ServiceConfigItem


def add_x_wps_output_context(request, service):
    # type: (Request, ServiceConfigItem) -> Request
    if "application/json" in request.content_type:
        body = request.json  # JSON generated from body, cannot override directly
        # following for testing purposes only
        body["hooks"] = len(service["hooks"])
        body["hook"] = "add_x_wps_output_context"
        request.body = json.dumps(body).encode()
    if request.user is not None:
        request.headers["X-WPS-Output-Context"] = "user-" + str(request.user.id)
    return request
