import inspect
import json
import os
import re
import sys
import zipfile
from collections import Counter
from random import sample
from typing import List, Tuple, Union, Iterable, Dict

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import numpy.random
import pandas as pd
import requests
import seaborn as sns
from IPython.display import HTML
from bs4 import BeautifulSoup
from matplotlib.pylab import rcParams

try:
    from wordcloud import WordCloud
except BaseException:
    pass #print(f"wordcloud er ikke installert, kan ikke lage ordskyer")


# ************** For defining wordbag search

def dict2pd(dictionary):
    res = pd.DataFrame.from_dict(dictionary).fillna(0)
    s = (res.mean(axis=0))
    s = s.rename('snitt')
    res = res.append(s)
    return res.sort_values(by='snitt', axis=1, ascending=False).transpose()


def def2dict(ddef):
    res = {}
    defs = ddef.split(';')
    for d in defs:
        lex = d.split(':')
        if len(lex) == 2:
            # print('#'.join(lex))
            hyper = lex[0].strip()
            occurrences = [x.strip() for x in lex[1].split(',')]
            res[hyper] = occurrences
    for value in res.values():
        for element in value:
            if element.capitalize() not in value:
                value.append(element.capitalize())
    return res


def create_wordbag_parameters(wordbag, urns):
    if isinstance(urns, list):
        if isinstance(urns[0], list):
            urns = [u[0] for u in urns]
    else:
        urns = [urns]
    param = {'wordbags': wordbag, 'urns': urns}
    return param


def wordbag_eval(wordbag, urns):
    param = create_wordbag_parameters(wordbag, urns)
    r = requests.post("https://api.nb.no/ngram/wordbags", json=param)
    return dict2pd(r.json())


def wordbag_eval_para(wordbag, urns):
    param = create_wordbag_parameters(wordbag, urns)
    r = requests.post("https://api.nb.no/ngram/wordbags_para", json=param)
    return r.json()


def get_paragraphs(urn, paras):
    """Return paragraphs for urn."""
    param = {'paragraphs': paras, 'urn': urn}
    r = requests.get("https://api.nb.no/ngram/paragraphs", json=param)
    return dict2pd(r.json())


# ******************* wordbag search end

def ner(text=None, dist=False):
    """Analyze text for named entities.

    :param dist:
        If True, return the four values that go into decision.
    """
    r = []
    if text is not None:
        r = requests.post("https://api.nb.no/ngram/ner",
                          json={'text': text, 'dist': dist})
    return r.json()


# **** names ****

def check_navn(name, limit=2,
               remove: list = None):
    """Removes all items in navn with frequency below limit,
    and words in all cases as well as all words in list 'remove'.
    """
    remove = ('Ja Nei Nå Dem De Deres Unnskyld Ikke Ah Hmm Javel Akkurat '
              'Jaja Jaha').split() if remove is None else remove
    r = {x: name[x] for x in name if
         name[x] > limit and x.upper() != x and x not in remove}
    return r


def sentences(urns, num=300):
    if isinstance(urns[0], list):
        urns = [str(x[0]) for x in urns]
    params = {'urns': urns,
              'num': num}
    res = requests.get("https://api.nb.no/ngram/sentences", params=params)
    return res.json()


