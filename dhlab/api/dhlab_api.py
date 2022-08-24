import pandas as pd
import requests

from dhlab.constants import BASE_URL

pd.options.display.max_rows = 100

# fetch metadata

def ner_from_urn(urn=None, model=None):
    """Get a NER object for a text by URN using a spacy model
    :param urn: a URN
    :param model: a spacy model (check with show_model what is available)"""
    
    params = locals()
    r = requests.get(f"{BASE_URL}/ner_urn", params=params)
    df = pd.read_json(r.json())
    return df

def show_spacy_models():
    """Show available models for use with spaCy"""
    r = requests.get(f"{BASE_URL}/ner_models")
    return r.json()

def get_places(urn=None) -> pd.DataFrame:
    """
    .. todo:: Add description of functionality + parameters

    :param urn: Defaults to None.
    """
    params = locals()
    r = requests.post(f"{BASE_URL}/places", json=params)
    #print(r.status_code)
    return pd.DataFrame(r.json())


def geo_lookup(places, feature_class = None, feature_code = None, field = 'alternatename'):
    """From a list of places return their geolocations
    :param places: a list of place names - max 1000
    :param feature_class: which classe to return
    :param feature_code: which code to return
    :field: which name field to match - default alternatename
    """
    res = requests.post(f"{BASE_URL}/geo_data", json={'words':places, 'feature_class':feature_class, 'feature_code':feature_code, 'field':field})
    columns = ["geonameid", "name", "alternatename", "latitude", "longitude", "feature_class", "feature_code"]
    return pd.DataFrame(res.json(), columns = columns)

def get_dispersion(urn=None, words=None, window=None, pr=None) -> pd.Series:
    """
    .. todo:: Add description of functionality + parameters

    :param urn:
    :param words:
    :param window:
    :param pr:
    :return:
    """
    params = locals()
    r = requests.post(f"{BASE_URL}/dispersion", json=params)
    return pd.Series(r.json())
   

def get_metadata(urns=None) -> pd.DataFrame:
    """Fetch metadata from a list of urns."""
    params = locals()
    r = requests.post(f"{BASE_URL}/get_metadata", json=params)
    return pd.DataFrame(r.json())


def get_chunks(urn=None, chunk_size: int = 300) -> dict:
    """Fetch chunks as wordbags from a document urn.

    :param chunk_size: TODO: add description of parameter.
    """

    if urn is None:
        return {}
    r = requests.get(f"{BASE_URL}/chunks", params=locals())
    if r.status_code == 200:
        result = r.json()
    else:
        result = {}
    return result


def get_chunks_para(urn=None) -> dict:
    """Fetch chunks from document, one for each paragraph.

    :param urn: TODO: add description of parameter.
    """

    if urn is None:
        return {}
    r = requests.get(f"{BASE_URL}/chunks_para", params=locals())
    if r.status_code == 200:
        result = r.json()
    else:
        result = {}
    return result


def evaluate_documents(wordbags=None, urns=None):
    """From a list of urns and wordbag as dictionary, return an evaluation
    :param wordbags: a dictionary of wordlists
    :param urns: a list of URNs"""
    
    res = requests.post(f"{BASE_URL}/evaluate", json={'wordbags':wordbags, 'urns':urns})
    df = pd.DataFrame(res.json()).transpose()
    return df


def get_reference(
    corpus: str = 'digavis',
    from_year: int = 1950,
    to_year: int = 1955,
    lang: str = 'nob',
    limit: int = 100000
) -> pd.DataFrame:
    """
    .. todo:: Add description of functionality + parameters

    :param corpus:
    :param from_year:
    :param to_year:
    :param lang:
    :param limit:
    :return: A :py:class:`pd.DataFrame` with the results.
    """
    params = locals()
    r = requests.get(BASE_URL + "/reference_corpus", params=params)
    if r.status_code == 200:
        result = r.json()
    else:
        result = []
    return pd.DataFrame(result, columns=['word', 'freq']).set_index('word')


def find_urns(docids=None, mode: str = 'json') -> pd.DataFrame:
    """Return a list of URNs.

    .. todo:: Add description of functionality + parameters

    :param docids: list of document IDs as a dictionary {docid: dhlab identifiers} or a pandas dataframe.
    :param mode: Default 'json'.
    :return:
    """
    params = locals()
    r = requests.post(BASE_URL + "/find_urn", json=params)
    if r.status_code == 200:
        res = pd.DataFrame.from_dict(r.json(), orient='index', columns=['urn'])
    else:
        res = pd.DataFrame()
    return res


