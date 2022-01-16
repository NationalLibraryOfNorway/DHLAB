from datetime import datetime

from ..api.dhlab_api import ngram_book, ngram_news
from .nb_ngram import nb_ngram

class Ngram():
    """Top level class for ngrams"""
    def __init__(self, words = None, from_year = None, to_year = None, doctype = None, lang = 'nob'):
       
        self.date = datetime.now()
        if to_year is None:
            to_year = self.date.year
        if from_year is None:
            from_year = 1950
            
        self.from_year = from_year
        self.to_year = to_year
        self.words = words
        self.lang = lang
        if not doctype is None:
            if 'bok' in doctype:
                doctype = 'bok'
            elif 'avis' in doctype:
                doctype = 'avis'
            else:
                doctype = 'bok'
        else:
            doctype = 'bok'
        ngrm = nb_ngram(terms = ', '.join(words), corpus = doctype, years = (from_year, to_year))
        ngrm.index = ngrm.index.astype(str)
        self.ngram = ngrm
        return None

    def plot(self, **kwargs):
        self.ngram.plot(**kwargs)
    
    def compare(self, another_ngram):
        from datetime import datetime
        start_year = max(datetime(self.from_year,1,1), datetime(another_ngram.from_year,1,1)).year
        end_year = min(datetime(self.to_year,1,1), datetime(another_ngram.to_year,1,1)).year
        compare =  (self.ngram.loc[str(start_year):str(end_year)].transpose()/another_ngram.ngram[str(start_year):str(end_year)].transpose().sum()).transpose()
        return compare

    
class Ngram_book(Ngram):
    """Extract ngrams using metadata with functions to be inherited"""

    def __init__(
        self,
        words = None,
        title = None,
        publisher = None,
        city = None,
        lang = 'nob',
        from_year = None,
        to_year = None,
        ddk = None,
        subject = None
    ):

        self.date = datetime.now()
        if to_year is None:
            to_year = self.date.year
        if from_year is None:
            from_year = 1950
        self.from_year = from_year
        self.to_year = to_year
        self.words = words
        self.title = title
        self.publisher = publisher
        self.city = city
        self.lang = lang
        self.ddk = ddk
        self.subject = subject
        self.ngram = ngram_book(word = words, title = title, publisher = publisher, lang = lang,city = city, period = (from_year, to_year), ddk = ddk, topic = subject)
        #self.cohort =  (self.ngram.transpose()/self.ngram.transpose().sum()).transpose()
        return None
    
class Ngram_news(Ngram):
    def __init__(
        self, 
        words = None,
        title = None,
        city = None,
        from_year = None,
        to_year = None
    ):
        self.date = datetime.now()
        if to_year is None:
            to_year = self.date.year
        if from_year is None:
            from_year = 1950
        self.from_year = from_year
        self.to_year = to_year
        self.words = words
        self.title = title
        self.ngram = ngram_news(word = words, title = title, period = (from_year, to_year))
        #self.cohort =  (self.ngram.transpose()/self.ngram.transpose().sum()).transpose()
        return None
