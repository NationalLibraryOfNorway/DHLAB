"""Tools for querying the Norwegian National Bibliography Marc 21
"""
import os
import requests
from dhlab.constants import BASE_URL


def api_call_deco(service):
    """Decorator for calling a service from DH-lab API

    :param service: Name of service
    
    """

    def inner_decorator(func):
        """Inner decorator

        :param func: function to decorate. Must return params
        """

        def wrapper(*args, **kwargs):
            params = func(*args, **kwargs)
            return requests.post(os.path.join(BASE_URL, service), json=params).json()

        return wrapper

    return inner_decorator


@api_call_deco("metadata_query")
def metadata_query(conditions, limit=5):
    """Query the Norwegian National Bibliography using Marc 21 fields and values
    
    Example:
    conditions = [
        ["245", "a", "kongen"],
        ["008", "", "nno"]
        ]

    :param conditions: Marc 21 fields and values to search for
    :type conditions: list of lists
    :param limit: number of records to return, defaults to 5
    :type limit: int, optional
    :return: list of urns
    :rtype: json
    """
    params = {"conditions": conditions, "limit": limit}
    return params


@api_call_deco("metadata_from_urn")
def metadata_from_urn(urns, fields=None):
    """Gets MARC 21 json for a URN or list of URN

    :param urns: list of URNs
    :param fields: list of marc 21 fields to return
    :return: API call parameters
    """
    params = {"urns": urns, "fields": fields}
    return params


## Utility

def pretty_print_marc21json(record):
    """Prints a record from the Norwegian National Bibliography in a readable format
    
    :param record: Marc 21 record in json format
    """
    
    
    print("Record:")
    for field in record["fields"]:
        for key, val in field.items():
            if "subfields" in val:
                print(key + ":")
                for subfield in val["subfields"]:
                    for subfield_k, subfield_val in subfield.items():
                        print("\t" +subfield_k + ": " + subfield_val)                    
            else:
                print(key + ": " + val)
    print()
