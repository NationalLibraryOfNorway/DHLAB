#!/usr/bin/env python
# coding: utf-8

# # La oss jobbe med dokumenter lasta ned fra Internett, Språkrådet!

# In[1]:


import json
import pandas as pd
import dhlab.nbtext as nb
from collections import Counter
from scipy.spatial import distance


# ### Funksjonalitet for å sjekke målform og mellomlagre nynorske dokumenter

# In[2]:


generating = False
nob_json = "https://raw.githubusercontent.com/Yoonsen/Modules/master/trigram_lang_model/nob_trilangmodel.json"
nno_json = "https://raw.githubusercontent.com/Yoonsen/Modules/master/trigram_lang_model/nno_trilangmodel.json"

def char_ngram_freqs(n=3, lang='nob', epochs=4):
    ngram = lambda x: [x[i:i+n] for i in range(len(x))] 
    sents = []
    freqs = Counter()
    
    for i in range(epochs):
        sents += nb.sentences(nb.book_urn(limit=20, lang=lang, period=(1990, 2020)))
    
    trigrams = list(map(ngram, sents))
    for t in trigrams: 
        freqs.update(t)
    
    return freqs

def ngramify(txt, n=3, c=300):
    ngram = lambda x: [x[i:i+n] for i in range(len(x))]
    freqs = Counter()
    freqs.update(ngram(txt))
    
    return freqs.most_common(c)
    

def nobornno(text, nob, nno):
    return 1 - distance.cosine(nno, text) > 1 - distance.cosine(nob, text)


# In[3]:


# Generating character n-gram frequences from random sentences in the bibliography between 1990 and 2020;
# Note that this can take a while ...
if generating == True:
    nob = char_ngram_freqs(epochs = 10)
    nno = char_ngram_freqs(lang='nno', epochs = 10)

    json.dump(nob, open('trigram_lang_model/nob_trilangmodel.json','w', encoding='utf-8'))
    json.dump(nno, open('trigram_lang_model/nno_trilangmodel.json','w', encoding='utf-8'))
else:
    nob = json.load(open(nob_json))
    nno = json.load(open(nno_json))


# In[ ]:





# In[4]:


# Checking whether the pages in a document is Nynorsk or Bokmål,
# and chaching if we can assume that it is.
def check_text(text):
        doc = dict(ngramify(text, n = 3, c = 300))
        df = pd.DataFrame.from_dict({'nno':nno, 'nob':nob, 'doc':doc}, 
                                    orient='index').transpose().fillna(0)
        return {'nno': 1 - distance.cosine(df['nno'], df['doc']), 'nob': 1 - distance.cosine(df['nob'], df['doc'])}
            


# In[5]:


#check_text('dette er galt')

