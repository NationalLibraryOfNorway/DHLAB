"""Text analysis functionality, including building text corpora."""

import lazy_loader

__getattr__, __dir__, __all__ = lazy_loader.attach_stub(__name__, __file__)

# For backwards-compatibility (not a heavy import).
from nb_tokenizer import (
    Tokens as Tokens,
    tokenize as tokenize,
)
