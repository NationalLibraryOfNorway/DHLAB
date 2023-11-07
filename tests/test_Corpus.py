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
        freq = c.freq()
        assert len(freq.frame) > 0 
        assert len(freq.frame.columns) == 2
        
    def test_empty_corpus(self):
        c = dh.Corpus(doctype="digavis", limit=0)
        assert len(c.frame) == 0
        assert "urn" in c.frame.columns
        assert c.size == 0
        
    def test_add_dunder(self):
        c = dh.Corpus(doctype="digavis", limit=4)
        assert c.size == 4
        d = dh.Corpus(doctype="digavis", limit=7)
        assert d.size == 7
        e = c + d
        assert e.size == 11
        
    def test_add(self):
        c = dh.Corpus(doctype="digavis", limit=4)
        assert c.size == 4
        d = dh.Corpus(doctype="digavis", limit=7)
        assert d.size == 7
        c.add(d)
        assert c.size == 11
        
    def test_extend_from_identifiers(self):
        c = dh.Corpus(doctype="digavis", limit=4)
        assert c.size == 4
        d = dh.Corpus(doctype="digavis", limit=7)
        assert d.size == 7
        c.extend_from_identifiers(d.frame)
        assert c.size == 11
    