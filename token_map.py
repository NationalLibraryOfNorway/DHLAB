import pandas as pd
import os
from nbtext import make_network_name_graph, token_map, urn_concordance


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
        df.to_excel(filename, index = False)
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

def count_name_strings(urn, token_map, names=None):
    """ return a count of the names in tokens"""
    if names == None:
        names = token_map_names(token_map)
    
    if isinstance(urn, list):
        urn = urn[0]
        
    # tokens should be a list of list of tokens. If it is list of dicts pull out the keys (= tokens)   
    if isinstance(tokens[0], dict):
        tokens = [list(x.keys()) for x in tokens]
        
    res = requests.post("https://api.nb.no/ngram/word_counts", json={'urn':urn, 'tokens':names, 'tokenmap':tokenmap})
    #print(r.text)
   
    return res
        
def character_network(urn, token_map, names = None):
    if names == None:
        names = token_map_names(token_map)
    return make_network_name_graph(urn, names, tokenmap = token_map)
