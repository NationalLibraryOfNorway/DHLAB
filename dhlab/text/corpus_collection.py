from typing import Dict, Optional

from dhlab.text.corpus import Corpus


class CorpusCollection:
    """A class for handling a collection of corpora."""

    def __init__(self, corpora: Optional[Dict[str, Corpus]] = None):
        """Initialize the class with a dictionary of corpora."""
        self.corpora = corpora if corpora is not None else {}

    def __getitem__(self, key: str) -> Corpus:
        """Get a corpus by name."""
        return self.corpora[key]

    def __setitem__(self, key: str, value: Corpus):
        """Set a corpus by name."""
        self.corpora[key] = value

    def __repr__(self) -> str:
        """Print the names of the corpora."""
        return "\n".join(self.corpora.keys())

    def __iter__(self):
        """Iterate over the names of the corpora."""
        for c in self.corpora:
            yield c

    def __len__(self) -> int:
        """Return the number of corpora."""
        return len(self.corpora)

    def __contains__(self, key: str) -> bool:
        """Check if a corpus is in the collection."""
        return key in self.corpora

    def add(self, name: str, corpus: Corpus):
        """Add a corpus to the collection."""
        self.corpora[name] = corpus

    def remove(self, name: str):
        """Remove a corpus from the collection."""
        del self.corpora[name]

    def get(self, name: str) -> Corpus:
        """Get a corpus by name."""
        return self.corpora[name]

    def show_corpora(self) -> Dict[str, Corpus]:
        """Show the corpora in the collection."""
        return self.corpora

    def concat_corpora(self) -> Corpus:
        """Concatenate all corpora in the collection into a single corpus."""
        new_corpus = Corpus()
        for c in self.corpora.values():
            new_corpus += c
        return new_corpus
