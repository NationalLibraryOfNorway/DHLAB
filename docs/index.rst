:hide-toc:

.. digital_tekstanalyse documentation master file, created by
    sphinx-quickstart on Thu Dec 30 16:43:55 2021.
    You can adapt this file completely to your liking, but it should at least
    contain the root `toctree` directive.


================================================
Welcome to DHLAB's documentation!
================================================

DHLAB is a library of python modules for accessing text and pictures at
the National Library of Norway.

The National Library of Norway (NLN), *Nasjonalbiblioteket* (*NB*) in Norwegian,
has developed an `API <https://api.nb.no/>`_ (Application Programming Interface)
to query the texts in the library's digital archive of books and newspapers,
`NB Digital`_.

`The Digital Humanities lab group <https://www.nb.no/dh-lab/>`_ at the NLN
has developed the dhlab_ library on top of the API, which offers
functionalities for scientists to access the literary archive with python.

The API allows for deeper analysis of the digital texts by generating e.g.
word frequency lists, concordances, collocations, n-grams, as well as
extracting names and narrative graphs.

Analyses can be performed on both a single document, and on a larger corpus.
It is also possible to build one's own corpora based on bibliographic metadata.

Example use
------------
The Jupyter Notebooks in the digital_tekstanalyse_ repo show examples on
how to use the library, and can be used
`directly in your browser <https://mybinder.org/v2/gh/DH-LAB-NB/DHLAB/master>`_
without prior programming experience.

.. _dhlab: https://github.com/NationalLibraryOfNorway/DHLAB
.. _dhlab_pypi: https://pypi.org/project/dhlab/
.. _NB Digital: https://www.nb.no/search
.. _digital_tekstanalyse: https://github.com/NationalLibraryOfNorway/digital_tekstanalyse


*******


.. toctree::
    :maxdepth: 2
    :caption: Docs

    getting_started.rst
    nbtext_docs.rst
    utilities_docs.rst


* :ref:`modindex`


.. toctree::
   :hidden:
   :caption: Development

   CHANGELOG
   GitHub Repository DHLAB <https://github.com/NationalLibraryOfNorway/DHLAB>
   GitHub Repository digital_tekstanalyse <https://github.com/NationalLibraryOfNorway/digital_tekstanalyse>
