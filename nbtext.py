import json
import random
import numpy.random
import re
from collections import Counter

import pandas as pd
import matplotlib.pyplot as plt
import requests
from IPython.display import HTML
import seaborn as sns
import networkx as nx
from pylab import rcParams
try:
    from wordcloud import WordCloud
except ImportError:
    print("wordcloud er ikke installert, kan ikke lage ordskyer")


#************** For defining wordbag search

def dict2pd(dictionary):
    res = pd.DataFrame(dictionary).fillna(0)
    s = (res.mean(axis=0))
    s = s.rename('snitt')
    res = res.append(s)
    return res.sort_values(by='snitt', axis=1, ascending=False).transpose()

def def2dict(ddef):
    res = dict()
    defs = ddef.split(';')
    for d in defs:
        lex = d.split(':')
        if len(lex) == 2:
            #print('#'.join(lex))
            hyper = lex[0].strip()
            occurrences = [x.strip() for x in lex[1].split(',')]
            res[hyper] = occurrences
    for x in res:
        for y in res[x]:
            if y.capitalize() not in res[x]:
                res[x].append(y.capitalize())
    return res

def wordbag_eval(wordbag, urns):
    if type(urns) is list:
        if isinstance(urns[0], list):
            urns = [u[0] for u in urns]
        else:
            urns = urns
    else:
        urns = [urns]
    param = dict()
    param['wordbags'] = wordbag
    param['urns'] = urns
    r = requests.post("https://api.nb.no/ngram/wordbags", json = param)
    return dict2pd(r.json())


### ******************* wordbag search end

def ner(text = None, dist=False):
    """Analyze text for named entities - set dist = True will return the four values that go into decision"""
    r = []
    if text != None:
        r = requests.post("https://api.nb.no/ngram/ner", json={'text':text,'dist':dist})
    return r.json()
    
#**** names ****

def check_navn(navn, limit=2, remove='Ja Nei Nå Dem De Deres Unnskyld Ikke Ah Hmm Javel Akkurat Jaja Jaha'.split()):
    """Removes all items in navn with frequency below limit and words in all case as well as all words in list 'remove'"""
    r = {x:navn[x] for x in navn if navn[x] > limit and x.upper() != x and not x in remove}
    return r


def sentences(urns, num=300):
    if isinstance(urns[0], list):
        urns = [str(x[0]) for x in urns]
    params = {'urns':urns,
             'num':num}
    res = requests.get("https://api.nb.no/ngram/sentences", params=params)
    return res.json()


def names(urn, ratio = 0.3, cutoff = 2):
    """ Return namens in book with urn. Returns uni- , bi-, tri- and quadgrams """
    if type(urn) is list:
        urn = urn[0]
    r = requests.get('https://api.nb.no/ngram/names', json={'urn':urn, 'ratio':ratio, 'cutoff':cutoff})
    x = r.json()
    result = (
        Counter(x[0][0]),
        Counter({tuple(x[1][i][0]):x[1][i][1] for i in range(len(x[1]))}),
        Counter({tuple(x[2][i][0]):x[2][i][1] for i in range(len(x[2]))}),
        Counter({tuple(x[3][i][0]):x[3][i][1] for i in range(len(x[3]))})
    )
    return result


def name_graph(name_struct):
    m = []
    for n in name_struct[0]:
        m.append(frozenset([n]))
    for n in name_struct[1:]:
        m += [frozenset(x) for x in n]
        
    G = []
    for x in m:
        for y in m:
            if x < y:
                G.append((' '.join(x), ' '.join(y)))
    N = []
    for x in m:
        N.append(' '.join(x))
    Gg = nx.Graph()
    Gg.add_nodes_from(N)
    Gg.add_edges_from(G)
    return Gg

def aggregate_urns(urnlist):
    """Sum up word frequencies across urns"""
    
    if isinstance(urnlist[0], list):
        urnlist = [u[0] for u in urnlist]
    r = requests.post("https://api.nb.no/ngram/book_aggregates", json={'urns':urnlist})
    return r.json()

# Norweigan word bank
def word_variant(word, form):
    """ Find alternative form for a given word form, e.g. word_variant('spiste', 'pres-part') """
    r = requests.get("https://api.nb.no/ngram/variant_form", params={'word':word, 'form':form})
    return r.json()

def check_edges(G, weight=1):    
    return nx.Graph([edge for edge in G.edges(data=True) if edge[2]['weight'] >= weight])

def word_freq(urn, words):
    params = {'urn':urn, 'words':words}
    r = requests.post("https://api.nb.no/ngram/freq", json=params)
    return dict(r.json())

def book_count(urns):
    params = {'urns':urns}
    r = requests.post("https://api.nb.no/ngram/book_count", json=params)
    return dict(r.json())

def sttr(urn, chunk=5000):
    r = requests.get("https://api.nb.no/ngram/sttr", json = {'urn':urn, 'chunk':chunk})
    return r.json()
                     
def totals(top=200):
    r = requests.get("https://api.nb.no/ngram/totals", json={'top':top})
    return dict(r.json())

def navn(urn):
    if type(urn) is list:
        urn = urn[0]
    r = requests.get('https://api.nb.no/ngram/tingnavn', json={'urn':urn})
    return dict(r.json())
    
def digibokurn_from_text(T):
    """Return URNs as 13 digits (any sequence of 13 digits is counted as an URN)"""
    return re.findall("(?<=digibok_)[0-9]{13}", T)

def urn_from_text(T):
    """Return URNs as 13 digits (any sequence of 13 digits is counted as an URN)"""
    return re.findall("[0-9]{13}", T)

def metadata(urn=None):
    if type(urn) is str:
        urns = urn.split()
    elif type(urn) is list:
        if isinstance(urn[0], list):
            urns = [u[0] for u in urn]
        else:
            urns = urn
    else:
        urns = [urn]
    #print(urns)
    r = requests.post("https://api.nb.no/ngram/meta", json={'urn':urns})
    return r.json()


