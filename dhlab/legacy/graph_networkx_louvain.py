from collections import Counter

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import requests
import seaborn as sns
from community import community_louvain
from matplotlib import colors as mcolors
from matplotlib.pylab import rcParams
from networkx.algorithms.community import k_clique_communities

from dhlab.legacy.nbtext import urn_coll, urn_coll_words, frame, get_freq, make_graph_from_result

colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
rcParams['figure.figsize'] = 15, 10


def cutdown(x):
    return x.subgraph([n[0] for n in x.degree() if n[1] > 1])


def make_graph_corp(word, corpus='eng'):
    query = (
        f"http://www.nb.no/sp_tjenester/beta/ngram_1/galaxies/query"
        f"?terms={word}&lang=all&corpus={corpus}"
    )
    result = requests.get(query)
    return make_graph_from_result(result)


def make_graph(word):
    query = f"http://www.nb.no/sp_tjenester/beta/ngram_1/galaxies/query?terms={word}"
    result = requests.get(query)
    return make_graph_from_result(result)


def draw_graph(G, nodelist: list = None, h=15, v=10, fontsize=12, layout=nx.spring_layout,
               arrows=False, node_color='orange', node_size=100,
               font_color='black'):
    if nodelist is not None:
        G = G.subgraph(nodelist)
    x, y = rcParams['figure.figsize']
    rcParams['figure.figsize'] = h, v
    pos = layout(G)
    ax = plt.subplot()
    ax.set_xticks([])
    ax.set_yticks([])
    nx.draw_networkx_labels(G, pos, font_size=fontsize, font_color=font_color)
    nx.draw_networkx_nodes(G, pos, alpha=0.1, node_color=node_color,
                           node_size=node_size)
    nx.draw_networkx_edges(G, pos, alpha=0.7, arrows=arrows,
                           edge_color='lightblue')

    rcParams['figure.figsize'] = x, y


def draw_graph_centrality(G, h=15, v=10, deltax=0, deltay=0, fontsize=18, k=0.2,
                          arrows=False, node_alpha=0.3, l_alpha=1,
                          node_color='blue', centrality=nx.degree_centrality,
                          font_color='black', threshold=0.01, multi=3000):
    node_dict = centrality(G)
    subnodes = dict(
        {x: node_dict[x] for x in node_dict if node_dict[x] >= threshold})
    x, y = rcParams['figure.figsize']
    rcParams['figure.figsize'] = h, v

    ax = plt.subplot()
    ax.set_xticks([])
    ax.set_yticks([])
    G = G.subgraph(subnodes)
    pos = nx.spring_layout(G, k=k)
    labelpos = {k: (v[0] + deltax, v[1] + deltay) for k, v in pos.items()}
    # print(labelpos)
    # print(pos)
    if l_alpha <= 1:
        nx.draw_networkx_labels(G, labelpos, font_size=fontsize, alpha=l_alpha,
                                font_color=font_color)
    nx.draw_networkx_nodes(G, pos, alpha=node_alpha,
                           node_color=range(len(subnodes.keys())),
                           # Cannot find reference 'Blues' in 'cm.py'
                           cmap=plt.cm.Blues, nodelist=subnodes.keys(),
                           node_size=[v * multi for v in subnodes.values()])
    nx.draw_networkx_edges(G, pos, alpha=0.4, arrows=arrows,
                           edge_color='lightblue')

    rcParams['figure.figsize'] = x, y


