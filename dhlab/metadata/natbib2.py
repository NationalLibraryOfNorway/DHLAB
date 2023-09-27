"Query service for natbib metadata"


import requests


class QueryBuilder:
    """Query builder for the metadata_query2 service.

    This service allows for querying the Norwegian National Bibliography using Marc 21 fields and values.

    Example of usage:
    builder = QueryBuilder()
    result = (builder.add_field("field1", "subfield1", "value1")
          .add_field("field2", "subfield2", "value2")
          .set_return_fields("returnField1", "returnField2", "returnField3")
          .set_limit(1000)
          .post())

    """

    endpoint = (
        "https://api.nb.no/dhlab/metadata_query2" 
    )

    def __init__(self):
        self.query = {"fields": [], "returnFields": [], "limit": None}

    def add_field(self, field, subfield=None, value=None):
        """Add a field constraint to the query.

        Should be field + value for marc21 without subfields (<11) and field + subfield + value for marc21 with subfields (>=11
        """
        field_entry = {"field": field}
        if subfield:
            field_entry["subfield"] = subfield
        if value:
            field_entry["value"] = value
        self.query["fields"].append(field_entry)
        return self

    def set_return_fields(self, *fields):
        "Specify which fields to return in the response."
        self.query["returnFields"] = list(fields)
        return self

    def set_limit(self, limit):
        "Specify the maximum number of records to return."
        self.query["limit"] = limit
        return self

    def build(self):
        "Build the query."
        # Remove optional keys if they are not set
        if not self.query["returnFields"]:
            del self.query["returnFields"]
        if self.query["limit"] is None:
            del self.query["limit"]
        return self.query

    def post(self):
        "Post the query to the service and return the response."
        constructed_query = self.build()
        response = requests.post(self.endpoint, json=constructed_query)
        return response.json()
