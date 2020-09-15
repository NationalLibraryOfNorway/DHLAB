import requests

# Norwegian word bank
def word_variant(word, form):
    """ Find alternative form for a given word form, e.g. word_variant('spiste', 'pres-part') """
    r = requests.get("https://api.nb.no/ngram/variant_form", params={'word':word, 'form':form})
    return r.json()

def word_paradigm(word):
    """ Find paradigm form for a word  """
    r = requests.get("https://api.nb.no/ngram/paradigm", params = {'word': word})
    return r.json()

def word_paradigm_many(wordlist):
    """ Find alternative form for a list words """
    r = requests.post("https://api.nb.no/ngram/paradigms", params = {'words': wordlist})
    return r.json()


def word_form(word):
    """ Find alternative form for a given word form, e.g. word_variant('spiste', 'pres-part') """
    r = requests.get("https://api.nb.no/ngram/word_form", params = {'word': word})
    return r.json()

def word_form_many(wordlist):
    """ Find alternative forms for a list of words """
    r = requests.post("https://api.nb.no/ngram/word_forms", params = {'words': wordlist})
    return r.json()

def word_lemma(word):
    """ Find lemma form for a given word form """
    r = requests.get("https://api.nb.no/ngram/word_lemma", params = {'word': word})
    return r.json()

def word_lemma_many(wordlist):
    """ Find lemma form for a given word form """
    r = requests.post("https://api.nb.no/ngram/word_lemmas", params = {'words': wordlist})
    return r.json()