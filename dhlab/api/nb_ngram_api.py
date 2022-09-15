import json

import networkx as nx
import requests

from dhlab.constants import NGRAM_API, GALAXY_API


def get_ngram(terms: str, corpus: str = "avis", lang: str = "nob") -> dict:
    """Fetch raw and relative frequencies for the ``terms``.

    Call the :py:data:`NGRAM_API`.
    The frequencies are aggregated per year between 1800-2021.

    :param str terms: comma separated string of words
    :param str corpus: type of documents to search through
    :return: table of annual frequency counts per term
    """
    req = requests.get(
        NGRAM_API,
        params={
            'terms': terms,
            'corpus': corpus,
            'lang':lang
        }
    )
    if req.status_code == 200:
        res = req.text
    else:
        res = "[]"
    return json.loads(res)


def make_word_graph(
        words: str, corpus: str = 'all', cutoff: int = 16, leaves: int = 0
) -> nx.DiGraph:
    """Get galaxy from ngram-database.

    Call the :py:obj:`~dhlab.constants.GALAXY_API` endpoint.

    :param str words: comma-separated string of words
    :param str corpus: document type: ``'book'``, ``'avis'``, or ``'all'``,
    :param int cutoff: Number of nodes to include.
    :param int leaves: Set leaves=1 to get the leaves.
    :return: A `networkx.DiGraph` with the results.
    """

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
        # print(graph)
        nodes = graph['nodes']
        edges = graph['links']
        for edge in edges:
            edgelist += [
                (nodes[edge['source']]['name'],
                 nodes[edge['target']]['name'],
                 abs(edge['value']))
            ]
    # print(edgelist)
    G.add_weighted_edges_from(edgelist)
    return G