def names(urn, ratio=0.3, cutoff=2):
    """ Return names in book with urn.
    Returns uni- , bi-, tri- and quadgrams.
    """
    if isinstance(urn, list):
        urn = urn[0]
    r = requests.get('https://api.nb.no/ngram/names',
                     json={'urn': urn, 'ratio': ratio, 'cutoff': cutoff})
    x = r.json()
    result = (
        Counter(x[0][0]),
        Counter({tuple(x[1][i][0]): x[1][i][1] for i in range(len(x[1]))}),
        Counter({tuple(x[2][i][0]): x[2][i][1] for i in range(len(x[2]))}),
        Counter({tuple(x[3][i][0]): x[3][i][1] for i in range(len(x[3]))})
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
    """Sum up word frequencies across urns."""

    if isinstance(urnlist[0], list):
        urnlist = [u[0] for u in urnlist]
    r = requests.post("https://api.nb.no/ngram/book_aggregates",
                      json={'urns': urnlist})
    return r.json()


# Norweigan word bank
def word_variant(word, form):
    """ Find alternative form for a given word form,
    e.g. word_variant('spiste', 'pres-part').
    """
    r = requests.get("https://api.nb.no/ngram/variant_form",
                     params={'word': word, 'form': form})
    return r.json()


def word_paradigm(word):
    """ Find alternative form for a given word form,
    e.g. word_variant('spiste', 'pres-part').
    """
    r = requests.get("https://api.nb.no/ngram/paradigm", params={'word': word})
    return r.json()


def word_form(word):
    """Find alternative form for a given word form,
    e.g. word_variant('spiste', 'pres-part').
    """
    r = requests.get(
        "https://api.nb.no/ngram/word_form", params={'word': word}
    )
    return r.json()


def word_lemma(word):
    """Find lemma form for a given word form."""
    r = requests.get("https://api.nb.no/ngram/word_lemma",
                     params={'word': word})
    return r.json()


def word_freq(urn, words):
    """Find frequency of words within urn."""
    params = {'urn': urn, 'words': words}
    r = requests.post("https://api.nb.no/ngram/freq", json=params)
    return dict(r.json())


def tot_freq(words):
    """Find total frequency of words."""
    params = {'words': words}
    r = requests.post("https://api.nb.no/ngram/word_frequencies", json=params)
    return dict(r.json())


def book_count(urns):
    params = {'urns': urns}
    r = requests.post("https://api.nb.no/ngram/book_count", json=params)
    return dict(r.json())


def sttr(urn: Union[str, int], chunk: int = 5000) -> float:
    """Compute a standardized type/token-ratio for text identified with urn.

    :param urn: The serial number of a URN for a book
    :param chunk: The number of words from the book to do the calculations with
    :return: The type/token-ratio as a floating point number
    """
    r = requests.get("https://api.nb.no/ngram/sttr",
                     json={'urn': urn, 'chunk': chunk})
    return r.json()


def totals(top=200):
    """Returns a dictionary of the top `top` number of words in the
    digital collection."""
    r = requests.get("https://api.nb.no/ngram/totals", json={'top': top})
    return dict(r.json())


def navn(urn: Union[List, str, int]) -> Dict:
    """Extract possible names in some document(s) and count their frequencies.

    :param urn: Serial number(s) of document(s) in NB Digital
    :return: Dict of frequencies for possible names in the document(s)
    """
    if isinstance(urn, list):
        urn = urn[0]
    r = requests.get('https://api.nb.no/ngram/tingnavn', json={'urn': urn})
    return dict(r.json())


def digibokurn_from_text(T):
    """Return URNs as 13 digits.

    Any sequence of 13 digits is counted as a URN.
    """
    return re.findall("(?<=digibok_)[0-9]{13}", T)


def urn_from_text(T):
    """Return a list of URNs as 13 digit serial numbers.
    Any sequence of 13 digits is counted as a URN."""
    return re.findall("[0-9]{13}", T)


def metadata(urn: str = None):
    """Return a list of metadata entries for given URN."""
    urns = pure_urn(urn)
    # print(urns)
    r = requests.post("https://api.nb.no/ngram/meta", json={'urn': urns})
    return r.json()


def pure_urn(data):
    """Convert URN-lists with extra data into list of serial numbers.

    Used to convert different ways of presenting URNs
    into a list of serial decimal digits.
    Designed to work with book URNs, and will not work for newspaper URNs.

    :param data:
        May be a list of URNs, a list of lists with URNs
        as their initial element, or a string of raw texts containing URNs.
    :return: List[str]:
        A list of URNs. Empty list if input is on the wrong format
        or contains no URNs.
    """
    korpus_def = []
    if isinstance(data, list):
        if not data:  # Empty list
            korpus_def = []
        if isinstance(data[0], list):  # List of lists
            try:
                korpus_def = [str(x[0]) for x in data]
            except IndexError:
                korpus_def = []
        else:  # Assume data is already a list of URNs
            korpus_def = [str(int(x)) for x in data]
    elif isinstance(data, str):
        korpus_def = [str(x) for x in urn_from_text(data)]
    elif isinstance(data, (int, np.integer)):
        korpus_def = [str(data)]
    elif isinstance(data, pd.DataFrame):
        col = data.columns[0]
        urns = pd.to_numeric(data[col])
        korpus_def = [str(int(x)) for x in urns.dropna()]
    elif isinstance(data, pd.Series):
        korpus_def = [str(int(x)) for x in data.dropna()]
    return korpus_def


# N-Grams from fulltext updated

def unigram(word, period=(1950, 2020), media='bok', ddk=None, topic=None,
            gender=None, publisher=None, lang=None, trans=None):
    r = requests.get("https://api.nb.no/ngram/unigrams", params={
        'word': word,
        'ddk': ddk,
        'topic': topic,
        'gender': gender,
        'publisher': publisher,
        'lang': lang,
        'trans': trans,
        'period0': period[0],
        'period1': period[1],
        'media': media
    })
    return frame(dict(r.json()))


def bigram(first, second, period=(1950, 2020), media='bok', ddk=None,
           topic=None, gender=None, publisher=None, lang=None, trans=None):
    r = requests.get("https://api.nb.no/ngram/bigrams", params={
        'first': first,
        'second': second,
        'ddk': ddk,
        'topic': topic,
        'gender': gender,
        'publisher': publisher,
        'lang': lang,
        'trans': trans,
        'period0': period[0],
        'period1': period[1],
        'media': media
    })
    return frame(dict(r.json()))


def book_counts(period=(1800, 2050)):
    r = requests.get("https://api.nb.no/ngram/book_counts", params={

        'period0': period[0],
        'period1': period[1],
    })
    return frame(dict(r.json()))


####

def difference(first, second, rf, rs, years=(1980, 2000), smooth=1,
               corpus='bok'):
    """Compute difference of difference (first/second)/(rf/rs) for n-grams."""
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
        f1 = s_a[a.columns[0]] / s_a[a.columns[1]]
        f2 = s_b[b.columns[0]] / s_b[b.columns[1]]
        res = f1 / f2
    # W0702: No exception type(s) specified (bare-except)
    except BaseException:
        res = 'Mangler noen data - har bare for: ' + ', '.join(
            list(a.columns.append(b.columns)))
    return res


def df_combine(array_df):
    """Combine single-column-dataframes into one dataframe."""
    cols = []
    # E0602: Undefined variable 'a' (undefined-variable).
    # Antar at 'a' skulle være array_df
    for i in enumerate(array_df):
        # print(i)
        if array_df[i].columns[0] in cols:
            array_df[i].columns = [array_df[i].columns[0] + '_' + str(i)]
        cols.append(array_df[i].columns[0])
    return pd.concat(array_df, axis=1, sort=True)


def col_agg(df, col='sum'):
    """Aggregate columns of a pandas dataframe."""
    c = df.sum(axis=0)
    c = pd.DataFrame(c)
    c.columns = [col]
    return c


def row_agg(df, col='sum'):
    """Aggregate rows of a pandas dataframe."""
    c = df.sum(axis=1)
    c = pd.DataFrame(c)
    c.columns = [col]
    return c


def get_freq(urn, top=50, cutoff=3):
    """Get frequency list of words for a given URN.

    :param urn: A serial number for an item in the digital collection.
    :return: A Counter object of term types and their frequencies.
    """
    if isinstance(urn, list):
        urn = urn[0]
    r = requests.get("https://api.nb.no/ngram/urnfreq",
                     json={'urn': urn, 'top': top, 'cutoff': cutoff})
    return Counter(dict(r.json()))


# =============== GET URNS ================== #
def book_corpus(words=None, author=None,
                title=None, subtitle=None, ddk=None, subject=None,
                period=(1100, 2020),
                gender=None,
                lang=None,
                trans=None,
                limit=20):
    return frame(
        book_urn(words, author, title, subtitle, ddk, subject, period, gender,
                 lang, trans, limit),
        "urn author title year".split())


def book_urn(words=None, author=None,
             title=None, subtitle=None, ddk=None, subject=None,
             period=(1100, 2020),
             gender=None,
             lang=None,
             trans=None,
             limit=20):
    """Get URNs for books with metadata"""
    dataframe = inspect.currentframe()
    args, _, _, values = inspect.getargvalues(dataframe)
    query = {
        i: values[i] for i in args if values[i] is not None and i != 'period'
    }
    query['year'] = period[0]
    query['next'] = period[1] - period[0]
    return get_urn(query)


def unique_urns(korpus, newest=True):
    author_title = {(c[1], c[2]) for c in korpus}
    corpus = {
        (c[0], c[1]): [d for d in korpus if c[0] == d[1] and c[1] == d[2]]
        for c in author_title
    }
    for c in corpus:
        corpus[c].sort(key=lambda c: c[3])

    if newest:
        res = [corpus[c][-1] for c in corpus]
    else:
        res = [corpus[c][0] for c in corpus]
    return res


def refine_book_urn(urns=None, words=None, author=None,
                    title=None, ddk=None, subject=None, period=(1100, 2020),
                    gender=None, lang=None, trans=None, limit=20):
    """Refine URNs for books with metadata"""

    # if empty urns nothing to refine

    if urns is None or urns == []:
        return []

    # check if urns is a metadata list,
    # and pick out first elements if that is the case
    if isinstance(urns[0], list):
        urns = [x[0] for x in urns]

    dataframe = inspect.currentframe()
    args, _, _, values = inspect.getargvalues(dataframe)
    query = {i: values[i] for i in args if
             values[i] is not None and i != 'period' and i != 'urns'}
    query['year'] = period[0]
    query['next'] = period[1] - period[0]
    # print(query)
    return refine_urn(urns, query)


def best_book_urn(word=None, author=None,
                  title=None, ddk=None, subject=None, period=(1100, 2020),
                  gender=None, lang=None, trans=None, limit=20):
    """Get URNs for books with metadata"""

    if word is None:
        return []

    dataframe = inspect.currentframe()
    args, _, _, values = inspect.getargvalues(dataframe)
    query = {i: values[i] for i in args if
             values[i] is not None and i != 'period' and i != 'word'}
    query['year'] = period[0]
    query['next'] = period[1] - period[0]
    return get_best_urn(word, query)


def get_urn(meta_data: dict = None):
    """Get URNs from metadata.

    :param meta_data: A dictionary of metadata.   Expected keys are:

        * `"corpus"`: "avis" or "bok".
        * `"author"`: Wildcard match using % as wildcard.
        * `"title"`:  Wildcard match using %.
          For newspapers this corresponds to name of paper.
        * `"year"`:   Integer (e.g. 1900, the default value),
          or string (e.g. "1900").
        * `"next"`: The number of years after `year`
          to include in the URN search. Defaults to 100.
        * `"ddk"`:    Dewey decimal number as wildcard match e.g. "64%".
        * `"gender"`: "m" for male or "f" for female.
        * `"subject"`: Keywords used to annotate text
          in the national bibliography.

    """
    if meta_data is None:
        meta_data = {}
    if not ('next' in meta_data or 'neste' in meta_data):
        meta_data['next'] = 100
    if 'year' not in meta_data:
        meta_data['year'] = 1900
    r = requests.get('https://api.nb.no/ngram/urn', json=meta_data)
    return r.json()


def refine_urn(urns, meta_data=None):
    """Refine a list urns using extra information"""
    if meta_data is None:
        meta_data = {}
    meta_data['urns'] = urns
    if 'words' not in meta_data:
        meta_data['words'] = []
    if not ('next' in meta_data or 'neste' in meta_data):
        meta_data['next'] = 520
    if 'year' not in meta_data:
        meta_data['year'] = 1500
    r = requests.post('https://api.nb.no/ngram/refineurn', json=meta_data)
    return r.json()


def get_best_urn(word, meta_data=None):
    """Get the best urns from metadata containing a specific word"""
    meta_data['word'] = word
    if not ('next' in meta_data or 'neste' in meta_data):
        meta_data['next'] = 600
    if 'year' not in meta_data:
        meta_data['year'] = 1500
    r = requests.get('https://api.nb.no/ngram/best_urn', json=meta_data)
    return r.json()


def get_papers(top=5, cutoff=5, name='%', yearfrom=1800, yearto=2020,
               samplesize=100):
    """Get newspapers as frequency lists.

    :param top: Number of top ranked words.
    :param cutoff: The lower frequency limit. Defaults to 5 occurrences.
    :param name:
        A string, indicating the title of a newspaper.
        Defaults to the wildcard symbol '%'.
    :param yearfrom: Start of time range for the query.
    :param yearto: End of time for the query.
    :param samplesize: Number of newspapers to return.
    :return:
        A list of dictionaries with the term frequencies for the newspapers.
    """

    def div(x, y):
        return int(x / y), x % y

    chunks = 20

    # split samplesize into chunks,
    # go through the chunks and then the remainder

    (first, second) = div(samplesize, chunks)
    r = []

    # collect chunkwise
    for _ in range(first):
        r += requests.get("https://api.nb.no/ngram/avisfreq",
                          json={'navn': name, 'top': top, 'cutoff': cutoff,
                                'yearfrom': yearfrom, 'yearto': yearto,
                                'samplesize': chunks}
                          ).json()

    # collect the remainder
    r += requests.get("https://api.nb.no/ngram/avisfreq",
                      json={'navn': name, 'top': top, 'cutoff': cutoff,
                            'yearfrom': yearfrom, 'yearto': yearto,
                            'samplesize': second}
                      ).json()

    return [dict(x) for x in r]


def urn_coll(word, urns=None, after=5, before=5, limit=1000):
    """Find collocations for `word` in a collection of book URNs.
    Only books at the moment.

    :param word: String with word to find collocations for.
    :param urns:
        List of URN serial numbers,
        or list of lists with a URN as the first element.
    :param after: Number of words following `word`
    :param before: Number of words preceding `word`
    :param limit: Maximum number of occurrences of `word` per URN.
    :return: Dataframe with collocations
    """

    if urns is None:
        urns = []
    # urns assumed to be list of list with urn-serial as first element
    if isinstance(urns[0], list):
        urns = [u[0] for u in urns]

    r = requests.post("https://api.nb.no/ngram/urncoll",
                      json={'word': word, 'urns': urns,
                            'after': after, 'before': before, 'limit': limit})
    res = pd.DataFrame.from_dict(r.json(), orient='index')
    if not res.empty:
        res = res.sort_values(by=res.columns[0], ascending=False)
    return res


def urn_coll_words(words, urns=None, after=5, before=5, limit=1000):
    """Find collocations for a group of words within a set of books
    given by a list of URNs.
    Only books at the moment
    """
    coll = pd.DataFrame()
    if urns is not None:
        # urns assumed to be list of list with urn-serial as first element
        if isinstance(urns[0], list):
            urns = [u[0] for u in urns]
        if isinstance(words, str):
            words = words.split()
        res = Counter()
        for word in words:
            try:
                res += Counter(
                    requests.post(
                        "https://api.nb.no/ngram/urncoll",
                        json={
                            'word': word,
                            'urns': urns,
                            'after': after,
                            'before': before,
                            'limit': limit}
                    ).json()
                )
            # W0702: No exception type(s) specified (bare-except)
            except BaseException:
                pass
        coll = pd.DataFrame.from_dict(res, orient='index')
        if not coll.empty:
            coll = coll.sort_values(by=coll.columns[0], ascending=False)
    return coll


def get_aggregated_corpus(urns, top=0, cutoff=0):
    res = Counter()
    # urns assumed to be list of list with urn-serial as first element
    if isinstance(urns[0], list):
        urns = [u[0] for u in urns]
    for u in urns:
        # print(u)
        res += get_freq(u, top=top, cutoff=cutoff)
    return pd.DataFrame.from_dict(res, orient='index').sort_values(
        by=0, ascending=False)


def compare_word_bags(bag_of_words, another_bag_of_words, first_freq=0,
                      another_freq=1, top=100, first_col=0, another_col=0):
    """Compare two columns taken from two or one frame.
    Parameters x_freq are frequency limits used to cut down candidate words
    from the bag of words.
    Compare along the columns where
    first_col and another_col are column numbers.
    Typical situation is that bag_of_words is a one column frame
    and another_bag_of_words is another one column frame.
    When the columns are all from one frame,
    just change column numbers to match the columns."""
    diff = (
        bag_of_words[bag_of_words > first_freq][bag_of_words.columns[first_col]] /
        another_bag_of_words[another_bag_of_words > another_freq][
            another_bag_of_words.columns[another_col]]
    )

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
    """Compute a collocation for a given word within indicated period.

    :param word: str
    :param yearfrom: int
    :param yearto: int
    :param before: The number of preceding words
    :param after:  The number of words following `word`
    :param limit: int
    :param corpus: str, default to 'avis'
    :param title: str
    :param ddk: str
    :param subtitle: str
    :return: A dataframe with the collocations
    """
    data = requests.get(
        "https://api.nb.no/ngram/collocation",
        params={
            'word': word,
            'corpus': corpus,
            'yearfrom': yearfrom,
            'before': before,
            'after': after,
            'limit': limit,
            'yearto': yearto,
            'title': title,
            'ddk': ddk,
            'subtitle': subtitle}).json()
    return pd.DataFrame.from_dict(data['freq'], orient='index')


def collocation_data(words, yearfrom=2000, yearto=2005, limit=1000, before=5,
                     after=5, title='%', corpus='bok'):
    """Collocation for a set of words sum up all the
    collocations words is a list of words or a
    blank separated string of words.
    """
    a = {}

    if isinstance(words, str):
        words = words.split()

    for word in words:

        print(word)
        try:

            a[word] = collocation(
                word,
                yearfrom=yearfrom, yearto=yearto, limit=limit,
                corpus=corpus, before=before,
                after=after, title=title
            )

            a[word].columns = [word]

        # W0702: No exception type(s) specified (bare-except)
        except BaseException:
            print(word, ' feilsituasjon', sys.exc_info())
    result = pd.DataFrame()
    for w in a.values():
        result = result.join(w, how='outer')
    return pd.DataFrame(result.sum(axis=1)).sort_values(by=0, ascending=False)


class CollocationCorpus:

    def __init__(self, corpus=None, name='', maximum_texts=500):
        urns = pure_urn(corpus)

        if len(urns) > maximum_texts:
            selection = numpy.random.choice(urns, maximum_texts)
        else:
            selection = urns

        self.corpus_def = selection
        self.corpus = get_aggregated_corpus(self.corpus_def, top=0, cutoff=0)

    def summary(self, head=10):
        info = {
            'corpus_definition': self.corpus[:head],
            'number_of_words': len(self.corpus)

        }
        return info


def collocation_old(word, yearfrom=2010, yearto=2018, before=3, after=3,
                    limit=1000, corpus='avis'):
    data = requests.get(
        "https://api.nb.no/ngram/collocation",
        params={
            'word': word,
            'corpus': corpus,
            'yearfrom': yearfrom,
            'before': before,
            'after': after,
            'limit': limit,
            'yearto': yearto}).json()
    return pd.DataFrame.from_dict(data['freq'], orient='index')


def heatmap(df: pd.DataFrame, color='green'):
    """A wrapper for heatmap of a dataframe `df`."""
    return df.fillna(0).style.background_gradient(
        cmap=sns.light_palette(color, as_cmap=True))


def get_corpus_text(urns, top=0, cutoff=0):
    """From a list of URNs that constitute a corpus,
    get the `top` most frequent words with a frequency above `cutoff`,
    and create a dataframe where each column represents a URN
    and each row is a frequent term.
    Uses :func:`get_freq` to get the frequency lists.

    Implementation summary::

        k = dict()
        for u in urns:
            k[u] = get_freq(u, top = top, cutoff = cutoff)
        return pd.DataFrame(k)

    :param urns: List of URN identifiers for the corpus.
    :param top: The number of most frequent terms to return.
    :param cutoff: The lower frequency limit.
    :return: A dataframe with URNs as row headers and words as indices.
    """
    k = {}
    if isinstance(urns, list):
        # a list of urns, or a korpus with urns as first element
        if isinstance(urns[0], list):
            urns = [u[0] for u in urns]
    else:
        # assume it is a single urn, text or number
        urns = [urns]
    for u in urns:
        # print(u)
        k[u] = get_freq(u, top=top, cutoff=cutoff)
    df = pd.DataFrame(k)
    res = df.sort_values(by=df.columns[0], ascending=False)
    return res


def normalize_corpus_dataframe(df: pd.DataFrame) -> bool:
    """Normalize all values in the `df` corpus.
    Changes `df` in situ, and returns `True`."""
    colsums = df.sum()
    for x in colsums.index:
        # print(x)
        df[x] = df[x].fillna(0) / colsums[x]
    return True


def show_korpus(korpus, start=0, size=4, vstart=0, vsize=20, sortby=''):
    """Show corpus as a pandas dataframe.

    :param korpus:  dataframe containing information about a corpus
    :param start:   int, column number indicating which document to show first.
                    Dataframe is sorted according to this.
    :param size:    int, number of columns (i.e. documents) that are shown
    :param vstart:  int, index number of row to start on
    :param vsize:   int, number of rows (i.e. words) to show
    :param sortby:  str, name of column to sort frequency values by.
                    Sorts by first column by default.
    :return:        Sliced view of the `korpus` pandas dataframe
    """
    if sortby != '':
        val = sortby
    else:
        val = korpus.columns[start]
    return korpus[korpus.columns[start:start + size]].sort_values(
        by=val, ascending=False)[vstart:vstart + vsize]


def aggregate(korpus):
    """Make an aggregated sum of all documents across the corpus.
    Here we use the average mean."""
    return pd.DataFrame(korpus.fillna(0).mean(axis=1))


def convert_list_of_freqs_to_dataframe(referanse):
    """Convert and normalize `referanse`, a list of term frequencies,
    e.g. as the one returned by :func:`get_papers`.
    """
    res = []
    for x in referanse:
        res.append(dict(x))
    result = pd.DataFrame(res).transpose()
    normalize_corpus_dataframe(result)
    return result


def get_corpus(top=0, cutoff=0, name='%', corpus='avis', yearfrom=1800,
               yearto=2020, samplesize=10):
    """Collect a corpus using :func:`get_papers` (for newspapers)
    and :func:`get_corpus` (for books).

    :return: Whatever :func:`get_papers` or :func:`get_corpus` returns.
    """

    if corpus == 'avis':
        result = get_papers(top=top, cutoff=cutoff, name=name,
                            yearfrom=yearfrom, yearto=yearto,
                            samplesize=samplesize)
        res = convert_list_of_freqs_to_dataframe(result)
    else:
        urns = get_urn(
            {'author': name, 'year': yearfrom, 'neste': yearto - yearfrom,
             'limit': samplesize})
        res = get_corpus_text([x[0] for x in urns], top=top, cutoff=cutoff)
    return res


class Cluster:
    """See clustering notebook for example and closer description."""

    def __init__(self, word='', filename='', period=(1950, 1960), before=5,
                 after=5, corpus='avis', reference=200,
                 word_samples=1000):
        if word != '':
            self.collocates = collocation(word, yearfrom=period[0],
                                          yearto=period[1], before=before,
                                          after=after,
                                          corpus=corpus, limit=word_samples)
            self.collocates.columns = [word]
            if isinstance(reference, pd.core.frame.DataFrame):
                pass  # Keep the reference value as is
            elif isinstance(reference, int):
                reference = get_corpus(
                    yearfrom=period[0],
                    yearto=period[1],
                    corpus=corpus,
                    samplesize=reference)
            else:
                reference = get_corpus(
                    yearfrom=period[0],
                    yearto=period[1],
                    corpus=corpus,
                    samplesize=int(reference))

            self.reference = aggregate(reference)
            self.reference.columns = ['reference_corpus']
            self.word = word
            self.period = period
            self.corpus = corpus
        else:
            if filename != '':
                self.load(filename)

    def cluster_set(self, exponent=1.1, top=200, aslist=True):
        combo_corp = self.reference.join(self.collocates, how='outer')
        normalize_corpus_dataframe(combo_corp)
        korpus = compute_assoc(combo_corp, self.word, exponent)
        korpus.columns = [self.word]
        if top <= 0:
            res = korpus.sort_values(by=self.word, ascending=False)
        else:
            res = korpus.sort_values(by=self.word, ascending=False).iloc[:top]
        if aslist:
            res = HTML(', '.join(list(res.index)))
        return res

    def add_reference(self, number=20):
        ref = get_corpus(yearfrom=self.period[0], yearto=self.period[1],
                         samplesize=number)
        ref = aggregate(ref)
        ref.columns = ['add_ref']
        normalize_corpus_dataframe(ref)
        self.reference = aggregate(self.reference.join(ref, how='outer'))
        return True

    def save(self, filename=''):
        if filename == '':
            filename = f"{self.word}_{self.period[0]}-{self.period[1]}.json"
        model = {
            'word': self.word,
            'period': self.period,
            'reference': self.reference.to_dict(),
            'collocates': self.collocates.to_dict(),
            'corpus': self.corpus
        }
        with open(filename, 'w', encoding='utf-8') as outfile:
            print('lagrer til:', filename)
            outfile.write(json.dumps(model))
        return True

    def load(self, filename):
        with open(filename, 'r', encoding="utf-8") as infile:
            try:
                model = json.loads(infile.read())
                # print(model['word'])
                self.word = model['word']
                self.period = model['period']
                self.corpus = model['corpus']
                self.reference = pd.DataFrame(model['reference'])
                self.collocates = pd.DataFrame(model['collocates'])
            # W0702: No exception type(s) specified (bare-except)
            except BaseException:
                print('noe gikk galt')
        return True

    def search_words(self, words, exponent=1.1):
        if isinstance(words, str):
            words = [w.strip() for w in words.split()]
        df = self.cluster_set(exponent=exponent, top=0, aslist=False)
        sub = [w for w in words if w in df.index]
        res = df.transpose()[sub].transpose().sort_values(by=df.columns[0],
                                                          ascending=False)
        return res


def wildcardsearch(params: Dict = None) -> pd.DataFrame:
    """See examples in notebook `wildcardsearch`.

    .. todo::
        Fill in reference to example notebook.

    :param params: A dict with the following default values:
        ``{'word': '', 'freq_lim': 50, 'limit': 50, 'factor': 2}``
    :return: A dataframe containing matches for `word`.
    """
    if params is None:
        params = {'word': '', 'freq_lim': 50, 'limit': 50, 'factor': 2}
    res = requests.get('https://api.nb.no/ngram/wildcards', params=params)
    if res.status_code == 200:
        result = res.json()
    else:
        result = {'status': 'feil'}
    resultat = pd.DataFrame.from_dict(result, orient='index')
    if not resultat.empty:
        resultat.columns = [params['word']]
    return resultat


def sorted_wildcardsearch(params):
    """Use :func:`wildcardsearch` and sort results on frequency."""
    res = wildcardsearch(params)
    if not res.empty:
        res = res.sort_values(by=params['word'], ascending=False)
    return res


def make_newspaper_network(key, wordbag, titel='%', yearfrom='1980',
                           yearto='1990', limit=500):
    """NB! Seems not to work at the moment."""
    if isinstance(wordbag, str):
        wordbag = wordbag.split()
    r = requests.post("https://api.nb.no/ngram/avisgraph", json={
        'key': key,
        'words': wordbag,
        'yearto': yearto,
        'yearfrom': yearfrom,
        'limit': limit})
    G = nx.Graph()
    if r.status_code == 200:
        G.add_weighted_edges_from(
            [(x, y, z) for (x, y, z) in r.json() if z > 0 and x != y])
    else:
        print(r.text)
    return G


def make_network(urn, wordbag, cutoff=0) -> nx.Graph:
    """Wrapper for :func:`make_network_graph`."""
    if isinstance(urn, list):
        urn = urn[0]
    if isinstance(wordbag, str):
        wordbag = wordbag.split()
    G = make_network_graph(urn, wordbag, cutoff)
    return G


def make_network_graph(urn, wordbag, cutoff=0):
    """Make a graph as a `networkx` object from `wordbag` and `urn`.
    Two words are connected if they occur within same paragraph.
    """
    r = requests.post("https://api.nb.no/ngram/graph",
                      json={'urn': urn, 'words': wordbag})
    G = nx.Graph()
    G.add_weighted_edges_from(
        [(x, y, z) for (x, y, z) in r.json() if z > cutoff and x != y])
    return G


def make_network_name_graph(urn, tokens, tokenmap=None, cutoff=2):
    if isinstance(urn, list):
        urn = urn[0]

    # tokens should be a list of list of tokens.
    # If it is list of dicts pull out the keys (= tokens)
    if isinstance(tokens[0], dict):
        tokens = [list(x.keys()) for x in tokens]

    r = requests.post(
        "https://api.nb.no/ngram/word_graph",
        json={'urn': urn, 'tokens': tokens, 'tokenmap': tokenmap})
    # print(r.text)
    G = nx.Graph()
    G.add_weighted_edges_from(
        [(x, y, z) for (x, y, z) in r.json() if z > cutoff and x != y])
    return G


def token_convert_back(tokens, sep='_'):
    """ convert a list of tokens to string representation"""
    res = [tokens[0]]
    for y in tokens:
        res.append([tuple(x.split(sep)) for x in y])
    length = len(res)
    for _ in range(1, 4 - length):
        res.append([])
    return res


def token_convert(tokens, sep='_'):
    """ convert back to tuples """
    tokens = [list(x.keys()) for x in tokens]
    tokens = [[(x,) for x in tokens[0]], tokens[1], tokens[2], tokens[3]]
    conversion = []
    for x in tokens:
        conversion.append([sep.join(t) for t in x])
    return conversion


def token_map_to_tuples(tokens_as_strings, sep='_', arrow='==>'):
    tuples = []
    for x in tokens_as_strings:
        token = x.split(arrow)[0].strip()
        mapsto = x.split(arrow)[1].strip()
        tuples.append((tuple(token.split(sep)), tuple(mapsto.split(sep))))
    return tuples


def token_map(tokens, strings=False, sep='_', arrow='==>'):
    """ tokens as from nb.names()"""
    if isinstance(tokens[0], dict):
        # get the keys(),
        # otherwise it is already just a list of tokens up to length 4
        tokens = [list(x.keys()) for x in tokens]

    # convert tokens to tuples and put them all in one list
    tokens = [(x,) for x in tokens[0]] + tokens[1] + tokens[2] + tokens[3]
    tm = []
    # print(tokens)
    for token in tokens:
        if isinstance(token, str):
            trep = (token,)
        elif isinstance(token, list):
            trep = tuple(token)
            token = tuple(token)
        else:
            trep = token
        n = len(trep)
        # print(trep)

        if trep[-1].endswith('s'):
            cp = list(trep[:n - 1])
            cp.append(trep[-1][:-1])
            cp = tuple(cp)

            # print('copy', cp, trep)
            if cp in tokens:
                # print(trep, cp)
                trep = cp

        larger = [ts for ts in tokens if set(ts) >= set(trep)]
        # print(trep, ' => ', larger)
        larger.sort(key=len, reverse=True)
        tm.append((token, larger[0]))
        res = tm
        if strings:
            res = [sep.join(x[0]) + ' ' + arrow + ' ' + sep.join(x[1]) for x in
                   tm]

    return res


def draw_graph_centrality(G, h=15, v=10, fontsize=20, k=0.2, arrows=False,
                          font_color='black', threshold=0.01):
    """Draw a graph using force atlas.

    .. todo:: Fill in parameter descriptions.

    :param G:
    :param h:
    :param v:
    :param fontsize:
    :param k:
    :param arrows:
    :param font_color:
    :param threshold:
    :return:
    """
    node_dict = nx.degree_centrality(G)
    subnodes = dict(
        {x: node_dict[x] for x in node_dict if node_dict[x] >= threshold})
    x, y = rcParams['figure.figsize']
    rcParams['figure.figsize'] = h, v
    pos = nx.spring_layout(G, k=k)
    ax = plt.subplot()
    ax.set_xticks([])
    ax.set_yticks([])
    G = G.subgraph(subnodes)
    nx.draw_networkx_labels(G, pos, font_size=fontsize, font_color=font_color)
    nx.draw_networkx_nodes(G, pos, alpha=0.5, nodelist=subnodes.keys(),
                           node_size=[v * 1000 for v in subnodes.values()])
    nx.draw_networkx_edges(G, pos, alpha=0.7, arrows=arrows,
                           edge_color='lightblue', width=1)

    rcParams['figure.figsize'] = x, y
    return True


def combine(clusters):
    """Make new collocation analyses from data in clusters."""
    collocates = clusters[0].collocates
    for c in clusters[1:]:
        collocates = collocates.join(c.collocates,
                                     rsuffix='-' + str(c.period[0]))
    return collocates


def cluster_join(cluster):
    """Join together serial clusters in one dataframe.

    See example in `cluster` notebook.

    .. todo:: Fill in example notebook reference.

    """
    clusters = [cluster[i] for i in cluster]
    clst = clusters[0].cluster_set(aslist=False)
    for c in clusters[1:]:
        clst = clst.join(c.cluster_set(aslist=False),
                         rsuffix='_' + str(c.period[0]))
    return clst


def serie_cluster(word, start_year, end_year, inkrement, before=5, after=5,
                  reference=150, word_samples=500):
    """Make a series of clusters."""
    tidscluster = {}
    for i in range(start_year, end_year, inkrement):
        tidscluster[i] = Cluster(
            word,
            corpus='avis',
            period=(i, i + inkrement - 1),
            before=after,
            after=after,
            reference=reference,
            word_samples=word_samples)
        print(i, i + inkrement - 1)
    return tidscluster


def save_serie_cluster(tidscluster) -> str:
    """Save series to files."""
    for i in tidscluster:
        tidscluster[i].save()
    return 'OK'


def les_serie_cluster(word, start_year, slutt_year, inkrement) -> Dict:
    """Read serial clusters."""
    tcluster = {}
    for i in range(start_year, slutt_year, inkrement):
        print(i, i + inkrement - 1)
        tcluster[i] = Cluster(filename=f'{word}_{i}-{i + inkrement - 1}.json')
    return tcluster


def make_cloud(json_text, top=100, background='white',
               stretch=lambda x: 2 ** (10 * x), width=500, height=500,
               font_path=None):
    """Create a word cloud from a frequency list."""
    pairs0 = Counter(json_text).most_common(top)
    pairs = {x[0]: stretch(x[1]) for x in pairs0}
    wc = WordCloud(
        font_path=font_path,
        background_color=background,
        width=width,
        # color_func=my_colorfunc,
        ranks_only=True,
        height=height).generate_from_frequencies(pairs)
    return wc


def draw_cloud(sky, width=20, height=20, fil=''):
    """Draw a word cloud produced by :func:`make_cloud`."""
    plt.figure(figsize=(width, height))
    plt.imshow(sky, interpolation='bilinear')
    figplot = plt.gcf()
    if fil != '':
        figplot.savefig(fil, format='png')


def cloud(df, column='', top=200, width=1000, height=1000, background='black',
          file='', stretch=10, font_path=None):
    """Make and draw a cloud from a pandas dataframe, using :func:`make_cloud` and
    :func:`draw_cloud`."""
    if column == '':
        column = df.columns[0]
    data = json.loads(df[column].to_json())
    a_cloud = make_cloud(data, top=top,
                         background=background, font_path=font_path,
                         stretch=lambda x: 2 ** (stretch * x), width=width,
                         height=height)
    draw_cloud(a_cloud, fil=file)


def make_a_collocation(word, period=(1990, 2000), before=5, after=5,
                       corpus='avis', samplesize=100, limit=2000):
    """Create a dataframe containing the given word and the contexts it appears in.
    Filter the result with the parameters.

    :param word: A string, the word of interest.
    :param period: Tuple or list with time range for the query.
    :param before: Number of context words preceding the `word`.
    :param after: Number of context words following `word`.
    :param corpus: String indicating the document type, defaults to 'avis'.
    :param samplesize:  TODO: Fill in description
    :param limit: TODO: Fill in description
    :return: A dataframe with the collocation.
    """

    collocates = collocation(word, yearfrom=period[0], yearto=period[1],
                             before=before, after=after,
                             corpus=corpus, limit=limit)
    collocates.columns = [word]
    reference = get_corpus(yearfrom=period[0], yearto=period[1],
                           samplesize=samplesize)
    ref_agg = aggregate(reference)
    ref_agg.columns = ['reference_corpus']
    return ref_agg


def compute_assoc(coll_frame, column, exponent=1.1):
    """Compute an association using PMI.

    :param coll_frame: A dataframe with the term frequencies.
    :param column: Column with values to calculate associations with.
    :param exponent: Floating point number
    :return: A dataframe with the resulting PMI values.
    """
    return pd.DataFrame(
        coll_frame[column] ** exponent / coll_frame.mean(axis=1))


class Corpus:
    """See `Corpus` notebook for examples and explanation."""

    def __init__(self, filename='', target_urns=None, reference_urns=None,
                 period=(1950, 1960), author='%',
                 title='%', ddk='%', gender='%', subject='%', reference=100,
                 max_books=100):
        params = {
            'year': period[0],
            'next': period[1] - period[0],
            'subject': subject,
            'ddk': ddk,
            'author': author,
            # 'gender':gender, ser ikke ut til å virke for get_urn
            # - sjekk opp APIet
            'title': title,
            'limit': max_books,
            'reference': reference
        }
        self.params = params
        self.coll = {}
        self.coll_graph = {}
        if filename == '':
            if target_urns is not None:
                target_corpus_def = target_urns
            else:
                target_corpus_def = get_urn(params)

            # print("Antall bøker i målkorpus ", len(målkorpus_def))
            if isinstance(target_corpus_def[0], list):
                target_corpus_urn = [str(x[0]) for x in target_corpus_def]
                # print(målkorpus_urn)
            else:
                target_corpus_urn = target_corpus_def
            if len(target_corpus_urn) > max_books > 0:
                target_urn = list(numpy.random.choice(
                    target_corpus_urn, max_books))
            else:
                target_urn = target_corpus_urn

            if reference_urns is not None:
                referansekorpus_def = reference_urns
            else:
                # select from period,
                # usually used only of target is by metadata
                referansekorpus_def = get_urn(
                    {'year': period[0], 'next': period[1] - period[0],
                     'limit': reference})

            # print("Antall bøker i referanse: ", len(referansekorpus_def))
            # referansen skal være distinkt fra målkorpuset
            referanse_urn = [str(x[0]) for x in referansekorpus_def]
            self.reference_urn = referanse_urn
            self.target_urn = target_urn
            # make sure there is no overlap between target and reference
            referanse_urn = list(set(referanse_urn) - set(target_urn))

            target_corpus_txt = get_corpus_text(target_urn)
            normalize_corpus_dataframe(target_corpus_txt)
            if referanse_urn and isinstance(referanse_urn, list):
                referanse_txt = get_corpus_text(referanse_urn)
                normalize_corpus_dataframe(referanse_txt)
                combo = target_corpus_txt.join(referanse_txt)

            else:
                referanse_txt = target_corpus_txt
                combo = target_corpus_txt

            self.combo = combo
            self.reference = referanse_txt
            self.target = target_corpus_txt

            self.reference = aggregate(self.reference)
            self.reference.columns = ['reference_corpus']

            # dokumentfrekvenser

            target_docf = pd.DataFrame(
                pd.DataFrame(
                    target_corpus_txt / target_corpus_txt).sum(axis=1)
            )
            combo_docf = pd.DataFrame(pd.DataFrame(combo / combo).sum(axis=1))
            ref_docf = pd.DataFrame(
                pd.DataFrame(referanse_txt / referanse_txt).sum(axis=1))

            # Normaliser dokumentfrekvensene
            normalize_corpus_dataframe(target_docf)
            normalize_corpus_dataframe(combo_docf)
            normalize_corpus_dataframe(ref_docf)

            self.target_corpus_tot = aggregate(target_corpus_txt)
            self.combo_tot = aggregate(combo)
            self.target_docf = target_docf
            self.combo_docf = combo_docf
            self.lowest = self.combo_tot.sort_values(by=0)[0][0]
        else:
            self.load(filename)

    def difference(self, freq_exp=1.1, doc_exp=1.1, top=200, aslist=True):
        res = pd.DataFrame(
            (
                self.target_corpus_tot ** freq_exp / self.combo_tot
            ) * (
                self.target_docf ** doc_exp / self.combo_docf
            )
        )
        res.columns = ['diff']
        if top > 0:
            res = res.sort_values(
                by=res.columns[0], ascending=False).iloc[:top]
        else:
            res = res.sort_values(
                by=res.columns[0], ascending=False)
        if aslist:
            res = HTML(', '.join(list(res.index)))
        return res

    def save(self, filename):

        model = {
            'params': self.params,
            'target': self.target_corpus_tot.to_json(),
            'combo': self.combo_tot.to_json(),
            'target_df': self.target_docf.to_json(),
            'combo_df': self.combo_docf.to_json()
        }

        with open(filename, 'w', encoding='utf-8') as outfile:
            outfile.write(json.dumps(model))
        return True

    def load(self, filename):
        with open(filename, encoding="utf-8") as infile:
            try:
                model = json.loads(infile.read())
                # print(model['word'])
                self.params = model['params']
                # print(self.params)
                self.target_corpus_tot = pd.read_json(model['target'])
                # print(self.målkorpus_tot[:10])
                self.combo_tot = pd.read_json(model['combo'])
                self.target_docf = pd.read_json(model['target_df'])
                self.combo_docf = pd.read_json(model['combo_df'])
            # W0702: No exception type(s) specified (bare-except)
            except BaseException:
                print('noe gikk galt')
        return True

    def collocations(self, word, after=5, before=5, limit=1000):
        """Find collocations for word in a set of book URNs.
        Only books at the moment."""

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
        self.coll[word] = temp.sort_values(by=temp.columns[0], ascending=False)
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
        return get_urnkonk(word,
                           {'urns': urns, 'before': before, 'after': after,
                            'limit': size})

    def sort_collocations(self, word, comparison=None, exp=1.0, above=None):

        if comparison is None:
            comparison = self.combo_tot[0]
        try:
            res = pd.DataFrame(self.coll[word][0] ** exp / comparison)

        except KeyError:
            print(f'Constructing a collocation for {word} '
                  f'with default parameters.')
            self.collocations(word)
            res = pd.DataFrame(self.coll[word][0] ** exp / comparison)
        if above is None:
            above = self.lowest
        res = res[self.combo_tot > above]
        return res.sort_values(by=0, ascending=False)

    def search_collocations(self, word, words, comparison=None, exp=1.0):

        if comparison is None:
            comparison = self.combo_tot[0]
        try:
            res = pd.DataFrame(self.coll[word][0] ** exp / comparison)
        except KeyError:
            print(f'Constructing a collocation for {word} '
                  f'with default parameters.')
            self.collocations(word)
            res = pd.DataFrame(self.coll[word][0] ** exp / comparison)
        search_items = list(set(res.index) & set(words))
        return res.transpose()[search_items].transpose().sort_values(
            by=0, ascending=False)

    def summary(self, head=10):
        info = {
            'parameters': self.params,
            'target_urn': self.target_urn[:head],
            'reference urn': self.reference_urn[:head],

        }
        return info

    def search_words(self, words, freq_exp=1.1, doc_exp=1.1):
        if isinstance(words, str):
            words = [w.strip() for w in words.split()]
        df = self.difference(freq_exp=freq_exp, doc_exp=doc_exp, top=0,
                             aslist=False)
        sub = [w for w in words if w in df.index]
        res = df.transpose()[sub].transpose().sort_values(by=df.columns[0],
                                                          ascending=False)
        return res

    def make_collocation_graph(self, target_word, top=15, before=4, after=4,
                               limit=1000, exp=1):
        """Make a cascaded network of collocations"""

        self.collocations(target_word, before=before, after=after, limit=limit)
        coll = self.sort_collocations(target_word, exp=exp)
        edges = []
        for word in coll[:top].index:
            edges.append((target_word, word))
            if word.isalpha():
                self.collocations(
                    word, before=before, after=after, limit=limit)
                for w in self.sort_collocations(word, exp=exp)[:top].index:
                    if w.isalpha():
                        edges.append((word, w))

        target_graph = nx.Graph()
        target_graph.add_edges_from(edges)
        self.coll_graph[target_word] = target_graph
        return target_graph


def vekstdiagram(urn, params=None):
    """Make a growth diagram for a given book using a set of words.

    :param urn: str or list where the first element is a URN serial number.
    :param dict params:

        * 'words': list of words
        * 'window': chunk size in the book
        * 'pr': how many words are skipped before next chunk

    :return: pandas.Dataframe
    """
    if params is None:
        params = {}

    # if urn is the value of get_urn() it is a list
    # otherwise it just passes
    if isinstance(urn, list):
        urn = urn[0]

    para = params
    para['urn'] = urn
    r = requests.post('https://api.nb.no/ngram/vekstdiagram', json=para)
    return pd.DataFrame(r.json())


def plot_book_wordbags(urn, wordbags, window=5000, pr=100):
    """Generate a diagram of wordbags in book.
    Use when plotting more than one growth diagram.
    Have a look at example notebook.

    .. todo:: Add reference to notebook.
    """
    return plot_sammen_vekst(urn, wordbags, window=window, pr=pr)


def gather_wordlists(ordlister):
    c = {}
    if isinstance(ordlister, list):
        if isinstance(ordlister[0], list):
            for liste in ordlister:
                if liste:
                    c[liste[0]] = liste
        else:
            c[ordlister[0]] = ordlister
    else:
        c = ordlister
    return c


def plot_sammen_vekst(urn, ordlister, window=5000, pr=100):
    """Plott alle seriene sammen"""
    rammer = []
    c = gather_wordlists(ordlister)

    for key in c:
        vekst = vekstdiagram(urn, params={'words': c[key], 'window': window,
                                          'pr': pr})
        vekst.columns = [key]
        rammer.append(vekst)
    return pd.concat(rammer)


def spurious_names(n=300):
    topwords = totals(n)
    Removals = [x.capitalize() for x in topwords if x.isalpha()]
    return Removals


def relaterte_ord(word, number=20, score=False):
    """Find related words using eigenvector centrality from networkx.
    Related words are taken from `NB Ngram
    <https://www.nb.no/sp_tjenester/beta/ngram_1/galaxies>`_.

    .. note:: Works for english and german - add parameter!!

    """
    G = make_graph(word)
    res = Counter(nx.eigenvector_centrality(G)).most_common(number)
    if not score:
        res = [x[0] for x in res]
    return res


def check_words(urn: Union[str, list], ordbag: Iterable) -> bool:
    """Find frequency of words in `ordbag` within a book given by `urn`."""
    if isinstance(urn, list):
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


def nb_ngram(
        terms: str,
        corpus: str = 'bok',
        smooth: int = 3,
        years: tuple = (1810, 2010),
        mode: str = 'relative') -> pd.DataFrame:
    """Collect an n-gram as json object from `NB N-gram
    Uses :func:`get_ngram` and :func:`ngram_conv`.

    :param terms: Comma separated n-grams (single words up to trigrams).
    """
    df = ngram_conv(
        get_ngram(terms, corpus=corpus),
        smooth=smooth,
        years=years,
        mode=mode
    )
    df.index = df.index.astype(int)
    return df


def get_ngram(terms="", corpus='avis'):
    reqs = f"https://api.nb.no/dhlab/nb_ngram/ngram/query?terms={terms}&lang=nor&case_sens=0&freq=rel&corpus={corpus}"
    #print(reqs)
    req = requests.get(reqs)
    if req.status_code == 200:
        res = req.text
    else:
        res = "[]"
    return json.loads(res)


def ngram_conv(
        ngrams,
        smooth=1,
        years=(1810, 2013),
        mode='relative'
) -> pd.DataFrame:
    """Convert n-grams to a dataframe."""
    ngc = {}
    # check if relative frequency or absolute frequency is in question
    if mode.startswith('rel') or mode == 'y':
        arg = 'y'
    else:
        arg = 'f'
    for x in ngrams:
        if x:
            ngc[x['key']] = {
                z['x']: z[arg] for z in x['values']
                if years[1] >= int(z['x']) >= years[0]}
    return pd.DataFrame(ngc).rolling(window=smooth, win_type='triang').mean()


def make_graph(words, lang: str = 'nob', cutoff: int = 20, leaves: int = 0):
    """Get galaxy from ngram-database, as used in `NB Ngram galaxies
    <https://www.nb.no/sp_tjenester/beta/ngram_1/galaxies>`_.

    :param words: string or list of words to get a galaxy for.
    :param lang: Defaults to 'nob' (Norwegian Bokmål).
        Specify English by setting lang='eng' and German by lang='ger'.
    :param cutoff: Only works for lang="nob".
    :param leaves: 0 or 1, works as a flag.
        Set leaves = 1 to get the leaves in the resulting galaxy.
    :return:
    """
    params = {
        'terms': words, 'corpus': lang, 'limit': cutoff, 'leaves': leaves
    }
    result = requests.get(
        "https://www.nb.no/sp_tjenester/beta/ngram_1/galaxies/query",
        params=params)
    return make_graph_from_result(result)


def make_graph_from_result(result):
    """Utility function to create a graph from the result of a request
    to the ngram service.
    """
    G = nx.DiGraph()
    edgelist = []
    if result.status_code == 200:
        graph = json.loads(result.text)
        # print(graph)
        nodes = graph['nodes']
        edges = graph['links']
        for edge in edges:
            edgelist += [(nodes[edge['source']]['name'],
                          nodes[edge['target']]['name'],
                          abs(edge['value']))]
    G.add_weighted_edges_from(edgelist)
    return G


def urn_concordance(urns=None, word=None, size=5, before=None, after=None):
    """Find a concordance within a corpus as list of URNs.
    This is a wrapper for :func:`get_urnkonk`"""

    # exit if list of urns is empty
    if urns is None or word is None:
        return []

    # The URNs may be presented in different ways.
    urns = pure_urn(urns)

    # find values and feed everything to get_urnkonk
    dataframe = inspect.currentframe()
    args, _, _, values = inspect.getargvalues(dataframe)
    query = {
        i: values[i] for i in args if values[i] is not None and i != 'word'
    }
    return get_urnkonk(word, query)


def konk(word, urns=None, before=5, after=5):
    if urns is None:
        print('URNer mangler')
        return
    urner = refine_book_urn(words=[word], urns=urns)
    return urn_concordance(word=word, urns=sample(urner, min(20, len(urner))),
                           before=before, after=after)


def concordance(word=None, corpus='bok', author=None, title=None,
                subtitle=None, lang=None, ddk=None, subject=None,
                yearfrom=None, yearto=None, before=None, after=None, size=5,
                gender=None, offset=None, kind='html'):
    if word is None:
        return []
    dataframe = inspect.currentframe()
    args, _, _, values = inspect.getargvalues(dataframe)
    query = {i: values[i] for i in args if
             values[i] is not None and i != 'word' and i != 'kind'}
    return get_konk(word, query, kind=kind)


def get_konk(word, params=None, kind='html'):
    """Get a concordance for given word.

    :param word: str
    :param params: Params are the same as for ``meta_data`` in :func:`get_urn`.
    :param kind: ``'html'``, ``'json'`` or ``''``
    :return: an HTML-page, a json structure, or a pandas dataframe,
        depending on the format specified by ``kind``.
    """
    #  R0912: Too many branches (13/12) (too-many-branches)
    if params is None:
        params = {}

    para = params
    para['word'] = word

    corpus = 'bok'
    if 'corpus' in para:
        corpus = para['corpus']
    else:
        para['corpus'] = corpus

    r = requests.get('https://api.nb.no/ngram/konk', params=para)
    if kind == 'html':
        rows = ""
        row_template = ("<tr>"
                        "<td><a href='{urn}?searchText={kw}' "
                        "target='_'>{urnredux}</a></td>"
                        "<td>{b}</td>"
                        "<td>{w}</td>"
                        "<td style='text-align:left'>{a}</td>"
                        "</tr>\n")
        if corpus == 'bok':
            for x in r.json():
                rows += row_template.format(
                    kw=word,
                    urn=x['urn'],
                    urnredux=','.join(
                        [x['author'], x['title'], str(x['year'])]),
                    b=x['before'],
                    w=x['word'],
                    a=x['after'])
        else:
            # print(r.json())
            for x in r.json():
                rows += row_template.format(
                    kw=word,
                    urn=x['urn'],
                    urnredux='-'.join(x['urn'].split('_')[2:6:3]),
                    b=x['before'],
                    w=x['word'],
                    a=x['after'])
        res = f"<table>{rows}</table>"
        res = HTML(res)
    elif kind == 'json':
        res = r.json()
    else:
        try:
            if corpus == 'bok':
                res = pd.DataFrame(r.json())
                res = res[['urn', 'author', 'title', 'year', 'before', 'word',
                           'after']]
            else:
                res = pd.DataFrame(r.json())
                res = res[['urn', 'before', 'word', 'after']]

        # W0702: No exception type(s) specified (bare-except)
        except BaseException:
            res = pd.DataFrame()
        # r = r.style.set_properties(subset=['after'],**{'text-align':'left'})
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
            urn=x['urn'], urnredux=x['urn'], b=x['before'], w=x['word'],
            a=x['after'])
    res = f"<table>{rows}</table>"
    return res