def pure_urn(data):
    """Convert URN-lists with extra data into list of serial numbers.
    Args:
        data: May be a list of URNs, a list of lists with URNs as their
            initial element, or a string of raw texts containing URNs
    Returns:
        List[str]: A list of URNs. Empty list if input is on the wrong
            format or contains no URNs
    """
    korpus_def = []
    if isinstance(data, list):
        if not data:  # Empty list
            korpus_def = []
        if isinstance(data[0], list):  # List of lists
            try:
                korpus_def = [x[0] for x in data]
            except IndexError:
                korpus_def = []
        else:  # Assume data is already a list of URNs
            korpus_def = data
    elif isinstance(data, str):
        korpus_def = urn_from_text(data)
    elif isinstance(data, int):
        korpus_def = [data]
    return korpus_def


def difference(first, second, rf, rs, years=(1980, 2000),smooth=1, corpus='bok'):
    """Compute difference of difference (first/second)/(rf/rs)"""
    try:
        a_first = nb_ngram(first, years=years, smooth=smooth, corpus=corpus)
        a_second = nb_ngram(second, years=years, smooth=smooth, corpus=corpus)
        a = a_first.join(a_second)  
        b_first = nb_ngram(rf, years=years, smooth=smooth, corpus=corpus)
        b_second = nb_ngram(rs, years=years, smooth=smooth, corpus=corpus)
        if rf == rs:
            b_second.columns = [rs + '2']
        b = b_first.join(b_second)
        s_a = a.mean()
        s_b = b.mean()
        f1 = s_a[a.columns[0]]/s_a[a.columns[1]]
        f2 = s_b[b.columns[0]]/s_b[b.columns[1]]
        res = f1/f2
    except:
        res = 'Mangler noen data - har bare for: ' + ', '.join([x for x in a.columns.append(b.columns)])
    return res

def df_combine(array_df):
    """Combine one columns dataframes"""
    import pandas as pd
    cols = []
    for i in range(len(a)):
        #print(i)
        if array_df[i].columns[0] in cols:
            array_df[i].columns = [array_df[i].columns[0] + '_' + str(i)]
        cols.append(array_df[i].columns[0])
    return pd.concat(a, axis=1, sort=True)

def col_agg(df, col='sum'):
    c = df.sum(axis=0)
    c = pd.DataFrame(c)
    c.columns = [col]
    return c

def row_agg(df, col='sum'):
    c = df.sum(axis=1)
    c = pd.DataFrame(c)
    c.columns = [col]
    return c


def get_freq(urn, top=50, cutoff=3):
    """Get frequency list for urn"""
    if isinstance(urn, list):
        urn = urn[0]
    r = requests.get("https://api.nb.no/ngram/urnfreq", json={'urn':urn, 'top':top, 'cutoff':cutoff})
    return Counter(dict(r.json()))


def book_urn(author='%', title="%", ddk="%", subject="", period=(1100, 2020), gender="", limit=20 ):
    """Get URNs for books with metadata"""
    return get_urn({
        "author": author,
        "title":title,
        "ddk":ddk,
        "subject":subject,
        "year":period[0],
        'next':period[1] - period[0],
        "limit":limit
    })

def get_urn(metadata=None):
    """Get urns from metadata"""
    if metadata is None:
        metadata = {}
    if not ('next' in metadata or 'neste' in metadata):
        metadata['next'] = 100
    if not 'year' in metadata:
        metadata['year'] = 1900
    r = requests.get('https://api.nb.no/ngram/urn', json=metadata)
    return r.json()

def refine_urn(urns, metadata=None):
    """Refine a list urns using extra information"""
    if metadata is None:
        metadata = {}
    metadata['urns'] = urns
    if not ('words' in metadata):
        metadata['words'] = []
    if not ('next' in metadata or 'neste' in metadata):
        metadata['next'] = 520
    if not 'year' in metadata:
        metadata['year'] = 1500
    r = requests.post('https://api.nb.no/ngram/refineurn', json=metadata)
    return r.json()

def get_best_urn(word, metadata=None):
    """Get the best urns from metadata containing a specific word"""
    metadata['word'] = word
    if not ('next' in metadata or 'neste' in metadata):
        metadata['next'] = 600
    if not 'year' in metadata:
        metadata['year'] = 1500
    r = requests.get('https://api.nb.no/ngram/best_urn', json=metadata)
    return r.json()

def get_papers(top=5, cutoff=5, navn='%', yearfrom=1800, yearto=2020, samplesize=100):
    """Get newspapers"""
    div = lambda x, y: (int(x/y), x % y)
    chunks = 20
    
    
    # split samplesize into chunks, go through the chunks and then the remainder
    
    (first, second) = div(samplesize, chunks)
    r = []
    
    # collect chunkwise 
    for i in range(first):
        r += requests.get("https://api.nb.no/ngram/avisfreq", json={'navn':navn, 'top':top, 'cutoff':cutoff,
                                                              'yearfrom':yearfrom, 'yearto':yearto,'samplesize':chunks}
                         ).json()
    
    
    # collect the remainder
    r += requests.get("https://api.nb.no/ngram/avisfreq", json={'navn':navn, 'top':top, 'cutoff':cutoff,
                                                              'yearfrom':yearfrom, 'yearto':yearto,'samplesize':second}
                         ).json()

    return [dict(x) for x in r]


def urn_coll(word, urns=[], after=5, before=5, limit=1000):
    """Find collocations for word in a set of book URNs. Only books at the moment"""
    
    if isinstance(urns[0], list):  # urns assumed to be list of list with urn-serial as first element
        urns = [u[0] for u in urns]
        
    r = requests.post("https://api.nb.no/ngram/urncoll", json={'word':word, 'urns':urns, 
                                                                   'after':after, 'before':before, 'limit':limit})
    res = pd.DataFrame.from_dict(r.json(), orient='index')
    if not res.empty:
        res = res.sort_values(by=res.columns[0], ascending = False)
    return res

