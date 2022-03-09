
import re

import pandas as pd

from dhlab.api.dhlab_api import get_document_frequencies, concordance, urn_collocation
from dhlab.text.corpus import urnlist


# convert cell to a link
def make_link(row):
    r = "<a target='_blank' href = 'https://urn.nb.no/{x}'>{x}</a>".format(
        x=str(row))
    return r


# find hits a cell
def find_hits(x): return ' '.join(re.findall("<b>(.+?)</b", x))


class Concordance:
    """Wrapper for concordance function with added functionality"""

    def __init__(self, corpus=None, query=None, window=20, limit=500):

        self.concordance = concordance(urns=urnlist(corpus), words=query, window=window, limit=limit)
        self.concordance['link'] = self.concordance.urn.apply(make_link)
        self.concordance = self.concordance[['link', 'urn', 'conc']]
        self.concordance.columns = ['link', 'urn', 'concordance']
        self.corpus = corpus
        self.size = len(self.concordance)

    def show(self, n=10, style=True):
        if style:
            result = self.concordance.sample(min(n, self.size))[
                ['link', 'concordance']].style
        else:
            result = self.concordance.sample(min(n, self.size))
        return result


class Collocations():
    """Collocations """

    def __init__(
        self,
        corpus=None,
        words=None,
        before=10,
        after=10,
        reference=None,
        samplesize=20000
    ):
        if isinstance(words, str):
            words = [words]
        coll = pd.concat(
            [
                urn_collocation(
                    urns=urnlist(corpus),
                    word=w,
                    before=before,
                    after=after,
                    samplesize=samplesize
                )
                for w in words
            ]
        )[['counts']]

        self.coll = coll.groupby(coll.index).sum()
        self.reference = reference
        self.before = before
        self.after = after

        if reference is not None:
            teller = self.coll.counts / self.coll.counts.sum()
            divisor = self.reference.freq / self.reference.freq.sum()
            self.coll['relevance'] = teller / divisor

    def show(self, sortby='counts', n=20):
        return self.coll.sort_values(by=sortby, ascending=False)

    def keywordlist(self, top=200, counts=5, relevance=10):
        mask = self.coll[self.coll.counts > counts]
        mask = mask[mask.relevance > relevance]
        return list(mask.sort_values(
            by='counts', ascending=False).head(200).index)


class Counts():
    """Provide counts for a corpus - shouldn't be too large"""

    def __init__(self, corpus=None, words=None):
        if corpus is None and words is None:
            self.counts = None
        elif not corpus is None:
            # count - if words is none result will be as if counting all words
            # in the corpus
            self.counts = get_document_frequencies(
                urns=urnlist(corpus), cutoff=0, words=words)
