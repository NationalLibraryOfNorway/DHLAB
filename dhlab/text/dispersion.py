import pandas as pd
from ..api.dhlab_api import get_dispersion

class Dispersion():
    def __init__(self, urn=None, wordbags=None, window=1000, pr=100):
        if isinstance(wordbags, list):
            self.dispersion = {w:get_dispersion(urn, words=[w], window=window, pr=pr) for w in wordbags}
        elif isinstance(wordbags, dict):
            self.dispersion = {w:get_dispersion(urn, words=wordbags[w], window=window, pr=pr) for w in wordbags}
        elif isinstance(wordbags,str):
            self.dispersion = {w:get_disperion(urn, words=[w], window=window, pr=pr)}
        else
            self.dispersion = {}
            
    def plot(**kwargs):
        self.dispersion.plot()