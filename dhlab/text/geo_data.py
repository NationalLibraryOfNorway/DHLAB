import pandas as pd

from dhlab.api.dhlab_api import get_places, geo_lookup, ner_from_urn
from dhlab.text.parse import NER, Models

spacy = Models()

class GeoData:
    """Fetch place data from a text (book, newspaper or ...) identified by URN
    with an appropriate and available spacy model. The models are gotten at by instantiaiting class Models()"""
    
    def __init__(self, urn=None, model=spacy.models[0]):
        df = NER(urn = urn, model = model).ner
        self.place_names = df[df['ner'].str.contains('LOC')]
        
    def add_geo_locations(self, feature_class = None, feature_code = None):
        """Get location data for the names in object, attribute self.place_names"""
        chunksize = 900
        names = list(self.place_names.token)
        length = len(names)
        
        # GeoNames takes 1000 names at a time so chunk things up
        # Each GeoNames object has an attribute .places a pandas dataframe
        
        chunks = [
            GeoNames(
                names[i:i+chunksize], 
                feature_class = feature_class, 
                feature_code = feature_code
            ).places for i in range(0, length, chunksize)
        ] 
        
        self.places = pd.concat(chunks) 

        
class GeoNames:
    """Fetch data from a list of names"""
    def __init__(self, names, feature_class = None, feature_code = None):
        self.places = geo_lookup(names, feature_class = feature_class, feature_code = feature_code)
        
        