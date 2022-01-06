.. _nbtext_docs:


NB Text analysis
=================
The nbtext module contains functions and classes that are wrappers around the
API for querying NB Digital, in addition to some extended functionality to present
the data back to the user.

.. code-block:: python

    from dhlab import nbtext


Functions
----------------------------

Metadata and URNs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: nbtext.totals

.. autofunction:: nbtext.urn_from_text

.. autofunction:: nbtext.metadata

.. autofunction:: nbtext.pure_urn

.. autofunction:: nbtext.col_agg

.. autofunction:: nbtext.row_agg


Access texts as frequency lists
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: nbtext.get_freq

.. autofunction:: nbtext.get_urn

.. autofunction:: nbtext.get_corpus_text

.. autofunction:: nbtext.get_papers



Collocations and clusters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: nbtext.make_a_collocation

.. autofunction:: nbtext.compute_assoc

.. autofunction:: nbtext.urn_coll

.. autofunction:: nbtext.collocation

.. autofunction:: nbtext.normalize_corpus_dataframe

.. autofunction:: nbtext.show_korpus

.. autofunction:: nbtext.aggregate

.. autofunction:: nbtext.convert_list_of_freqs_to_dataframe

.. autofunction:: nbtext.get_corpus



Graphs and network analysis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: nbtext.make_newspaper_network

.. autofunction:: nbtext.make_network

.. autofunction:: nbtext.make_network_graph

.. autofunction:: nbtext.draw_graph_centrality


Wordclouds
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: nbtext.make_cloud

.. autofunction:: nbtext.draw_cloud

.. autofunction:: nbtext.cloud


Growth diagrams (sentiment analysis)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: nbtext.vekstdiagram

.. autofunction:: nbtext.plot_sammen_vekst


Word relations and n-grams
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: nbtext.difference

.. autofunction:: nbtext.relaterte_ord

.. autofunction:: nbtext.nb_ngram

.. autofunction:: nbtext.ngram_conv

.. autofunction:: nbtext.make_graph


Concordances
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: nbtext.get_konk

.. autofunction:: nbtext.get_urnkonk


Character Analysis and graphs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: nbtext.central_characters

.. autofunction:: nbtext.central_betweenness_characters

.. autofunction:: nbtext.check_words


Text complexity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: nbtext.sttr

.. autofunction:: nbtext.navn


Utilities
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: nbtext.heatmap

.. autofunction:: nbtext.df_combine

.. autofunction:: nbtext.wildcardsearch

.. autofunction:: nbtext.sorted_wildcardsearch

.. autofunction:: nbtext.combine

.. autofunction:: nbtext.cluster_join

.. autofunction:: nbtext.serie_cluster

.. autofunction:: nbtext.save_serie_cluster

.. autofunction:: nbtext.les_serie_cluster

.. autofunction:: nbtext.frame

.. autofunction:: nbtext.get_urns_from_docx

.. autofunction:: nbtext.get_urns_from_text

.. autofunction:: nbtext.get_urns_from_files


Classes
--------------
.. autoclass:: nbtext.Cluster
    :members:
    :noindex:

.. autoclass:: nbtext.Corpus
    :members:
    :noindex:


