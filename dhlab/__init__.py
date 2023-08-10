"""The dhlab library subpackages and modules contain functions and objects
to retrieve and analyze data from the digital collection of the National Library of Norway.

You can build text corpora, retrieve their metadata, search for images, and do quantitative analyses.

## Objects available at the top level of the package (`dhlab.*`)

### Subpackages

- `api`: Python wrappers for API calls to the databases containing NLN's digital archive.
- `images`: Retrieve and analyze image data.
- `metadata`: Extract metadata on objects from the digital archive.
- `ngram`: Retrieve n-gram data.
- `text`: Retrieve and analyze text data.
- `utils`: Utility functions.

### Modules

- `constants`: Constant variables used across modules.
- `nbpictures`: Retrieve and analyze image data.
- `nbtokenizer`: Tokenize text.

### Classes and functions

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


Examples:
    >>> from dhlab import totals, Corpus
    >>> totals(5)                          # get the 5 most frequent words in the whole digital text collection
            freq
    .   7655423257
    ,   5052171514
    i   2531262027
    og  2520268056
    -   1314451583

    >>> Corpus.build(doctype='digibok', limit=5)        # build a corpus of 5 books
        dhlabid                                  urn                                              title  ...  doctype ocr_creator ocr_timestamp
    0  100380777  URN:NBN:no-nb_digibok_2018061307595                           Meldal rotaryklubb 50 år  ...  digibok          nb      20060101
    1  100539747  URN:NBN:no-nb_digibok_2011051808092                  Peter : fisker, discipel, apostel  ...  digibok          nb      20060101
    2  100284614  URN:NBN:no-nb_digibok_2016022548132                             Barcelona og Catalonia  ...  digibok          nb      20060101
    3  100184299  URN:NBN:no-nb_digibok_2009060904091                   Det kan komme fine dager : roman  ...  digibok          nb      20060101
    4  100363545  URN:NBN:no-nb_digibok_2018021305017  Miljølære i grunnskolen : [for barnetrinnet]. ...  ...  digibok          nb      20060101
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
