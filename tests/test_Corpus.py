import dhlab as dh
import pytest
import pandas as pd
from typing import List


class TestCorpus:
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


class TestCorpusConc:
    def test_corpus_conc(self):
        c = dh.Corpus(doctype="digavis", limit=2)
        conc = c.conc("og")
        assert len(conc) > 0
        assert len(conc.frame.columns) == 3

    def test_corpus_conc_all_doctypes(self):
        for doctype in dh.Corpus.doctypes:
            c = dh.Corpus(doctype=doctype, limit=2)
            conc = c.conc('"."', limit=2)
            assert isinstance(conc, dh.Concordance)
            assert len(conc.frame.columns) == 3


class TestCorpusColl:
    def test_corpus_coll(self):
        for doctype in dh.Corpus.doctypes:
            c = dh.Corpus(doctype=doctype, limit=2)
            coll = c.coll(".", samplesize=2)
            assert len(coll) > 0


class TestCorpusIntegrityCheck:
    def test_with_empty_corpus(self):
        c = dh.Corpus()
        with pytest.raises(ValueError) as exc_info:
            c.check_integrity()
        assert "Corpus is empty." in str(exc_info.value)

    def test_with_all_doctypes(self):
        for doctype in dh.Corpus.doctypes:
            c = dh.Corpus(doctype=doctype, limit=5)
            assert c.check_integrity() == True, f"Failed for {doctype}"

    def test_with_wrong_datatype(self):
        c = dh.Corpus.from_df(pd.DataFrame({"urn": ["123", "456"]}))
        with pytest.raises(ValueError) as exc_info:
            c.check_integrity()


class TestCheckForUrnDuplicates:
    test_urns: List[str] = [["URN:NBN:no-nb_digibok_2008040104069"]]
    test_str: List[str] = [
        "Undersøgelseskomiteens Indberetning sammenholdt med de virkelige Begivenheder i 1884 og 1893"
    ]

    @pytest.mark.parametrize("txt", test_str)
    def test_corpus_from_str_w_duplicates(self, txt):
        c = dh.Corpus(title=txt, allow_duplicates=True)
        assert len(c) == 2

    @pytest.mark.parametrize("txt", test_str)
    def test_corpus_from_str_wo_duplicates(self, txt):
        c = dh.Corpus(title=txt, allow_duplicates=False)
        assert len(c) == 1

    @pytest.mark.parametrize("urn", test_urns)
    def test_extend_w_deduplication(self, urn):
        c = dh.Corpus()
        c.extend_from_identifiers(urn)
        assert len(c) == 1
