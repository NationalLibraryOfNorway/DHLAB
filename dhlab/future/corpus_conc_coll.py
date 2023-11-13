"""Possible future funcs"""
import re

import pandas as pd
from IPython.display import HTML

import dhlab as dh
from dhlab.api.dhlab_api import (
    concordance,
    document_corpus,
    get_document_frequencies,
    get_metadata,
    urn_collocation,
)
from dhlab.text.utils import urnlist


# convert cell to a link
def make_link(row):
    r = "<a target='_blank' href = 'https://urn.nb.no/{x}'>{x}</a>".format(x=str(row))
    return r


# find hits a cell
def find_hits(x):
    return " ".join(re.findall("<b>(.+?)</b", x))


class Corpus(pd.DataFrame):
    @classmethod
    def build(
        self,
        doctype=None,
        author=None,
        freetext=None,
        fulltext=None,
        from_year=None,
        to_year=None,
        from_timestamp=None,
        to_timestamp=None,
        title=None,
        ddk=None,
        subject=None,
        lang=None,
        limit=10,
        order_by="random",
    ):
        res = document_corpus(
            doctype,
            author,
            freetext,
            fulltext,
            from_year,
            to_year,
            from_timestamp,
            to_timestamp,
            title,
            ddk,
            subject,
            lang,
            limit,
            order_by,
        )
        return Corpus(res)

    def extend_from_identifiers(self, identifiers=None):
        new_corpus = get_metadata(urnlist(identifiers))
        return pd.concat([self, new_corpus], axis=0)

    def get_freqs(self):
        return Frequencies.get_freqs(self)

    def get_concordances(self, words, window=20, limit=500):
        return Concordance.get_concordances(self, words, window=window, limit=limit)

    def get_collocations(
        self,
        #  corpus=None,
        words=None,
        before=10,
        after=10,
        reference=None,
        samplesize=20000,
        alpha=False,
        ignore_caps=False,
    ):
        return Collocations.get_collocations(
            corpus=self,
            words=words,
            before=before,
            after=after,
            reference=reference,
            samplesize=samplesize,
            alpha=alpha,
            ignore_caps=ignore_caps,
        )

    @property
    def _constructor(self):
        return Corpus


class Frequencies(pd.DataFrame):
    _metadata = ["_title_dct"]

    @classmethod
    def get_freqs(self, corpus, words=None):
        res = get_document_frequencies(urns=urnlist(corpus), words=words)
        self._title_dct = {k: v for k, v in zip(corpus.dhlabid, corpus.title)}
        return Frequencies(res)

    @property
    def _constructor(self):
        return Frequencies

    def sum_freqs(self):
        return self.sum(axis=1).to_frame("frequencies")

    def display_names(self):
        """Display data with record names as column titles."""
        return self.rename(self._title_dct, axis=1)


class Concordance(pd.DataFrame):
    @property
    def _constructor(self):
        return Concordance

    @classmethod
    def get_concordances(self, corpus, words, window=20, limit=500):
        res = concordance(urns=urnlist(corpus), words=words, window=window, limit=limit)

        res["link"] = res.urn.apply(make_link)

        res.rename({"conc": "concordance"}, axis=1, inplace=True)

        return Concordance(res)

    def show(self, n=10, style=True):
        if style:
            result = self.sample(min(n, len(self)))[["link", "concordance"]].style
        else:
            result = self.sample(min(n, len(self)))
        return result

    def split_view(self, html=False):
        df = self.concordance.str.split("</?b>", expand=True)
        df.rename(
            {0: "left", 1: "hit", 2: "right", 3: "hit2", 4: "right2"},
            axis=1,
            inplace=True,
        )
        df.index = self.urn

        if html:
            return HTML(df.to_html())
        else:
            return df


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
