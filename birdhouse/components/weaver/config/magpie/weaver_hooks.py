#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
These hooks will be running within Twitcher, using MagpieAdapter context, applied for Weaver requests.

The code below can make use of any package that is installed by Magpie/Twitcher.
"""

import json
from typing import TYPE_CHECKING

from magpie.api.management.resource import resource_utils as ru
from magpie.api.requests import get_user
from magpie.constants import get_constant
from magpie.permissions import Access, Permission
from magpie.utils import get_header

if TYPE_CHECKING:
    from pyramid.request import Request
    from pyramid.response import Response

    from magpie.adapter import HookContext


def is_admin(request):
    # type: (Request) -> bool
    admin_group = get_constant("MAGPIE_ADMIN_GROUP", settings_container=request)
    if not request.user:  # no user authenticated (public)
        return False
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


def filter_allowed_processes(response, context):
    # type: (Response, HookContext) -> Response
    """
    Filter processes returned by Weaver response according to allowed resources by user.

    Following are sample (clipped) JSON body that can be expected from Weaver (or any OGC API - Processes).

    Using ``GET https://<weaver.url>/processes``

    .. code-block:: json
        :caption: Detailed process listing from Weaver (other fields than 'processes' are removed for concise example).

        {
          "processes": [
            {
              "id": "ColibriFlyingpigeon_SubsetBbox",
              "title": "ColibriFlyingpigeon_SubsetBbox",
              "mutable": true,
              "keywords": [
                "application"
              ],
              "metadata": [],
              "jobControlOptions": [
                "async-execute"
              ],
              "outputTransmission": [
                "reference",
                "value"
              ],
              "processDescriptionURL": "https://<weaver.url>/processes/ColibriFlyingpigeon_SubsetBbox",
              "processEndpointWPS1": "https://<weaver.url>/ows/wps",
              "executeEndpoint": "https://<weaver.url>/processes/ColibriFlyingpigeon_SubsetBbox/jobs"
            }
          ]
        }

    Using ``GET https://<weaver.url>/processes?detail=false``

    .. code-block:: json
        :caption: Simple process listing from Weaver (other fields than 'processes' are removed for concise example).

        {
          "description": "Listing of available processes successful.",
          "processes": [
            "CatFile",
            "ColibriFlyingpigeon_SubsetBbox",
          ],
          "page": 0,
          "total": 2
        }

    """
    if "application/json" in response.content_type:
        body = response.json
        if "processes" in body:
            if is_admin(response.request):  # don't waste time checking permissions, full access anyway
                return response

            # depending on 'detail' query, processes can be returned as list of IDs or nested JSON summaries
            processes = {
                proc if isinstance(proc, str) else proc.get("id"): proc
                for proc in body["processes"]
            }

            # only need 2 first levels ('processes' and each process 'id' under it)
            children = ru.get_resource_children(context.resource, response.request.db, limit_depth=2)
            proc_res = None
            for res in children.values():
                if res["node"].resource_name == "processes":
                    # if nothing under 'processes' resource, then guarantee no permissions, done check
                    if not res["children"]:
                        return response
                    proc_res = res
                    break
            if not proc_res:
                return response  # 'processes' itself does not exist, no permissions possible and done check

            allowed_processes = []
            known_processes = proc_res["children"].values()
            known_processes = {res["node"].resource_name: res for res in known_processes}
            request_user = get_user(response.request)
            for proc_name in processes:
                if proc_name not in known_processes:
                    continue  # do not bother checking missing resource
                child_proc = known_processes[proc_name]["node"]
                perms = context.service.effective_permissions(request_user, child_proc, [Permission.READ])
                if perms[0].access == Access.ALLOW:
                    proc = processes[proc_name]
                    allowed_processes.append(proc)

            # override collected and permitted processes access by user
            body["processes"] = allowed_processes

            # WARNING:
            #  JSON generated from 'body' attribute cannot be overridden directly (computed inline).
            #  Also, since we override, must set any Content header accordingly with modifications.
            data = json.dumps(body).encode("UTF-8")
            response.body = data
            c_len = len(data)
            response.content_length = c_len
            response.headers["Content-Length"] = str(c_len)

    return response
