import pytest
from dhlab.text.corpus_collection import CorpusCollection
from dhlab.text.corpus import Corpus


class TestCorpusCollection:
    def test_init(self):
        cc = CorpusCollection()
        assert cc.corpora == {}

    def test_add(self):
        cc = CorpusCollection()
        cc.add("a", Corpus())
        assert "a" in cc

    def test_remove(self):
        cc = CorpusCollection()
        cc.add("a", Corpus())
        cc.add("b", Corpus())
        cc.remove("a")
        cc.remove("b")
        assert "a" not in cc
        assert "b" not in cc

    def test_get(self):
        cc = CorpusCollection()
        cc.add("a", Corpus())
        assert isinstance(cc.get("a"), Corpus)

    def test_concat(self):
        cc = CorpusCollection()
        cc.add("a", Corpus())
        cc.add("b", Corpus())
        assert isinstance(cc.concat_corpora(), Corpus)

    def test_iter(self):
        cc = CorpusCollection()
        cc.add("a", Corpus())
        cc.add("b", Corpus())
        assert len([x for x in cc]) == 2

    def test_len(self):
        cc = CorpusCollection()
        cc.add("a", Corpus())
        cc.add("b", Corpus())
        assert len(cc) == 2

    def test_contains(self):
        cc = CorpusCollection()
        cc.add("a", Corpus())
        assert "a" in cc

    def test_repr(self):
        cc = CorpusCollection()
        cc.add("a", Corpus())
        cc.add("b", Corpus())
        assert "a\nb" in str(cc)

    def test_show_corpora(self):
        cc = CorpusCollection()
        cc.add("a", Corpus())
        assert isinstance(cc.show_corpora(), dict)

    def test_getitem(self):
        cc = CorpusCollection()
        cc.add("a", Corpus())
        assert isinstance(cc["a"], Corpus)

    def test_setitem(self):
        cc = CorpusCollection()
        cc["a"] = Corpus()
        assert isinstance(cc["a"], Corpus)

    def test_get(self):
        cc = CorpusCollection()
        cc.add("a", Corpus())
        assert isinstance(cc.get("a"), Corpus)

    def test_concat_corpora(self):
        cc = CorpusCollection()
        cc.add("a", Corpus())
        cc.add("b", Corpus())
        assert isinstance(cc.concat_corpora(), Corpus)