def urn_coll_words(words, urns=None, after=5, before=5, limit=1000):
    """Find collocations for a group of words within a set of books given by a list of URNs. Only books at the moment"""
    coll = pd.DataFrame()
    if urns != None:
        if isinstance(urns[0], list):  # urns assumed to be list of list with urn-serial as first element
            urns = [u[0] for u in urns]
        colls = Counter()
        if isinstance(words, str):
            words = words.split()
        res = Counter()
        for word in words: 
            try:
                res += Counter(
                    requests.post(
                        "https://api.nb.no/ngram/urncoll", 
                        json={
                            'word':word, 
                            'urns':urns, 
                            'after':after, 
                            'before':before, 
                            'limit':limit}
                    ).json()
                )
            except:
                True
        coll = pd.DataFrame.from_dict(res, orient='index')
        if not coll.empty:
            coll = coll.sort_values(by=coll.columns[0], ascending = False) 
    return coll


def get_aggregated_corpus(urns, top=0, cutoff=0):
    res = Counter()
    if isinstance(urns[0], list):  # urns assumed to be list of list with urn-serial as first element
        urns = [u[0] for u in urns]
    for u in urns:
        #print(u)
        res += get_freq(u, top = top, cutoff = cutoff)
    return pd.DataFrame.from_dict(res, orient='index').sort_values(by=0, ascending = False)


def compare_word_bags(bag_of_words, another_bag_of_words, first_freq = 0, another_freq = 1, top=100, first_col = 0, another_col= 0):
    """Compare two columns taken from two or one frame. Parameters x_freq are frequency limits used to cut down candidate words
    from the bag of words. Compare along the columns where first_col and another_col are column numbers. Typical situation is that
    bag_of_words is a one column frame and another_bag_of_words is another one column frame. When the columns are all from one frame, 
    just change column numbers to match the columns"""
    diff = bag_of_words[bag_of_words > first_freq][bag_of_words.columns[first_col]]/another_bag_of_words[another_bag_of_words > another_freq][another_bag_of_words.columns[another_col]] 
       
    return frame(diff, 'diff').sort_values(by='diff', ascending=False)[:top]


def collocation(
    word, 
    yearfrom=2010, 
    yearto=2018, 
    before=3, 
    after=3, 
    limit=1000, 
    corpus='avis',
    lang='nob',
    title='%',
    ddk='%', 
    subtitle='%'):
    """Defined collects frequencies for a given word"""
    
    data =  requests.get(
        "https://api.nb.no/ngram/collocation", 
        params={
            'word':word,
            'corpus':corpus, 
            'yearfrom':yearfrom, 
            'before':before,
            'after':after,
            'limit':limit,
            'yearto':yearto,
        'title':title,
        'ddk':ddk,
        'subtitle':subtitle}).json()
    return pd.DataFrame.from_dict(data['freq'], orient='index')


def collocation_data(words, yearfrom = 2000, yearto = 2005, limit = 1000, before = 5, after = 5, title = '%', corpus='bok'):
    """Collocation for a set of words sum up all the collocations words is a list of words or a blank separated string of words"""
    import sys
    a = dict()
    
    if isinstance(words, str):
        words = words.split()
    
    for word in words:
        
        print(word)
        try:
            
            a[word] = collocation(
                word, 
                yearfrom = yearfrom, yearto = yearto, limit = limit, 
                corpus = corpus, before = before, 
                after = after, title = title
            )
            
            a[word].columns = [word]
        
        except:    
            print(word, ' feilsituasjon', sys.exc_info())
    result = pd.DataFrame()
    for w in a:
        result = result.join(a[w], how='outer')
    return pd.DataFrame(result.sum(axis=1)).sort_values(by=0, ascending=False)

class CollocationCorpus:
    from random import sample
    
    def __init__(self, corpus = None, name='', maximum_texts = 500):
        urns = pure_urn(corpus)
        
        if len(urns) > maximum_texts:      
            selection = random(urns, maximum_texts)
        else:
            selection = urns
            
        self.corpus_def = selection
        self.corpus = get_aggregated_corpus(self.corpus_def, top=0, cutoff=0)


    def summary(self, head=10):
        info = {
            'corpus_definition':self.corpus[:head],
            'number_of_words':len(self.corpus)
            
        }
        return info

def collocation_old(word, yearfrom=2010, yearto=2018, before=3, after=3, limit=1000, corpus='avis'):
    data =  requests.get(
        "https://api.nb.no/ngram/collocation", 
        params={
            'word':word,
            'corpus':corpus, 
            'yearfrom':yearfrom, 
            'before':before,
            'after':after,
            'limit':limit,
            'yearto':yearto}).json()
    return pd.DataFrame.from_dict(data['freq'], orient='index')

def heatmap(df, color='green'):
    return df.fillna(0).style.background_gradient(cmap=sns.light_palette(color, as_cmap=True))

def get_corpus_text(urns, top = 0, cutoff=0):
    k = dict()
    for u in urns:
        #print(u)
        k[u] = get_freq(u, top = top, cutoff = cutoff)
    return pd.DataFrame(k)

def normalize_corpus_dataframe(df):
    colsums = df.sum()
    for x in colsums.index:
        #print(x)
        df[x] = df[x].fillna(0)/colsums[x]
    return True

def show_korpus(korpus, start=0, size=4, vstart=0, vsize=20, sortby = ''):
    """Show corpus as a panda dataframe
    start = 0 indicates which dokument to show first, dataframe is sorted according to this
    size = 4 how many documents (or columns) are shown
    top = 20 how many words (or rows) are shown"""
    if sortby != '':
        val = sortby
    else:
        val = korpus.columns[start]
    return korpus[korpus.columns[start:start+size]].sort_values(by=val, ascending=False)[vstart:vstart + vsize]

