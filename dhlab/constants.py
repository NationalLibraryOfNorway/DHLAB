import os

"""Constant variables used across modules, override using environment variable"""

BASE_URL = os.getenv("NB_DHLAB_BASE_URL", "https://api.nb.no/dhlab")  #: REST-API URL adress to fulltext query functions
NGRAM_API =  os.getenv("NB_DHLAB_NGRAM_API", "https://api.nb.no/dhlab/nb_ngram/ngram/query") #: URL adress for API calls to ngram-databases
GALAXY_API = os.getenv("NB_DHLAB_GALAXY_API", "https://api.nb.no/dhlab/nb_ngram_galaxies/galaxies/query")  #: URL adress for word galaxy API queries
