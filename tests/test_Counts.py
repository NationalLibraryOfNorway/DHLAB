import dhlab as dh
from dhlab.text.utils import urnlist


def counts_test_func(corpus_like, words=None):
    counts = dh.Counts(corpus_like, words=words)
    assert len(counts.frame) > 0
    assert len(counts.frame.columns) == 5
    return True


class TestCounts:
    def test_counts(self):
        aviser = dh.Corpus(doctype="digavis", limit=5)
        # boker = dh.Corpus(doctype="digibok", limit=5)
        c = dh.Counts(aviser)
        assert len(c.frame) > 0
        assert len(c.frame.columns) == 5

    def test_counts_func(self):
        aviser = dh.Corpus(doctype="digavis", limit=5)
        boker = dh.Corpus(doctype="digibok", limit=5)
        assert counts_test_func(aviser), "Counts test failed for newspapers"
        assert counts_test_func(boker), "Counts test failed for books"

    def test_counts_dataframe(self):
        aviser = dh.Corpus(doctype="digavis", limit=5)
        # boker = dh.Corpus(doctype="digibok", limit=5)
        df = aviser.frame
        assert counts_test_func(df), "Counts test failed for dataframe"

    def test_counts_urnlist(self):
        aviser = dh.Corpus(doctype="digavis", limit=5)
        # boker = dh.Corpus(doctype="digibok", limit=5)
        urns = urnlist(aviser.frame)
        assert counts_test_func(urns), "Counts test failed for urnlist"

    def test_counts_words(self):
        aviser = dh.Corpus(doctype="digavis", limit=5)
        # boker = dh.Corpus(doctype="digibok", limit=5)
        words = ["og", "eller"]
        assert counts_test_func(aviser, words=words), "Counts test failed for words"

    def test_display_names(self):
        boker = dh.Corpus(doctype="digibok", limit=5)
        c = dh.Counts(boker)
        assert c.display_names() is not None

    def test_head(self):
        boker = dh.Corpus(doctype="digibok", limit=5)
        counts = dh.Counts(boker)
        head = counts.head()
        assert len(head.frame) == 5
        assert len(head.frame.columns) == 5
