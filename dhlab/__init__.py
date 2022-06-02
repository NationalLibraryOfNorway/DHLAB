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
from dhlab.text.corpus import Corpus
from dhlab.text.chunking import Chunks
from dhlab.text.conc_coll import Collocations, Concordance, Counts
from dhlab.text.geo_data import GeoData
from dhlab.ngram.ngram import Ngram, NgramBook, NgramNews

from dhlab.wordbank.wordbank import WordParadigm, WordLemma, WordForm