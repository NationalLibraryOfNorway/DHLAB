"""Handle a corpus of digital objects (books, newspapers, etc.)"""
import pandas as pd

from dhlab.api.dhlab_api import document_corpus, get_metadata
from dhlab.text.collocations import Collocations
from dhlab.text.concordance import Concordance
from dhlab.text.frequencies import Frequencies
from dhlab.text.utils import remove_empty_columns, urnlist


class Corpus(pd.DataFrame):
    """Collection of metadata about digital objects (books, newspapers, etc.).

    Examples:
        >>> from dhlab import Corpus
        >>> Corpus.build(doctype='digibok', limit=5)
            dhlabid                                  urn                                              title  ...  doctype ocr_creator ocr_timestamp
        0  100131623  URN:NBN:no-nb_digibok_2013012306066  Jeg vil bestemt avvise at jeg snakker tåkete :...  ...  digibok          nb      20060101
        1  100130790  URN:NBN:no-nb_digibok_2013012306049                              Viser for vêr og vind  ...  digibok          nb      20060101
        2  100452778  URN:NBN:no-nb_digibok_2008080500063  The King's many bodies : the self-destruction ...  ...  digibok          nb      20060101
        3  100205526  URN:NBN:no-nb_digibok_2014051308028  Samling af Eksempler til Indøvelse af Grammati...  ...  digibok          nb      20060101
        4  100145471  URN:NBN:no-nb_digibok_2013041908040                                          Vilt blod  ...  digibok          nb      20060101

    The attributes of the corpus are the same as for a
    [pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html),
    with metadata columns for the text objects in the corpus.

    Attributes:
        dhlabid (int): Unique, internal identifier for the digital text object in the NLN digital archive.
        urn (str): Uniform Resource Name (URN) for the scanned document.
        oaiid (str): Unique identifier for the metadata of the publication.
        sesamid (str): Hash string of the metadata identifier.
        isbn10 (str): International Standard Book Number (ISBN) for the publication.
        title (str): Title of the document.
        authors (str): Authors of the document.
        year (int): Year of publication.
        timestamp (int): Timestamp of the publication.
            Only relevant for newspapers.
            Will revert to 1st of January of the year of publication for books.
        city (str): City of publication.
        publisher (str): Publisher of the document.
        langs (str): Language(s) of the document.
        subjects (str): Subject/topic(s) of the document.
        ddc (str): Dewey Decimal Classification (DDC) of the document.
        doctype (str): Type of document (e.g. digibok, avis, tidsskrift, etc.).
        literaryform (str): Literary form of the document (e.g. skjønnlitteratur, faglitteratur, etc.).
        ocr_creator (str): Creator of the digital text object generated with optical character recognition (OCR).
        ocr_timestamp (int): Timestamp of the OCR process.
    """

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
