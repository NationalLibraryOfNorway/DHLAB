import pandas as pd
from pandas import DataFrame

from ..api.dhlab_api import document_corpus, get_metadata


class Corpus():
    def __init__(
        self,
        doctype = None,
        author = None,
        freetext = None,
        from_year = None,
        to_year = None,
        from_timestamp = None,
        to_timestamp = None,
        title = None,
        ddk = None,
        subject = None,
        lang = None,
        limit = None):
        
        self.corpus = document_corpus(
            doctype,
            author,
            freetext,
            from_year,
            to_year,
            from_timestamp,
            to_timestamp,
            title,
            ddk,
            subject,
            lang,
            limit
        )
        
        self.size = len(self.corpus)
        
        return
    
class Corpus_from_identifiers(Corpus):
    def __init__(self, identifiers = None):
        self.corpus = get_metadata(urnlist(identifiers))
        

def urnlist(corpus):
    """Try to pull out a list of URNs from corpus"""
    
    if isinstance(corpus, Corpus):
        urnlist = list(corpus.corpus.urn)
    elif isinstance(corpus, DataFrame):
        urnlist = list(corpus.urn)
    else:
        urnlist = []
    return urnlist