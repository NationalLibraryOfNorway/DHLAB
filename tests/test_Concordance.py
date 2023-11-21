import pytest
from dhlab import Concordance, Corpus


def test_concordance():
    c = Concordance()
    assert c is not None


def test_concordance_corpus():
    c = Corpus(doctype="digibok")
    r = Concordance(c, "og")
    assert r is not None
    assert r.size > 0


# def test_concordance_corpus_show():
#     c = Corpus(doctype="digibok")
#     r = Concordance(c, "og")
#     assert r.show() is not None
#     assert r.show(5) is not None
