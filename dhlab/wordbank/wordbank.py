import pandas as pd
from dhlab.api.dhlab_api import (
    word_variant, 
    word_paradigm, 
    word_paradigm_many,
    word_form, 
    word_form_many, 
    word_lemma, 
    word_lemma_many
)
from typing import Union

class WordbankSuper():
    """Super class for wordbank classes"""
    def __init__(self, frame):
        self.frame = frame
    
    def __repr__(self) -> str:
        return self.frame.__repr__()
    
    def _repr_html_(self) -> Union[str, None]:
        """
        Return the HTML representation of the DhlabObj frame attribute
        """
        return self.frame._repr_html_()


class WordParadigm(WordbankSuper):
    """Fetch inflection paradigms for a list of words, or just one word"""
    def __init__(self, words, lang='nob'):
        if isinstance(words, list):
            self.paradigms = pd.DataFrame(word_paradigm_many(words, lang))
        elif isinstance(words, str):
            self.paradigms = pd.DataFrame(word_paradigm(words, lang))
        else:
            self.paradigms = None
        
        super().__init__(self.paradigms)
            
class WordForm(WordbankSuper):
    """Fetch possible forms of a word or list of words"""
    def __init__(self, words, lang='nob'):
        if isinstance(words, list):
            self.forms = pd.DataFrame(word_form_many(words, lang))
        elif isinstance(words, str):
            self.forms = pd.DataFrame(word_form(words, lang))
        else:
            self.forms = None

        super().__init__(self.forms)
        
class WordLemma(WordbankSuper):
    """Fetch possbile lemmas for a given word form"""
    def __init__(self, words, lang='nob'):
        if isinstance(words, list):
            self.lemmas = pd.DataFrame(word_lemma_many(words, lang))
        elif isinstance(words, str):
            self.lemmas = pd.DataFrame(word_lemma(words, lang))
        else:
            self.lemmas = None
            
        super().__init__(self.lemmas)
    
    