import requests
import pandas as pd


BASE_URL = "https://api.nb.no/ngram/db2"

pd.options.display.max_rows = 100

def document_corpus(doctype = None, author = None,  from_year = None, to_year = None, title = None, ddk = None, subject = None, lang = None, limit = None):
    """ Fetch a corpus based on metadata - doctypes are digibok, digavis, digitidsskrift"""
    
    parms = locals()
    params = {x:parms[x] for x in parms if not parms[x] is None }
    
    if "ddk" in params:
        params["ddk"]  = params['ddk'].replace('.', '"."')
        
    r=requests.post(BASE_URL + "/build_corpus", json=params)
    
    return pd.DataFrame(r.json(), columns = ['urn', 'author', 'title','year'])
    

    
def concordance(urns = None, words = None, window = 25, limit = 100):
    if words is None:
        return {}
    else:
        params = {
            'urns': urns,
            'query': words,
            'window': window,
            'limit': limit
        }
        r = requests.post(BASE_URL + "/conc", json = params)
    return pd.DataFrame(r.json())
    
def konkordans(urns = None, query = None, window = 25, limit = 100):
    if query is None:
        return {}
    else:
        params = {
            'urns': urns,
            'query': query,
            'window': window,
            'limit': limit
        }
        r = requests.post(BASE_URL + "/conc", json = params)
    return pd.DataFrame(r.json())

def collocation(corpusquery = 'norge', word = 'arbeid', before = 5, after = 0):
    params = {
        'corpusquery': corpusquery,
        'word': word,
        'before': before,
        'after': after
    }
    r = requests.post(BASE_URL + "/urncolldist", json = params)
    return pd.read_json(r)

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
        r = requests.post(BASE_URL + "/conc_loop", json = params)
    return r.json()
