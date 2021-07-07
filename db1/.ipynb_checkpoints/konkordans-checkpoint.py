import requests
import pandas as pd


baseurl = "https://api.nb.no/ngram/db2"

pd.options.display.max_rows = 100

def konkordans(urns=None, query = None, window = 25, limit = 100):
    if query is None:
        return {}
    else:
        params = {
            'urns': urns,
            'query': query,
            'window': window,
            'limit': limit
        }
        r = requests.post(baseurl + "/conc", json = params)
    return pd.DataFrame(r.json())


def konk_loop(urns=None, query = None, window = 25, limit = 100):
    if query is None:
        return {}
    else:
        params = {
            'urns': urns,
            'query': query,
            'window': window,
            'limit': limit
        }
        r = requests.post(baseurl + "/conc_loop", json = params)
    return r.json()