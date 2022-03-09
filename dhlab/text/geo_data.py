from dhlab.api.dhlab_api import get_places


class GeoData:
    def __init__(self, urn=None):
        self.places = get_places(urn=urn)
        # [9135838, 'Kongen', 'Kongen', 62.47274, 7.6388, 'T', 'MT']
        self.places.columns = "geonameid name alternatename latitude longitude feature_class feature_code".split()
