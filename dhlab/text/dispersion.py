import pandas as pd

from dhlab.api.dhlab_api import get_dispersion


class Dispersion:
    def __init__(self, urn=None, wordbag=None, window=1000, pr=100):
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
