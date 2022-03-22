from datetime import datetime

from dhlab.api.dhlab_api import ngram_book, ngram_news
from dhlab.ngram.nb_ngram import nb_ngram
from dhlab.text.dhlab_object import DhlabObj
class Ngram(DhlabObj):
    """Top level class for ngrams"""

    def __init__(self,
                 words=None,
                 from_year=None,
                 to_year=None,
                 doctype='bok',
                 mode='relative',
                 lang="nob",
                 **kwargs
                 ):
        """Ngram builder class.

        Build Ngrams from the National Librarys collections.
        Use with book corpus or newspaper corpus.
        Lang parameter is only supported for book (`bok`) corpus.
        Defaults to `None` if doctype is `avis`.

        :param words: words to examine, defaults to None
        :type words: str or list of str, optional
        :param from_year: lower period cutoff, defaults to None
        :type from_year: int, optional
        :param to_year: upper period cutoff, defaults to None
        :type to_year: int, optional
        :param doctype: `bok` or `avis` , defaults to 'bok'
        :type doctype: str, optional
        :param mode: Frequency measure, defaults to 'relative'
        :type mode: str, optional
        :param lang: `nob`, `nno`. Only use with docytype='bok', defaults to 'nob'
        :type lang: str, optional
        :param \**kwargs: Keyword arguments for  Ngram._ipython_display_() Ngram.plot()
        """

        self.date = datetime.now()
        if to_year is None:
            to_year = self.date.year
        if from_year is None:
            from_year = 1950

        self.from_year = from_year
        self.to_year = to_year
        self.words = words
        self.lang = lang
        if doctype is not None:
            if 'bok' in doctype:
                doctype = 'bok'
            elif 'avis' in doctype:
                doctype = 'avis'
            else:
                doctype = 'bok'
        else:
            doctype = 'bok'

        # Set default lang for 'bok'-corpus
        if doctype == "avis":
            lang = None


        ngrm = nb_ngram(terms=', '.join(words),
                        corpus=doctype,
                        years=(from_year, to_year),
                        smooth = 1, lang = lang,
                        mode=mode)
        ngrm.index = ngrm.index.astype(str)
        self.ngram = ngrm

        self.kwargs = kwargs

        super().__init__(self.ngram)

    def plot(self, smooth = 4, **kwargs):
        """:param smooth: smoothing the curve"""
        grf = self.ngram.rolling(window=smooth, win_type='triang').mean()
        grf.plot(**kwargs)

    def compare(self, another_ngram):
        """Divide one ngram by another - measures difference"""
        start_year = max(datetime(self.from_year, 1, 1),
                         datetime(another_ngram.from_year, 1, 1)).year
        end_year = min(datetime(self.to_year, 1, 1), datetime(another_ngram.to_year, 1, 1)).year
        transposed_ngram = self.ngram.loc[str(start_year):str(end_year)].transpose()
        sum_other_ngram = another_ngram.ngram[str(start_year):str(end_year)].transpose().sum()
        compare = (transposed_ngram / sum_other_ngram).transpose()
        return compare

    def _ipython_display_(self):
        self.plot(**self.kwargs)

class NgramBook(Ngram):
    """Extract ngrams using metadata with functions to be inherited."""

    def __init__(
            self,
            words=None,
            title=None,
            publisher=None,
            city=None,
            lang='nob',
            from_year=None,
            to_year=None,
            ddk=None,
            subject=None,
            **kwargs
        ):
        """Create Dhlab Ngram from metadata

        :param words: words to examine, defaults to None
        :type words: str or list of str optional
        :param title: _description_, defaults to None
        :type title: _type_, optional
        :param publisher: _description_, defaults to None
        :type publisher: _type_, optional
        :param city: _description_, defaults to None
        :type city: _type_, optional
        :param lang: _description_, defaults to 'nob'
        :type lang: str, optional
        :param from_year: _description_, defaults to None
        :type from_year: _type_, optional
        :param to_year: _description_, defaults to None
        :type to_year: _type_, optional
        :param ddk: _description_, defaults to None
        :type ddk: _type_, optional
        :param subject: _description_, defaults to None
        :type subject: _type_, optional
        :return: _description_
        :rtype: _type_
        """

        super().__init__(words, from_year = from_year,
                         to_year = to_year, lang = lang, doctype = 'bok', **kwargs)
        self.date = datetime.now()
        if to_year is None:
            to_year = self.date.year
        if from_year is None:
            from_year = 1950
        self.from_year = from_year
        self.to_year = to_year
        self.words = words
        self.title = title
        self.publisher = publisher
        self.city = city
        self.lang = lang
        self.ddk = ddk
        self.subject = subject
        self.ngram = ngram_book(word=words, title=title, publisher=publisher, lang=lang, city=city,
                                period=(from_year, to_year), ddk=ddk, topic=subject)
        # update frame attribute
        self.frame = self.ngram
        # self.cohort =  (self.ngram.transpose()/self.ngram.transpose().sum()).transpose()


class NgramNews(Ngram):
    def __init__(
            self,
            words=None,
            title=None,
            city=None,
            from_year=None,
            to_year=None,
            **kwargs
    ):
        super().__init__(words, from_year = from_year, to_year = to_year, doctype = 'avis', **kwargs)
        self.date = datetime.now()
        self.from_year = 1950 if from_year is None else from_year
        self.to_year = self.date.year if to_year is None else to_year
        self.words = words
        self.title = title
        self.ngram = ngram_news(word=words, title=title, period=(from_year, to_year))
        # update frame attribute
        self.frame = self.ngram
        # self.cohort =  (self.ngram.transpose()/self.ngram.transpose().sum()).transpose()
