# Modules
This repository only contains python modules for accessing text and pictures at the National Library of Norway.

# nbtext.py



# Metadata and URNs

### `totals(top=200)`
Returns a dictionary of the top ´top´ words in the digital collection


### `urn_from_text(T)`
Return a list of URNs as 13 digit serial numbers. 

### `metadata(urn="""text""")`
Returns a list of metada entries for given URN.

### `pure_urn(data)`
Convert URN-lists with extra data into list of serial numbers. Used to convert different ways of presenting URNs into a list of serial decimal digits. Designed to work with book URNs, and will not work for newspaper URNs.
```    
    Args:
        data: May be a list of URNs, a list of lists with URNs as their
            initial element, or a string of raw texts containing URNs
    Returns:
        List[str]: A list of URNs. Empty list if input is on the wrong
            format or contains no URNs
```


### `col_agg(df, col='sum')`
Aggregate columns of a panda dataframe.

### `row_agg(df, col='sum')`
Aggregate rows of a panda dataframe.


# Access texts as frequency lists

### `get_freq(urn, top=50, cutoff=3)`
Get frequency list of words for a given URN (as a serial number).

### `get_urn(metadata=None)`
Get URNSs from metadata specified as a dictionary. Keys specified in quotes are:
* "corpus": "avis" or "bok"
* "author": wildcard match using % as wildcard.
* "title": wildcard match using %. For newspapers this corresponds to name of paper.
* "year": starting year as number or number as string.
* "next": the next number of years starting from ´year´
*  "ddk": Dewy decimal number as wildcard match e.g. "64%" 
*   "gender": value is "m" for male or "f" for female
*  "subject": keywords used to annotate text in the national bibliography.

### `get_corpus_text(urns, top = 10000, cutoff=5)`
From a corpus as a list of URNs, get the top `top` words that have a frequency above `cutoff`. Builds on top of `get_freq`.
Returns a dataframe with URNs as row headers and words as indices.
``
    k = dict()
    for u in urns:
        k[u] = get_freq(u, top = top, cutoff = cutoff)
    return pd.DataFrame(k)
``
### `get_papers(top=5, cutoff=5, navn='%', yearfrom=1800, yearto=2020, samplesize=100)`
Get newspapers as frequency lists. Parameter `top` asks for the top ranked words, `cutoff` indicates the lower frequency limit, while `navn` indicates newspaper name as wildcard string.


# Collocations and clusters

### `make_a_collocation(word, period=(1990, 2000), before=5, after=5, corpus='avis', samplesize=100, limit=2000)`
Return a collocation as dataframe.


### `compute_assoc(coll_frame, column, exponent=1.1, refcolumn = 'reference_corpus')`
Compute an association using PMI.
``    return pd.DataFrame(coll_frame[column]**exponent/coll_frame.mean(axis=1))``

### `urn_coll(word, urns=[], after=5, before=5, limit=1000)`
limit is max number of occurences of word pr. urn. 
Find collocations for word in a set of book URNs. Only books at the moment

### `collocation(word, yearfrom=2010, yearto=2018, before=3, after=3, limit=1000, corpus='avis')`
Compute a collocation for a given word within indicated period.
`before` is the number of preceeding words, `after` number of words following, `limit`. 
``
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
``



### `normalize_corpus_dataframe(df)`
Normalized all values in corpus `df` as a dataframe. Changes `df` in situ, and returns `True`.

### `show_korpus(korpus, start=0, size=4, vstart=0, vsize=20, sortby = '')`
Show part of a dataframe `korpus`, slicing along columns starting from `start`and numbers by `size` and slicing rows by `vstart`and `vsize`. Sorts by first column by default.

### `aggregate(korpus)`
Make an aggregated sum of all documents across the corpus, here we use average
``    return pd.DataFrame(korpus.fillna(0).mean(axis=1))``

### `convert_list_of_freqs_to_dataframe(referanse)`
The function get_papers() returns a list of frequencies - convert it and normalize.

### `get_corpus(top=5, cutoff=5, navn='%', corpus='avis', yearfrom=1800, yearto=2020, samplesize=10)`
First version of collecting a corpus using parameters described above for `get_papers` (for newspapers) and `get_corpus` (for books).


# Classes

### `class Cluster`
    def __init__(self, word = '', filename = '', period = (1950,1960) , before = 5, after = 5, corpus='avis', reference = 200, 
                 word_samples=1000):
See clustering notebook for example and closer description.

### `class Corpus`
See `Corpus` notebook for examples and explanation.

### `Corpus_urn`
See example notebook

# Graphs and network analysis

### `make_newspaper_network(key, wordbag, titel='%', yearfrom='1980', yearto='1990', limit=500)`
Seems not to work at the moment.

### `make_network(urn, wordbag, cutoff=0)`
Make a graph as `networkx` object from `wordbag` and `urn`. Two words are connected if they occur within same paragraph.

### `make_network_graph(urn, wordbag, cutoff=0)`
Make a graph as `networkx` object from `wordbag` and `urn`. Two words are connected if they occur within same paragraph.

