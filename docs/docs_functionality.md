
# Functionality

<!-- start docs-functionality -->

Here are some of the text mining and automatic analyses you can do with `dhlab`:

- Build a [corpus](#dhlab.Corpus) from bibliographic metadata about publications: 

```{code-block} python
:caption: **Example**: A corpus with books published between 1980 and 2005
:lineno-start: 1

import dhlab as dh

book_corpus = dh.Corpus(doctype="digibok", from_year=1980, to_year=2005)
```
- Retrieve word (token) [frequencies](#dhlab.Corpus.count) from a corpus
- Fetch [chunks of text](#dhlab.Chunks) (paragraphs) from a specific publication
- Extract [concordances](#dhlab.Concordance)  (See the defitition of [concordance](<#Concordance>)).
- [collocations](#dhlab.Collocations)
- [n-grams](#dhlab.ngram.ngram)
  Check out our [N-gram app](https://www.nb.no/ngram/#1_1_1__1_1_3_1810%2C2022_2_2_2_12_2) for an interactive, visual graph of all uni-, bi-, and trigrams in the National Library's digitized collection of publications.
- [named entity extraction](#dhlab.NER)
- narrative graphs (word [dispersion](#dhlab.Dispersion))

Analyses can be performed on both a single document, and on a larger corpus.

The python package calls the [DHLAB API](https://api.nb.no/dhlab/) to retrieve and present data from the digital texts.

<!-- end docs-functionality -->
