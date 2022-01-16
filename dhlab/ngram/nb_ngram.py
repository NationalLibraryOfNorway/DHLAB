import pandas as pd
from ..api.nb_ngram_api import get_ngram

def nb_ngram(terms, corpus='bok', smooth=3, years=(1810, 2010), mode='relative'):
    df = ngram_conv(get_ngram(terms, corpus=corpus), smooth=smooth, years=years, mode=mode)
    df.index = df.index.astype(int)
    return df.sort_index()

def ngram_conv(ngrams, smooth=1, years=(1810,2013), mode='relative'):
    ngc = {}
    # check if relative frequency or absolute frequency is in question
    if mode.startswith('rel') or mode=='y':
        arg = 'y'
    else:
        arg = 'f'
    for x in ngrams:
        if x != []:
            ngc[x['key']] = {
                z['x']:z[arg]
                for z in x['values'] 
                if int(z['x']) <= years[1] and int(z['x']) >= years[0]
            }
    return pd.DataFrame(ngc).rolling(window=smooth, win_type='triang').mean()


