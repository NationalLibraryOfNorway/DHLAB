import dhlab.nbtext as nb
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


def dist_coll_urn(word, urns=None, after=5, before=0, limit=1000):
    coll = urn_coll(word, urns=urns, after=after, before=before, limit=limit)
    coll['dist'] = round(coll['dist'], 2)
    coll['score'] = round(dist(coll['dist'], calculate_midpoint(before, after), coll['freq']), 2)
    return coll
   
def check(word, frames):
    return {c:inspect(frames[c]['score'], word) for c in frames if word in frames[c].index}

def dist(obs_mean, expected, freq):
    factor = ((freq-1)/(freq))*obs_mean
    ratio = obs_mean/(obs_mean - factor)
    return obs_mean + (expected - obs_mean)/ratio


def create_frame(coll, expected):
    df = nb.frame(frame(coll).transpose(), 'freq doc dist'.split())
    df['score'] = dist(df['dist'], expected, df['freq'])
    return df

def colls2df(colls, expected):
    colls_df = dict()
    for c in colls:
        colls_df[c] = create_frame(colls[c], expected)
    return colls_df

def calculate_midpoint(before, after):
    if before == 0:
        corr = 1
    elif after == 0:
        corr = -1
    else:
        corr = 0
    return (after - before + corr)/2
    
def make_collocations(word, period=(1945, 1990), step = 3, before = 0, after = 10):
    colls = dict()
    for year in range(period[0], period[1], step):
        print('behandler: ', year, year + step)
        try:
            colls[(year, year + step)] = collocation(word, yearfrom = year, yearto = year + step, corpus='avis', before= before, after = after)
        except:
            # try again - things may have loaded on the server...
            print('prøver en gang til for: ', (year, year + step))
            try:
                colls[(year, year + step)] = collocation(word, yearfrom = year, yearto = year + step, corpus='avis', before= before, after = after)
            except:
                print('klarte ikke: ', (year, year + step))
    colls_df = colls2df(colls, calculate_midpoint(before, after))
    return  colls_df, score_df(colls_df)


score_df = lambda df: nb.frame({x:df[x]['score'] for x in df }).transpose()
display_vals = lambda kr_df, word, clip = 0: kr_df[kr_df >= clip].loc[word]

def show_frame(df, colnum = 0,  clip = 0, fillval= 10, cmap = 'Blues', up = True, axis=0, first_row=0, number_of_rows = 20): 
    if up == True:
        cmap = cmap + '_r'
        dfc = df[df >= clip]
    else:
        dfc = df[df <= clip]
    return dfc.sort_values(by = df.columns[colnum], ascending=up)[first_row:first_row + number_of_rows].fillna(fillval).style.background_gradient(cmap=cmap,axis=axis)
