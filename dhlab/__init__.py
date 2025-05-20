"""The dhlab python library provides functions and objects
to retrieve and analyze image and text data from the digital collection of the National Library of Norway.

You can build text corpora, retrieve their metadata, search for images, and do quantitative analyses.

The dhlab python package calls the [DHLAB API](https://api.nb.no/dhlab/) under the hood to retrieve data.
"""

# Lazy imports - https://scientific-python.org/specs/spec-0001/
import lazy_loader

# `lazy_loader.attach_stub(...)` looks for imports in `__init__.pyi`, and lazily
# imports them.
#   - Must be used in favor of `lazy_loader.attach(...)` in order to give
#     static analyzers (LSP/code completion, mypy, etc) knowledge of the
#     lazy-loaded modules.
#
#   - A submodule's `__init__.py` still needs to explicitly expose the
#     modules/attributes.
#         Do this using `lazy_loader.attach(...)` (or `lazy_loader.attach_stub(...)
#         in the case of further nesting) to retain lazy-loading.
#         See: `dhlab/legacy/__init__.py`
#
#   - More information:
#         https://scientific-python.org/specs/spec-0001/#type-checkers
#         `dhlab/__init__.pyi`
__getattr__, __dir__, __all__ = lazy_loader.attach_stub(__name__, __file__)

# api
from dhlab.api.dhlab_api import totals

# metadata
from dhlab.metadata.natbib import metadata_from_urn, metadata_query

# ngram
from dhlab.ngram.ngram import Ngram, NgramBook, NgramNews

# text
from dhlab.text import nbtokenizer
from dhlab.text.chunking import Chunks
from dhlab.text.conc_coll import Collocations, Concordance, Counts
from dhlab.text.corpus import Corpus
from dhlab.text.dispersion import Dispersion
from dhlab.text.geo_data import GeoData, GeoNames
from dhlab.text.parse import NER, POS, Models
from dhlab.text.wildcard import WildcardWordSearch
from dhlab.utils.display import css
from dhlab.utils.files import download_from_github, get_file_from_github

# wordbank
from dhlab.wordbank.wordbank import WordForm, WordLemma, WordParadigm
