Notebooks
==============

We have developed `jupyter notebooks`_ to demonstrate example use cases, with executable
code cells that you can play around with.

.. hint::

   **There are multiple ways to view or use these notebooks:**

   * `view notebooks`_
   * `execute notebook code locally`_
   * view the source ``.ipynb`` files in the `digital_tekstanalyse`_ repo
   * interactively execute the code cells `in the browser`_ on Binder_



View notebooks
----------------------

.. admonition:: Scroll through a static view of the notebooks
   :class: dropdown

   .. toctree::
      :titlesonly:
      :maxdepth: 1
      :caption: Jupyter notebooks using dhlab
      :name: jupytertoc

      notebooks/Oppstart.ipynb
      notebooks/1_Bygg_korpus.ipynb
      notebooks/2_Konkordans.ipynb
      notebooks/3_Kollokasjoner.ipynb
      notebooks/4_N-gram_og_galakser.ipynb
      notebooks/5_Navnegrafer.ipynb
      notebooks/6_Søk_med_trunkering.ipynb
      notebooks/7_Setningsuttrekk.ipynb
      notebooks/8_Sammenlign_metadata.ipynb
      notebooks/9_Ordparadigmer.ipynb
      notebooks/10_Søk_i_aviser.ipynb
      notebooks/10_Frekvenslister.ipynb
      notebooks/Anbefalt_lesning.ipynb



Execute notebook code locally
-----------------------------------------------------------

.. admonition:: Interactively execute the code in the notebooks from your own machine.
   :class: dropdown

   #. Ensure dhlab_ is installed:

      .. code-block:: python

         pip install dhlab

   #. Ensure jupyter_ is installed:

      .. tab:: jupyter lab

         .. code-block:: shell

            pip install jupyterlab

      .. tab:: jupyter notebook

         .. code-block:: shell

            pip install notebook


   #. Clone the `digital_tekstanalyse`_ Github repo (from a terminal or command line):

      .. code-block:: shell

         git clone git@github.com:NationalLibraryOfNorway/digital_tekstanalyse.git

   #. Navigate into the cloned repo and start `jupyter lab`_ from the terminal

      .. code-block:: shell

         cd digital_tekstanalyse
         jupyter-lab


   Once `jupyter lab`_ is up and running, just open any notebook file in the left-hand
   menu and follow the instructions to execute the code in the cells.

---------------------------

.. _in the browser: https://mybinder.org/v2/gh/DH-LAB-NB/DHLAB/master
.. _Binder: https://mybinder.org/
.. _dhlab_pypi: https://pypi.org/project/dhlab/
.. _dhlab: dhlab_pypi_
.. _digital_tekstanalyse: https://github.com/NationalLibraryOfNorway/digital_tekstanalyse
.. _jupyter: https://jupyter.org/
.. _jupyter lab: jupyter_
.. _jupyter notebooks: jupyter_
.. _homepage: https://www.nb.no/dh-lab/digital-tekstanalyse/



