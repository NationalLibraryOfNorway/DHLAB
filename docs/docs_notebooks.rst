Notebooks
==============

We have developed jupyter_ notebooks  to demonstrate example use cases, with
executable
code cells that you can play around with.

**There are multiple ways to view or use these notebooks:**


.. _view notebooks:

.. admonition:: View notebooks
   :class: dropdown

   Scroll through a static view of the notebooks

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


.. _Execute notebook code in the browser:

.. admonition:: Execute notebook code in the browser
   :class: dropdown

   The notebooks are hosted on Binder_, and the code can be executed from your browser
   without installing anything:

   `Run dhlab code in the browser <https://mybinder.org/v2/gh/DH-LAB-NB/DHLAB/master>`_


.. _Execute notebook code locally:

.. admonition:: Execute notebook code locally
   :class: dropdown

   Interactively execute the code in the notebooks from your own machine.

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

   #. Navigate into the cloned repo and start ``jupyter-lab``   from the terminal

      .. code-block:: shell

         cd digital_tekstanalyse
         jupyter-lab


   Once ``jupyter lab`` is up and running, just open any notebook file in the left-hand
   menu and follow the instructions to execute the code in the cells.



Or view the source ``.ipynb`` files in the `digital_tekstanalyse`_ repo.


---------------------------

..
   hyperlink refs

.. _in the browser: https://mybinder.org/v2/gh/DH-LAB-NB/DHLAB/master
.. _dhlab_pypi: https://pypi.org/project/dhlab/
.. _dhlab: dhlab_pypi_
.. _digital_tekstanalyse: https://github.com/NationalLibraryOfNorway/digital_tekstanalyse
.. _jupyter: https://jupyter.org/
.. _homepage: https://www.nb.no/dh-lab/digital-tekstanalyse/
.. _binder: https://mybinder.org/


