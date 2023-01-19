
# Functionality

<!-- start docs-functionality -->

Here are some of the text mining and automatic analyses you can do with `dhlab`:

- [Build corpora](./docs_example_use.md) with [bibliographic metadata](https://github.com/NationalLibraryOfNorway/DHLAB/blob/main/dhlab/text/corpus.py#L8) about publications
- [word/token frequencies](https://github.com/NationalLibraryOfNorway/DHLAB/blob/main/dhlab/text/conc_coll.py)
- [text chunks](https://github.com/NationalLibraryOfNorway/DHLAB/blob/main/dhlab/text/chunking.py) (paragraphs)
- [concordances](https://github.com/NationalLibraryOfNorway/DHLAB/blob/main/dhlab/text/conc_coll.py)
- [collocations](https://github.com/NationalLibraryOfNorway/DHLAB/blob/main/dhlab/text/conc_coll.py)
- [n-grams](https://github.com/NationalLibraryOfNorway/DHLAB/blob/main/dhlab/ngram/ngram.py)
- [named entity extraction](https://github.com/NationalLibraryOfNorway/DHLAB/blob/main/dhlab/text/parse.py)
- narrative graphs (word [dispersion](https://github.com/NationalLibraryOfNorway/DHLAB/blob/main/dhlab/text/dispersion.py))

Analyses can be performed on both a single document, and on a larger corpus.
You can build your own corpus based on bibliographic metadata.

The python package calls the [DHLAB API](https://api.nb.no/dhlab/) to retrieve and present data from the digital texts.

<!-- end docs-functionality -->