def aggregate(korpus):
    """Make an aggregated sum of all documents across the corpus, here we use average"""
    return pd.DataFrame(korpus.fillna(0).mean(axis=1))

def convert_list_of_freqs_to_dataframe(referanse):
    """The function get_papers() returns a list of frequencies - convert it"""
    res = []
    for x in referanse:
        res.append( dict(x))
    result = pd.DataFrame(res).transpose()
    normalize_corpus_dataframe(result)
    return result

def get_corpus(top=0, cutoff=0, navn='%', corpus='avis', yearfrom=1800, yearto=2020, samplesize=10):
    if corpus == 'avis':
        result = get_papers(top=top, cutoff=cutoff, navn=navn, yearfrom=yearfrom, yearto=yearto, samplesize=samplesize)
        res = convert_list_of_freqs_to_dataframe(result)
    else:
        urns = get_urn({'author':navn, 'year':yearfrom, 'neste':yearto-yearfrom, 'limit':samplesize})
        res = get_corpus_text([x[0] for x in urns], top=top, cutoff=cutoff)
    return res


class Cluster:
    def __init__(self, word = '', filename = '', period = (1950,1960) , before = 5, after = 5, corpus='avis', reference = 200, 
                 word_samples=1000):
        if word != '':
            self.collocates = collocation(word, yearfrom=period[0], yearto = period[1], before=before, after=after,
                                corpus=corpus, limit=word_samples)
            self.collocates.columns = [word]
            if type(reference) is pd.core.frame.DataFrame:
                reference = reference
            elif type(reference) is int:
                reference = get_corpus(yearfrom=period[0], yearto=period[1], corpus=corpus, samplesize=reference)
            else:
                reference = get_corpus(yearfrom=period[0], yearto=period[1], corpus=corpus, samplesize=int(reference))

            self.reference = aggregate(reference)
            self.reference.columns = ['reference_corpus']        
            self.word = word
            self.period = period
            self.corpus = corpus
        else:
            if filename != '':
                self.load(filename)
            
                
    def cluster_set(self, exponent=1.1, top = 200, aslist=True):
        combo_corp = self.reference.join(self.collocates, how='outer')
        normalize_corpus_dataframe(combo_corp)
        korpus = compute_assoc(combo_corp, self.word, exponent)
        korpus.columns = [self.word]
        if top <= 0:
            res = korpus.sort_values(by=self.word, ascending=False)
        else:
            res = korpus.sort_values(by=self.word, ascending=False).iloc[:top]
        if aslist == True:
            res = HTML(', '.join(list(res.index)))
        return res
    
    def add_reference(self, number=20):
        ref = get_corpus(yearfrom=self.period[0], yearto=self.period[1], samplesize=number)
        ref = aggregate(ref)
        ref.columns = ['add_ref']
        normalize_corpus_dataframe(ref)
        self.reference = aggregate(self.reference.join(ref, how='outer'))
        return True
    
    def save(self, filename=''):
        if filename == '':
            filename = "{w}_{p}-{q}.json".format(w=self.word,p=self.period[0], q = self.period[1])
        model = {
            'word':self.word,
            'period':self.period,
            'reference':self.reference.to_dict(),
            'collocates':self.collocates.to_dict(),
            'corpus':self.corpus
        }
        with open(filename, 'w', encoding = 'utf-8') as outfile:
            print('lagrer til:', filename)
            outfile.write(json.dumps(model))
        return True

    def load(self, filename):
        with open(filename, 'r') as infile:
            try:
                model = json.loads(infile.read())
                #print(model['word'])
                self.word = model['word']
                self.period = model['period']
                self.corpus = model['corpus']
                self.reference = pd.DataFrame(model['reference'])
                self.collocates = pd.DataFrame(model['collocates'])
            except:
                print('noe gikk galt')
        return True
    
       
    def search_words(self, words, exponent=1.1):
        if type(words) is str:
            words = [w.strip() for w in words.split()]
        df = self.cluster_set(exponent=exponent, top=0, aslist=False)
        sub= [w for w in words if w in df.index]
        res = df.transpose()[sub].transpose().sort_values(by=df.columns[0], ascending=False)
        return res


def wildcardsearch(params=None):
    if params is None:
        params = {'word': '', 'freq_lim': 50, 'limit': 50, 'factor': 2}
    res = requests.get('https://api.nb.no/ngram/wildcards', params=params)
    if res.status_code == 200:
        result = res.json()
    else:
        result = {'status':'feil'}
    resultat = pd.DataFrame.from_dict(result, orient='index')
    if not(resultat.empty):
        resultat.columns = [params['word']]
    return resultat

def sorted_wildcardsearch(params):
    res = wildcardsearch(params)
    if not res.empty:
        res = res.sort_values(by=params['word'], ascending=False)
    return res
            
def make_newspaper_network(key, wordbag, titel='%', yearfrom='1980', yearto='1990', limit=500):
    if type(wordbag) is str:
        wordbag = wordbag.split()
    r = requests.post("https://api.nb.no/ngram/avisgraph", json={
        'key':key, 
        'words':wordbag,
        'yearto':yearto,
    'yearfrom':yearfrom,
    'limit':limit})
    G = nx.Graph()
    if r.status_code == 200:
        G.add_weighted_edges_from([(x,y,z) for (x,y,z) in r.json() if z > 0 and x != y])
    else:
        print(r.text)
    return G

def make_network(urn, wordbag, cutoff=0):
    if type(urn) is list:
        urn = urn[0]
    if type(wordbag) is str:
        wordbag = wordbag.split()
    G = make_network_graph(urn, wordbag, cutoff)
    return G

