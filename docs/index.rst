:hide-toc:

.. digital_tekstanalyse documentation master file, created by
    sphinx-quickstart on Thu Dec 30 16:43:55 2021.
    You can adapt this file completely to your liking, but it should at least
    contain the root `toctree` directive.


================================================
Welcome to DHLAB's documentation!
================================================


..
    # Include the text from the README.md file

.. include:: ../README.md
   :parser: myst_parser.sphinx_

..
    # TODO: Maybe add a changelog/news section?

..
    # TODO: Add a demo view?

..
    For more examples of use, see :doc:`usage_examples`.

*******


Contents
--------------


..
    # The following toctree blocks are shown in the left side panel

.. toctree::
   :caption: Introduction
   :name: top-toc

   docs_getting_started.rst
   docs_notebooks.rst


.. toctree::
   :maxdepth: 2
   :caption: Code documentation
   :name: code-toc

   package_summary.rst
   usage_api.rst
   usage_images.rst
   usage_metadata.rst
   usage_ngrams.rst
   usage_text.rst
   usage_utilities.rst
   CHANGELOG.md


.. toctree::
   :hidden:
   :name: extlinks-toc
   :caption: External links

   The DH-lab at the National Library of Norway <https://www.nb.no/dh-lab/>
   Web applications using the DHLAB API <https://www.nb.no/dh-lab/apper/>
   Search through the digital archive <https://www.nb.no/search>
   Jupyter Notebook Examples on Binder <https://mybinder.org/v2/gh/DH-LAB-NB/DHLAB/master>
   dhlab pypi package <https://pypi.org/project/dhlab/>
   DHLAB source code, GitHub <https://github.com/NationalLibraryOfNorway/DHLAB>
   digital_tekstanalyse, GitHub <https://github.com/NationalLibraryOfNorway/digital_tekstanalyse>



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
