class Concordance:
    """Wrapper for concordance function with added functionality"""
    def __init__(self, corpus, query):
        self.concordance = concordance(urns = list(corpus.urn), words = query)
        self.concordance['link'] = self.concordance.urn.apply(make_link)
        self.concordance = self.concordance[['link', 'urn', 'conc']]
        self.concordance.columns = ['link', 'urn', 'concordance']
        self.corpus = corpus
        self.size = len(self.concordance)
    
    def show(self, n = 10, style = True):
        if style:
            result =  self.concordance.sample(min(n, self.size))[['link', 'concordance']].style
        else:
            result =  self.concordance.sample(min(n, self.size))
        return result
    
class Cooccurence():
    """Collocations """
    def __init__(self, corpus = None, words = None, before = 10, after = 10, reference = None):
        if isinstance(words, str):
            words = [words]
        coll = pd.concat([urn_collocation(urns = list(corpus.urn), word = w, before = before, after = after) for w in words])[['counts']]
        self.coll = coll.groupby(coll.index).sum()
        self.reference = reference
        self.before = before
        self.after = after
        
        if reference is not None:
            self.coll['relevance'] = (self.coll.counts/self.coll.counts.sum())/(self.reference.freq/self.reference.freq.sum())
    
    def show(self, sortby = 'counts', n = 20):
        return self.coll.sort_values(by = sortby, ascending = False)
    
    def keywordlist(self, top = 200, counts = 5, relevance = 10):
        mask = self.coll[self.coll.counts > counts]
        mask = mask[mask.relevance > relevance]
        return list(mask.sort_values(by = 'counts', ascending = False).head(200).index)
    
class Ngram():
    def __init__(self, words = None, from_year = None, to_year = None, doctype = None, lang = 'nob'):
        from datetime import datetime
        
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
    """"""

    def __init__(self, words = None, title = None, publisher = None, city = None, lang = 'nob', from_year = None, to_year = None, ddk = None, subject = None):
        from datetime import datetime

        
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
            from datetime import datetime


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