def make_network_graph(urn, wordbag, cutoff=0):
    r = requests.post("https://api.nb.no/ngram/graph", json={'urn':urn, 'words':wordbag})
    G = nx.Graph()
    G.add_weighted_edges_from([(x,y,z) for (x,y,z) in r.json() if z > cutoff and x != y])
    return G

def draw_graph_centrality(G, h=15, v=10, fontsize=20, k=0.2, arrows=False, font_color='black', threshold=0.01): 
    node_dict = nx.degree_centrality(G)
    subnodes = dict({x:node_dict[x] for x in node_dict if node_dict[x] >= threshold})
    x, y = rcParams['figure.figsize']
    rcParams['figure.figsize'] = h, v
    pos =nx.spring_layout(G, k=k)
    ax = plt.subplot()
    ax.set_xticks([])
    ax.set_yticks([])
    G = G.subgraph(subnodes)
    nx.draw_networkx_labels(G, pos, font_size=fontsize, font_color=font_color)
    nx.draw_networkx_nodes(G, pos, alpha=0.5, nodelist=subnodes.keys(), node_size=[v * 1000 for v in subnodes.values()])
    nx.draw_networkx_edges(G, pos, alpha=0.7, arrows=arrows, edge_color='lightblue', width=1)

    rcParams['figure.figsize'] = x, y
    return True

def combine(clusters):
    """Make new collocation analyses from data in clusters"""
    colls = []
    collocates = clusters[0].collocates
    for c in clusters[1:]:
        collocates = collocates.join(c.collocates, rsuffix='-' + str(c.period[0]))
    return collocates

def cluster_join(cluster):
    clusters = [cluster[i] for i in cluster]
    clst = clusters[0].cluster_set(aslist=False)
    for c in clusters[1:]:
        clst = clst.join(c.cluster_set(aslist=False), rsuffix = '_'+str(c.period[0]))
    return clst

def serie_cluster(word, startår, sluttår, inkrement, before=5, after=5, reference=150, word_samples=500):
    tidscluster = dict()
    for i in range(startår, sluttår, inkrement):
        tidscluster[i] = Cluster(
        word, 
        corpus='avis', 
        period=(i, i + inkrement - 1), 
        before=after, 
        after=after, 
        reference=reference, 
        word_samples=word_samples)
        print(i, i+inkrement - 1)
    return tidscluster

def save_serie_cluster(tidscluster):
    for i in tidscluster:
        tidscluster[i].save()
    return 'OK'

def les_serie_cluster(word, startår, sluttår, inkrement):
    tcluster = dict()
    for i in range(startår, sluttår, inkrement):
        print(i, i+inkrement - 1)
        tcluster[i] = Cluster(filename='{w}_{f}-{t}.json'.format(w=word, f=i,t=i+inkrement - 1))
    return tcluster




def make_cloud(json_text, top=100, background='white', stretch=lambda x: 2**(10*x), width=500, height=500, font_path=None):
    pairs0 = Counter(json_text).most_common(top)
    pairs = {x[0]:stretch(x[1]) for x in pairs0}
    wc = WordCloud(
    font_path=font_path,  
    background_color=background,
    width=width, 
    #color_func=my_colorfunc,
    ranks_only=True,
    height=height).generate_from_frequencies(pairs)
    return wc

def draw_cloud(sky, width=20, height=20, fil=''):
    plt.figure(figsize=(width,height))
    plt.imshow(sky, interpolation='bilinear')
    figplot = plt.gcf()
    if fil != '':
        figplot.savefig(fil, format='png')
    return 

def cloud(pd, column='', top=200, width=1000, height=1000, background='black', file='', stretch=10, font_path=None):
    if column == '':
        column = pd.columns[0]
    data = json.loads(pd[column].to_json())
    a_cloud = make_cloud(data, top=top, 
                         background=background, font_path=font_path, 
                         stretch=lambda x: 2**(stretch*x), width=width, height=height)
    draw_cloud(a_cloud, fil=file)
    return


def make_a_collocation(word, period=(1990, 2000), before=5, after=5, corpus='avis', samplesize=100, limit=2000):
    collocates = collocation(word, yearfrom=period[0], yearto=period[1], before=before, after=after,
                             corpus=corpus, limit=limit)
    collocates.columns = [word]
    reference = get_corpus(yearfrom=period[0], yearto=period[1], samplesize=samplesize)
    ref_agg = aggregate(reference)
    ref_agg.columns = ['reference_corpus']
    return  ref_agg



def compute_assoc(coll_frame, column, exponent=1.1, refcolumn = 'reference_corpus'):
    return pd.DataFrame(coll_frame[column]**exponent/coll_frame.mean(axis=1))
    


