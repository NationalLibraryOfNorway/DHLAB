from dhlab.api.dhlab_api import get_places, geo_lookup, ner_from_urn
from dhlab.text.parse import NER, Models

models = Models()

class GeoData:
    """Fetch data from a book"""
    def __init__(self, urn=None, model=models[0], feature_class = None, feature_code = None):
        parse = ner_from(urn=urn)
        df = dh.NER(urn = urn, model = model).ner
        self.place_names = df[df['ner'].str.contains('LOC')]
        self.places = GeoNames(list(self.place_names.values()) , feature_class = feature_class, feature_code = feature_code)
        
class GeoNames:
    """Fetch data from a list of names"""
    def __init__(self, names, feature_class = None, feature_code = None):
        self.places = geo_lookup(names, feature_class = feature_class, feature_code = feature_code)
        
        