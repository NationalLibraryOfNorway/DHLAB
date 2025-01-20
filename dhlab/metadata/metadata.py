"""Retrieve metadata from objects in the digital archive."""
from typing import List, Optional

import pandas as pd
import requests

from dhlab.constants import BASE_URL


def get_metadata(urns: Optional[List] = None):
    """Fetch metadata from a list of urns.

    Args:
        urns: uniform resource names, example:
            `["URN:NBN:no-nb_digibok_2011051112001"]`
    """
    params = {"urns": urns}
    r = requests.post(f"{BASE_URL}/get_metadata", json=params)
    return pd.DataFrame(r.json())