def ngram_book(
    word=['.'],
    title=None,
    period=None,
    publisher=None,
    lang=None,
    city=None,
    ddk=None,
    topic=None
):
    """Get a time series for a word as string,
    title is name of book period is (year, year),
    lang is three letter iso code.
    Use % as wildcard where appropriate - no wildcards in word and lang"""
    params = locals()
    if isinstance(word, str):
        # assume a comma separated string
        word = [w.strip() for w in word.split(',')]
    params['word'] = tuple(word)
    params = {x: params[x] for x in params if not params[x] is None}
    r = requests.post(BASE_URL + "/ngram_book", json=params)
    # print(r.status_code)
    df = pd.DataFrame.from_dict(r.json(), orient='index')
    df.index = df.index.map(lambda x: tuple(x.split()))
    columns = df.index.levels[0]
    df = pd.concat([df.loc[x] for x in columns], axis=1)
    df.columns = columns
    #df.index = df.index.map(pd.Timestamp)
    return df


def ngram_periodicals(
    word=['.'],
    title=None,
    period=None,
    publisher=None,
    lang=None,
    city=None,
    ddk=None,
    topic=None
):
    """Get a time series for a word as string,
    title is name of periodical period is (year, year),
    lang is three letter iso code.
    Use % as wildcard where appropriate - no wildcards in word and lang"""

    params = locals()
    if isinstance(word, str):
        # assume a comma separated string
        word = [w.strip() for w in word.split(',')]
    params['word'] = tuple(word)
    params = {x: params[x] for x in params if not params[x] is None}
    r = requests.post(BASE_URL + "/ngram_periodicals", json=params)
    # print(r.status_code)
    df = pd.DataFrame.from_dict(r.json(), orient='index')
    df.index = df.index.map(lambda x: tuple(x.split()))
    columns = df.index.levels[0]
    df = pd.concat([df.loc[x] for x in columns], axis=1)
    df.columns = columns
    #df.index = df.index.map(pd.Timestamp)
    return df


def ngram_news(word=['.'], title=None, period=None):
    """ get a time series period is a tuple of (year, year), (yearmonthday, yearmonthday)
    word is string and title is the title of newspaper, use % as wildcard"""
    params = locals()
    if isinstance(word, str):
        # assume a comma separated string
        word = [w.strip() for w in word.split(',')]
    params['word'] = tuple(word)
    params = {x: params[x] for x in params if not params[x] is None}
    r = requests.post(BASE_URL + "/ngram_newspapers", json=params)
    # print(r.status_code)
    df = pd.DataFrame.from_dict(r.json(), orient='index')
    df.index = df.index.map(lambda x: tuple(x.split()))
    columns = df.index.levels[0]
    df = pd.concat([df.loc[x] for x in columns], axis=1)
    df.columns = columns
    #df.index = df.index.map(pd.Timestamp)
    return df

def get_document_frequencies(urns=None, cutoff=0, words = None):
    """Get frequency numbers from documents as a list of URNs
    :urns: list of urns
    :cutoff: minimum frequency of a word to be counted
    :word: a list of words to be counted - if left None, whole document is returned"""
    params = locals()
    r = requests.post(f"{BASE_URL}/frequencies", json=params)
    result = r.json()
    # check if words are passed - return differs a bit
    # check if words are passed - return differs a bit
    if words is None:
        structure = dict()
        for u in result:
            try:
                structure[u[0][0]] = dict([(x[1],x[2]) for x in u ]) 
            except IndexError:
                pass
        df = pd.DataFrame(structure)
        df = df.sort_values(by=df.columns[0], ascending=False).fillna(0)
    else:     
        df = pd.DataFrame(result)
        df.columns = ["urn", "word", "count", "urncount"]  
        df = pd.pivot_table(df,  values = 'count', index = 'word', columns = "urn").fillna(0)
    return df

def get_word_frequencies(urns=None, cutoff=0, words=None):
    """Get frequency numbers from documents as a list of URNs 
    :urns: list of urns
    :cutoff: minimum frequency of a word to be counted
    :word: a list of words to be counted - should not be left None"""
    return get_document_frequencies(urns, cutoff, words)


def get_document_corpus(**kwargs):
    return document_corpus(**kwargs)


