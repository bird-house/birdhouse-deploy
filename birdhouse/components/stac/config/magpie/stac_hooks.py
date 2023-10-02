#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
These hooks will be running within Twitcher, using MagpieAdapter context, applied for STAC requests.

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

LOGGER = get_logger("magpie.stac")

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
        # Getting a new session from the request, since the current session found in the request is already handled with his own transaction manager.
        session = get_session_from_other(request.db)
        children = ru.get_resource_children(service, db_session=session, limit_depth=3)
        # Create the resource tree
        create_resource_tree(f"stac/collections/{collection_id}", children, 0, service.resource_id , session, display_name)
        session.commit()

    except Exception as exc:
        LOGGER.error("Unexpected error while creating the collection ", str(exc), exc_info=exc)
        session.rollback() 
        return response

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
        # Getting a new session from the request, since the current session found in the request is already handled with his own transaction manager.
        session = get_session_from_other(request.db)
        children = ru.get_resource_children(service, db_session=session, limit_depth=5)
        # Create the resource tree
        create_resource_tree(f"stac/collections/{collection_id}/items/{item_id}", children, 0, service.resource_id, session, display_name)
        session.commit()

    except Exception as exc:
        LOGGER.error("Unexpected error while creating the item %s %s", display_name, str(exc), exc_info=exc)
        session.rollback()
        return response

    return response

def extract_display_name(links):
    # type: (List[Dict[str, str]]) -> str
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

def create_resource_tree(resource_tree, nodes, current_depth, parent_id, session, display_name):
    # type: (str, OrderedDict, int, int, session, str) -> None 
    """
    Create the resource tree on Magpie
    """
    tree = resource_tree.split("/")
    # We are at the max depth of the tree , return
    if current_depth > len(tree) - 1:
        return 

    # The current resource to find/create.
    resource = tree[current_depth]

    create_resource = True
    for childs in nodes.values():
        # Find the resource in the curent childrens
        if childs["node"].resource_name == resource:
            children = childs["children"]
            # Since the resource exist, we can use it's id to create the next resource.
            parent_id = childs["node"].resource_id
            next_depth = current_depth + 1
            return create_resource_tree(resource_tree, children, next_depth, parent_id, session, display_name)
            create_resource = False
            break

    # The resource wasn't found in the current depth, we need to create it.
    if create_resource:
        # Creating the last resource in the tree, we need to use the display_name.
        if current_depth == len(tree) - 1:
            ru.create_resource(resource, display_name, Route.resource_type_name, parent_id, db_session=session)
            return
        else:
            # Creating a resource somewhere in the middle of the tree, we need to create it before using it's id.
            node = ru.create_resource(resource, None, Route.resource_type_name, parent_id, db_session=session)
            parent_id = node.json["resource"]["resource_id"]
            next_depth = current_depth + 1
            create_resource_tree(resource_tree, nodes, next_depth, parent_id, session, display_name)

    return 
