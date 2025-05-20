import lazy_loader # See `dhlab/__init__.py`

__getattr__, __dir__, _ = lazy_loader.attach(
    __name__,
    submodules = [
        "graph_networkx_louvain",
        "module_update",
        "nb_external_files",
        "nbpictures",
        "nbtext",
        "token_map",
    ],
)