def central_characters(graph, n: int = 10) -> List[Tuple]:
    """Wrapper around `networkx`."""
    res = Counter(nx.degree_centrality(graph)).most_common(n)
    return res


def central_betweenness_characters(graph, n=10):
    """wrapper around `networkx`."""
    res = Counter(nx.betweenness_centrality(graph)).most_common(n)
    return res


def get_urnkonk(word, params: dict = None, html: bool = True):
    """Equivalent to :func:`get_konk`, but from a list of URNs.

    :return: Either an html page or a dataframe, depending on the `html` flag.
    """
    if params is None:
        params = {}

    para = params
    para['word'] = word
    try:
        para['urns'] = pure_urn(para['urns'])
    # W0702: No exception type(s) specified (bare-except)
    except BaseException:
        print('Parameter urns missing')
    r = requests.post('https://api.nb.no/ngram/urnkonk', json=para)
    if html:
        rows = ""
        for x in r.json():
            rows += f"""<tr>
                <td>
                    <a
                    href='{x['urn']}?searchText={word}'
                    target='_blank'
                    style='text-decoration:none'>
                    {x['title']}, {x['author']}, {x['year']}
                    </a>
                </td>
                <td>{x['before']}</td>
                <td>{x['word']}</td>
                <td style='text-align:left'>{x['after']}</td>
            </tr>\n"""
        res = f"<table>{rows}</table>"
        res = HTML(res)
    else:
        res = pd.DataFrame(r.json())
        res = res[['urn', 'before', 'word', 'after']]
        # r = r.style.set_properties(subset=['after'],**{'text-align':'left'})
    return res


