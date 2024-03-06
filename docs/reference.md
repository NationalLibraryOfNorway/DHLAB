This pages gives an overview of objects available at the top level of the package,
that can be imported directly from `dhlab.*`, for example: `from dhlab import Corpus`


### Classes and functions

!!! info inline end

    We recommend importing these objects directly from dhlab, e.g.:

        from dhlab import Corpus

    The internal subpackages and module structure may change.
    If you access the top level objects via full module paths,
    you may need to refactor your imports with future releases of `dhlab`.

- [`Corpus`][dhlab.text.corpus.Corpus]
- [`Ngram`][dhlab.ngram.ngram.Ngram]
- [`Chunks`][dhlab.text.chunking.Chunks]
- [`Collocations`][dhlab.text.collocations.Collocations]
- [`Concordance`][dhlab.text.concordance.Concordance]
- [`Frequencies`][dhlab.text.frequencies.Frequencies]
- [`WildcardWordSearch`][dhlab.text.wildcard.WildcardWordSearch]
- [`metadata_from_urn`][dhlab.metadata.natbib.metadata_from_urn]
- [`metadata_query`][dhlab.metadata.natbib.metadata_query]
- [`totals`][dhlab.api.dhlab_api.totals]

### Subpackages

- [`api`][dhlab.api]
- [`images`][dhlab.images]: Retrieve and analyze image data.
- [`metadata`][dhlab.metadata]: Extract metadata on objects from the digital archive.
- [`ngram`][dhlab.ngram]: Retrieve n-gram data.
- [`text`][dhlab.text]: Retrieve and analyze text data.
