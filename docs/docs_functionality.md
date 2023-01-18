
# Functionality

<!-- start docs-functionality -->

Here are some of the text mining and automatic analyses you can do with `dhlab`:

- [Build corpora](./docs_example_use.md) with [bibliographic metadata](../dhlab/text/corpus.py) about publications
- [word/token frequencies](../dhlab/text/conc_coll.py)
- [text chunks](../dhlab/text/chunking.py) (paragraphs)
- [concordances](../dhlab/text/conc_coll.py)
- [collocations](../dhlab/text/conc_coll.py)
- [n-grams](../dhlab/ngram/ngram.py)
- [named entity extraction](../dhlab/text/parse.py)
- narrative graphs (word [dispersion](../dhlab/text/dispersion.py))

Analyses can be performed on both a single document, and on a larger corpus.
You can build your own corpus based on bibliographic metadata.

The python package calls the [DHLAB API](https://api.nb.no/dhlab/) to retrieve and present data from the digital texts.

<!-- end docs-functionality -->
