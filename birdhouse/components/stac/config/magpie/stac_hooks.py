#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
These hooks will be running within Twitcher, using MagpieAdapter context, applied for STAC requests.

The code below can make use of any package that is installed by Magpie/Twitcher.

.. seealso::
    Documentation about Magpie/Twitcher request/response hooks is available here:
    https://pavics-magpie.readthedocs.io/en/latest/configuration.html#service-hooks
"""

import re
from typing import TYPE_CHECKING, List, Dict

from magpie.api.management.resource import resource_utils as ru
from magpie.api.requests import get_service_matchdict_checked
from magpie.models import Route
from magpie.utils import get_logger
from magpie.db import get_session_from_other
from ziggurat_foundations.models.services.resource import ResourceService

if TYPE_CHECKING:
    from pyramid.response import Response
    from sqlalchemy.orm.session import Session

LOGGER = get_logger("magpie.stac")

def create_collection_resource(response):
    # type: (Response) -> Response
    """
    Create the stac collection resource
    """
    request = response.request
    body = request.json
    collection_id = body["id"]
    try:
        display_name = extract_display_name(body["links"])
    except Exception as exc:
        LOGGER.error("Error when extracting display_name from links %s %s", body["links"], str(exc), exc_info=exc)
        return response

    # note: matchdict reference of Twitcher owsproxy view is used, just so happens to be same name as Magpie
    service = get_service_matchdict_checked(request)
    # Getting a new session from the request, since the current session found in the request is already handled with his own transaction manager.
    session = get_session_from_other(request.db)
    try:
        # Create the resource tree
        create_resource_tree(f"stac/collections/{collection_id}", 0, service.resource_id , session, display_name)
        session.commit()

    except Exception as exc:
        LOGGER.error("Unexpected error while creating the collection %s %s", display_name, str(exc), exc_info=exc)
        session.rollback() 

    return response

def create_item_resource(response):
    # type: (Response) -> Response
    """
    Create the stac item resource
    """
    request = response.request
    body = request.json
    item_id = body["id"]
    try:
        display_name = extract_display_name(body["links"])
    except Exception as exc:
        LOGGER.error("Error when extracting display_name from links %s %s", body["links"], str(exc), exc_info=exc)
        return response

    # Get the <collection_id> from url -> /collections/{collection_id}/items
    collection_id = re.search(r'(?<=collections/)[0-9a-zA-Z_.-]+?(?=/items)', request.url).group()

    # note: matchdict reference of Twitcher owsproxy view is used, just so happens to be same name as Magpie
    service = get_service_matchdict_checked(request)
    # Getting a new session from the request, since the current session found in the request is already handled with his own transaction manager.
    session = get_session_from_other(request.db)
    try:
        # Create the resource tree
        create_resource_tree(f"stac/collections/{collection_id}/items/{item_id}", 0, service.resource_id, session, display_name)
        session.commit()

    except Exception as exc:
        LOGGER.error("Unexpected error while creating the item %s %s", display_name, str(exc), exc_info=exc)
        session.rollback()

    return response

def extract_display_name(links):
    # type: (List[Dict[str, str]]) -> str
    """
    Extract THREDD path from a STAC links
    """
    display_name = None
    for link in links:
        if link["rel"] == "source":
            # Example of title `thredds:birdhouse/CMIP6`
            display_name = link["title"]
            break
    if not display_name:
        raise ValueError("The display name was not extracted properly")

    return display_name 

def create_resource_tree(resource_tree, current_depth, parent_id, session, display_name):
    # type: (str, int, int, session, str) -> None 
    """
    Create the resource tree on Magpie
    """
    tree = resource_tree.split("/")
    # We are at the max depth of the tree.
    if current_depth > len(tree) - 1:
        return 

    resource_name = tree[current_depth]
    query = session.query(ResourceService.model).filter(ResourceService.model.resource_name == resource_name, ResourceService.model.parent_id == parent_id)
    resource = query.first()

    if resource is not None:
        # Since the resource exists, we can use its id to create the next resource.
        parent_id = resource.resource_id
        next_depth = current_depth + 1
        create_resource_tree(resource_tree, next_depth, parent_id, session, display_name)

    # The resource wasn't found in the current depth, we need to create it.
    else:
        # Creating the last resource in the tree, we need to use the display_name.
        if current_depth == len(tree) - 1:
            ru.create_resource(resource_name, display_name, Route.resource_type_name, parent_id, db_session=session)
        else:
            # Creating the resource somewhere in the middle of the tree before using its id.
            node = ru.create_resource(resource_name, None, Route.resource_type_name, parent_id, db_session=session)
            parent_id = node.json["resource"]["resource_id"]
            next_depth = current_depth + 1
            create_resource_tree(resource_tree, next_depth, parent_id, session, display_name)
