import requests
import pandas as pd

def frame(something, name = None):
    """Try to make a frame out of something and name columns according to name, which should be a string or a list of strings,
    one for each column. Mismatch in numbers is taken care of."""
    
    if isinstance(something, dict):
        res = pd.DataFrame.from_dict(something, orient='index')
    else:
        res =  pd.DataFrame(something)
    number_of_columns = len(res.columns)
    if name != None:
        if isinstance(name, list):
            if len(name) >= number_of_columns:
                res.columns = name[:number_of_columns]
            else:
                res.columns = name + list(range(len(name), number_of_columns))
        else:
            res.columns = [name] + list(range(1, number_of_columns))
    return res

def collocation(
    word, 
    yearfrom=2010, 
    yearto=2018, 
    before=3, 
    after=3, 
    limit=1000, 
    corpus='avis',
    lang='nob',
    title='%',
    ddk='%', 
    subtitle='%'):
    """Defined collects frequencies for a given word"""
    
    data =  requests.get(
        "https://api.nb.no/ngram/collocation", 
        params={
            'word':word,
            'corpus':corpus, 
            'yearfrom':yearfrom, 
            'before':before,
            'after':after,
            'limit':limit,
            'yearto':yearto,
        'title':title,
        'ddk':ddk,
        'subtitle':subtitle}).json()
    return data['freq'],data['doc'], data['dist'] 


def urn_coll(word, urns=[], after=5, before=5, limit=1000):
    """Find collocations for word in a set of book URNs. Only books at the moment"""
    
    if isinstance(urns[0], list):  # urns assumed to be list of list with urn-serial as first element
        urns = [u[0] for u in urns]
        
    r = requests.post("https://api.nb.no/ngram/urncolldist", json={'word':word, 'urns':urns, 
                                                                'after':after, 'before':before, 'limit':limit})
    df = frame(r.json()).transpose()
    df.columns = ['freq','dist']
    
    return df