def draw_graph_centrality2(G, Subsets=None, h=15, v=10, deltax=0, deltay=0,
                           fontsize=18, k=0.2, arrows=False,
                           node_alpha=0.3, l_alpha=1, node_color='blue',
                           centrality=nx.degree_centrality,
                           font_color='black',
                           threshold=0.01,
                           multi=3000,
                           edge_color='olive',
                           edge_alpha=0.1,
                           colstart=0.2,
                           coldark=0.5):
    if Subsets is None:
        Subsets = []
    # W0621: Redefining name 'colors' from outer scope (line 16)
    # (redefined-outer-name)
    # W0612: Unused variable 'colors'
    colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
    node_dict = centrality(G)
    subnodes = {x: node_dict[x]
                for x in node_dict if node_dict[x] >= threshold}
    x, y = rcParams['figure.figsize']
    rcParams['figure.figsize'] = h, v

    ax = plt.subplot()
    ax.set_xticks([])
    ax.set_yticks([])
    # G = G.subgraph(subnodes)
    glob_col = sns.hls_palette(len(G), h=colstart, l=coldark)[0]
    pos = nx.spring_layout(G, k=k)
    labelpos = {k: (v[0] + deltax, v[1] + deltay) for k, v in pos.items()}
    # print(labelpos)
    # print(pos)
    if l_alpha <= 1:
        nx.draw_networkx_labels(G, labelpos, font_size=fontsize, alpha=l_alpha,
                                font_color=font_color)
    sub_color = 0  # W0612: Unused variable 'sub_color' (unused-variable)
    if Subsets != []:
        i = 0
        colpalette = sns.hls_palette(len(Subsets), h=colstart, l=coldark)
        # print(colpalette)
        for Sub in Subsets:
            sublist = dict({x: subnodes[x] for x in subnodes if x in Sub})
            # print(sublist)
            # sub_col = list(colors.values())[np.random.randint(20,100)]
            sub_col = colpalette[i]
            # print(i, sub_col, sublist.keys())
            # print(i, sub_col)
            nx.draw_networkx_nodes(G, pos, alpha=node_alpha,
                                   node_color=[sub_col],
                                   nodelist=list(sublist.keys()),
                                   node_size=[v * multi for v in
                                              sublist.values()])
            i += 1
    else:
        nx.draw_networkx_nodes(G, pos, alpha=node_alpha, node_color=glob_col,
                               nodelist=subnodes.keys(),
                               node_size=[v * multi for v in subnodes.values()])

    nx.draw_networkx_edges(G, pos, alpha=edge_alpha, arrows=arrows,
                           edge_color=edge_color)

    rcParams['figure.figsize'] = x, y


# Set palette using: sns.hls_palette(10, h=.6, l=.1)


def sentrale(Graph, top=20):
    # mc = Counter([('ord',0)])
    # SubGraph = nx.Graph()
    # SubGraph.add_edges_from([(x,y) for (x,y) in Graph.edges() \
    #   if Graph.degree(x)>1 and Graph.degree(y)>1])
    # if Graph.__len__() > 0:
    mc = Counter(nx.closeness_centrality(Graph)).most_common(top)
    return mc


def mcommunity(Graph, random=10):
    G = Graph.to_undirected()

    m_partition = community_louvain.best_partition(G, random_state=random)
    # print(m_partition)
    list_nodes = []
    for com in set(m_partition.values()):
        list_nodes += [
            {nodes for nodes in m_partition.keys(
            ) if m_partition[nodes] == com}
        ]
    return list_nodes


def kcliques(agraph):
    i = 3
    x = list(k_clique_communities(agraph, i))
    comms = {}
    while x and isinstance(x, list):
        # print(x)
        j = 1
        for el in x:
            comms[(i, j)] = el
            j += 1
        i += 1
        x = list(k_clique_communities(agraph, i))
    return comms


def subsetgraph(comms, centrals, labels=2):
    """comms is communities """
    subgraph = nx.DiGraph()
    comkeys = sorted(comms.keys(), key=lambda x: x[0], reverse=True)
    for i, top in enumerate(comkeys):
        label_small = str(top[0]) + str(top[1])
        small_ordered = Counter(
            {r: centrals[r] for r in comms[top]}).most_common(labels)
        label_small = label_small + ' ' + ' '.join(
            [x[0] for x in small_ordered])
        subgraph.add_node(label_small)
        j = i + 1
        found = False
        while j < len(comkeys) and not found:
            nodej = comms[comkeys[j]]

            found = comms[top].issubset(nodej)
            # print(top,comkeys[j], found)
            if found:
                label_large = str(comkeys[j][0]) + str(comkeys[j][1])
                large_ordered = Counter(
                    {r: centrals[r] for r in nodej}).most_common(labels)
                label_large = label_large + ' ' + ' '.join(
                    [x[0] for x in large_ordered])
                # print(label_small, label_large)
                subgraph.add_edge(label_small, label_large)
            j += 1
    return subgraph


