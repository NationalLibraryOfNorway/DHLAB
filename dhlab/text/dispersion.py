import pandas as pd

from dhlab.api.dhlab_api import get_dispersion


class Dispersion:
    """
    Wrapper class for get_dispersion
    
    Count occurrences of words in the given URN object.
    """
    def __init__(self, urn=None, wordbag=None, window=1000, pr=100):
        """:param urn: urn, defaults to None
        :type urn: str, optional
        :param wordbag: words, defaults to None
        :type wordbag: list, optional
        :param window: The number of tokens to search through per row, defaults to 1000
        :type window: int, optional
        :param pr:, defaults to 100
        :type pr: int, optional
        """
        if isinstance(wordbag, list):
            dispersion = {w: get_dispersion(urn, words=[w], window=window, pr=pr) for w in wordbag}
        elif isinstance(wordbag, dict):
            dispersion = {w: get_dispersion(urn, words=wordbag[w], window=window, pr=pr) for w in
                          wordbag}
        elif isinstance(wordbag, str):
            dispersion = {wordbag: get_dispersion(urn, words=[wordbag], window=window, pr=pr)}
        else:
            dispersion = {}
        self.dispersion = pd.DataFrame(dispersion)

    def plot(self, **kwargs):
        self.dispersion.plot(**kwargs)
