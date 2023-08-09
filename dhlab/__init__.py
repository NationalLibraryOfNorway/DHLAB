"""Retrieve data from the digital collection of the National Library of Norway.

Build text or image corpora, retrieve their metadata, and do quantitative analyses.

Examples:

    >>> import dhlab as dh
    >>> word_frequencies = dh.totals(5)
            freq
    .   7655423257
    ,   5052171514
    i   2531262027
    og  2520268056
    -   1314451583
    >>> corpus = dh.Corpus.build(doctype='digibok', limit=5)
        dhlabid                                  urn                                              title  ...  doctype ocr_creator ocr_timestamp
    0  100131623  URN:NBN:no-nb_digibok_2013012306066  Jeg vil bestemt avvise at jeg snakker tåkete :...  ...  digibok          nb      20060101
    1  100130790  URN:NBN:no-nb_digibok_2013012306049                              Viser for vêr og vind  ...  digibok          nb      20060101
    2  100452778  URN:NBN:no-nb_digibok_2008080500063  The King's many bodies : the self-destruction ...  ...  digibok          nb      20060101
    3  100205526  URN:NBN:no-nb_digibok_2014051308028  Samling af Eksempler til Indøvelse af Grammati...  ...  digibok          nb      20060101
    4  100145471  URN:NBN:no-nb_digibok_2013041908040                                          Vilt blod  ...  digibok          nb      20060101

    [5 rows x 19 columns]


Subpackages exported by this package:

- `api`: Python wrappers for API calls to the databases containing NLN's digital archive.
- `images`: Retrieve and analyze image data.
- `metadata`: Extract metadata on objects from the digital archive.
- `ngram`: Retrieve n-gram data.
- `text`: Retrieve and analyze text data.
- `utils`: Utility functions.

Modules exported at the top level of this package:

- `constants`: Constant variables used across modules.
- `nbpictures`: Retrieve and analyze image data.
- `nbtokenizer`: Tokenize text.

Classes and functions exported at the top level of this package:
- `Corpus`
- `Ngram`
- `Chunks`
- `Collocations`
- `Concordance`
- `Frequencies`
- `WildcardWordSearch`
- `metadata_from_urn`
- `metadata_query`
- `totals`
"""

# api
from dhlab.api.dhlab_api import totals

# metadata
from dhlab.metadata.natbib import metadata_from_urn, metadata_query

# ngram
from dhlab.ngram.ngram import Ngram

# text
from dhlab.text.chunking import Chunks
from dhlab.text.collocations import Collocations
from dhlab.text.concordance import Concordance
from dhlab.text.corpus import Corpus
from dhlab.text.frequencies import Frequencies
from dhlab.text.wildcard import WildcardWordSearch

# utils
from dhlab.utils.display import css
from dhlab.utils.files import download_from_github, get_file_from_github