def make_cliques(words, lable_num=2):
    ggg = make_graph(words).to_undirected()
    centrals = nx.closeness_centrality(ggg)
    coms = kcliques(ggg)
    sg = subsetgraph(coms, centrals, lable_num)
    return (ggg, coms, sg)


def make_w_graph(weight_matrix):
    """weight_matrix a list on the form [((x,y,weight), ...]"""

    G = nx.Graph()
    G.add_weighted_edges_from(weight_matrix)
    return G


def make_cliques_from_graph(G, lable_num=2):
    ggg = G
    centrals = nx.closeness_centrality(ggg)
    coms = kcliques(ggg)
    sg = subsetgraph(coms, centrals, lable_num)
    return (ggg, coms, sg)


def my_layout(G):
    """For grafer fra make_cliques der koden ligger i de to første tallene"""
    pos = {}
    for i in G.nodes():
        x = i.split()[0]
        pos[i] = (int(x[0]), int(x[1]))
    return pos


'''
def tree_layout(G):
    """For grafer fra make_cliques der koden ligger i de to første tallene.

    OBS! Denne funksjonen vil ikke fungere uten refaktorering.
    Se kommentarer på de aktuelle linjene som må fikses.
    """
    pos = {}
    roots = root_nodes(G)  # W0612: Unused variable 'roots' (unused-variable)
    for r in G.nodes():  # W0612: Unused variable 'r' (unused-variable)
        x = i.split()[0]  # E0602: Undefined variable 'i' (undefined-variable)
        pos[i] = (int(x[0]), int(x[1]))
    return pos
'''


def root_nodes(G):
    res = []
    for x in G.nodes():
        found = False
        for y in G.nodes():
            found = found or (x, y) in G.edges()
            if found:
                break
        if not found:
            res += [x]
    return res


def tree_positions(Tree, spacing, increment=1):
    root = root_nodes(Tree)[0]
    return tree_pos(root, Tree, 1, spacing, 3, 3, level_increment=increment)[0]


def tree_pos(x, G, level, spacing, num, left_edge, level_increment=1):
    """Draw from left to right for left_edge"""
    positions = {}
    daughters = [y for (y, z) in G.edges() if x == z]
    if daughters == []:
        positions[x] = (left_edge, level)
        d_left = left_edge
    else:
        i = 1
        d_left = left_edge
        vals = []
        d_level = level + level_increment
        for d in daughters:
            d_positions, d_width = tree_pos(
                d,
                G,
                d_level - np.random.randint(1, 5) * level_increment / 10,
                spacing,
                i,
                d_left,
                level_increment=level_increment)
            i += 1
            d_left += spacing + d_width
            positions.update(d_positions)
            vals += [d_positions[d][0]]
            # print(vals)
        averagex = np.mean(vals)
        positions[x] = (averagex, level)
    return positions, d_left


def forest(G):
    roots = root_nodes(G)
    g_forest = []
    for r in roots:
        nr = node_set(r, G)
        g_forest += [G.subgraph(nr)]
    return g_forest


def node_set(root, G):
    span = [root]
    daughters = [y for (y, z) in G.edges() if z == root]
    if daughters != []:
        for d in daughters:
            span += node_set(d, G)
    return span


def draw_tree(G, node_size=1, node_color='slategrey', n=2, m=1, h=10, v=10):
    # plt.subplot()
    draw_graph(G, h=h, v=v, layout=lambda g: tree_positions(g, n, increment=m),
               node_color=node_color, node_size=node_size, fontsize=18,
               arrows=False)
    fmin, fmax = plt.xlim()
    plt.xlim(fmin - 10, fmax + 10)
    # ax.set_xticks([])
    # ax.set_yticks([])
    # plt.savefig('krig.svg')


