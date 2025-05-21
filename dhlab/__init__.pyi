# Declare modules to be lazily loaded using lazy_loader.attach_stub()
#
# More information:
#     https://scientific-python.org/specs/spec-0001/#type-checkers
#     `dhlab/__init__.py` comments
#

# The explicit import style `import module_name as module_name` is
# necessary due to PEP 484.
#     More information: https://scientific-python.org/specs/spec-0001/#type-checkers
from .legacy import (
    graph_networkx_louvain  as graph_networkx_louvain,
    module_update           as module_update,
    nb_external_files       as nb_external_files,
    nbpictures              as nbpictures,
    nbtext                  as nbtext,
    token_map               as token_map,
)

from .api.dhlab_api import totals as totals

from .metadata.natbib import (
    metadata_from_urn as metadata_from_urn,
    metadata_query as metadata_query,
)

from .metadata.natbib import (
    metadata_from_urn       as metadata_from_urn,
    metadata_query          as metadata_query,
)

from .ngram.ngram import (
    Ngram as Ngram,
    NgramBook as NgramBook,
    NgramNews as NgramNews,
)

from .text.chunking import Chunks as Chunks
from .text.conc_coll import (
    Collocations as Collocations,
    Concordance as Concordance,
    Counts as Counts,
)
from .text.corpus import Corpus as Corpus
from .text.dispersion import Dispersion as Dispersion
from .text.geo_data import GeoData as GeoData
from .text.parse import (
    NER as NER,
    POS as POS,
    Models as Models,
)
from .text.wildcard import WildcardWordSearch as WildcardWordSearch

from .utils.display import css as css
from .utils.files import (
    download_from_github as download_from_github,
    get_file_from_github as get_file_from_github,
)

from .wordbank.wordbank import (
    WordForm as WordForm,
    WordLemma as WordLemma,
    WordParadigm as WordParadigm,
)
