"""Tools for querying the Norwegian National Bibliography Marc 21"""

import os
from functools import wraps
from typing import List, Optional

import requests

from dhlab.constants import BASE_URL

import requests

from dhlab.constants import BASE_URL

# TODO: Add support for more fields


def _api_call_deco(service: str):
    """Decorator for calling a service from DH-lab API"""

    def inner_decorator(func):
        """
        Args:
            func: function to decorate. Must return params
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            params = func(*args, **kwargs)
            return requests.post(os.path.join(BASE_URL, service), json=params).json()

        return wrapper

    return inner_decorator


@_api_call_deco("metadata_query")
def metadata_query(conditions: List[list], limit: Optional[int] = 5) -> dict:
    """Query the Norwegian National Bibliography using Marc 21 fields and values

    Examples:
        >>> conditions = [["245", "a", "kongen"],["008", "", "nno"]]
        >>> metadata_query(conditions, limit=5)

    Args:
        conditions: Marc 21 fields and values to search
            for
        limit: number of records to return.

    Returns:
        a dict of the input parameters
    """
    params = {"conditions": conditions, "limit": limit}
    return params


@_api_call_deco("metadata_from_urn")
def metadata_from_urn(urns: list, fields: Optional[list] = None) -> dict:
    """Gets MARC 21 json for a URN or list of URN

    Args:
        urns: list of URNs
        fields: list of marc 21 fields to return

    Returns:
        API call parameters
    """
    params = {"urns": urns, "fields": fields}
    return params


## Utility


def pretty_print_marc21json(record: dict):
    """Prints a record from the Norwegian National Bibliography in a readable format

    Args:
        record: Marc 21 record in json format
    """

    print("Record:")
    for field in record["fields"]:
        for key, val in field.items():
            if "subfields" in val:
                print(key + ":")
                for subfield in val["subfields"]:
                    for subfield_k, subfield_val in subfield.items():
                        print("\t" + subfield_k + ": " + subfield_val)
            else:
                print(key + ": " + val)
    print()