class Corpus:
    def __init__(self, filename = '', target_urns = None, reference_urns = None,  period = (1950,1960), author='%', 
                 title='%', ddk='%', gender='%', subject='%', reference = 100, max_books=100):
        params = {
            'year':period[0], 
            'next': period[1]-period[0], 
            'subject':subject,
            'ddk':ddk, 
            'author':author, 
            #'gender':gender, ser ikke ut til å virke for get_urn - sjekk opp APIet
            'title':title, 
            'limit':max_books,
            'reference':reference
        }
        self.params = params
        self.coll = dict()
        self.coll_graph = dict()
        if filename == '':
            if target_urns != None:
                målkorpus_def = target_urns
            else:
                målkorpus_def = get_urn(params)

            #print("Antall bøker i målkorpus ", len(målkorpus_def))
            if isinstance(målkorpus_def[0], list):
                målkorpus_urn = [str(x[0]) for x in målkorpus_def]
                #print(målkorpus_urn)
            else:
                målkorpus_urn = målkorpus_def
            if len(målkorpus_urn) > max_books and max_books > 0:
                target_urn = list(numpy.random.choice(målkorpus_urn, max_books))
            else:
                target_urn = målkorpus_urn

            if reference_urns != None:
                referansekorpus_def = reference_urns
            else:
                # select from period, usually used only of target is by metadata
                referansekorpus_def = get_urn({'year':period[0], 'next':period[1]-period[0], 'limit':reference})


            #print("Antall bøker i referanse: ", len(referansekorpus_def))
            # referansen skal være distinkt fra målkorpuset
            referanse_urn = [str(x[0]) for x in referansekorpus_def]
            self.reference_urn = referanse_urn
            self.target_urn = target_urn
            # make sure there is no overlap between target and reference
            # 
            referanse_urn = list(set(referanse_urn) - set(target_urn))


            målkorpus_txt = get_corpus_text(target_urn)
            normalize_corpus_dataframe(målkorpus_txt)
            if referanse_urn != []:
                referanse_txt = get_corpus_text(referanse_urn)
                normalize_corpus_dataframe(referanse_txt)
                combo = målkorpus_txt.join(referanse_txt)

            else:
                referanse_txt = målkorpus_txt
                combo = målkorpus_txt
                
            self.combo = combo 
            self.reference = referanse_txt
            self.target = målkorpus_txt

            self.reference = aggregate(self.reference)
            self.reference.columns = ['reference_corpus']

            ## dokumentfrekvenser

            mål_docf = pd.DataFrame(pd.DataFrame(målkorpus_txt/målkorpus_txt).sum(axis=1))
            combo_docf = pd.DataFrame(pd.DataFrame(combo/combo).sum(axis=1))
            ref_docf = pd.DataFrame(pd.DataFrame(referanse_txt/referanse_txt).sum(axis=1))

            ### Normaliser dokumentfrekvensene
            normalize_corpus_dataframe(mål_docf)
            normalize_corpus_dataframe(combo_docf)
            normalize_corpus_dataframe(ref_docf)

            self.målkorpus_tot = aggregate(målkorpus_txt)
            self.combo_tot = aggregate(combo)
            self.mål_docf = mål_docf
            self.combo_docf = combo_docf
            self.lowest = self.combo_tot.sort_values(by=0)[0][0]
        else:
            self.load(filename)
        return 
            
    
    def difference(self, freq_exp=1.1, doc_exp=1.1, top = 200, aslist=True):
        res = pd.DataFrame(
            (self.målkorpus_tot**freq_exp/self.combo_tot)*(self.mål_docf**doc_exp/self.combo_docf)
        )
        res.columns = ['diff']
        if top > 0:
            res = res.sort_values(by=res.columns[0], ascending=False).iloc[:top]
        else:
            res = res.sort_values(by=res.columns[0], ascending=False)
        if aslist == True:
            res = HTML(', '.join(list(res.index)))
        return res
    

    def save(self, filename):

        model = {
            'params':self.params,   
            'target': self.målkorpus_tot.to_json(),
            'combo': self.combo_tot.to_json(),
            'target_df': self.mål_docf.to_json(),
            'combo_df': self.combo_docf.to_json()
        }

        with open(filename, 'w', encoding = 'utf-8') as outfile:
            outfile.write(json.dumps(model))
        return True

    def load(self, filename):
        with open(filename, 'r') as infile:
            try:
                model = json.loads(infile.read())
                #print(model['word'])
                self.params = model['params']
                #print(self.params)
                self.målkorpus_tot = pd.read_json(model['target'])
                #print(self.målkorpus_tot[:10])
                self.combo_tot = pd.read_json(model['combo'])
                self.mål_docf = pd.read_json(model['target_df'])
                self.combo_docf = pd.read_json(model['combo_df'])
            except:
                print('noe gikk galt')
        return True
    
    def collocations(self, word, after=5, before=5, limit=1000):
        """Find collocations for word in a set of book URNs. Only books at the moment"""
        
        r = requests.post(
            "https://api.nb.no/ngram/urncoll", 
            json={
                'word': word, 
                'urns': self.target_urn,
                'after': after, 
                'before': before, 
                'limit': limit
            }
        )

        temp = pd.DataFrame.from_dict(r.json(), orient='index')
        normalize_corpus_dataframe(temp)
        self.coll[word] = temp.sort_values(by = temp.columns[0], ascending = False)
        return True
    
    def conc(self, word, before=8, after=8, size=10, combo=0):
        
        
        if combo == 0:
            urns = self.target_urn + self.reference_urn
        elif combo == 1:
            urns = self.target_urn
        else:
            urns = self.reference_urn
        if len(urns) > 300:
            urns = list(numpy.random.choice(urns, 300, replace=False))
        return get_urnkonk(word, {'urns':urns, 'before':before, 'after':after, 'limit':size})
    
    def sort_collocations(self, word, comparison = None, exp = 1.0, above = None):
        
        if comparison == None:
            comparison = self.combo_tot[0]
        try:
            res = pd.DataFrame(self.coll[word][0]**exp/comparison)

        except KeyError:
            print('Constructing a collocation for {w} with default parameters.'.format(w=word))
            self.collocations(word)
            res = pd.DataFrame(self.coll[word][0]**exp/comparison)
        if above == None:
        	above = self.lowest
        res = res[self.combo_tot > above]
        return res.sort_values(by = 0, ascending = False)
    
    def search_collocations(self, word, words, comparison = None, exp = 1.0):
        
        if comparison == None:
            comparison = self.combo_tot[0]
        try:
            res = pd.DataFrame(self.coll[word][0]**exp/comparison)
        except KeyError:
            print('Constructing a collocation for {w} with default parameters.'.format(w=word))
            self.collocations(word)
            res = pd.DataFrame(self.coll[word][0]**exp/comparison)
        search_items = list(set(res.index) & set(words))
        return res.transpose()[search_items].transpose().sort_values(by = 0, ascending = False)
    
    def summary(self, head=10):
        info = {
            'parameters':self.params,
            'target_urn':self.target_urn[:head],
            'reference urn':self.reference_urn[:head],
            
        }
        return info

    def search_words(self, words, freq_exp=1.1, doc_exp=1.1):
        if type(words) is str:
            words = [w.strip() for w in words.split()]
        df = self.difference(freq_exp = freq_exp, doc_exp=doc_exp,top=0, aslist=False)
        sub = [w for w in words if w in df.index]
        res = df.transpose()[sub].transpose().sort_values(by=df.columns[0], ascending=False)
        return res
    
    def make_collocation_graph(self, target_word, top = 15, before = 4, after = 4, limit = 1000, exp=1):
        """Make a cascaded network of collocations"""

        self.collocations(target_word, before=before, after=after, limit=limit)
        coll = self.sort_collocations(target_word, exp = exp)
        target_graf = dict()
        edges = []
        for word in coll[:top].index:
            edges.append((target_word, word))
            if word.isalpha():
                self.collocations(word, before=before, after=after,  limit=limit)
                for w in self.sort_collocations(word, exp = exp)[:top].index:
                    if w.isalpha():
                        edges.append((word, w)) 

        target_graph = nx.Graph()
        target_graph.add_edges_from(edges)
        self.coll_graph[target_word] = target_graph
        return target_graph
        