def frame(something, name: Union[str, List[str]] = None) -> pd.DataFrame:
    """Try to make a frame out of ``something``
    and name columns according to ``name``.

    :param something: A collection that can be turned into a dataframe.
    :param name: A string or a list of strings, one for each column.
        Mismatch in numbers (of columns and names) is taken care of.
    """

    if isinstance(something, dict):
        res = pd.DataFrame.from_dict(something, orient='index')
    else:
        res = pd.DataFrame(something)
    number_of_columns = len(res.columns)
    if name is not None:
        if isinstance(name, list):
            if len(name) >= number_of_columns:
                res.columns = name[:number_of_columns]
            else:
                res.columns = name + list(range(len(name), number_of_columns))
        else:
            res.columns = [name] + list(range(1, number_of_columns))
    return res


def frame_sort(dataframe, by=0, ascending=False):
    """Sort a dataframe.
    If value of `by` is a column it will sort by that, otherwise it is
    interpreted as an index for the columns."""
    if by in dataframe.columns:
        res = dataframe.sort_values(by=by, ascending=ascending)
    elif isinstance(by, int):
        col = max(by, len(dataframe.columns) - 1)
        res = dataframe.sort_values(
            by=dataframe.columns[col], ascending=ascending)
    else:
        res = dataframe.sort_values(
            by=dataframe.columns[0], ascending=ascending)
    return res


