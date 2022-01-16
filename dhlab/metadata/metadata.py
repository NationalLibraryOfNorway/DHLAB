import requests
import pandas as pd
import json


BASE_URL = "https://api.nb.no/dhlab"

def get_metadata(urns = None):
    """ Fetch metadata from a list of urns """
    params = locals()
    r = requests.post(f"{BASE_URL}/get_metadata", json = params)
    return pd.DataFrame(r.json())
