import json

import requests
import networkx as nx

NGRAM_API = "https://api.nb.no/dhlab/nb_ngram/ngram/query"
GALAXY_API = "https://api.nb.no/dhlab/nb_ngram_galaxies/galaxies/query"

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
            edgelist += [
                (nodes[edge['source']]['name'],
                 nodes[edge['target']]['name'],
                 abs(edge['value']))
            ]
    #print(edgelist)
    G.add_weighted_edges_from(edgelist)
    return G