def vekstdiagram(urn, params=None):
    if params is None:
        params = {}

    # if urn is the value of get_urn() it is a list
    # otherwise it just passes
    if type(urn) is list:
        urn = urn[0]
    
    para = params
    para['urn']= urn
    r = requests.post('https://api.nb.no/ngram/vekstdiagram', json = para)
    return pd.DataFrame(r.json())

def plot_book_wordbags(urn, wordbags, window=5000, pr = 100):
    """Generate a diagram of wordbags in book """
    return plot_sammen_vekst(urn, wordbags, window=window, pr=pr)
    

def plot_sammen_vekst(urn, ordlister, window=5000, pr = 100):
    """Plott alle seriene sammen"""
    rammer = []
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
        vekst = vekstdiagram(urn, params = {'words': c[key], 'window':window, 'pr': pr} )
        vekst.columns = [key]
        rammer.append(vekst)
    return pd.concat(rammer, sort = True)

def spurious_names(n=300):
    topwords = totals(n)
    Removals = [x.capitalize() for x in topwords if x.isalpha()]
    return Removals

def relaterte_ord(word, number = 20, score=False):
    G = make_graph(word)
    res = Counter(nx.eigenvector_centrality(G)).most_common(number) 
    if score == False:
        res = [x[0] for x in res]
    return res


def check_words(urn, ordbag):
    if type(urn) is list:
        urn = urn[0]
    ordliste = get_freq(urn, top=50000, cutoff=0)
    res = Counter()
    for w in ordbag:
        res[w] = ordliste[w]
    for p in res.most_common():
        if p[1] != 0:
            print(p[0], p[1])
        else:
            break
    return True

def nb_ngram(terms, corpus='bok', smooth=3, years=(1810, 2010), mode='relative'):
    df = ngram_conv(get_ngram(terms, corpus=corpus), smooth=smooth, years=years, mode=mode)
    df.index = df.index.astype(int)
    return df

def get_ngram(terms, corpus='avis'):
    req = requests.get(
        "http://www.nb.no/sp_tjenester/beta/ngram_1/ngram/query?terms={terms}&corpus={corpus}".format(
            terms=terms,
            corpus=corpus
        ))
    if req.status_code == 200:
        res = req.text
    else:
        res = "[]"
    return json.loads(res)

def ngram_conv(ngrams, smooth=1, years=(1810,2013), mode='relative'):
    ngc = {}
    # check if relative frequency or absolute frequency is in question
    if mode.startswith('rel') or mode=='y':
        arg = 'y'
    else:
        arg = 'f'
    for x in ngrams:
        if x != []:
            ngc[x['key']] = {z['x']:z[arg] for z in x['values'] if int(z['x']) <= years[1] and int(z['x']) >= years[0]}
    return pd.DataFrame(ngc).rolling(window=smooth, win_type='triang').mean()


def make_graph(words, lang='nob', cutoff=20, leaves=0):
    """Get galaxy from ngram-database. English and German provided by Google N-gram. 
    Set leaves=1 to get the leaves. Parameter cutoff only works for lang='nob'. 
    Specify English by setting lang='eng' and German by lang='ger'"""
    
    params = dict()
    params['terms'] = words
    params['corpus'] = lang
    params['limit'] = cutoff
    params['leaves'] = leaves
    result = requests.get("https://www.nb.no/sp_tjenester/beta/ngram_1/galaxies/query", params=params)
    G = nx.DiGraph()
    edgelist = []
    if result.status_code == 200:
        graph = json.loads(result.text)
        #print(graph)
        nodes = graph['nodes']
        edges = graph['links']
        for edge in edges:
            edgelist += [(nodes[edge['source']]['name'], nodes[edge['target']]['name'], abs(edge['value']))]
    #print(edgelist)
    G.add_weighted_edges_from(edgelist)

    return G