### `draw_graph_centrality(G, h=15, v=10, fontsize=20, k=0.2, arrows=False, font_color='black', threshold=0.01)` 
Draw a graph using force atlas.


# Wordclouds

### `make_cloud(json_text, top=100, background='white', stretch=lambda x: 2**(10*x), width=500, height=500, font_path=None)`*
Create a word cloud from a frequency list. First line of code: ``pairs0 = Counter(json_text).most_common(top)``

### `draw_cloud(sky, width=20, height=20, fil='')`
Draw a word cloud produces by `make_cloud` 

### `cloud(pd, column='', top=200, width=1000, height=1000, background='black', file='', stretch=10, font_path=None)`
Make and draw a cloud from  a pandas dataframe, using `make_cloud` and `draw_cloud`.

# Growth diagrams (sentiment analysis)

### `vekstdiagram(urn, params=None)`
Make a growth diagram for a given book using a set of words:
Parameters 

``
'words': list of words 
'window': chunk size in the book
'pr': how many words are skipped before next chunk
``

### `plot_sammen_vekst(urn, ordlister, window=5000, pr = 100)`
For ploting more than one growth diagram. Have a look at example notebook.

# Word relations and n-grams

### `difference(first, second, rf, rs, years=(1980, 2000),smooth=1, corpus='bok')`
Compute difference of difference (first/second)/(rf/rs) for ngrams.


### `relaterte_ord(word, number = 20, score=False)`
Find related words using eigenvector centrality from networkx. Related words are taken from [NB Ngram](https://www.nb.no/sp_tjenester/beta/ngram_1/galaxies). Note: Works for english and german - add parameter!!


### `nb_ngram(terms, corpus='bok', smooth=3, years=(1810, 2010), mode='relative')`
Collect an ngram as json object from [NB Ngram](https://www.nb.no/sp_tjenester/beta/ngram_1/trends#ngram/query?terms=norway). Terms is string of comma separated ngrams (single words up to trigrams).

### `ngram_conv(ngrams, smooth=1, years=(1810,2013), mode='relative')`
Convert ngrams to a dataframe.


### `make_graph(word)`
Get graph like in [NB Ngram](https://www.nb.no/sp_tjenester/beta/ngram_1/galaxies)


# Concordances

### `get_konk(word, params=None, kind='html')`
Get a concordance for given word. Params are like `get_urn`. Value is either an HTML-page, a json structure, or a dataframe. Specify `kind` as 'html', 'json' or '' respectively.

### `get_urnkonk(word, params=None, html=True)`
Same as `get_konk` but from a list of URNs.


# Character Analysis and graphs

### `central_characters(graph, n=10)`
wrapper around `networkx`
``    res = Counter(nx.degree_centrality(graph)).most_common(n)
    return res
``
### `central_betweenness_characters(graph, n=10)`
wrapper around `networkx`
``    res = Counter(nx.betweenness_centrality(graph)).most_common(n)
    return res
  ``  

### `check_words(urn, ordbag)`
Find frequency of words in `ordbag` within a book given by `urn`.


# Text complexity

### `sttr(urn, chunk=5000)`
Compute a standardized type/token-ratio for text identified with urn. The function expects the serial number of a URN for a book. Returns a number.

### `navn(urn)`
Returns a dictionary of frequency of possible names from URN as serial number.    

# Utilities

### `heatmap(df, color='green')`
A wrapper for heatmap of df as a Pandas dataframe, like this:
``return df.fillna(0).style.background_gradient(cmap=sns.light_palette(color, as_cmap=True))``

### `df_combine(array_df)`
Combine one column dataframes into one dataframe.

### `wildcardsearch(params=None)`
Default values: ``params = {'word': '', 'freq_lim': 50, 'limit': 50, 'factor': 2}``
Returns a dataframe containing matches for `word`. See examples in notebook `wildcardsearch`.

### `sorted_wildcardsearch(params)`
Same as `wildcardsearch` with results sorted on frequency.

### `combine(clusters)`
Make new collocation analyses from data in clusters

### `cluster_join(cluster)`
Used with serial clusters. Join them together in one dataframe. See example in cluster notebook.

### `serie_cluster(word, startår, sluttår, inkrement, before=5, after=5, reference=150, word_samples=500)`
Make a series of clusters.

#### `save_serie_cluster(tidscluster)`
Save series to files.

#### `les_serie_cluster(word, startår, sluttår, inkrement)`
Read them
### `frame(something, name)`
Create a dataframe of `something`


### `get_urns_from_docx(document)`
A file in `docx` format may contain a list of URNs.

### `get_urns_from_text(document)`
URNs from a `.txt`-document.

### `get_urns_from_files(mappe, file_type='txt')`
Extract URNs from a folder with `.txt` and `.docs` files. Returns a dictionary with filenames as keys, each with a list of URNs.


### `check_vals(korpus, vals)`
A wrapper for dataframes: ``
    return korpus[korpus.index.isin(vals)].sort_values(by=0, ascending=False)``

