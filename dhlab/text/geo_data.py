import pandas as pd

from dhlab.api.dhlab_api import get_places, geo_lookup, ner_from_urn
from dhlab.text.parse import NER, Models


class GeoData:
    """Fetch place data from a text (book, newspaper or ...) identified by URN
    with an appropriate and available spacy model.

    The models are retrieved by instantiating :py:class:`~text.parse.Models`.
    """
    
    def __init__(self, urn=None, model=None):
        self.place_names = self._fetch_place_names(urn, model)
        

    def _fetch_place_names(self, urn, model):
        try:
            assert urn is not None
            spacy = Models()
            model = model if model is not None else spacy.models[0]
            df = NER(urn = urn, model = model).ner
            place_names = df[df['ner'].str.contains('LOC')]
        except AssertionError:
            print("Please provide a document URN to fill the ``place_names`` dataframe attribute.")
            place_names = pd.DataFrame()
        except IndexError as error:
            print("GeoData couldn't load any SpaCy NER models.")
            place_names = pd.DataFrame()
        except Exception as error:
            print(error.__doc__, error)
            place_names = pd.DataFrame()
        return place_names


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
        
        