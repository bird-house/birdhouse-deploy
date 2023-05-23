# encoding: utf-8
"""
STAC API collection processor
-------------

Create a STAC collection or update its summaries based on its queryables.
"""
__author__ = "Mathieu Provencher"
__date__ = "20 Apr 2022"
__copyright__ = "Copyright 2022 Computer Research Institute of Montreal"
__license__ = "MIT"
__holder__ = "Computer Research Institute of Montreal (CRIM)"
__contact__ = "mathieu.provencher@crim.ca"

import requests
import os
import pystac
import datetime
import hashlib
import yaml
import sys


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class CollectionProcessor:
    """
    Create a STAC collection or update its summaries based on its queryables.
    """

    def __init__(self):
        filepath = sys.argv[1]
        collections = []

        with open(filepath) as file:
            document = yaml.full_load(file)

            for item, val in document.items():
                if item == "stac_host":
                    stac_host = val
                elif item == "collections":
                    collections = val

        for col in collections:
            self.process_collection(stac_host, col["name"], col["description"])

    def process_collection(self, stac_host, collection_name, collection_description):
        collection_id = hashlib.md5(
            collection_name.encode("utf-8")
        ).hexdigest()
        stac_collection = self.get_stac_collection(stac_host, collection_id)

        if stac_collection:
            # update collection
            stac_collection_queryables = self.get_stac_collection_queryables(stac_host, collection_id)
            stac_collection = self.update_stac_collection(stac_collection, stac_collection_queryables)
            self.post_collection(stac_host, stac_collection)
        else:
            # create collection
            default_collection = self.create_stac_collection(collection_id, collection_name, collection_description)
            self.post_collection(stac_host, default_collection)

    def get_stac_collection(self, stac_host, collection_id):
        """
        Get a STAC collection

        Returns the collection JSON.
        """
        r = requests.get(os.path.join(stac_host, "collections", collection_id))

        if r.status_code == 200:
            return r.json()

        return {}

    def get_stac_collection_queryables(self, stac_host, collection_id):
        """
        Get the queryables of a STAC collection.

        Returns the queryables JSON.
        """
        r = requests.get(os.path.join(stac_host, "collections", collection_id, "queryables"))

        if r.status_code == 200:
            return r.json()

        return {}

    def update_stac_collection(self, stac_collection, stac_collection_queryables):
        """
        Update a STAC collection with summaries obtain by queryables.

        Returns the collection with updated summaries.
        """
        summaries = {}

        for k, v in stac_collection_queryables["properties"].items():
            summaries[k] = v["enum"]

        stac_collection["summaries"] = summaries

        return stac_collection

    def create_stac_collection(self, collection_id, collection_name, collection_description):
        """
        Create a basic STAC collection.

        Returns the collection.
        """

        sp_extent = pystac.SpatialExtent([[-140.99778, 41.6751050889, -52.6480987209, 83.23324]])
        capture_date = datetime.datetime.strptime('2015-10-22', '%Y-%m-%d')
        end_capture_date = datetime.datetime.strptime('2100-10-22', '%Y-%m-%d')
        tmp_extent = pystac.TemporalExtent([(capture_date, end_capture_date)])
        extent = pystac.Extent(sp_extent, tmp_extent)

        collection = pystac.Collection(id=collection_id,
                                       title=collection_name,
                                       description=collection_description,
                                       extent=extent,
                                       keywords=[
                                           "climate change",
                                           "CMIP5",
                                           "WCRP",
                                           "CMIP"
                                       ],
                                       providers=None,
                                       summaries=pystac.Summaries({"needs_summaries_update": ["true"]}))

        return collection.to_dict()

    def post_collection(self, stac_host, json_data):
        """
        Post a STAC collection.

        Returns the collection id.
        """
        collection_id = json_data['id']
        r = requests.post(os.path.join(stac_host, "collections"), json=json_data)

        if r.status_code == 200:
            print(f"{bcolors.OKGREEN}[INFO] Pushed STAC collection [{collection_id}] to [{stac_host}] ({r.status_code}){bcolors.ENDC}")
        elif r.status_code == 409:
            print(f"{bcolors.WARNING}[INFO] STAC collection [{collection_id}] already exists on [{stac_host}] ({r.status_code}), updating..{bcolors.ENDC}")
            r = requests.put(os.path.join(stac_host, "collections"), json=json_data)
            r.raise_for_status()
        else:
            r.raise_for_status()

        return collection_id


if __name__ == "__main__":
    CollectionProcessor()
