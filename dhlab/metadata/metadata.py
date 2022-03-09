import pandas as pd
import requests

from dhlab.constants import BASE_URL


def get_metadata(urns=None):
    """ Fetch metadata from a list of urns """
    params = locals()
    r = requests.post(f"{BASE_URL}/get_metadata", json=params)
    return pd.DataFrame(r.json())
