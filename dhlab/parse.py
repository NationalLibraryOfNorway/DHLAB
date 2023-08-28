import pandas as pd
import requests

from pandas import DataFrame
from typing import Union, List, Tuple, Dict
from dhlab.constants import BASE_URL

class Models:
    """Show the spaCy language models available"""
    def __init__(self):
        self.models = show_spacy_models()
        
    def __repr__(self):
        return "\n".join(sorted(self.models))
        
class NER:
    """Provide NER """
    def __init__(self, urn=None, model=None, start_page=0, to_page=0):
        self.model = model
        self.frame = ner_from_urn(urn=urn, model=self.model, start_page=start_page, to_page=to_page)
        
class POS:
    """Provide POS and a parse"""
    def __init__(self, urn=None, model=None, start_page=0, to_page=0):
        self.model = model
        self.frame = pos_from_urn(urn=urn, model=self.model, start_page=start_page, to_page=to_page)


def ner_from_urn(urn: str = None, model: str = None, start_page = 0, to_page = 0) -> DataFrame:
    """Get NER annotations for a text (``urn``) using a spacy ``model``.

    :param str urn: uniform resource name, example: ``URN:NBN:no-nb_digibok_2011051112001``
    :param str model: name of a spacy model.
        Check which models are available with :func:`show_spacy_models`
    :return: Dataframe with annotations and their frequencies
    """

    params = locals()
    r = requests.get(f"{BASE_URL}/ner_urn", params=params)
    df = pd.read_json(r.json())
    return df

def pos_from_urn(urn: str = None, model: str = None, start_page = 0, to_page = 0) -> DataFrame:
    """Get part of speech tags and dependency parse annotations for a text (``urn``) with a SpaCy ``model``.

    :param str urn: uniform resource name, example: ``URN:NBN:no-nb_digibok_2011051112001``
    :param str model: name of a spacy model.
        Check which models are available with :func:`show_spacy_models`
    :return: Dataframe with annotations and their frequencies
    """
    params = locals()
    r = requests.get(f"{BASE_URL}/pos_urn", params=params)
    df = pd.read_json(r.json())
    return df


def show_spacy_models() -> List:
    """Show available SpaCy model names."""
    try:
        r = requests.get(f"{BASE_URL}/ner_models")
        #r.raise_for_status()
        res = r.json()
    except: #(HTTPError, JSONDecodeError, ConnectionError) as error:
        #print(error.__doc__, error)
        print("Server-request gikk ikke gjennom. Kan ikke vise SpaCy-modellnavn.")
        res =  []
    return res