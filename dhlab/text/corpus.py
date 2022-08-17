from pandas import DataFrame
import pandas as pd

from dhlab.api.dhlab_api import document_corpus, get_metadata, evaluate_documents


class Corpus:
    def __init__(
            self,
            doctype=None,
            author=None,
            freetext=None,
            fulltext=None,
            from_year=None,
            to_year=None,
            from_timestamp=None,
            to_timestamp=None,
            title=None,
            ddk=None,
            subject=None,
            lang=None,
            limit=10):

        self.corpus = document_corpus(
            doctype,
            author,
            freetext,
            fulltext,
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



    def add(self, corpus = None):
        """Add a corpus to existing corpus"""
        new_corpus = pd.concat([self.corpus, corpus.corpus]).drop_duplicates()
        self.corpus = new_corpus
        self.size = len(self.corpus)
    
    def extend_from_identifiers(self, identifiers=None):
        corpus = get_metadata(urnlist(identifiers))
        self.corpus = pd.concat([self.corpus, corpus]).drop_duplicates()
        self.size = len(self.corpus)
        
    def evaluate_words(self, wordbags = None):
        df = evaluate_documents(wordbags = wordbags, urns = list(self.corpus.urn))
        df.index = df.index.astype(int)
        cols = df.columns
        df = pd.concat([df, self.corpus[['dhlabid','urn']].set_index('dhlabid')], axis = 1)
        df = df.set_index('urn')
        return df[cols].fillna(0)
    
class EmptyCorpus(Corpus):
    def __init__(self):
        self.corpus = pd.DataFrame()
        self.size = 0
        
class Corpus_from_identifiers(Corpus):
    def __init__(self, identifiers=None):
        self.corpus = get_metadata(urnlist(identifiers))
        self.size = len(self.corpus)


def urnlist(corpus):
    """Try to pull out a list of URNs from corpus"""

    if isinstance(corpus, Corpus):
        urnlist = list(corpus.corpus.urn)
    elif isinstance(corpus, DataFrame):
        urnlist = list(corpus.urn)
    elif isinstance(corpus, list):
        urnlist = corpus
    else:
        urnlist = []
    return urnlist
