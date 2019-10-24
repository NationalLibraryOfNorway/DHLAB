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

inspect = lambda harry, w: harry.loc[w] if w in harry.index else 0

def dist(obs_mean, expected, freq):
    factor = ((freq-1)/(freq))*obs_mean
    ratio = obs_mean/(obs_mean - factor)
    return round(obs_mean + (expected - obs_mean)/ratio,2)

show = lambda harry, cutoff: harry[harry.freq > cutoff].sort_values(by='score')

def calculate_midpoint(before, after):
    if before == 0:
        corr = 1
    elif after == 0:
        corr = -1
    else:
        corr = 0
    return (after - before + corr)/2
    

def create_collocations(words, corpus, before=None, after=None):
    if before == None or after== None:
        print('husk before og after')
        return
    colls = dict()
    for character in words:
        colls[character] = urn_coll(character, nb.pure_urn(corpus), before=before, after=after)
    frames = dict()
    for c in colls:
        frames[c] = nb.frame({'dist':colls[c][1], 'freq':colls[c][0]}).transpose()

    for c in frames:
        frames[c]['dist'] = round(frames[c].dist, 2)

    for c in frames:
        frames[c]['score'] = dist(frames[c].dist, calculate_midpoint(before, after), frames[c].freq)
    return frames

def dist_coll(word, corpus, before=None, after=None):
    
    if before == None or after== None:
        print('husk before og after')
        return
    
    coll = urn_coll(word, nb.pure_urn(corpus), before=before, after=after)
    coll.dist = round(coll.dist, 2)
    coll['score'] = dist(coll.dist, calculate_midpoint(before, after), coll.freq)
    
    return coll

def create_frame(coll, expected):
    df = nb.frame(nb.frame(coll).transpose(), 'freq doc dist'.split())
    df['score'] = dist(df['dist'], expected, df['freq'])
    return df

def colls2df(colls, expected):
    colls_df = dict()
    for c in colls:
        colls_df[c] = create_frame(colls[c], expected)
    return colls_df

    
def make_collocations(word, yeafrom, yearto, step, before = 0, after = 10):
    colls = dict()
    step = 3
    for year in range(perio[0], period[1], step):
        print('behandler: ', year, year + step)
        colls[(year, year + step)] = collocation('kreft', yearfrom=year, yearto=year + step, corpus='avis', before= 0, after = 20)
    if before == 0:
        pos_from = -1
    else:
        pos_from = -before
    if after == 0:
        pos_to = 1
    else:
        post_to = after
    colls_df = colls2df(colls, (pos_to + pos_from)/2)
    return colls_df                


score_df = lambda df: nb.frame({x:df[x]['score'] for x in df }).transpose()
display_vals = lambda kr_df, word, clip = 0: kr_df[kr_df >= clip].loc[word]
show_frame = lambda df, colnum = 0,  clip = 0, up = True: df[df >= clip].sort_values(by = df.columns[colnum], ascending=up)