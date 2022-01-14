from datetime import datetime
from datetime import datetime


class Ngram_book(Ngram):
    """Extract ngrams using dynamics"""

    def __init__(self, words = None, title = None, publisher = None, city = None, lang = 'nob', from_year = None, to_year = None, ddk = None, subject = None):

        
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
        def __init__(self, words = None, title = None, city = None, from_year = None, to_year = None):



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
