.. _api_docs:


NB API
=========================================
The `NB Application Programming Interface`_ provides access to various
representations of `NB Digital`_, the digital collection at the National Library of Norway.

The :py:mod:`dhlab.api` subpackage contains wrapper functions that post requests to
the National Library's internal databases with full texts, tokens, and metadata from the text
collection.

Most of the call requests are made to ``BASE_URL='https://api.nb.no/dhlab'``,
as defined in :mod:`constants`.

Most functions return a json (python) object.

.. _NB Digital: https://www.nb.no/search
.. _NB Application Programming Interface: https://api.nb.no/

------------------------

.. toctree::
   :caption: Code documentation
   :name: apitoc
   :titlesonly:

   api.dhlab_api
   api.nb_search_api
   api.nb_ngram_api