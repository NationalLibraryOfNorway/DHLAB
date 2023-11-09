:hide-toc:

.. digital_tekstanalyse documentation master file, created by
    sphinx-quickstart on Thu Dec 30 16:43:55 2021.
    You can adapt this file completely to your liking, but it should at least
    contain the root `toctree` directive.


================================================
dhlab documentation
================================================


..
    # Include the text from the README.md file

.. include:: ../README.md
   :parser: myst_parser.sphinx_
   :start-after: <!-- start dhlab-intro -->
   :end-before: <!-- end dhlab-intro -->
 

On our `official homepage <https://www.nb.no/dh-lab/>`_ (in Norwegian), 
you can view and run `example jupyter notebooks <https://www.nb.no/dh-lab/digital-tekstanalyse/>`_
in your browser. 

.. include:: ../README.md
   :parser: myst_parser.sphinx_
   :start-after: <!-- start installation -->
   :end-before: <!-- end installation -->

Get started with some :doc:`examples <./docs_example_use>`.

.. include:: docs_functionality.md
   :parser: myst_parser.sphinx_

-------------------

- :ref:`Alphabetical Index <genindex>`
- :ref:`Module Index <modindex>`
- :ref:`Search <search>`

..
    # This toctree is only shown in the left side panel

.. toctree::
   :name: contents
   :hidden:
   :glob:
   :maxdepth: 1

   docs_installation
   docs_example_use
   library/dhlab
   term_definitions

.. toctree::
   :hidden:
   :name: extlinks-toc
   :caption: External links

   Official Homepage (nb.no) <https://www.nb.no/dh-lab/>
   GitHub repo <https://github.com/NationalLibraryOfNorway/DHLAB>
   pypi package <https://pypi.org/project/dhlab/>
   R package on Github <https://github.com/NationalLibraryOfNorway/dhlab-r>
   Web applications <https://www.nb.no/dh-lab/apper/>
   Knowledge base <https://nationallibraryofnorway.github.io/DHLAB-kunnskapsbase/>
   The National Library online <https://www.nb.no/search>
