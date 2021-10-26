import dhlab.nbtext as nb
import dhlab.graph_networkx_louvain as gnl
import dhlab.nbtokenizer as tok
from dhlab.module_update import css, update, code_toggle

import requests
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns



def get_json(frases, mediatype='aviser', title='*', metadata = False):
    import requests
    
    querystring = " + ".join(['"'+frase+'"' for frase in frases])
    
    if metadata == False:
        search_type = 'FIELD_RESTRICTED_SEARCH'
    else:
        search_type = 'FULL_TEXT_SEARCH'
        
    query = {
        'q':querystring,
        'size':1,
        'snippets':mediatype,
        'aggs':'year',
        
       'filter':['mediatype:{mt}'.format(mt=mediatype),'title:{title}'.format(title=title)],
        'searchType': search_type
        #'filter':
    }
    r = requests.get("https://api.nb.no/catalog/v1/items", params = query)
    
    aggs = r.json()
    
    return aggs

def get_data(frase, media='aviser', title='jazznytt'):
    import requests
    query = {
        'q':'"'+frase+'""',
        'size':1,
        'aggs':'year',
        'filter':['mediatype:{mt}'.format(mt=media),'title:{title}'.format(title=title)]
    }
    r = requests.get("https://api.nb.no/catalog/v1/items", params = query)
    return r.json()



def get_df_pd(frase, media='bøker'):
    import pandas as pd
    return pd.DataFrame.from_dict(get_df(frase, media=media ), orient='index').sort_index()

def phrase_plots(phrase_sets, title='aftenposten', fra = 1960, til = 2020, step=5, rot=0, colours = ['r', 'b','g','y','m','c']):
    df_all = []
    for f in phrase_sets:
        df_all.append(nb.frame(get_df(f, title= title), ', '.join(f)))
    df = pd.concat(df_all, sort=False)
    df.index = df.index.astype(int)
    df = df.sort_index()
    df['bins'] = pd.cut(df.index, range(fra, til, step), precision = 0)
    df.groupby('bins').sum().plot(kind='bar', color=colours, figsize=(15,5), rot=rot)
    return

def phrase_plots_anno(phrase_sets, title='aftenposten', fra = 1960, til = 2020, rot=0, colours = ['r', 'b','g']):
    df_all = []
    for f in phrase_sets:
        df_all.append(nb.frame(get_df(f, title= title), ', '.join(f)))
    df = pd.concat(df_all, sort=False)
    df.index = df.index.astype(int)
    df = df.sort_index()
    #df['bins'] = pd.cut(df.index, range(fra, til, step), precision=0)
    df.plot(kind='bar', figsize=(15,5), rot=rot, color=colours)
    return

def graph_from_df(df, threshold = 100):
    edges =  []
    normalizer = {(x, y): df.stack()[(x,x)]*df.stack()[(y,y)] for (x,y) in df.stack().index}
    for (x, y) in df.stack().index:
        if x != y:
            if df.stack()[(x,y)] > threshold:
                edges.append([x,y,df.stack()[(x,y)]/normalizer[(x,y)]])
    G = nx.Graph()
    G.add_weighted_edges_from(edges)
    return G

def super_search(title, number=50, page=0, mediatype='aviser', period = (18000101, 20401231)):
    """Søk etter term og få ut json"""
    number = min(number, 50)
    r = requests.get(
        "https://api.nb.no:443/catalog/v1/items", 
         params = { 
             'filter':[
                 'mediatype:{mediatype}'.format(mediatype=mediatype),
                 'title:{title}'.format(title=title),
                 'date:[{date_from} TO {date_to}]'.format(date_from = period[0], date_to = period[1])
             ],
             'page':page, 
             'size':number
         }
    )
    return r.json()