def document_corpus(
    doctype=None,
    author=None,
    freetext=None,
    fulltext=None,
    from_year=None,
    to_year=None,
    from_timestamp=None,
    to_timestamp=None,
    title=None,
    ddk=None,
    subject=None,
    lang=None,
    limit=None
):
    """ Fetch a corpus based on metadata - doctypes are digibok, digavis, digitidsskrift"""

    parms = locals()
    params = {x: parms[x] for x in parms if not parms[x] is None}

    r = requests.post(BASE_URL + "/build_corpus", json=params)

    return pd.DataFrame(r.json())


def urn_collocation(
    urns=None,
    word='arbeid',
    before=5,
    after=0,
    samplesize=200000
):
    """ Create a collocation from a list of URNs -
    returns distance (sum of distances and bayesian distance) and frequency"""

    params = {
        'urn': urns,
        'word': word,
        'before': before,
        'after': after,
        'samplesize': samplesize
    }
    r = requests.post(BASE_URL + "/urncolldist_urn", json=params)
    return pd.read_json(r.text)


def totals(n=50000):
    """ Get total frequencies of words in database"""

    r = requests.get(BASE_URL + "/totals/{n}".format(n=n))
    return pd.DataFrame.from_dict(
        dict(r.json()), orient='index', columns=['freq'])


def concordance(urns=None, words=None, window=25, limit=100):
    """ Get a list of concordances from database, words is an fts5 string search expression"""
    if words is None:
        return {}  # exit condition
    else:
        params = {
            'urns': urns,
            'query': words,
            'window': window,
            'limit': limit
        }
        r = requests.post(BASE_URL + "/conc", json=params)
    return pd.DataFrame(r.json())


def concordance_counts(urns=None, words=None, window=25, limit=100):
    """ Get a list of concordances from database, words is an fts5 string search expression"""
    if words is None:
        return {}  # exit condition
    else:
        params = {
            'urns': urns,
            'query': words,
            'window': window,
            'limit': limit
        }
        r = requests.post(BASE_URL + "/conccount", json=params)
    return pd.DataFrame(r.json())


def konkordans(urns=None, query=None, window=25, limit=100):
    if query is None:
        return {}  # exit condition
    else:
        params = {
            'urns': urns,
            'query': query,
            'window': window,
            'limit': limit
        }
        r = requests.post(BASE_URL + "/conc", json=params)
    return pd.DataFrame(r.json())


def collocation(corpusquery='norge', word='arbeid', before=5, after=0):
    params = {
        'metadata_query': corpusquery,
        'word': word,
        'before': before,
        'after': after
    }
    r = requests.post(BASE_URL + "/urncolldist", json=params)
    return pd.read_json(r.text)


import requests

# Norwegian word bank
def word_variant(word, form, lang = 'nob'):
    """ Find alternative form for a given word form, e.g. word_variant('spiste', 'pres-part') """
    r = requests.get(f"{BASE_URL}/variant_form", params={'word':word, 'form':form, 'lang':lang})
    return r.json()

def word_paradigm(word, lang = 'nob'):
    """ Find paradigm form for a word  """
    r = requests.get(f"{BASE_URL}/paradigm", params = {'word': word, 'lang':lang})

    return r.json()

def word_paradigm_many(wordlist, lang = 'nob'):
    """ Find alternative form for a list words """
    r = requests.post(f"{BASE_URL}/paradigms", json = {'words': wordlist, 'lang':lang})
    return r.json()


def word_form(word, lang = 'nob'):
    """ Find alternative form for a given word form, e.g. word_variant('spiste', 'pres-part') """
    r = requests.get(f"{BASE_URL}/word_form", params = {'word': word, 'lang':lang})
    return r.json()

def word_form_many(wordlist, lang = 'nob'):
    """ Find alternative forms for a list of words """
    r = requests.post(f"{BASE_URL}/word_forms", json = {'words': wordlist, 'lang':lang})
    return r.json()

def word_lemma(word, lang = 'nob'):
    """ Find lemma form for a given word form """
    r = requests.get(f"{BASE_URL}/word_lemma", params = {'word': word, 'lang':lang})
    return r.json()

def word_lemma_many(wordlist, lang = 'nob'):
    """ Find lemma form for a given word form """
    r = requests.post(f"{BASE_URL}/word_lemmas", json = {'words': wordlist, 'lang':lang})
    return r.json()