---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Examples of use

The python package calls the [DHLAB API](https://api.nb.no/dhlab/) to retrieve and present data from the digital texts.

Analyses can be performed on both a single document, and on a larger corpus.

<!-- start example-use -->

Here are some of the text mining and automatic analyses you can do with `dhlab`:

(example_corpus)=
## Build a corpus

Build a [corpus](#text.corpus.Corpus) from bibliographic metadata about publications, e.g. books published between 1980 and 2005:

```{code-block}
import dhlab.dhlab as dh

corpus = dh.Corpus(doctype="digibok", from_year=1980, to_year=2005)
```

(example_count)=
## Word frequencies

Retrieve word (token) [frequencies](#text.corpus.Corpus.count) from a corpus:

```{code-block}
# Frequencies of each word (rows) per book, referenced by their unique ID (columns) 
corpus.count()
```

(example_chunks)=
## Bags of words

Fetch [chunks of text](#text.chunking.Chunks) (paragraphs) as bag of words from a specific publication:

```{code-block}

docid = "URN:NBN:no-nb_digibok_2007091701028"
c = dh.Chunks(urn=docid, chunks="para")
c.chunks[0]  # The first bag-of-words is the title
# {'TROLLBYEN': 1}

c.chunks[1] # Second bag-of-words is a paragraph, with word counts
```

(example_concordance)=
## Concordance

Extract [concordances](#text.conc_coll.Concordance) from the corpus:

```{code-block}
concs = corpus.conc(words="troll")

concs.concordance  
# Output is a pandas Dataframe, 
# including links to the concordance's positions in books on nb.no
```

(example_collocations)=
## Collocations

Compute [collocations](#text.conc_coll.Collocations), a ranking of relevant words to a given word:

```{code-block}
colls = corpus.coll(words="sol")
colls.coll.sort_values("counts", ascending=False).head(10) # The top 10 most relevant words to "sol" in our corpus
       counts
,          10
.           9
og          5
på          3
nicht       3
man         3
the         3
to          3
lte         3
ein         3
```

(example_ngram)=
## N-grams

Retrieve [n-gram](#ngram.nb_ngram.nb_ngram) frequencies per year in a time period.

```{code-block}
from dhlab.ngram.nb_ngram import nb_ngram

n= nb_ngram("sol,troll,skog")
n.plot()
```

The `plot` method gives us this graph:
![image](./_images/plot_ngram.png)

Check out our [N-gram app](https://www.nb.no/ngram/#1_1_1__1_1_3_1810%2C2022_2_2_2_12_2) for an online visual graph of all uni-, bi-, and trigrams in the National Library's digitized collection of publications.

(example_ner)=
## Named Entity Recognition

Extract occurrences of [named entities](#text.parse.NER), for example place names:

```{code-block}
from dhlab import NER

docid = 'URN:NBN:no-nb_digibok_2007091701028'
ner = NER(docid)
```

(example_dispersion)=
## Word dispersions

Plot narrative graphs of word [dispersions](#text.dispersion.Dispersion) in a publication, for instance in "Kristin Lavransdatter":

```{code-block}
from dhlab.text.dispersion import Dispersion

docid = "URN:NBN:no-nb_digibok_2018021248144"
d = Dispersion(docid, wordbag=["Kristin","Lavrans"], window=1000, pr=500)
d.plot()
```

`Dispersion.plot()` gives us this diagram:
![image](./_images/dispersion_plot.png)

<!-- end example-use -->