def get_urns_from_docx(document) -> List:
    """Find all URNs specified in a Word document,
    typically a ``.docx`` file."""
    with zipfile.ZipFile(document, 'r') as zfp:
        with zfp.open('word/document.xml') as fp:
            soup = BeautifulSoup(fp.read(), 'xml')

    return re.findall("[0-9]{13}", str(soup))


def get_urns_from_text(document):
    """Find all URNs in a plain text file (``.txt``)"""
    with open(document, encoding="utf-8") as fp:
        text = fp.read()
    # print(text)
    return re.findall("[0-9]{13}", text)


def get_urns_from_files(mappe: str, file_type='txt') -> Dict:
    """Extract URNs from a folder with ``.txt`` and ``.docs`` files.

    :param mappe: Name of the folder to search through.
    :param file_type: Unused parameter.
    :return: A dictionary with filenames as keys, each with a list of URNs.
    """
    froot, _, files = next(os.walk(mappe))
    urns = {}
    for f in files:
        fn = (os.path.join(froot, f))
        # print(fn)
        if f.endswith('.docx'):
            urns[f] = get_urns_from_docx(fn)
        elif f.endswith('.txt'):
            urns[f] = get_urns_from_text(fn)
    return urns


# ======================== Utilities

def xmlpretty(xmls):
    soup = BeautifulSoup(xmls, features='lxml')
    soup.prettify()
    # '<html>\n <head>\n</head>\n <body>\n <a href="http://example.com/">\n...'

    print(soup.prettify())


