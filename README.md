[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/NationalLibraryOfNorway/digital_tekstanalyse/HEAD)
# DHLAB
<!-- start dhlab-intro -->

 [`dhlab`](https://pypi.org/project/dhlab/) is a python library for doing qualitative and quantitative analyses of the digital texts from [nettbiblioteket](https://www.nb.no/search) at the National Library of Norway (NLN), *Nasjonalbiblioteket* (*NB*) in Norwegian. Nettbiblioteket is the NLN's digital collection of books and newspapers.

The python package uses functionality from the [DHLAB API](https://api.nb.no/dhlab/) (Application
Programming Interface):

- word frequencies
- concordances
- collocations
- n-grams
- named entity extraction
- narrative graphs

Analyses can be performed on both a single document, and on a larger corpus.
You can build your own corpus based on bibliographic metadata.

<!-- end dhlab-intro -->

<<<<<<< HEAD
The Jupyter Notebooks in the [digital_tekstanalyse](https://github.com/NationalLibraryOfNorway/digital_tekstanalyse) repo show examples on
how to use the library, and can be used
[directly in your browser](https://mybinder.org/v2/gh/NationalLibraryOfNorway/digital_tekstanalyse/HEAD)
without prior programming experience.
=======
## Ways of doing automatic text analysis with DH-lab functionality
>>>>>>> 6f9cb0b (docs: update README)

<!-- start usage-platforms -->
* Via [our streamlit apps](https://www.nb.no/dh-lab/apper/)
* Jupyter Notebooks with example code and use cases on our website (in Norwegian): [digital_tekstanalyse](https://www.nb.no/dh-lab/digital-tekstanalyse/) ([view the notebooks on github](https://github.com/NationalLibraryOfNorway/digital_tekstanalyse) )
* In the python console or an IDE with the [`dhlab` pypi package](https://pypi.org/project/dhlab/)
* With API-calls to the [REST-API](https://api.nb.no/dhlab/)
* With R: [dhlab-r](https://github.com/NationalLibraryOfNorway/dhlab-r)
<!-- end usage-platforms-->


## Installation

<!-- start installation -->

Install the latest version of `dhlab` in your terminal with pip:

```
pip install -U dhlab
```

<!-- end installation -->


## Example use
<!-- start example-use -->

You could start by building your own [corpus](https://en.wikipedia.org/wiki/Text_corpus), e.g. of
books published between 1814 and 1905:

```python
import dhlab as dh

book_corpus = dh.Corpus(doctype="digibok", from_year=1814, to_year=1905)
```

You can now use `book_corpus` and to do quantitative text analyses.
`book_corpus.corpus` is a [Pandas dataframe](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html#pandas.DataFrame) with metadata information about the publications in the corpus.

<!-- end example-use -->


## Contact
<!-- start contact-info -->
The code here is developed and maintained by [The Digital Humanities lab group](https://www.nb.no/dh-lab/).

If you have any questions, or run into any problems with the code, please log them in our [issue
tracker](https://github.com/NationalLibraryOfNorway/DHLAB/issues).
<!-- end contact-info -->
