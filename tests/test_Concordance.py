import pytest
from dhlab import Concordance, Corpus


def test_concordance():
    c = Concordance()
    assert c is not None


def test_concordance_corpus():
    c = Corpus(doctype="digibok", limit=2)
    r = Concordance(c, "og")
    assert r is not None
    assert r.size > 0


def test_concordance_sort():
    c = Corpus(doctype="digibok", limit=2)
    r = Concordance(c, "og")
    sorted = r.sort()
    assert sorted is not None
    assert sorted.size > 0
    assert sorted.frame is not None
    assert sorted.frame.columns is not None
    assert "concordance" in sorted.frame.columns
