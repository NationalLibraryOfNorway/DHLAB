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

from .ngram.ngram import (
    Ngram as Ngram,
    NgramBook as NgramBook,
    NgramNews as NgramNews,
)