def get_df_level(frases, title='*', coord = 'OR', media='aviser', period = (18000101, 20401231)):
    """Get dokument frequencies for phrases, coordinated with coord OR AND or +"""
    import requests
    coord = " " + coord + " "
    querystring = coord.join(['"'+frase+'"' for frase in frases])
    if media == 'bøker':
        agg_level = 'year'
    elif media == 'tidsskrift':
        agg_level = 'year,month'
    else:
        agg_level = 'year,month,day'
    query = {
        'q':querystring,
        'size':1,
        'aggs':agg_level,
        'filter':[
            'mediatype:{mt}'.format(mt=media),
            'title:{title}'.format(title=title),
            'date:[{date_from} TO {date_to}]'.format(date_from = period[0], date_to = period[1])
        ]
        
    }
    r = requests.get("https://api.nb.no/catalog/v1/aggregations", params = query)
    aggs = r.json()['_embedded']['aggregations'][0]['buckets']
    df = create_frame_from_bucket(aggs) #{x['key']:x['count'] for x in aggs}
    df.columns = [querystring]
    return df

def phrase_plots_level(phrase_set, title='*', period=(20100101, 20301231), media='aviser'):
    df_all = [nb.frame(get_df_level(f, title = title, period = period, media=media), ', '.join(f)) for f in phrase_set]
    df = pd.concat(df_all, sort=False, axis=1)
    return df



def term_urn_search(term, number=50, page=0, mediatype='aviser', period=(18000101, 20401231)):
    """Søk etter term og få ut json"""
    number = min(number, 50)
    #print(period)
    r = requests.get(
        "https://api.nb.no:443/catalog/v1/search", 
         params = { 
             'q':term,
             'sort':'date,desc',
            
             'filter':[
                 'mediatype:{mediatype}'.format(mediatype=mediatype),
                 'date:[{date_from} TO {date_to}]'.format(date_from = period[0], date_to = period[1] )
             ],
             'page':page, 
             'size':number,
             'random':'true'
         }
    )
    res = r.json()
    tot = res['totalElements']
    if tot > 0:
        result = res['_embedded']['mediaTypeResults'][0]['result']['_embedded']['items']
        urns = [r['metadata']['identifiers']['urn'] for r in result]
    else:
        urns = []
    return tot, urns

def term_docs(term, number=50, page=0, mediatype='aviser', period=(18000101, 20401231)):
    """Søk etter term og få ut json"""
    number = min(number, 50)
    #print(period)
    r = requests.get(
        "https://api.nb.no:443/catalog/v1/search", 
         params = { 
             'q':term,
             'sort':'date,desc',
            
             'filter':[
                 'mediatype:{mediatype}'.format(mediatype=mediatype),
                 'date:[{date_from} TO {date_to}]'.format(date_from = period[0], date_to = period[1] )
             ],
             'page':page, 
             'size':number,
             'random':'true'
         }
    )
    res = r.json()
    tot = res['totalElements']
    if tot > 0:
        result = res['_embedded']['mediaTypeResults'][0]['result']['_embedded']['items']
        urns = [r['metadata']['identifiers']['urn'] for r in result]
    else:
        urns = []
    return tot, urns

def get_konks(urn, phrase, window=1000, n = 1000):
    import requests
    querystring = '"'+ phrase +'"' 
    query = {
        'q':querystring,
        'fragments': n,
        'fragSize':window
       
    }
    r = requests.get("https://api.nb.no/catalog/v1/items/{urn}/contentfragments".format(urn=urn), params = query)
    res = r.json()
    results = []
    try:
        for x in res['contentFragments']:
            urn = x['pageid']
            hit = x['text']
            splits = hit.split('<em>')
            s2 = splits[1].split('</em>')
            before = splits[0]
            word = s2[0]
            after = s2[1]
            results.append({'urn': urn, 'before': before, 'word':word, 'after':after})
    except:
        True
    return results

def get_phrase_info(urn, phrase, window=1000, n = 1000):
    import requests
    querystring = '"'+ phrase +'"' 
    query = {
        'q':querystring,
       
    }
    r = requests.get("https://api.nb.no/catalog/v1/items/{urn}/contentfragments".format(urn=urn), params = query)
    res = r.json()
    return res

def get_all_konks(term, urns):
    konks = []
    for u in urns:
        konks += get_konks(u, term)
    return konks
