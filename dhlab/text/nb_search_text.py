import pandas as pd
import networkx as nx

from ..api.nb_search_api import get_df

def phrase_plots(
    phrase_sets,
    title='aftenposten',
    fra = 1960,
    til = 2020,
    step=5,
    rot=0,
    colours = ['r', 'b','g','y','m','c']
):
    df_all = []
    for f in phrase_sets:
        df_all.append(nb.frame(get_df(f, title= title), ', '.join(f)))
    df = pd.concat(df_all, sort=False)
    df.index = df.index.astype(int)
    df = df.sort_index()
    df['bins'] = pd.cut(df.index, range(fra, til, step), precision=0)
    df.groupby('bins').sum().plot(kind='bar', color=colours, figsize=(15,5), rot=rot)
    return

def phrase_plots_anno(
    phrase_sets,
    title = 'aftenposten',
    fra = 1960,
    til = 2020,
    rot=0,
    colours = ['r', 'b','g']
):
    df_all = []
    for f in phrase_sets:
        df_all.append(nb.frame(get_df(f, title = title), ', '.join(f)))
    df = pd.concat(df_all, sort = False)
    df.index = df.index.astype(int)
    df = df.sort_index()
    #df['bins'] = pd.cut(df.index, range(fra, til, step), precision=0)
    df.plot(kind = 'bar', figsize = (15,5), rot = rot, color = colours)
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
