import requests
import pandas as pd
import json
import networkx as nx

BASE_URL = "https://api.nb.no/dhlab"
BASE_URL1 = "https://api.nb.no/dhlab"

pd.options.display.max_rows = 100


import re

# convert cell to a link
def make_link(row):
        r = "<a target='_blank' href = 'https://urn.nb.no/{x}'>{x}</a>".format(x = str(row))
        return r

# find hits a cell
find_hits = lambda x: ' '.join(re.findall("<b>(.+?)</b", x))

# fetch metadata

def get_metadata(urns = None):
    """ Fetch metadata from a list of urns """
    params = locals()
    r = requests.post(f"{BASE_URL}/get_metadata", json = params)
    return r.json()


# class for displaying concordances
class Concordance:
    """Wrapper for concordance function with added functionality"""
    def __init__(self, corpus, query):
        self.concordance = concordance(urns = list(corpus.urn), words = query)
        self.concordance['link'] = self.concordance.urn.apply(make_link)
        self.concordance = self.concordance[['link', 'urn', 'conc']]
        self.concordance.columns = ['link', 'urn', 'concordance']
        self.corpus = corpus
        self.size = len(self.concordance)
    
    def show(self, n = 10, style = True):
        if style:
            result =  self.concordance.sample(min(n, self.size))[['link', 'concordance']].style
        else:
            result =  self.concordance.sample(min(n, self.size))
        return result
    
class Cooccurence():
    """Collocations """
    def __init__(self, corpus = None, words = None, before = 10, after = 10, reference = None):
        if isinstance(words, str):
            words = [words]
        coll = pd.concat([urn_collocation(urns = list(corpus.urn), word = w, before = before, after = after) for w in words])[['counts']]
        self.coll = coll.groupby(coll.index).sum()
        self.reference = reference
        self.before = before
        self.after = after
        
        if reference is not None:
            self.coll['relevance'] = (self.coll.counts/self.coll.counts.sum())/(self.reference.freq/self.reference.freq.sum())
    
    def show(self, sortby = 'counts', n = 20):
        return self.coll.sort_values(by = sortby, ascending = False)
    
    def keywordlist(self, top = 200, counts = 5, relevance = 10):
        mask = self.coll[self.coll.counts > counts]
        mask = mask[mask.relevance > relevance]
        return list(mask.sort_values(by = 'counts', ascending = False).head(200).index)
    
class Ngram():
    def __init__(self, words = None, from_year = None, to_year = None, doctype = None, lang = 'nob'):
        from datetime import datetime
        
        self.date = datetime.now()
        if to_year is None:
            to_year = self.date.year
        if from_year is None:
            from_year = 1950
            
        self.from_year = from_year
        self.to_year = to_year
        self.words = words
        self.lang = lang
        if not doctype is None:
            doctype = 'bok'
            if 'bok' in doctype:
                doctype = 'bok'
            elif 'avis' in doctype:
                doctype = 'avis'
        else:
            doctype = 'bok'
        ngrm = d2.nb_ngram(terms = ', '.join(words), corpus = doctype, years = (from_year, to_year))
        ngrm.index = ngrm.index.astype(str)
        self.ngram = ngrm
        return None

    def plot(self, **kwargs):
        self.ngram.plot( **kwargs)
    
    def compare(self, another_ngram):
        from datetime import datetime
        start_year = max(datetime(self.from_year,1,1), datetime(another_ngram.from_year,1,1)).year
        end_year = min(datetime(self.to_year,1,1), datetime(another_ngram.to_year,1,1)).year
        compare =  (self.ngram.loc[str(start_year):str(end_year)].transpose()/another_ngram.ngram[str(start_year):str(end_year)].transpose().sum()).transpose()
        return compare

class Ngram_book(Ngram):
    """"""

    def __init__(self, words = None, title = None, publisher = None, city = None, lang = 'nob', from_year = None, to_year = None, ddk = None, subject = None):
        from datetime import datetime

        
        self.date = datetime.now()
        if to_year is None:
            to_year = self.date.year
        if from_year is None:
            from_year = 1950
        self.from_year = from_year
        self.to_year = to_year
        self.words = words
        self.title = title
        self.publisher = publisher
        self.city = city
        self.lang = lang
        self.ddk = ddk
        self.subject = subject
        self.ngram = d2.ngram_book(word = words, title = title, publisher = publisher, lang = lang,city = city, period = (from_year, to_year), ddk = ddk, topic = subject)
        #self.cohort =  (self.ngram.transpose()/self.ngram.transpose().sum()).transpose()
        return None
    

    
class Ngram_news(Ngram):
        def __init__(self, words = None, title = None, city = None, from_year = None, to_year = None):
            from datetime import datetime


            self.date = datetime.now()
            if to_year is None:
                to_year = self.date.year
            if from_year is None:
                from_year = 1950
            self.from_year = from_year
            self.to_year = to_year
            self.words = words
            self.title = title
            self.ngram = d2.ngram_news(word = words, title = title, period = (from_year, to_year))
            #self.cohort =  (self.ngram.transpose()/self.ngram.transpose().sum()).transpose()
            return None

