from pandas import DataFrame, Series
import dhlab as dh

def urnlist(corpus):
    """Try to pull out a list of URNs from corpus"""
    if isinstance(corpus, dh.Corpus):
        _urnlist = list(corpus.urn)
    elif isinstance(corpus, DataFrame):
        _urnlist = list(corpus.urn)
    elif isinstance(corpus, list):
        _urnlist = corpus
    elif isinstance(corpus, Series):
        _urnlist = corpus.to_list()
    else:
        _urnlist = []
    return _urnlist

# convert cell to a link
def make_link(row):
    r = "<a target='_blank' href = 'https://urn.nb.no/{x}'>{x}</a>".format(x=str(row))
    return r
