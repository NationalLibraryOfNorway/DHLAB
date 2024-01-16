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



