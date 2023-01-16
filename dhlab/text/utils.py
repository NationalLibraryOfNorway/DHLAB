from pandas import DataFrame, Series
import dhlab as dh

def urnlist(corpus):
    """Try to pull out a list of URNs from corpus"""
    if isinstance(corpus, dh.Corpus):
        _urnlist = list(corpus.corpus.urn)
    elif isinstance(corpus, DataFrame):
        _urnlist = list(corpus.urn)
    elif isinstance(corpus, list):
        _urnlist = corpus
    elif isinstance(corpus, Series):
        _urnlist = corpus.to_list()
    else:
        _urnlist = []
    return _urnlist
