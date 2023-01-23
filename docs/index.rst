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
 

.. include:: docs_functionality.md
   :parser: myst_parser.sphinx_


Further reading <https://nationallibraryofnorway.github.io/DHLAB-kunnskapsbase/>

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

   docs_getting_started
   library/dhlab
   glossary
   whats_new

.. toctree::
   :hidden:
   :name: extlinks-toc
   :caption: External links

   pypi package <https://pypi.org/project/dhlab/>
   DHLAB on GitHub <https://github.com/NationalLibraryOfNorway/DHLAB>
   DH-lab Homepage (nb-no) <https://www.nb.no/dh-lab/>
   DH-lab Web applications <https://www.nb.no/dh-lab/apper/>
   DH-lab Knowledge base <https://nationallibraryofnorway.github.io/DHLAB-kunnskapsbase/>
   The online National Library <https://www.nb.no/search>
