.. _api_docs:

=========
API
=========

The DHLAB Application Programming Interface provides access to various
representations of the digital collection at the National Library of Norway.

The subpackage ``api`` and its modules contain python wrapper functions.
Most of the call requests are made to the following ``BASE_URL``:

>>> from dhlab.api import dhlab_api
>>> dhlab_api.BASE_URL
'https://api.nb.no/dhlab'

Most functions return a json (python) object.

Modules in ``dhlab.api``
--------------------------------

.. currentmodule:: api

.. autosummary::
   :toctree: generated

   dhlab_api
   nb_ngram_api
   nb_search_api
