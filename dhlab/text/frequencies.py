import pandas as pd

from dhlab.api.dhlab_api import get_document_frequencies
from dhlab.text.utils import urnlist


class Frequencies(pd.DataFrame):
    _metadata = ["_title_dct"]

    @classmethod
    def get_freqs(self, corpus, words=None):
        res = get_document_frequencies(urns=urnlist(corpus), words=words)
        self._title_dct = {k: v for k, v in zip(corpus.dhlabid, corpus.title)}
        return Frequencies(res)

    @property
    def _constructor(self):
        return Frequencies

    def sum_freqs(self):
        return self.sum(axis=1).to_frame("frequencies")

    def display_names(self):
        "Display data with record names as column titles."
        return self.rename(self._title_dct, axis=1)
