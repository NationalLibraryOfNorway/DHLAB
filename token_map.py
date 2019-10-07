import pandas as pd
import os
from nbtext import make_network_name_graph, token_map, urn_concordance
import requests

def token_map_names(tmap): 
    return [
    [z[0][0] for z in (tmap) if len(z[0]) == 1]
] + [
    [z[0] for z in (tmap) if len(z[0]) == 2]
] + [
    [z[0] for z in (tmap) if len(z[0]) == 3]
]+ [
    [z[0] for z in (tmap) if len(z[0]) == 4]
]


# create a character network with only tokens in tokenmap
# see nb.make_network_name_graph in nbtext



def names_to_token_map_file(wp, filename='', orient='column'):
    """Save token map to file for editing, exit if file exists"""
    
    # check  exit conditions
    if filename != '':
        if os.path.exists(filename):
            print('filen {f} eksisterer - prøve et nytt filnavn'.format(f=filename))
            return 
    else:
        print('angi et filnavn')
        return
        
    # if all ok go ahead
    
    table_names = dict()
    #print(wp)
    tmap = token_map(wp)
    ##print(tmap)
    for (name, target) in tmap:
        x_str = ' '.join(target)
        y_str = ' '.join(name)
        if x_str in table_names:
            table_names[x_str].append(y_str)
        else:
            table_names[x_str] = [y_str]
    
    dfs = []
    for x in table_names:
        dfs.append( pd.DataFrame({x:table_names[x]}))
    df = pd.concat(dfs, axis=1)
    if orient == 'row':    
        df = df.transpose()
    rv = True
    if filename.endswith('csv'):
        df.to_csv(filename)
    elif filename.endswith('xls'):
        df.to_excel(filename, index = orient == "row")
    else:
        rv = df
    return rv

def read_token_map_file(filename, sep=', ', orient = 'column'):
    """Read a token map from file, either xls or csv"""
    
    if filename.endswith('xls'):
        res = pd.read_excel(filename, index_col=0 ).dropna(how='all').fillna('')
    elif filename.endswith('csv'):
        res = pd.read_csv(filename, sep=sep, index_col=0).dropna(how='all').fillna('')
    if orient.startswith('row'):
        res = res.transpose()
    result = []
    for x in res:
        xt = tuple(x.split())
        for value in res[x]:
            vt = tuple(value.split())
            if vt != ():
                result.append((vt, xt))
    return result


def show_names(wp):
    """Display found names with frequency"""
    i = 1
    for c in wp:
        print('Lag', i)
        print("=========")
        print()
        i += 1
        for x in c.most_common():
            if isinstance(x[0], str):
                print("   ", x[0] + ' - ' + str(x[1]))
            else:
                print("   ", ' '.join(x[0]) + ' - ' + str(x[1]))
        print()
        
def character_network(urn, token_map, names = None):
    if names == None:
        names = token_map_names(token_map)
    return make_network_name_graph(urn, names, tokenmap = token_map)

from nbtext import names
from collections import Counter

def count_name_strings(urn, token_map, names=None):
    """ return a count of the names in tokenmap"""
    if names == None:
        names = token_map_names(token_map)
    
    if isinstance(urn, list):
        urn = urn[0]
        
    # tokens should be a list of list of tokens. If it is list of dicts pull out the keys (= tokens)   
    #if isinstance(tokens[0], dict):
    #    tokens = [list(x.keys()) for x in tokens]
        
    res = requests.post("https://api.nb.no/ngram/word_counts", json={'urn':urn, 'tokens':names, 'tokenmap':token_map})
    #print(r.text)
   
    return pd.read_json(res.json()).sort_values(by=0, ascending = False)

def corpus_names(corpus, ratio=0.5, cutoff = 10):
    # check status of corpus if it is a frame or a list of list 
    # for now assume it is a list of URNs
    urn_names = dict()
    for urn in corpus:
        try:
            urn_names[urn] = names(urn, ratio = ratio, cutoff = cutoff)
        except:
            print("Fikk ikke laget navn for:", urn)
    return urn_names

def combine_names(namedict):
    total_names = [Counter(), Counter(), Counter(), Counter()]
    for urn in namedict:
        for i in range(4):
            total_names[i] += namedict[urn][i]
    return total_names

def filter_names(tm_names, gazetteers):
    from collections import Counter
    """Filter name findings using a gazetteer - the gazetteer should consist of a list of first and last names"""
    
    # check single names
    def member(w, gazetteer):
        res = False
        if w in gazetteer:
            res = True
        elif w[-1] == 's' and w[:-1] in gazetteer:
            res = True
        return res
    
    def add_name(name_struct, struct, val):
        size = len(name_struct)
        if 0 < size <= 4:
            #print(size, name_struct)
            #print(struct)
            if size == 1:
                name_struct = name_struct[0]
            if name_struct in struct[size]:
                struct[size][name_struct] += val
            else:
                struct[size][name_struct] = val
        return struct
    
    name_structure = [Counter(), Counter(), Counter(), Counter()]
    single_names = Counter()
    single_remove = Counter()
    for w in tm_names[0]:
        if member(w, gazetteers) :
            single_names[w] = tm_names[0][w]
        else:
            single_remove[w] = tm_names[0][w]
    
    name_structure[0].update(single_names)

    # check double names (check for genitives)
    double_names = Counter()
    double_remove = Counter()
    doubles = tm_names[1]
    for w in doubles:
        new_token = []
        for token in w:
            #print(token)
            if member(token, gazetteers):
                new_token.append(token)
        new_token = tuple(new_token)
        #print(new_token)
        val = 0
        if new_token != ():
            name_structure = add_name(new_token, name_structure, doubles[w])
        else:
            double_remove[w] = doubles[w]
    
    # check triple names (check for genitives)
    triple_names = Counter()
    triple_remove = Counter()
    triples = tm_names[2]
    for w in triples:
        new_token = []
        for token in w:
            #print(token)
            if member(token, gazetteers):
                new_token.append(token)
        new_token = tuple(new_token)
        #print(new_token)
        val = 0
        if new_token != ():
            name_structure = add_name(new_token, name_structure, triples[w])
        else:
            triple_remove[w] = triples[w]
            
    # check quadruple names (check for genitives)
    quad_names = Counter()
    quad_remove = Counter()
    quads = tm_names[3]
    for w in quads:
        new_token = []
        for token in w:
            #print(token)
            if member(token, gazetteers):
                new_token.append(token)
        new_token = tuple(new_token)
        #print(new_token)
        val = 0
        if new_token != ():
            name_structure = add_name(new_token, name_structure, quads[w])
        else:
            quad_remove[w] = quads[w]


    return {'filtered': tuple(name_structure),
            'removed': (single_remove, double_remove, triple_names, quad_names)}
        
