import re

import pandas as pd

import dhlab as dh
from dhlab.api.dhlab_api import concordance, get_document_frequencies, urn_collocation
from dhlab.text.dhlab_object import DhlabObj
from dhlab.text.utils import urnlist


# convert cell to a link
def make_link(row):
    r = "<a target='_blank' href = 'https://urn.nb.no/{x}'>{x}</a>".format(x=str(row))
    return r


# find hits a cell
def find_hits(x):
    return " ".join(re.findall("<b>(.+?)</b", x))


class Concordance(DhlabObj):
    """Wrapper for concordance function"""

    def __init__(self, corpus=None, query=None, window=20, limit=500):
        """Get concordances for word(s) in corpus

        :param corpus: Target corpus, defaults to None
        :param query: word or list or words, defaults to None
        :param window: how many tokens to consider around the target word, \
            defaults to 20
        :param limit: limit returned hits, defaults to 500
        """

        if corpus is None:
            self.concordance = pd.DataFrame()
            self.corpus = None
        else:
            self.concordance = concordance(
                urns=urnlist(corpus), words=query, window=window, limit=limit
            )
            self.concordance["link"] = self.concordance.urn.apply(make_link)
            self.concordance = self.concordance[["link", "urn", "conc"]]
            self.concordance.columns = ["link", "urn", "concordance"]
            self.corpus = corpus
        # self.size = len(self.concordance)

        super().__init__(self.concordance)

    def show(self, n=10, style=True):
        if style:
            result = self.concordance.sample(min(n, self.size))[
                ["link", "concordance"]
            ].style
        else:
            result = self.concordance.sample(min(n, self.size))
        return result
    
    @classmethod
    def from_df(cls, df):
        "Typecast DataFrame to Concordance"
        obj = Concordance()
        obj.concordance = df
        obj.frame = df
        return obj


class Collocations(DhlabObj):
    """Collocations"""

    def __init__(
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
        """Create collocations object

        :param corpus: target corpus, defaults to None
        :type corpus: dh.Corpus, optional
        :param words: target words(s), defaults to None
        :type words: str or list, optional
        :param before: words to include before, defaults to 10
        :type before: int, optional
        :param after: words to include after, defaults to 10
        :type after: int, optional
        :param reference: reference frequency list, defaults to None
        :type reference: pd.DataFrame, optional
        :param samplesize: _description_, defaults to 20000
        :type samplesize: int, optional
        :param alpha: Only include alphabetical tokens, defaults to False
        :type alpha: bool, optional
        :param ignore_caps: Ignore capitalized letters, defaults to False
        :type ignore_caps: bool, optional
        """
        if isinstance(words, str):
            words = [words]

        coll = pd.concat(
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

        if alpha:
            coll = coll.loc[[x for x in coll.index if x.isalpha()]]
            if reference is not None:
                reference = reference.loc[[x for x in reference.index if x.isalpha()]]

        if ignore_caps:
            coll.index = [x.lower() for x in coll.index]
            if reference is not None:
                reference.index = [x.lower() for x in reference.index]

        self.coll = coll.groupby(coll.index).sum()
        self.reference = reference
        self.before = before
        self.after = after

        if reference is not None:
            teller = self.coll.counts / self.coll.counts.sum()
            divisor = self.reference.iloc[:, 0] / self.reference.iloc[:, 0].sum()
            self.coll["relevance"] = teller / divisor

        super().__init__(self.coll)

    def show(self, sortby="counts", n=20):
        return self.coll.sort_values(by=sortby, ascending=False).head(n)

    def keywordlist(self, top=200, counts=5, relevance=10):
        mask = self.coll[self.coll.counts > counts]
        mask = mask[mask.relevance > relevance]
        return list(mask.sort_values(by="counts", ascending=False).head(200).index)

    @classmethod
    def from_df(cls, df):
        """Typecast DataFrame to Collocation

        :param df: DataFrame
        :return: Collocation
        """
        obj = Counts()
        obj.counts = df
        obj.frame = df
        return obj


class Counts(DhlabObj):
    """Provide counts for a corpus - shouldn't be too large"""

    def __init__(self, corpus=None, words=None):
        """Get frequency list for Corpus

        :param corpus: target Corpus, defaults to None
        :param words: list of words to be counted, defaults to None
        """
        if corpus is None and words is None:
            self.freq = pd.DataFrame()
            self.title_dct = None
        elif corpus is not None:
            # Make sure corpus is a dhlab corpus
            # if not, try to make it one
            # if isinstance(corpus, pd.DataFrame):
            #     corpus = dh.Corpus.from_df(corpus)
            
            # if not isinstance(corpus, dh.Corpus):
            #     raise TypeError("Corpus must be of type dh.Corpus or pd.DataFrame")

            # count - if words is none result will be as if counting all words
            # in the corpus
            self.freq = get_document_frequencies(
                urns=urnlist(corpus), cutoff=0, words=words
            )

            # Include dhlab and title link in object
            try:
                self.title_dct = {
                    k: v for k, v in zip(corpus.frame.dhlabid, corpus.frame.title)
                }
            except:
                self.title_dct = None

            # Add relative frequencies if available
            if words is not None:
                self.relfreq = self.freq.relfreq
                self.freq = self.freq.freq

        super().__init__(self.freq)

    def sum(self):
        """Summarize Corpus frequencies

        :return: frequency list for Corpus
        """
        return self.from_df(self.counts.sum(axis=1).to_frame("freq"))

    def display_names(self):
        "Display data with record names as column titles."
        assert self.title_dct is not None, "No titles available"            
        return self.frame.rename(self.title_dct, axis=1)
    
    def display_rel_names(self):
        "Display relfreq data with record names as column titles."
        return self.relfreq.rename(self.title_dct, axis=1)

    @classmethod
    def from_df(cls, df):
        obj = Counts()
        obj.freq = df
        obj.frame = df
        return obj

    ### Legacy properties and methods ###

    @property
    def counts(self):
        "Legacy property for freq"
        return self.freq

