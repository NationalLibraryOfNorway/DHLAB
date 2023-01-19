[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/NationalLibraryOfNorway/digital_tekstanalyse/HEAD)
# DHLAB
<!-- start dhlab-intro -->

 [`dhlab`](https://pypi.org/project/dhlab/) is a python library for accessing reduced representations of text and pictures at
the National Library of Norway (NLN), *Nasjonalbiblioteket* (*NB*) in Norwegian. 
 It is developed and maintained by [The Digital Humanities lab group](https://www.nb.no/dh-lab/).

The python package includes wrapper functions for the [DHLAB API](https://api.nb.no/dhlab) (Application 
Programming Interface) that can be used to query the texts in [NB Digital](https://www.nb.no/search), the NLN's digital collection of books and newspapers.

The API allows for textual qualitative and quantitative analyses of the digital texts by generating 
e.g. word frequency lists, concordances, collocations, n-grams, as well as
extracting names and narrative graphs.

Analyses can be performed on both a single document, and on a larger corpus.
It is also possible to build one's own corpora based on bibliographic metadata.
<!-- end dhlab-intro -->

The Jupyter Notebooks in the [digital_tekstanalyse](https://github.com/NationalLibraryOfNorway/digital_tekstanalyse) repo show examples on
how to use the library, and can be used
[directly in your browser](https://mybinder.org/v2/gh/NationalLibraryOfNorway/digital_tekstanalyse/HEAD)
without prior programming experience.



## Installation

<!-- start installation -->

Install `dhlab` in your terminal with pip: 

```
pip install dhlab
```

<!-- end installation -->


## Example use
<!-- start example-use -->

You could start by building your own [corpus](https://en.wikipedia.org/wiki/Text_corpus), e.g. of 
books published between 1814 and 1905: 

```python
from dhlab.text import Corpus

book_corpus = Corpus(doctype="digibok", from_year=1814, to_year=1905)
```

<!-- end example-use -->

## Contact
If you have any questions, or run into any problems with the code, please log them in our [issue 
tracker](https://github.com/NationalLibraryOfNorway/DHLAB/issues) in the DHLAB repo. 

