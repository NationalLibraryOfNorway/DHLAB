.. _usage-api:

API
=========================================
The `NB Application Programming Interface`_ provides access to various
representations of `NB Digital`_, the digital collection at the National Library of Norway.

The :doc:`dhlab.api <generated/api>` subpackage contains wrapper functions that post requests to
the National Library's internal databases with full texts, tokens, and metadata from the text
collection.

Most of the call requests are made to ``BASE_URL='https://api.nb.no/dhlab'``,
as defined in :mod:`constants`.

Most functions return a json (python) object.



Use
-------
Import :doc:`dhlab.api <generated/api>` wrapper functions like this:



.. code-block::

   from dhlab.api.dhlab_api import ...

* :doc:`list of general API wrapper functions <generated/api.dhlab_api>`

-----------------

.. code-block::

   from dhlab.api.nb_ngram_api import ...

* :doc:`list of N-gram API wrapper functions <generated/api.nb_ngram_api>`

----------------------------------------------

.. code-block::

   from dhlab.api.nb_search_api import ...

* :doc:`list of search API wrapper functions <generated/api.nb_search_api>`


-----------------------------------

..
    References and subpages...

.. _NB Digital: https://www.nb.no/search
.. _NB Application Programming Interface: https://api.nb.no/


..
       commented out:
       toctree::
       :caption: Code documentation
       :name: apitoc
       :titlesonly:

       api.dhlab_api.docs
       api.nb_search_api.docs
       api.nb_ngram_api.docs
