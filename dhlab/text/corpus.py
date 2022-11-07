from pandas import DataFrame
import pandas as pd

from dhlab.api.dhlab_api import document_corpus, get_metadata, evaluate_documents
from typing import Union

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
        
        self.urn = self.corpus.urn
        self.size = len(self.corpus)

    @classmethod
    def from_df(cls, df):
        """Typecast Pandas DataFrame to Corpus class
        
        DataFrame most contain URN column"""        
        corpus = Corpus()
        corpus.corpus = cls._urn_id_in_dataframe_cols(df)
        corpus.urn = corpus.corpus.urn
        corpus.size = len(corpus.corpus)
        return corpus
        
    @staticmethod
    def _urn_id_in_dataframe_cols(dataframe):
        """Checks if dataframe contains URN column"""
        
        if "urn" in dataframe.columns:
            if dataframe.urn.str.contains("^URN:NBN:no-nb_.+").all():
                return dataframe                    
        raise ValueError("No'urn'-column in dataframe.")       
    
    def __repr__(self) -> str:
        """
        Return the string representation of the corpus datafrane
        """
        return self.corpus.__repr__()
    
    def _repr_html_(self) -> Union[str, None]:
        """
        Return the HTML representation of the corpus datafrane
        """
        return self.corpus._repr_html_()
    

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