def get_reference(corpus = 'digavis', from_year = 1950, to_year = 1955, lang = 'nob', limit = 100000):
    params = locals()
    r = requests.get(BASE_URL + "/reference_corpus", params = params)
    if r.status_code == 200:
        result = r.json()
    else:
        result = []
    return pd.DataFrame(result, columns = ['word', 'freq']).set_index('word')

def find_urns(docids = None, mode = 'json'):
    """ Return a list of URNs from a list of docids as a dictionary {docid: URN} or as a pandas dataframe"""
    
    params = locals()
    r = requests.post(BASE_URL1 + "/find_urn", json = params)
    if r.status_code == 200:
        res = pd.DataFrame.from_dict(r.json(), orient = 'index', columns = ['urn'])
    else:
        res = pd.DataFrame()
    return res

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

def ngram_periodicals(word = ['.'], title = None, period = None, publisher = None, lang=None, city = None, ddk = None, topic = None):
    """Get a time series for a word as string, title is name of periodical period is (year, year), lang is three letter iso code.
    Use % as wildcard where appropriate - no wildcards in word and lang"""
    params = locals()
    if isinstance(word, str):
        # assume a comma separated string
        word = [w.strip() for w in word.split(',')]
    params['word'] = tuple(word)
    params = {x:params[x] for x in params if not params[x] is None}
    r = requests.post(BASE_URL1 + "/ngram_periodicals", json = params)
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

def get_document_frequencies(urns = None, cutoff = 0):
    params = locals()
    r = requests.post(BASE_URL1 + "/frequencies", json = params)
    result = r.json()
    structure = {u[0][0] : dict([tuple(x[1:]) for x in u]) for u in result if u != []}
    df = pd.DataFrame(structure)
    return df.sort_values(by = df.columns[0], ascending = False)

def get_document_corpus(**kwargs):
    return document_corpus(**kwargs)

def document_corpus(doctype = None, author = None, freetext = None, from_year = None, to_year = None, from_timestamp = None, to_timestamp = None, title = None, ddk = None, subject = None, lang = None, limit = None):
    """ Fetch a corpus based on metadata - doctypes are digibok, digavis, digitidsskrift"""
    
    parms = locals()
    params = {x:parms[x] for x in parms if not parms[x] is None }
    if "ddk" in params:
        params["ddk"]  = "^" + params['ddk'].replace('.', '"."')
        
    r=requests.post(BASE_URL + "/build_corpus", json=params)
    
    return pd.DataFrame(r.json())
    
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

def concordance_counts(urns = None, words = None, window = 25, limit = 100):
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
        r = requests.post(BASE_URL + "/conccount", json = params)
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



### -------------------------- NB ngram ------------------ ###

def nb_ngram(terms, corpus='bok', smooth=3, years=(1810, 2010), mode='relative'):
    df = ngram_conv(get_ngram(terms, corpus=corpus), smooth=smooth, years=years, mode=mode)
    df.index = df.index.astype(int)
    return df

def get_ngram(terms, corpus='avis'):
    req = requests.get(
        "https://beta.nb.no/dhlab/ngram_1/ngram/query?", 
        params = { 
            'terms':terms,
            'corpus':corpus
        }
    )
    if req.status_code == 200:
        res = req.text
    else:
        res = "[]"
    return json.loads(res)

def ngram_conv(ngrams, smooth=1, years=(1810,2013), mode='relative'):
    ngc = {}
    # check if relative frequency or absolute frequency is in question
    if mode.startswith('rel') or mode=='y':
        arg = 'y'
    else:
        arg = 'f'
    for x in ngrams:
        if x != []:
            ngc[x['key']] = {z['x']:z[arg] for z in x['values'] if int(z['x']) <= years[1] and int(z['x']) >= years[0]}
    return pd.DataFrame(ngc).rolling(window=smooth, win_type='triang').mean()


def make_word_graph(words, corpus = 'all', cutoff = 16, leaves = 0):
    """Get galaxy from ngram-database. 
    corpus is bok, avis or both
    words is a commaseparated string
    English and German provided by Google N-gram. 
    Set leaves=1 to get the leaves. Parameter cutoff only works for lang='nob'. 
    Specify English by setting lang='eng' and German by lang='ger'"""
    
    params = dict()
    params['terms'] = words
    params['corpus'] = corpus
    params['limit'] = cutoff
    params['leaves'] = leaves
    result = requests.get("https://beta.nb.no/dhlab/galaxies/query", params=params)
    G = nx.DiGraph()
    edgelist = []
    if result.status_code == 200:
        graph = json.loads(result.text)
        #print(graph)
        nodes = graph['nodes']
        edges = graph['links']
        for edge in edges:
            edgelist += [(nodes[edge['source']]['name'], nodes[edge['target']]['name'], abs(edge['value']))]
    #print(edgelist)
    G.add_weighted_edges_from(edgelist)

    return G