def get_konk(word, params=None, kind='html'):
    if params is None:
        params = {}

    para = params
    para['word']= word

    corpus = 'bok'
    if 'corpus' in para:
        corpus = para['corpus']
    else:
        para['corpus'] = corpus
        
    r = requests.get('https://api.nb.no/ngram/konk', params=para)
    if kind=='html':
        rows = ""
        row_template = ("<tr>"
                        "<td><a href='{urn}?searchText={kw}' target='_'>{urnredux}</a></td>"
                        "<td>{b}</td>"
                        "<td>{w}</td>"
                        "<td style='text-align:left'>{a}</td>"
                        "</tr>\n")
        if corpus == 'bok':
            for x in r.json():
                rows += row_template.format(
                    kw = word,
                    urn=x['urn'],
                    urnredux=','.join([x['author'], x['title'], str(x['year'])]),
                    b=x['before'],
                    w=x['word'],
                    a=x['after'])
        else:
            #print(r.json())
            for x in r.json():
                rows += row_template.format(
                    kw = word,
                    urn=x['urn'],
                    urnredux='-'.join(x['urn'].split('_')[2:6:3]),
                    b=x['before'],
                    w=x['word'],
                    a=x['after'])
        res = "<table>{rows}</table>".format(rows=rows)
        res = HTML(res)
    elif kind == 'json':
        res = r.json()
    else:
        try:
            if corpus == 'bok':
                res = pd.DataFrame(r.json())
                res = res[['urn','author','title','year','before','word','after']]
            else:
                res = pd.DataFrame(r.json())
                res = res[['urn','before','word','after']]
            
        except:
            res= pd.DataFrame()
        #r = r.style.set_properties(subset=['after'],**{'text-align':'left'})
    return res



def konk_to_html(jsonkonk):
    rows = ""
    row_template = ("<tr>"
                    "<td><a href='{urn}' target='_'>{urnredux}</a></td>"
                    "<td>{b}</td>"
                    "<td>{w}</td>"
                    "<td style='text-align:left'>{a}</td>"
                    "</tr>\n")
    for x in jsonkonk:
        rows += row_template.format(
            urn=x['urn'], urnredux=x['urn'], b=x['before'], w=x['word'], a=x['after'])
    res = "<table>{rows}</table>".format(rows=rows)
    return res

def central_characters(graph, n=10):
    res = Counter(nx.degree_centrality(graph)).most_common(n)
    return res

def central_betweenness_characters(graph, n=10):
    res = Counter(nx.betweenness_centrality(graph)).most_common(n)
    return res
    

def get_urnkonk(word, params=None, html=True):
    if params is None:
        params = {}

    para = params
    para['word']= word
    try:
        para['urns'] = pure_urn(para['urns'])
    except:
        print('Parameter urns missing')
    r = requests.post('https://api.nb.no/ngram/urnkonk', json = para)
    if html:
        rows = ""
        for x in r.json():
            rows += """<tr>
                <td>
                    <a href='{urn}?searchText={kw}' target='_blank' style='text-decoration:none'>{urnredux}</a>
                </td>
                <td>{b}</td>
                <td>{w}</td>
                <td style='text-align:left'>{a}</td>
            </tr>\n""".format(kw=word,
                              urn=x['urn'],
                              urnredux="{t}, {f}, {y}".format(t=x['title'], f=x['author'], y=x['year']),
                              b=x['before'],
                              w=x['word'],
                              a=x['after']
                             )
        res = """<table>{rows}</table>""".format(rows=rows)
        res = HTML(res)
    else:
        res = pd.DataFrame(r.json())
        res = res[['urn','before','word','after']]
        #r = r.style.set_properties(subset=['after'],**{'text-align':'left'})
    return res

def frame(something, name = None):
    """Try to make a frame out of something and name columns according to name, which should be a string or a list of strings,
    one for each column. Mismatch in numbers is taken care of."""
    
    if isinstance(something, dict):
        res = pd.DataFrame.from_dict(something, orient='index')
    else:
        res =  pd.DataFrame(something)
    number_of_columns = len(res.columns)
    if name != None:
        if isinstance(name, list):
            if len(name) >= number_of_columns:
                res.columns = name[:number_of_columns]
            else:
                res.columns = name + list(range(len(name), number_of_columns))
        else:
            res.columns = [name] + list(range(1, number_of_columns))
    return res

def get_urns_from_docx(document):
    """Find all URNs specified in a Word document - typically .docx"""
    import sys
    import zipfile
    import re
    from bs4 import BeautifulSoup

    with zipfile.ZipFile(document, 'r') as zfp:
        with zfp.open('word/document.xml') as fp:
            soup = BeautifulSoup(fp.read(), 'xml')

    return re.findall("[0-9]{13}", str(soup))

def get_urns_from_text(document):
    """Find all URNs in a text-file"""
    
    import re

    with open(document) as fp:
        text = fp.read()
    #print(text)
    return re.findall("[0-9]{13}", text)


def get_urns_from_files(mappe, file_type='txt'):
    """Find URNs in files in a folder - specify folder"""
    import os
    froot, _, files = next(os.walk(mappe))
    urns = dict()
    for f in files:
        fn = (os.path.join(froot, f))
        #print(fn)
        if f.endswith('.docx'):
            urns[f] = get_urns_from_docx(fn)
        elif f.endswith('.txt'):
            urns[f] = get_urns_from_text(fn)
    return urns


#======================== Utilities

def xmlpretty(xmls):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(xmls, features='lxml')
    soup.prettify()
    # '<html>\n <head>\n </head>\n <body>\n  <a href="http://example.com/">\n...'

    print(soup.prettify())

def dewey(dewey):
    r = requests.get("https://api.nb.no:443/dewey/v1/list", params={'class':dewey, 'language':'nob'})
    try:
        ddk = r.json()

        ddc = dict()

        if 'deweyPathList' in ddk:
            for item in ddk['deweyPathList']:
                ddc[str(item['level'])] = [item['classValue'], item['heading']]
    except:
        ddc = []
    return ddc

def metadata_xml(URN, kind='marcxml'):
    if isinstance(URN, int):
        URN = "URN:NBN:no-nb_digibok_{urn}".format(urn=str(URN))
    elif isinstance(URN, str):
        if URN.startswith('URN'):
            URN = URN
        else:
            URN = "URN:NBN:no-nb_digibok_{urn}".format(urn=URN)
    
    r = requests.get("https://api.nb.no:443/catalog/v1/metadata/{urn}/{kind}".format(urn=URN, kind=kind))
    try:
        res = r.text
    except:
        res = ""
    return res
