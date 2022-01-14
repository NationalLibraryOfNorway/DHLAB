### -------------------------- NB ngram ------------------ ###
import networkx as nx
import pandas as pd
import json

def nb_ngram(terms, corpus='bok', smooth=3, years=(1810, 2010), mode='relative'):
    df = ngram_conv(get_ngram(terms, corpus=corpus), smooth=smooth, years=years, mode=mode)
    df.index = df.index.astype(int)
    return df.sort_index()

def get_ngram(terms, corpus='avis'):
    req = requests.get(
        NGRAM_API, 
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
    result = requests.get(GALAXY_API, params=params)
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