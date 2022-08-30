import pandas as pd

from dhlab.api.dhlab_api import ner_from_urn, pos_from_urn, show_spacy_models

class Models:
    """Show the spaCy language models available"""
    def __init__(self):
        self.models = show_spacy_models()
        
class NER:
    """Provide NER """
    def __init__(self, urn=None, model=None):
        self.model = model
        self.ner = ner_from_urn(urn=urn, model=self.model)
        
class POS:
    """Provide POS and a parse"""
    def __init__(self, urn=None, model=None):
        self.model = model
        self.pos = pos_from_urn(urn=urn, model=self.model)

