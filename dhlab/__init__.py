"""The dhlab python library provides functions and objects
to retrieve and analyze image and text data from the digital collection of the National Library of Norway.

You can build text corpora, retrieve their metadata, search for images, and do quantitative analyses.

The dhlab python package calls the [DHLAB API](https://api.nb.no/dhlab/) under the hood to retrieve data.
"""

# Lazy imports - https://scientific-python.org/specs/spec-0001/
import lazy_loader

# For backwards-compatibility (not a heavy import).
import nb_tokenizer as nbtokenizer

# `lazy_loader.attach_stub(...)` looks for imports in `__init__.pyi`, and lazily
# imports them.
#   - Must be used in favor of `lazy_loader.attach(...)` in order to give
#     static analyzers (LSP/code completion, mypy, etc) knowledge of the
#     lazy-loaded modules.
#
#   - A submodule's `__init__.py` needs to explicitly expose any submodules.
#         Do this using `lazy_loader.attach(...)` (or `lazy_loader.attach_stub(...)
#         in the case of further nesting) to retain lazy-loading.
#         See: `dhlab/legacy/__init__.py`
#
#   - More information:
#         https://scientific-python.org/specs/spec-0001/#type-checkers
#         `dhlab/__init__.pyi`
__getattr__, __dir__, __all__ = lazy_loader.attach_stub(__name__, __file__)
