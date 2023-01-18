from pandas import DataFrame
import pandas as pd
from dhlab.text.dhlab_object import DhlabObj
from dhlab.api.dhlab_api import document_corpus, get_metadata, evaluate_documents
import dhlab as dh
from dhlab.text.utils import urnlist
# from dhlab.text.conc_coll import Concordance, Collocations, Counts


class Corpus(DhlabObj):
    """Class representing as DHLAB Corpus

    Primary object for working with dhlab data. Contains references to texts
    in National Library's collections and metadata about them.
    Use with `.coll`, `.conc` or `.freq` to analyse using dhlab tools.
    """
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
            ):

        if (doctype
            or author
            or freetext
            or fulltext
            or from_year
            or to_year
            or from_timestamp
            or to_timestamp
            or title
            or ddk
            or lang):
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
                limit
            )

        else:
            self.corpus = pd.DataFrame(columns=["urn"])

        super().__init__(self.corpus)
        self.size = len(self.corpus)
        
    @classmethod
    def from_identifiers(cls, identifiers):
        """Construct Corpus from list of identifiers"""
        corpus = Corpus()
        corpus.extend_from_identifiers(identifiers=identifiers)
        return corpus
        

    @classmethod
    def from_df(cls, df, check_for_urn=False):
        """Typecast Pandas DataFrame to Corpus class

        DataFrame most contain URN column"""
        corpus = Corpus()
        if check_for_urn:
            corpus.corpus = cls._urn_id_in_dataframe_cols(df)
        else:
            corpus.corpus = df
        corpus.frame = corpus.corpus
        corpus.size = len(corpus.corpus)
        return corpus

    @classmethod
    def from_csv(cls, path):
        """Import corpus from csv"""
        df = pd.read_csv(path)
        return cls.from_df(df)

    @staticmethod
    def _urn_id_in_dataframe_cols(dataframe):
        """Checks if dataframe contains URN column"""
        if "urn" in dataframe.columns:
            if dataframe.urn.str.contains("^URN:NBN:no-nb_.+").all():
                return dataframe
        raise ValueError("No'urn'-column in dataframe.")

    def extend_from_identifiers(self, identifiers=None):
        new_corpus = get_metadata(urnlist(identifiers))
        self.add(new_corpus)

    def evaluate_words(self, wordbags = None):
        df = evaluate_documents(wordbags = wordbags, urns = list(self.corpus.urn))
        df.index = df.index.astype(int)
        cols = df.columns
        df = pd.concat([df, self.corpus[['dhlabid','urn']].set_index('dhlabid')], axis = 1)
        df = df.set_index('urn')
        return df[cols].fillna(0)

    def add(self, new_corpus):
        """Utility for appending Corpus or DataFrame to self"""
        if self._is_Corpus(new_corpus):
            new_corpus = new_corpus.frame
        self.frame = pd.concat([self.frame, new_corpus]).drop_duplicates().reset_index(drop=True)
        self.corpus = self.frame
        self.size = len(self.frame)

    def sample(self, n=5):
        "Create random subkorpus with `n` entries"
        n = min(n, self.size)
        sample = self.corpus.sample(n).copy()
        return self.from_df(sample)

    def conc(self, words, window=20, limit=500):
        "Get concodances of `words` in corpus"
        return dh.Concordance(corpus=self.frame, query=words, window=window, limit=limit)

    def coll(
        self,
        words=None,
        before=10,
        after=10,
        reference=None,
        samplesize=20000,
        alpha=False,
        ignore_caps=False):
        "Get collocations of `words` in corpus"
        return dh.Collocations(
            corpus=self.frame,
            words=words,
            before=before,
            after=after,
            reference=reference,
            samplesize=samplesize,
            alpha=alpha,
            ignore_caps=ignore_caps
            )

    def count(self, words=None):
        return dh.Counts(self.frame, words)

    @staticmethod
    def _is_Corpus(corpus) -> bool:
        """Check if `input` is Corpus or DataFrame"""
        if type(corpus) not in [DataFrame, Corpus]:
            raise TypeError("Input is not Corpus or DataFrame")
        return isinstance(corpus, Corpus)



