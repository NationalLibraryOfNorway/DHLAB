from dhlab.text import Corpus, Collocations

test_urns = [
    "URN:NBN:no-nb_digibok_2008091004038",
    "URN:NBN:no-nb_digibok_2021030248529",
    "URN:NBN:no-nb_digibok_2020100607613",
]


class TestCollocation:
    c = Corpus()
    c.extend_from_identifiers(test_urns)
    coll = Collocations(c, "og", samplesize=2)

    def test_collocation(self):
        assert len(self.coll.frame) > 0
        assert len(self.coll.frame.columns) == 1
        assert "counts" in self.coll.frame.columns

    def test_fromdf(self):
        df = self.coll.frame
        coll = Collocations.from_df(df)
        assert coll is not None

    def test_collocation_sort(self):
        sorted = self.coll.sort()
        assert len(sorted.frame) > 0, "No sorted frame"
