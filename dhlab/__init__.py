# api
from dhlab.api.dhlab_api import totals

# legacy code
from dhlab.legacy import (
    graph_networkx_louvain,
    module_update,
    nb_external_files,
    nbpictures,
    nbtext,
    token_map,
)

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
