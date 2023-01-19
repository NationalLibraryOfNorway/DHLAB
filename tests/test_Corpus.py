import dhlab as dh


class TestCorpus():

    def test_book_corpus(self):
        c = dh.Corpus(doctype="digibok")
        assert len(c.frame) == 10
        assert "urn" in c.frame.columns
        
    def test_news_corpus(self):
        c = dh.Corpus(doctype="digavis")
        assert len(c.frame) == 10
        assert "urn" in c.frame.columns
        
    def test_corpus_freq(self):
        c = dh.Corpus(doctype="digavis", limit=2)
        freq = c.count()
        assert len(freq.frame) > 0 
        assert len(freq.frame.columns) == 2
    