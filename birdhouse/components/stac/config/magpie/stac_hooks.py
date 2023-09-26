#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
These hooks will be running within Twitcher, using MagpieAdapter context, applied for Stac requests.

The code below can make use of any package that is installed by Magpie/Twitcher.

.. seealso::
    Documentation about Magpie/Twitcher request/response hooks is available here:
    https://pavics-magpie.readthedocs.io/en/latest/configuration.html#service-hooks
"""

import json
from typing import TYPE_CHECKING

from magpie.api.management.resource import resource_utils as ru
from magpie.api.management.user import user_utils as uu
from magpie.api.requests import get_user, get_service_matchdict_checked
from magpie.constants import get_constant
from magpie.models import Route, Service
from magpie.register import magpie_register_permissions_from_config
from magpie.permissions import Access, Permission, PermissionSet, Scope
from magpie.utils import get_header, get_logger
from magpie.constants import MAGPIE_LOG_LEVEL
from magpie.db import get_session_from_other
import logging

if TYPE_CHECKING:
    from pyramid.request import Request
    from pyramid.response import Response

LOGGER = get_logger("magpie.stac",level=logging.DEBUG)

def create_collection_resource(response):
    # type: (Response) -> Response
    """
    Create the stac collection resource
    """
    request = response.request
    body = request.json
    collection_id = body['id']
    # note: matchdict reference of Twitcher owsproxy view is used, just so happens to be same name as Magpie
    service = get_service_matchdict_checked(request)
    try:
        # Getting a new session from the request
        session = get_session_from_other(request.db)
        children = ru.get_resource_children(service, db_session=session, limit_depth=2)
        collection_res_create = True
        # find the nested resource id matching: "stac/stac"
        for childs in children.values():
            if childs["node"].resource_name == "stac":
                stac_res_id = childs["node"].resource_id
                for stac_child in childs["children"].values():
                    # find the nested resource id matching: "stac/stac/collection"
                    if stac_child["node"].resource_name == "collections":
                        collection_res_id = stac_child["node"].resource_id
                        collection_res_create = False

        # create /stac/stac/collections if does not exist
        if collection_res_create:
            collection_res = ru.create_resource("collections", None, Route.resource_type_name, stac_res_id, db_session=session)
            collection_res_id = collection_res.json["resource"]["resource_id"]

        # create /stac/stac/collections/<collection_id>
        collection = ru.create_resource(collection_id, None, Route.resource_type_name, collection_res_id, db_session=session)
        session.commit()   
   
    except Exception as exc:
        LOGGER.error("Failed creation of resource %s", str(exc), exc_info=exc)
    
    return response
