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
.. autofunction:: dhlab.nbtext.totals

.. autofunction:: dhlab.nbtext.urn_from_text

.. autofunction:: dhlab.nbtext.metadata

.. autofunction:: dhlab.nbtext.pure_urn

.. autofunction:: dhlab.nbtext.col_agg

.. autofunction:: dhlab.nbtext.row_agg


Access texts as frequency lists
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: dhlab.nbtext.get_freq

.. autofunction:: dhlab.nbtext.get_urn

.. autofunction:: dhlab.nbtext.get_corpus_text

.. autofunction:: dhlab.nbtext.get_papers



Collocations and clusters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: dhlab.nbtext.make_a_collocation

.. autofunction:: dhlab.nbtext.compute_assoc

.. autofunction:: dhlab.nbtext.urn_coll

.. autofunction:: dhlab.nbtext.collocation

.. autofunction:: dhlab.nbtext.normalize_corpus_dataframe

.. autofunction:: dhlab.nbtext.show_korpus

.. autofunction:: dhlab.nbtext.aggregate

.. autofunction:: dhlab.nbtext.convert_list_of_freqs_to_dataframe

.. autofunction:: dhlab.nbtext.get_corpus



Graphs and network analysis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: dhlab.nbtext.make_newspaper_network

.. autofunction:: dhlab.nbtext.make_network

.. autofunction:: dhlab.nbtext.make_network_graph

.. autofunction:: dhlab.nbtext.draw_graph_centrality


Wordclouds
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: dhlab.nbtext.make_cloud

.. autofunction:: dhlab.nbtext.draw_cloud

.. autofunction:: dhlab.nbtext.cloud


Growth diagrams (sentiment analysis)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: dhlab.nbtext.vekstdiagram

.. autofunction:: dhlab.nbtext.plot_sammen_vekst


Word relations and n-grams
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: dhlab.nbtext.difference

.. autofunction:: dhlab.nbtext.relaterte_ord

.. autofunction:: dhlab.nbtext.nb_ngram

.. autofunction:: dhlab.nbtext.ngram_conv

.. autofunction:: dhlab.nbtext.make_graph


Concordances
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: dhlab.nbtext.get_konk

.. autofunction:: dhlab.nbtext.get_urnkonk


Character Analysis and graphs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: dhlab.nbtext.central_characters

.. autofunction:: dhlab.nbtext.central_betweenness_characters

.. autofunction:: dhlab.nbtext.check_words


Text complexity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: dhlab.nbtext.sttr

.. autofunction:: dhlab.nbtext.navn


Utilities
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: dhlab.nbtext.heatmap

.. autofunction:: dhlab.nbtext.df_combine

.. autofunction:: dhlab.nbtext.wildcardsearch

.. autofunction:: dhlab.nbtext.sorted_wildcardsearch

.. autofunction:: dhlab.nbtext.combine

.. autofunction:: dhlab.nbtext.cluster_join

.. autofunction:: dhlab.nbtext.serie_cluster

.. autofunction:: dhlab.nbtext.save_serie_cluster

.. autofunction:: dhlab.nbtext.les_serie_cluster

.. autofunction:: dhlab.nbtext.frame

.. autofunction:: dhlab.nbtext.get_urns_from_docx

.. autofunction:: dhlab.nbtext.get_urns_from_text

.. autofunction:: dhlab.nbtext.get_urns_from_files


Classes
--------------
.. autoclass:: dhlab.nbtext.Cluster
    :members:
    :noindex:

.. autoclass:: dhlab.nbtext.Corpus
    :members:
    :noindex:


