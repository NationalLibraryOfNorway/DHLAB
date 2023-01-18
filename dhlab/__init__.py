# legacy code
from dhlab.text import nbtokenizer
from dhlab.legacy import (
    nbtext,
    graph_networkx_louvain,
    token_map,
    nbpictures,
    nb_external_files,
    module_update
)

# code from further down in the code tree

# text 
from dhlab.text.corpus import Corpus
from dhlab.text.chunking import Chunks
from dhlab.text.conc_coll import Collocations, Concordance, Counts
from dhlab.text.geo_data import GeoData, GeoNames
from dhlab.text.parse import NER, POS, Models
from dhlab.text.wildcard import WildcardWordSearch

# ngram 
from dhlab.ngram.ngram import Ngram, NgramBook, NgramNews

# wordbank 
from dhlab.wordbank.wordbank import WordParadigm, WordLemma, WordForm

# api
from dhlab.api.dhlab_api import totals