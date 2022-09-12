import pandas as pd
import requests
from typing import List

from dhlab.constants import BASE_URL


def get_metadata(urns: List = None):
    """Fetch metadata from a list of urns.

    :param list urns: uniform resource names, example: ``["URN:NBN:no-nb_digibok_2011051112001", ...]``
    """
    params = locals()
    r = requests.post(f"{BASE_URL}/get_metadata", json=params)
    return pd.DataFrame(r.json())
