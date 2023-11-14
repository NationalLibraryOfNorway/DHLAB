from datetime import datetime

import pandas as pd

from dhlab.api.dhlab_api import ngram_book, ngram_news
from dhlab.ngram.nb_ngram import nb_ngram


class Ngram(pd.DataFrame):
    """A sketch for a new Ngram class."""

    _metadata = ["from_year", "to_year"]

    @property
    def _constructor(self):
        return Ngram

    @classmethod
    def build(
        self,
        words=None,
        from_year=1950,
        to_year=datetime.now().year,
        doctype="bok",
        mode="relative",
        lang="nob",
        **kwargs
    ):
        res = nb_ngram(
            terms=", ".join(words),
            corpus=doctype,
            years=(from_year, to_year),
            lang=lang,
            mode=mode,
        )

        return Ngram(res)

    @classmethod
    def from_news(
        self,
        words=None,
        title=None,
        city=None,
        from_year=1950,
        to_year=datetime.now().year,
        **kwargs
    ):
        res = ngram_news(word=words, period=(from_year, to_year))

        return Ngram(res)

    @classmethod
    def from_book(
        self,
        words=None,
        title=None,
        publisher=None,
        city=None,
        lang="nob",
        from_year=1950,
        to_year=datetime.now().year,
        ddk=None,
        subject=None,
        **kwargs
    ):
        res = ngram_book(
            word=words,
            title=title,
            publisher=publisher,
            lang=lang,
            city=city,
            period=(from_year, to_year),
            ddk=ddk,
            topic=subject,
        )

        self.from_year = from_year
        self.to_year = to_year

        return Ngram(res)

    def ngram_plot(self, smooth=4, **kwargs):
        grf = self.rolling(window=smooth, win_type="triang").mean()
        grf.plot(**kwargs)

    def compare(self, another_ngram):
        """Divide one ngram by another - measures difference"""
        start_year = max(
            datetime(self.from_year, 1, 1), datetime(another_ngram.from_year, 1, 1)
        ).year
        end_year = min(
            datetime(self.to_year, 1, 1), datetime(another_ngram.to_year, 1, 1)
        ).year
        transposed_ngram = self.loc[str(start_year) : str(end_year)].transpose()
        sum_other_ngram = (
            another_ngram[str(start_year) : str(end_year)].transpose().sum()
        )
        compare = (transposed_ngram / sum_other_ngram).transpose()
        return compare
