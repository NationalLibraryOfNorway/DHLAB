import pandas as pd

from dhlab.api.dhlab_api import document_corpus, get_metadata
from dhlab.text.collocations import Collocations
from dhlab.text.concordance import Concordance
from dhlab.text.frequencies import Frequencies
from dhlab.text.utils import remove_empty_columns, urnlist


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
        return remove_empty_columns(Corpus(res))

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
