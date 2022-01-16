# DHLAB
<!-- start dhlab-intro -->

DHLAB is a library of python modules for accessing text and pictures at
the National Library of Norway.

The National Library of Norway (NLN), *Nasjonalbiblioteket* (*NB*) in Norwegian,
has developed an [API](https://api.nb.no/) (Application Programming Interface)
to query the texts in the library's digital archive of books and newspapers,
[NB Digital](https://www.nb.no/search).

[The Digital Humanities lab group](https://www.nb.no/dh-lab/) at the NLN
has developed the [`dhlab`](https://pypi.org/project/dhlab/) library on top of the API, which offers
functionalities for scientists to access the literary archive with python.

The API allows for deeper analysis of the digital texts by generating e.g.
word frequency lists, concordances, collocations, n-grams, as well as
extracting names and narrative graphs.

Analyses can be performed on both a single document, and on a larger corpus.
It is also possible to build one's own corpora based on bibliographic metadata.
<!-- end dhlab-intro -->


## Example use
<!-- start example-use -->

The Jupyter Notebooks in the [digital_tekstanalyse](https://github.com/NationalLibraryOfNorway/digital_tekstanalyse) repo show examples on
how to use the library, and can be used
[directly in your browser](https://mybinder.org/v2/gh/DH-LAB-NB/DHLAB/master)
without prior programming experience.

<!-- end example-use -->


## Installation

<!-- start installation -->

Install dhlab with pip: 

```
pip install dhlab
```

<!-- end installation -->
