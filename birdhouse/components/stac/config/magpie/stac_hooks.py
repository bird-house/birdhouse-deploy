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
import logging
import re
from typing import TYPE_CHECKING

from magpie.api.management.resource import resource_utils as ru
from magpie.api.requests import get_service_matchdict_checked
from magpie.models import Route, Service
from magpie.utils import get_logger
from magpie.db import get_session_from_other

if TYPE_CHECKING:
    from pyramid.request import Request
    from pyramid.response import Response

LOGGER = get_logger("magpie.stac", level=logging.DEBUG)

def create_collection_resource(response):
    # type: (Response) -> Response
    """
    Create the stac collection resource
    """
    request = response.request
    body = request.json
    collection_id = body["id"]
    display_name = extract_display_name(body["links"])

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
                    # find the nested resource id matching: "stac/stac/collections"
                    if stac_child["node"].resource_name == "collections":
                        collection_res_id = stac_child["node"].resource_id
                        collection_res_create = False
                        break

        # create resource /stac/stac/collections if does not exist
        if collection_res_create:
            collection_res = ru.create_resource("collections", None, Route.resource_type_name, stac_res_id, db_session=session)
            collection_res_id = collection_res.json["resource"]["resource_id"]

        # create resource /stac/stac/collections/<collection_id>
        # In try catch since Magpie resource are persistent but stac-db could be wiped
        try:
            collection = ru.create_resource(collection_id, display_name, Route.resource_type_name, collection_res_id, db_session=session)
        except Exception as exc:
            LOGGER.warning("Failed creation of the collection %s %s", collection_id, str(exc), exc_info=exc)

        session.commit()   
   
    except Exception as exc:
        LOGGER.error("Unexpected error while creating the collection %s", str(exc), exc_info=exc)
    
    return response

def create_item_resource(response):
    # type: (Response) -> Response
    """
    Create the stac item resource
    """
    request = response.request
    body = request.json
    item_id = body["id"]
    display_name = extract_display_name(body["links"])

    # Get the <collection_id> from url -> /collections/{collection_id}/items
    collection_id = re.search(r'(?<=collections\/).*?(?=\/items)', request.url).group()

    # note: matchdict reference of Twitcher owsproxy view is used, just so happens to be same name as Magpie
    service = get_service_matchdict_checked(request)
    try:
        # Getting a new session from the request
        session = get_session_from_other(request.db)
        children = ru.get_resource_children(service, db_session=session, limit_depth=5)
        item_res_create = True
        # find "stac/stac"
        for childs in children.values():
            if childs["node"].resource_name == "stac":
                # find "stac/stac/collections"
                for stac_child in childs["children"].values():
                    if stac_child["node"].resource_name == "collections":
                        # find the id of the resource matching stac/stac/collections/<collection_id>
                        for collection_child in stac_child["children"].values():
                            if collection_child["node"].resource_name == collection_id:
                                collection_res_id = collection_child["node"].resource_id
                                # find the id of the resource matching stac/stac/collections/<collection_id>/items
                                for item_child in collection_child["children"].values():
                                    if item_child["node"].resource_name == "items":
                                        item_res_id = item_child["node"].resource_id
                                        item_res_create = False
                                        break

        # create resource /stac/stac/collections/<collection_id>/items if does not already exist
        if item_res_create:
            item_res = ru.create_resource("items", None, Route.resource_type_name, collection_res_id, db_session=session)
            item_res_id = item_res.json["resource"]["resource_id"]

        # create resource stac/stac/collection/<collection_id>/items/<item_id>
        # In try catch since Magpie resource are persistent but stac-db could be wiped
        try:
            item_res = ru.create_resource(item_id, display_name, Route.resource_type_name, item_res_id, db_session=session)
        except Exception as exc:
            LOGGER.warning("Failed creation of the item %s %s", display_name, str(exc), exc_info=exc)
        session.commit()   
   
    except Exception as exc:
        LOGGER.error("Unexpected error while creating the item %s %s", display_name, str(exc), exc_info=exc)
    
    return response

def extract_display_name(links):
    # type: (JSON array) -> string
    """
    Extract THREDD path from a STAC links
    """
    display_name = None
    for link in links:
        if link["rel"] == "source":
            # Example of title `thredds:birdhouse/CMIP6` -> `birdhouse/CMIP6`
            display_name = link["title"].split(":")[1]
            break

    return display_name 