'''
def draw_forest(F, spacing, h=15, v=10, save_name=False):
    """Denne funksjonen vil ikke fungere uten refaktorering.

    Se kommentarer på/over de aktuelle linjene.
    """
    # rows = len(F)
    # row = 1
    # plt.figsize=(15,10)
    for tree in F:
        # print(tree.nodes())
        # plt.subplot(rows,row,1)
        # plt.figure(row)
        # row += 1

        # Expected type 'int', got 'float' instead for node_size
        draw_tree(tree, node_size=0.5, h=h, v=v)
        if save_name:
            # E0602: Undefined variable 'row' (undefined-variable)
            plt.savefig(f'{save_name}-{row}.png', dpi=300)
'''


def print_list_of_sets(los):
    for x in los:
        print(', '.join(x), '\n')


def print_sets(graph):
    for x in graph[1]:
        print(x, ', '.join(graph[1][x]), '\n')
    return True


def make_collocation_graph(target, top=15, urns=None, cutoff=0, cut_val=2,
                           before=4, after=4, limit=1000):
    """Make a cascaded network from collocations"""
    if urns is None:
        urns = []
    antall = Counter()
    for urn in urns:
        antall += get_freq(urn[0], top=0, cutoff=0)

    korpus_totalen = frame(antall, 'total')
    Total = korpus_totalen[korpus_totalen > cut_val]

    if isinstance(target, str):
        target = target.split()

    I = urn_coll_words(target, urns=urns, before=before, after=after,
                       limit=limit)
    toppis = frame(I[0] ** 1.2 / Total['total'], target[0]).sort_values(
        by=target[0], ascending=False)

    # toppis[:top].index

    isgraf = {}
    for word in toppis[:top].index:
        if word.isalpha():
            isgraf[word] = urn_coll(
                word, urns=urns, before=before, after=after)

    isframe = {}
    for w, value in isgraf.items():
        isframe[w] = frame(value, w)

    tops = {}
    if len(target) == 1:
        tops[target[0]] = toppis
    else:
        tops['_'.join(target[:2])] = toppis
    for w, value in isframe.items():
        tops[w] = frame(value[w] ** 1.2 / Total['total'], w).sort_values(
            by=w, ascending=False)

    edges = []
    for w, value in tops.items():
        edges += [(w, coll) for coll in value[:top].index if coll.isalpha()]

    ice = nx.Graph()

    ice.add_edges_from(edges)

    return ice


def show_graph(G, spread=0.2, fontsize=10, deltax=0, deltay=0):
    return draw_graph_centrality2(G, mcommunity(G), k=spread, fontsize=fontsize,
                                  deltax=deltax, deltay=deltay)


def show_cliques(G):
    C = make_cliques_from_graph(G.to_undirected())
    for t in C[1]:
        print(t, ', '.join(C[1][t]))
        print()


def show_community(G):
    MC = mcommunity(G)
    for i, element in enumerate(MC):
        print(i + 1, ', '.join(element))
        print()
    return True


def community_dict(G):
    sorter = Counter(dict(nx.degree(G)))
    cd = {}
    for c in mcommunity(G):
        l = [(x, sorter[x]) for x in c if sorter[x] > 0]
        # print(l)
        l.sort(key=lambda i: i[1], reverse=True)
        # print(l)
        cd['-'.join([x[0] for x in l[:2]])] = [x[0] for x in l]
    return cd


def show_communities(G):
    Gc = community_dict(G)
    for c, value in Gc.items():
        print(c, ': ', ', '.join(value))
        print()


def reduce_MxM_graph(G, words, factor=0.01):
    Gm = nx.Graph()
    edges = []
    for x in G.edges(data=True):
        w = x[2]['weight']
        w1 = x[0]
        w2 = x[1]
        new_weight = w / (int(words.loc[w1]) * int(words.loc[w2]))
        if new_weight > factor:
            edges.append((w1, w2, new_weight))
    Gm.add_weighted_edges_from(edges)
    return Gm
