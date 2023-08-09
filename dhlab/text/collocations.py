"""Handle collocations from a corpus."""
import pandas as pd

from dhlab.api.dhlab_api import urn_collocation
from dhlab.text.utils import urnlist


class Collocations(pd.DataFrame):
    @property
    def _constructor(self):
        return Collocations

    @classmethod
    def get_collocations(
        self,
        corpus=None,
        words=None,
        before=10,
        after=10,
        reference=None,
        samplesize=20000,
        alpha=False,
        ignore_caps=False,
    ):
        if isinstance(words, str):
            words = [words]

        res = pd.concat(
            [
                urn_collocation(
                    urns=urnlist(corpus),
                    word=w,
                    before=before,
                    after=after,
                    samplesize=samplesize,
                )
                for w in words
            ]
        )[["counts"]]

        if reference is not None:
            teller = res.counts / res.counts.sum()
            divisor = reference.iloc[:, 0] / reference.iloc[:, 0].sum()
            res["relevance"] = teller / divisor

        return Collocations(res)

    def show(self, sortby="counts", n=20):
        return self.sort_values(by=sortby, ascending=False).head(n)
