from nbtokenizer import tokenize
from collections import Counter
from bs4 import BeautifulSoup
import os
import pandas as pd

def text_from_html_file(filename):
    """Get a flat list of tokens from a file"""
    with open(filename, encoding='utf-8') as f:
        content = f.read()
    soup = BeautifulSoup(content, 'html.parser')
    text = []
    for para in soup.find_all('p'):
        text += tokenize(para.text)
    return text

def growth_diagram_from_text(tekst, ordlister, window = 5000, pr = 100):
    """serier fra ordlistene sammen 
    ordlister er en dictionary eller en liste av en liste over ord"""
    rammer = dict()
    c = dict()
    if isinstance(ordlister, list):
        if isinstance(ordlister[0], list):
            for l in ordlister:
                if l != []:
                    c[l[0]] = l
        else:
            c[ordlister[0]] = ordlister
    else:
        c = ordlister
    for key in c:
        rammer[key] = []
    for i in range(0, len(tekst), pr):
        # count words of size windows - check below if text is overrun
        word_counts = Counter(tekst[i : i + window])
        for key in c:
            key_counts = sum([word_counts[word] for word in c[key]])
            rammer[key].append(key_counts)
        if i + window > len(tekst):
            break
    return pd.DataFrame(rammer)