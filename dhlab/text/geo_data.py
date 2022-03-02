import pandas as pd
from pandas import DataFrame

from ..api.dhlab_api import get_places

# [9135838, 'Kongen', 'Kongen', 62.47274, 7.6388, 'T', 'MT']
class GeoData():
    def __init__(self, urn=None):
        self.places = pd.DataFrame(get_places(urn=urn), columns="geonameid name alternatename latitude longitude feature_class feature_code".split())
    
