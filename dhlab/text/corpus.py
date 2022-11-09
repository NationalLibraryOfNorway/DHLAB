from pandas import DataFrame
import pandas as pd
from dhlab.text.dhlab_object import DhlabObj
from dhlab.api.dhlab_api import document_corpus, get_metadata, evaluate_documents
from typing import Union

class Corpus(DhlabObj):
    """Class representing as DHLAB Corpus"""
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
            limit=10,
            ):

        if (doctype 
            or author
            or freetext
            or fulltext
            or from_year
            or to_year
            or from_timestamp
            or to_timestamp
            or title
            or ddk
            or lang):
            
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
            
        else:
            self.corpus = pd.DataFrame(columns=["urn"])
        
        super().__init__(self.corpus)
        self.urn = self.corpus.urn
        self.size = len(self.corpus)

    @classmethod
    def from_df(cls, df):
        """Typecast Pandas DataFrame to Corpus class
        
        DataFrame most contain URN column"""        
        corpus = Corpus()
        corpus.corpus = cls._urn_id_in_dataframe_cols(df)
        corpus.urn = corpus.corpus.urn
        corpus.frame = corpus.corpus
        corpus.size = len(corpus.corpus)
        return corpus
    
    @classmethod
    def from_csv(cls, path):
        """Import corpus from csv"""
        df = pd.read_csv(path)
        return cls.from_df(df)
        
    @staticmethod
    def _urn_id_in_dataframe_cols(dataframe):
        """Checks if dataframe contains URN column"""
        
        if "urn" in dataframe.columns:
            if dataframe.urn.str.contains("^URN:NBN:no-nb_.+").all():
                return dataframe                    
        raise ValueError("No'urn'-column in dataframe.")       
    
    def to_csv(self, path):
        self.corpus.to_csv(path, index=None)        

    def add(self, corpus = None):
        """Add a corpus to existing corpus"""
        self.corpus = pd.concat([self.corpus, corpus.corpus]).drop_duplicates().reset_index(drop=True)
        self.size = len(self.corpus)
    
    def extend_from_identifiers(self, identifiers=None):
        corpus = get_metadata(urnlist(identifiers))
        self.corpus = pd.concat([self.corpus, corpus]).drop_duplicates().reset_index(drop=True)
        self.size = len(self.corpus)
        
    def evaluate_words(self, wordbags = None):
        df = evaluate_documents(wordbags = wordbags, urns = list(self.corpus.urn))
        df.index = df.index.astype(int)
        cols = df.columns
        df = pd.concat([df, self.corpus[['dhlabid','urn']].set_index('dhlabid')], axis = 1)
        df = df.set_index('urn')
        return df[cols].fillna(0)
    
    def sample(self, n=5):
        "Create random subkorpus with `n` entries"
        # if n >= self.size:            
        n = min(n, self.size)
            #raise ValueError(f"Sample must be smaller than main corpus ({self.size})")        
        sample = self.corpus.sample(n).copy()
        return Corpus.from_df(sample)
    
class EmptyCorpus(Corpus):
    """DEPRECATED: call Corpus without parameters to represent an empty corpus"""
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
