from typing import List, Union

import pandas as pd
from pandas import DataFrame

# import dhlab as dh
# from dhlab.text.conc_coll import Concordance, Collocations, Counts
import dhlab.text.conc_coll as dh
from dhlab.api.dhlab_api import document_corpus, evaluate_documents, get_metadata
from dhlab.text.dhlab_object import DhlabObj
from dhlab.text.utils import urnlist


class Corpus(DhlabObj):
    """Class representing as DHLAB Corpus

    Primary object for working with dhlab data. Contains references to texts
    in National Library's collections and metadata about them.
    Use with `.coll`, `.conc` or `.freq` to analyse using dhlab tools.
    """

    doctypes = [
        "digibok",
        "digavis",
        "digitidsskrift",
        "digistorting",
        "digimanus",
        "kudos",
    ]

    def __init__(
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
        allow_duplicates=False,
    ):
        """Create Corpus

        :param str doctype: ``"digibok"``, ``"digavis"``, \
            ``"digitidsskrift"`` or ``"digistorting"``
        :param str author: Name of an author.
        :param str freetext: any of the parameters, for example:\
            ``"digibok AND Ibsen"``.
        :param str fulltext: words within the publication.
        :param int from_year: Start year for time period of interest.
        :param int to_year: End year for time period of interest.
        :param int from_timestamp: Start date for time period of interest.
            Format: ``YYYYMMDD``, books have ``YYYY0101``
        :param int to_timestamp: End date for time period of interest.
            Format: ``YYYYMMDD``, books have ``YYYY0101``
        :param str title: Name or title of a document.
        :param str ddk: `Dewey Decimal Classification \
            <https://no.wikipedia.org/wiki/Deweys_desimalklassifikasjon>`\
                _ identifier.
        :param str subject: subject (keywords) of the publication.
        :param str lang: Language of the publication, as a 3-letter ISO code.
            Example: ``"nob"`` or ``"nno"``
        :param int limit: number of items to sample.
        """

        if (
            doctype
            or author
            or freetext
            or fulltext
            or from_year
            or to_year
            or from_timestamp
            or to_timestamp
            or title
            or ddk
            or lang
        ):
            self.corpus = document_corpus(
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

        else:
            self.corpus = pd.DataFrame(columns=["urn"])

        super().__init__(self.corpus)

        self.frame.rename(
            columns={
                "urn": "urn",
                "authors": "author",
                "langs": "language",
                "genres": "genre",
            },
            inplace=True,
        )

        if not allow_duplicates:
            self._check_for_urn_duplicates()

    @classmethod
    def from_identifiers(cls, identifiers: List[Union[str, int]]):
        """Construct Corpus from list of identifiers"""
        corpus = Corpus()
        corpus.extend_from_identifiers(identifiers=identifiers)
        return corpus

    @classmethod
    def from_df(cls, df: DataFrame, check_for_urn: bool = False):
        """Typecast Pandas DataFrame to Corpus class

        DataFrame most contain URN column"""

        # If Series, return as is
        if isinstance(df, pd.Series):
            return df

        df = df.copy()  # Avoid modifying original DataFrame

        corpus = Corpus()
        if check_for_urn:
            corpus.corpus = cls._urn_id_in_dataframe_cols(df)
        else:
            corpus.corpus = df
        corpus.frame = corpus.corpus
        return corpus

    @classmethod
    def from_csv(cls, path: str):
        """Import corpus from csv"""
        df = pd.read_csv(path)
        return cls.from_df(df)

    @staticmethod
    def _urn_id_in_dataframe_cols(
        dataframe: Union[DataFrame, type("Corpus")]
    ) -> DataFrame:
        """Checks if dataframe contains URN column"""
        if "urn" in dataframe.columns:
            if dataframe.urn.str.contains("^URN:NBN:no-nb_.+").all():
                return dataframe
        raise ValueError("No'urn'-column in dataframe.")

    def extend_from_identifiers(self, identifiers: list = None):
        new_corpus = get_metadata(urnlist(identifiers))
        self.add(new_corpus)

    def evaluate_words(self, wordbags=None):
        df = evaluate_documents(wordbags=wordbags, urns=list(self.corpus.urn))
        df.index = df.index.astype(int)
        cols = df.columns
        df = pd.concat(
            [df, self.corpus[["dhlabid", "urn"]].set_index("dhlabid")], axis=1
        )
        df = df.set_index("urn")
        return df[cols].fillna(0)

    def add(self, new_corpus: Union[DataFrame, type("Corpus")]):
        """Utility for appending Corpus or DataFrame to self"""
        if isinstance(new_corpus, Corpus):
            new_corpus = new_corpus.frame
        self.frame = pd.concat([self.frame, new_corpus])
        self.corpus = self.frame
        self._drop_urn_duplicates()
        # self.size = len(self.frame)

    def sample(self, n: int = 5):
        """Create random subkorpus with `n` entries"""
        n = min(n, self.size)
        sample = self.corpus.sample(n).copy()
        return self.from_df(sample)

    def only_one_author(self):
        """Only select items with one author"""
        mask = self.frame.author.apply(lambda x: len(x.split("/"))) == 1
        return self.from_df(self.frame[mask])

    def only_one_language(self):
        """Only select items with one language"""
        mask = self.frame.language.apply(lambda x: len(x.split("/"))) == 1
        return self.from_df(self.frame[mask])

    def conc(self, words, window: int = 20, limit: int = 500) -> dh.Concordance:
        """Get concodances of `words` in corpus"""
        return dh.Concordance(
            corpus=self.frame, query=words, window=window, limit=limit
        )

    def coll(
        self,
        words=None,
        before=10,
        after=10,
        reference=None,
        samplesize=20000,
        alpha=False,
        ignore_caps=False,
    ) -> dh.Collocations:
        """Get collocations of `words` in corpus"""
        return dh.Collocations(
            corpus=self.frame,
            words=words,
            before=before,
            after=after,
            reference=reference,
            samplesize=samplesize,
            alpha=alpha,
            ignore_caps=ignore_caps,
        )

    def count(self, words=None):
        """Get word frequencies for corpus"""
        return dh.Counts(self, words)

    def freq(self, words=None):
        """Get word frequencies for corpus"""
        return dh.Counts(self, words)

    @staticmethod
    def _is_Corpus(corpus: "Corpus") -> bool:
        """Check if `input` is Corpus or DataFrame"""
        if type(corpus) not in [DataFrame, Corpus]:
            raise TypeError("Input is not Corpus or DataFrame")
        return isinstance(corpus, Corpus) | isinstance(corpus, DataFrame)

    def __add__(self, other):
        """Add two Corpus objects"""
        if not self._is_Corpus(other):
            raise TypeError("Input is not Corpus or DataFrame")
        new = self.from_df(pd.concat([self.frame, other.frame]).reset_index(drop=True))
        new._drop_urn_duplicates()

        return new

    def _make_subcorpus(self, **kwargs) -> "Corpus":
        dct = kwargs.copy()
        year_range = dct.pop("year_range", None)

        for key in dct.keys():
            if key not in self.frame.columns:
                print(f"Key {key} not in corpus")
                return None

        # Make result dataframe
        res = self.frame.copy()

        # Get year range
        if year_range is not None:
            y1 = int(year_range[0])
            y2 = int(year_range[1])

            # Apply year range
            res = res.loc[res["year"] >= y1].loc[res["year"] <= y2]

        for key, val in dct.items():
            res = res.loc[res[key].str.contains(val)]

        return self.from_df(res)

    def make_subcorpus(self, authors: str = None, title: str = None) -> "Corpus":
        """Make subcorpus based on author and title

        Args:
            authors (str, optional): search for author field. Defaults to None.
            title (str, optional): search title field. Defaults to None.

        Returns:
            Corpus: A subset of the original corpus
        """
        dct = {}
        if authors is not None:
            dct["author"] = authors
        if title is not None:
            dct["title"] = title

        return self._make_subcorpus(**dct)

    def check_integrity(self):
        """Check the integrity of the corpus data."""

        def test_dhlabid_series(series: pd.Series) -> bool:
            """Check if dhlabid series is valid"""
            if not series.apply(lambda x: isinstance(x, int)).all():
                return False
            if not ((series >= 1e8) & (series < 1e9)).all():
                return False

            return True

        def test_urn_series(series: pd.Series) -> bool:
            """Check if URN series is valid"""
            if series.str.startswith("URN:NBN:no-nb_").all():
                return True
            try:
                series = series.apply(lambda x: int(x))
                return test_dhlabid_series(series)
            except:
                return False

        # Check if the DataFrame is empty
        if self.corpus.empty:
            raise ValueError("Corpus is empty.")

        # Check for the presence of essential columns
        required_columns = ["urn", "dhlabid", "author", "language", "genre"]
        for col in required_columns:
            if col not in self.corpus.columns:
                raise ValueError(f"Essential column '{col}' is missing.")

        # Validate dhlabid format
        if not test_dhlabid_series(self.corpus["dhlabid"]):
            raise ValueError("Some dhlabid values are in an incorrect format.")

        # Validate URN format
        if not test_urn_series(self.corpus["urn"]):
            raise ValueError("Some URN values are in an incorrect format.")

        return True

    def _check_for_urn_duplicates(self):
        """Check for duplicate URNs in corpus"""
        if self.frame.urn.duplicated().any():
            self._drop_urn_duplicates()

    def _drop_urn_duplicates(self, reset_index=True):
        """Drop duplicate URNs in corpus

        dhlab sometimes contains multiple versions of the text for a text object.
        Usually these are different OCR results. This method drops all but the last as this is usually the best.
        Dhlabid is always unique."""

        if len(self.frame) == 0:
            return

        self.frame.sort_values(by="dhlabid", inplace=True)
        self.frame.drop_duplicates(subset="urn", inplace=True, keep="last")
        if reset_index:
            self.frame.reset_index(drop=True, inplace=True)
        self.corpus = self.frame
