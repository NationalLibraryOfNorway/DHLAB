import requests

# Norwegian word bank
def word_variant(word, form, lang = 'nob'):
    """ Find alternative form for a given word form, e.g. word_variant('spiste', 'pres-part') """
    r = requests.get("https://api.nb.no/ngram/variant_form", params={'word':word, 'form':form, 'lang':lang})
    return r.json()

def word_paradigm(word, lang = 'nob'):
    """ Find paradigm form for a word  """
    r = requests.get("https://api.nb.no/ngram/paradigm", params = {'word': word, 'lang':lang})

    return r.json()

def word_paradigm_many(wordlist, lang = 'nob'):
    """ Find alternative form for a list words """
    r = requests.post("https://api.nb.no/ngram/paradigms", json = {'words': wordlist, 'lang':lang})
    return r.json()


def word_form(word, lang = 'nob'):
    """ Find alternative form for a given word form, e.g. word_variant('spiste', 'pres-part') """
    r = requests.get("https://api.nb.no/ngram/word_form", params = {'word': word, 'lang':lang})
    return r.json()

def word_form_many(wordlist, lang = 'nob'):
    """ Find alternative forms for a list of words """
    r = requests.post("https://api.nb.no/ngram/word_forms", json = {'words': wordlist, 'lang':lang})
    return r.json()

def word_lemma(word, lang = 'nob'):
    """ Find lemma form for a given word form """
    r = requests.get("https://api.nb.no/ngram/word_lemma", params = {'word': word, 'lang':lang})
    return r.json()

def word_lemma_many(wordlist, lang = 'nob'):
    """ Find lemma form for a given word form """
    r = requests.post("https://api.nb.no/ngram/word_lemmas", json = {'words': wordlist, 'lang':lang})
    return r.json()