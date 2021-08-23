import requests
import pandas as pd


BASE_URL = "https://api.nb.no/ngram/db2"
BASE_URL1 = "https://api.nb.no/ngram/db1"

pd.options.display.max_rows = 100


def ngram_book(word = ['.'], title = None, period = None, publisher = None, lang=None, city = None, ddk = None, topic = None):
    """Get a time series for a word as string, title is name of book period is (year, year), lang is three letter iso code.
    Use % as wildcard where appropriate - no wildcards in word and lang"""
    params = locals()
    if isinstance(word, str):
        # assume a comma separated string
        word = [w.strip() for w in word.split(',')]
    params['word'] = tuple(word)
    params = {x:params[x] for x in params if not params[x] is None}
    r = requests.post(BASE_URL1 + "/ngram_book", json = params)
    #print(r.status_code)
    df = pd.DataFrame.from_dict(r.json(), orient = 'index')
    df.index = df.index.map(lambda x: tuple(x.split()))
    columns = df.index.levels[0]
    df = pd.concat([df.loc[x] for x in columns], axis = 1)
    df.columns = columns 
    #df.index = df.index.map(pd.Timestamp)
    return df

def ngram_news(word = ['.'], title = None, period = None):
    """ get a time series period is a tuple of (year, year), (yearmonthday, yearmonthday) 
    word is string and title is the title of newspaper, use % as wildcard"""
    params = locals()
    if isinstance(word, str):
        # assume a comma separated string
        word = [w.strip() for w in word.split(',')]
    params['word'] = tuple(word)
    params = {x:params[x] for x in params if not params[x] is None}
    r = requests.post(BASE_URL1 + "/ngram_newspapers", json = params)
    #print(r.status_code)
    df = pd.DataFrame.from_dict(r.json(), orient = 'index')
    df.index = df.index.map(lambda x: tuple(x.split()))
    columns = df.index.levels[0]
    df = pd.concat([df.loc[x] for x in columns], axis = 1)
    df.columns = columns
    #df.index = df.index.map(pd.Timestamp)
    return df


def document_corpus(doctype = None, author = None,  from_year = None, to_year = None, title = None, ddk = None, subject = None, lang = None, limit = None):
    """ Fetch a corpus based on metadata - doctypes are digibok, digavis, digitidsskrift"""
    
    parms = locals()
    params = {x:parms[x] for x in parms if not parms[x] is None }
    
    if "ddk" in params:
        params["ddk"]  = params['ddk'].replace('.', '"."')
        
    r=requests.post(BASE_URL + "/build_corpus", json=params)
    
    return pd.DataFrame(r.json(), columns = ['urn', 'author', 'title','year'])
    
def urn_collocation(urns = None, word = 'arbeid', before = 5, after = 0, samplesize = 200000):
    """ Create a collocation from a list of URNs - returns distance (sum of distances and bayesian distance) and frequency"""
    params = {
        'urn': urns,
        'word': word,
        'before': before,
        'after': after,
        'samplesize': samplesize
    }
    r = requests.post(BASE_URL1 + "/urncolldist_urn", json = params)
    return pd.read_json(r.text)

def totals(n = 50000):
    """ Get total frequencies of words in database"""
    
    r = requests.get(BASE_URL + "/totals/{n}".format(n = n))
    return pd.DataFrame.from_dict(dict(r.json()),orient = 'index', columns = ['freq'])
    
def concordance(urns = None, words = None, window = 25, limit = 100):
    """ Get a list of concordances from database, words is an fts5 string search expression"""
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
        'metadata_query': corpusquery,
        'word': word,
        'before': before,
        'after': after
    }
    r = requests.post(BASE_URL1 + "/urncolldist", json = params)
    return pd.read_json(r.text)