def dewey(dewey_):
    r = requests.get("https://api.nb.no:443/dewey/v1/list",
                     params={'class': dewey_, 'language': 'nob'})
    try:
        ddk = r.json()
        ddc = {}

        if 'deweyPathList' in ddk:
            for item in ddk['deweyPathList']:
                ddc[str(item['level'])] = [item['classValue'], item['heading']]
    # W0702: No exception type(s) specified (bare-except)
    except BaseException:
        ddc = []
    return ddc


def metadata_xml(URN, kind='marcxml'):
    if isinstance(URN, int):
        URN = f"URN:NBN:no-nb_digibok_{URN}"
    elif isinstance(URN, str):
        if not URN.startswith('URN'):
            URN = f"URN:NBN:no-nb_digibok_{URN}"

    r = requests.get(
        f"https://api.nb.no:443/catalog/v1/metadata/{URN}/{kind}")
    try:
        res = r.text
    # W0702: No exception type(s) specified (bare-except)
    except BaseException:
        res = ""
    return res


def save_frame_to_excel(df, filename, index=False):
    if os.path.exists(filename):
        print(f'Det eksisterer allerede en fil {filename}'
              f' - velg nytt navn og prøv igjen')
        df.to_excel(filename, index=index)


def restore_metadata_from_excel(data):
    df = pd.DataFrame()
    try:
        df = pd.read_excel(data)
        # From excel some stray rows with null values for urn may occur.
        # Drop those.
        indexNames = df[df[df.columns[0]].isnull()].index
        df.drop(indexNames, inplace=True)
        try:
            urn = df.columns[0]
            year = df.columns[2]
            df = df.astype({urn: 'int64', year: 'int'})
            df = df.astype({urn: 'str'})
        # W0702: No exception type(s) specified (bare-except)
        except BaseException:
            pass
    # W0702: No exception type(s) specified (bare-except)
    except BaseException:
        if not os.path.exists(data):
            print(f'filen {data} ble ikke funnet')
        else:
            print('noe gikk galt ved import av dataene')
    return df
