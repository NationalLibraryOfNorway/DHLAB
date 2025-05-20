# """Python wrappers for API calls to the databases containing NLN's digital archive."""

import lazy_loader # See `dhlab/__init__.py`

__getattr__, __dir__, _ = lazy_loader.attach(
    __name__,
    submodules = [
        "dhlab_api",
        "nb_ngram_api",
        "nb_search_api",
    ]
)
