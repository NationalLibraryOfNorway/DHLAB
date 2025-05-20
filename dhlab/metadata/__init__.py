"""Metadata extraction."""

import lazy_loader # See `dhlab/__init__.py`

__getattr__, __dir__, _ = lazy_loader.attach(
    __name__,
    submodules = [
        "metadata",
        "natbib",
        "natbib2",
    ]
)
